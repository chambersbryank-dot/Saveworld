"""Oct 16: superseded by scripts/seo-lint.py (stricter: 5 langs, hreflang reciprocity, schema.org vocabulary, OG/Twitter, sitemap).
Kept as a non-failing alias so older notes/commands still work: python3 scripts/seo-audit.py [--list]"""
import os, subprocess, sys
sys.exit(subprocess.call([sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'seo-lint.py'), '--no-fail', *sys.argv[1:]]))
