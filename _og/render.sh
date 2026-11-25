#!/bin/sh
# Renders the link-preview images at the repository root:
#   og-hy.png  (Armenian home, /)     og-en.png  (English home, /en/)
# Each is 1200 x 630, from _og/card.html, captured by headless Chrome with a
# throwaway profile (never your own). Needs network access for Google Fonts.
#
#   sh _og/render.sh            CHROME=/path/to/chrome sh _og/render.sh
#
# Then open both PNGs and look: the Armenian letters must be real glyphs, not
# empty boxes, and each file must stay under 300 KB.
set -eu
here=$(cd "$(dirname "$0")" && pwd)
root=$(dirname "$here")
chrome=${CHROME:-"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"}
profile=$(mktemp -d "${TMPDIR:-/tmp}/og-chrome.XXXXXX")
trap 'rm -rf "$profile"' EXIT INT TERM
for lang in hy en; do
  "$chrome" --headless=new --hide-scrollbars --no-first-run --no-default-browser-check \
    --disable-extensions --disable-sync --mute-audio \
    --user-data-dir="$profile" --force-device-scale-factor=1 --window-size=1200,630 \
    --virtual-time-budget=20000 --screenshot="$root/og-$lang.png" \
    "file://$here/card.html#$lang" 2>/dev/null
  echo "wrote og-$lang.png"
done
