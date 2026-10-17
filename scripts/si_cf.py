"""Oct 16: tiny Cloudflare REST helper for the SI Helper (index + setup). Reads the token/account from box files; never prints them."""
import json, urllib.request, urllib.error
def _r(p): return open(p).read().strip()
TOKEN = lambda: _r('/home/box/.cloudflare_token')
ACCOUNT = lambda: _r('/home/box/.cloudflare_account_id')
API = 'https://api.cloudflare.com/client/v4'
def call(method, path, body=None, ctype='application/json', raw=False):
    data = body if (raw or body is None) else json.dumps(body).encode()
    req = urllib.request.Request(API + path.replace('{acct}', ACCOUNT()), data=data, method=method,
                                 headers={'Authorization': 'Bearer ' + TOKEN(), 'Content-Type': ctype})
    try:
        with urllib.request.urlopen(req, timeout=120) as r: return json.loads(r.read())
    except urllib.error.HTTPError as e:
        raise RuntimeError(f'{method} {path.split("?")[0]} -> {e.code}: {e.read()[:400].decode(errors="replace")}') from None
