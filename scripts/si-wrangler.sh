#!/bin/bash
# Oct 16: run Wrangler 4 (needs Node 22) for the SI Helper Worker. Reads the Cloudflare token/account from box files;
# never prints them. Installs a private Node 22 + Wrangler in ~/.cache/si-wr on first use.
set -e
W="$HOME/.cache/si-wr"
if [ ! -x "$W/node_modules/node/bin/node" ] || [ ! -f "$W/node_modules/wrangler/bin/wrangler.js" ]; then
  mkdir -p "$W" && (cd "$W" && [ -f package.json ] || npm init -y >/dev/null; cd "$W" && npm i --silent node@22 wrangler@4 >/dev/null 2>&1)
fi
export CLOUDFLARE_API_TOKEN="$(cat /home/box/.cloudflare_token)"
export CLOUDFLARE_ACCOUNT_ID="$(cat /home/box/.cloudflare_account_id)"
export WRANGLER_SEND_METRICS=false
exec "$W/node_modules/node/bin/node" "$W/node_modules/wrangler/bin/wrangler.js" "$@"
