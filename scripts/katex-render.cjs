// Oct 16: build-time KaTeX. stdin: JSON list of TeX strings; stdout: JSON list of HTML (htmlAndMathml, display mode). Throws on bad TeX.
const katex = require('katex'); let s = ''; process.stdin.on('data', c => s += c).on('end', () => {
  const out = JSON.parse(s).map(t => katex.renderToString(t, { displayMode: true, output: 'htmlAndMathml', throwOnError: true, strict: 'error' }));
  process.stdout.write(JSON.stringify(out));
});
