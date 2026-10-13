/* Saving Planets semantic search layer (replaceable module).
 *
 * CONTRACT (keep this stable; anything implementing it can replace this file):
 *   import * as semantic from '/search/semantic.js';
 *   semantic.supports(lang)            -> boolean  (English only today; bge-small-en is an English model)
 *   await semantic.load({ base })      -> engine   (fetches /search/semantic-index.json + semantic-vectors.bin,
 *                                                   lazy-loads Transformers.js and the query model)
 *   await engine.search(query, k=10)   -> [{ url, title, desc, kind, score }]  best first, score = cosine 0..1
 *
 * DATA FILES (written at deploy by scripts/build-search.mjs):
 *   semantic-index.json  { version:1, model, dtype, pooling, dim, scale, queryPrefix, pages:[{url,title,desc,kind}], chunkPage:[pageIdx per chunk] }
 *   semantic-vectors.bin Int8Array, chunkPage.length * dim, value = round(normalizedVector * scale)
 * A page's score is the best score of any of its chunks, minus PAGE_PENALTY for kind 'page' (general site pages)
 * so solution/hub pages win close calls. Query and documents MUST use the same model/pooling.
 *
 * Libraries: Transformers.js (Apache-2.0), Xenova/bge-small-en-v1.5 (MIT). Inspired by romanI04/sift (MIT), no code dependency.
 */
const TJS = 'https://cdn.jsdelivr.net/npm/@huggingface/transformers@3.7.6';

const PAGE_PENALTY = 0.03;

export function supports(lang) { return /^en\b/i.test(lang || 'en'); }

export async function load({ base = '/search/' } = {}) {
  const [meta, buf] = await Promise.all([
    fetch(base + 'semantic-index.json').then(r => { if (!r.ok) throw new Error('index ' + r.status); return r.json(); }),
    fetch(base + 'semantic-vectors.bin').then(r => { if (!r.ok) throw new Error('vectors ' + r.status); return r.arrayBuffer(); }),
  ]);
  const vecs = new Int8Array(buf), D = meta.dim;
  const { pipeline } = await import(TJS);
  const embed = await pipeline('feature-extraction', meta.model, { dtype: meta.dtype });
  return {
    meta,
    async search(query, k = 10) {
      const out = await embed(meta.queryPrefix + query, { pooling: meta.pooling, normalize: true });
      const q = out.data, best = new Float32Array(meta.pages.length).fill(-1);
      for (let c = 0; c < meta.chunkPage.length; c++) {
        let s = 0; const o = c * D;
        for (let d = 0; d < D; d++) s += q[d] * vecs[o + d];
        s /= meta.scale;
        const p = meta.chunkPage[c]; if (s > best[p]) best[p] = s;
      }
      return [...best].map((score, i) => ({ ...meta.pages[i], score: meta.pages[i].kind === 'page' ? score - PAGE_PENALTY : score }))
        .sort((a, b) => b.score - a.score).slice(0, k);
    },
  };
}
