# nordram.am — the website

GitHub Pages serves this repo from `main` (legacy Jekyll build, no CI). Jekyll
does not publish dot-folders or `_` folders, so this file and `_checks/` stay
off the site.

## Pages come in pairs

English pages are at the root; their Armenian copies are under `hy/`:

- `index.html` ↔ `hy/index.html`
- `privacy.html` ↔ `hy/privacy.html`

## The privacy policy changes in both languages at once

Founder decision 2026-11-21 (asked whether the Armenian policy must change
with the English one, as a written rule — answered "Yes"):

- Any change to `privacy.html` lands in the same commit and the same PR as the
  matching change to `hy/privacy.html`, and the other way round.
- The two say the same thing, no more and no less.
- Both "Last updated" dates are changed together and stay equal.
- An English policy change without its Armenian half is not merged. If the
  Armenian text isn't ready, the English change waits.
- Before opening any PR that touches either policy, run
  `python3 -I _checks/policy_pair.py` and paste its output into the PR body.

The app's in-app Privacy sheet loads the English page,
`https://nordram-am.github.io/privacy.html`, so the English page's address
must not move.
