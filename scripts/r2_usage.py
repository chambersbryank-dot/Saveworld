#!/usr/bin/env python3
"""Oct 16 2026: R2 usage this calendar month vs the free tier (10 GB-month storage, 1M Class A, 10M Class B).
Runs on the box only; reads /home/box/.cloudflare_token (needs Account Analytics: Read) and never prints it.
Usage: python3 scripts/r2-usage.py            -> markdown section on stdout
       import: from r2_usage import section    (events-report.py appends it to the weekly summary)"""
import json, urllib.request, urllib.error, datetime
BUCKETS = ['savingplanets-media']
FREE = {'storage_gb': 10, 'A': 1_000_000, 'B': 10_000_000}
CLASS_A = {'ListBuckets', 'PutBucket', 'ListObjects', 'PutObject', 'CopyObject', 'CompleteMultipartUpload', 'CreateMultipartUpload',
           'UploadPart', 'UploadPartCopy', 'ListMultipartUploads', 'ListParts', 'PutBucketEncryption', 'PutBucketCors',
           'PutBucketLifecycleConfiguration', 'LifecycleStorageTierTransition', 'PutBucketStorageClass'}
FREE_OPS = {'DeleteObject', 'DeleteBucket', 'AbortMultipartUpload', 'DeleteObjects'}
Q = '''query($a:String!,$s:Time!,$e:Time!,$d:Date!,$de:Date!){viewer{accounts(filter:{accountTag:$a}){
 ops: r2OperationsAdaptiveGroups(limit:1000,filter:{datetime_geq:$s,datetime_leq:$e}){sum{requests} dimensions{actionType bucketName}}
 st: r2StorageAdaptiveGroups(limit:100,filter:{date_geq:$d,date_leq:$de},orderBy:[date_DESC]){max{payloadSize metadataSize objectCount} dimensions{bucketName date}}}}}'''

def fetch():
    T = open('/home/box/.cloudflare_token').read().strip(); A = open('/home/box/.cloudflare_account_id').read().strip()
    now = datetime.datetime.now(datetime.timezone.utc); start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    v = {'a': A, 's': start.strftime('%Y-%m-%dT%H:%M:%SZ'), 'e': now.strftime('%Y-%m-%dT%H:%M:%SZ'), 'd': start.strftime('%Y-%m-%d'), 'de': now.strftime('%Y-%m-%d')}
    r = urllib.request.Request('https://api.cloudflare.com/client/v4/graphql', data=json.dumps({'query': Q, 'variables': v}).encode(),
                               headers={'Authorization': 'Bearer ' + T, 'Content-Type': 'application/json'})
    d = json.loads(urllib.request.urlopen(r, timeout=60).read())
    if d.get('errors'): raise RuntimeError('; '.join(e.get('message', '') for e in d['errors'])[:300])
    acc = d['data']['viewer']['accounts'][0]; a = b = 0
    for g in acc['ops']:
        t = g['dimensions']['actionType']; n = g['sum']['requests']
        if t in FREE_OPS: continue
        if t in CLASS_A: a += n
        else: b += n
    latest = {}
    for g in acc['st']:  # newest day per bucket
        latest.setdefault(g['dimensions']['bucketName'], g)
    size = sum(g['max']['payloadSize'] + g['max']['metadataSize'] for g in latest.values()); objs = sum(g['max']['objectCount'] for g in latest.values())
    src = 'analytics'
    if not latest:  # storage analytics lag about a day: count the bucket directly (1 Class A op per 1000 objects)
        size = objs = 0; src = 'live listing'
        for bk in BUCKETS:
            cur = ''
            while True:
                u = f'https://api.cloudflare.com/client/v4/accounts/{A}/r2/buckets/{bk}/objects?per_page=1000' + (f'&cursor={cur}' if cur else '')
                j = json.loads(urllib.request.urlopen(urllib.request.Request(u, headers={'Authorization': 'Bearer ' + T}), timeout=60).read())
                for o in j.get('result') or []: size += int(o.get('size', 0)); objs += 1
                cur = (j.get('result_info') or {}).get('cursor')
                if not cur or not (j.get('result_info') or {}).get('is_truncated'): break
    return {'src': src, 'month': start.strftime('%B %Y'), 'storage_gb': size / 1e9, 'objects': objs, 'A': a, 'B': b, 'buckets': sorted(latest)}

def section():
    try: u = fetch()
    except Exception as e: return f'## Cloudflare R2 usage\n\n(unavailable: {e})\n'
    pct = lambda x, f: f'{100 * x / f:.2f}%'
    return '\n'.join([f'## Cloudflare R2 usage ({u["month"]}, month to date)', '',
        '| metric | used | free tier | % of free |', '|---|---|---|---|',
        f'| storage | {u["storage_gb"]:.3f} GB ({u["objects"]} objects, {u["src"]}) | 10 GB-month | {pct(u["storage_gb"], 10)} |',
        f'| Class A ops (uploads, lists) | {u["A"]:,} | 1,000,000 | {pct(u["A"], FREE["A"])} |',
        f'| Class B ops (reads that reach R2) | {u["B"]:,} | 10,000,000 | {pct(u["B"], FREE["B"])} |', '',
        'Reads served from the Cloudflare edge cache are not Class B operations. Egress is free. Storage is the latest daily figure (billing averages it over the month).', ''])

if __name__ == '__main__': print(section())
