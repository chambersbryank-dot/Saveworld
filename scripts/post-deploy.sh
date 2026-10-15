#!/usr/bin/env bash
# Run AFTER weekly-sync.sh output is committed and pushed (GitHub Pages deploy).
# Waits for the live IndexNow key file, then submits pages changed since the last successful ping. Never fails.
cd "$(dirname "$0")/.."
node scripts/indexnow-ping.js --send --wait || echo "IndexNow ping failed (ignored)"
