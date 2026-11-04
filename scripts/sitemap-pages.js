// English page URLs live in sitemap-en.xml. sitemap.xml is a sitemap index (PR #206).
const fs = require('fs');

function readEnglishSitemap() {
  if (fs.existsSync('sitemap-en.xml')) return fs.readFileSync('sitemap-en.xml', 'utf8');
  if (fs.existsSync('sitemap.xml')) {
    const legacy = fs.readFileSync('sitemap.xml', 'utf8');
    if (!legacy.includes('<sitemapindex')) return legacy;
  }
  return '';
}

module.exports = { readEnglishSitemap };
