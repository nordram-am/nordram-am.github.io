# nordram.am — the website

GitHub Pages serves this repo from `main` (legacy Jekyll build, no CI). Jekyll
does not publish dot-folders or `_` folders, so this file and `_checks/` stay
off the site.

## Pages come in pairs

Armenian is the site's default language (founder, 2026-11-24). Each page has
an Armenian and an English copy:

- Home: Armenian `index.html` (served at `/`) ↔ English `en/index.html`
  (served at `/en/`).
- Privacy: English `privacy.html` (`/privacy.html`) ↔ Armenian
  `hy/privacy.html` (`/hy/privacy.html`). Both privacy addresses stay where
  they are; see the rules below.
- `hy/index.html` is only a redirect to `/` (it keeps any `#hash`), so old
  `/hy/` links still work. It is not a page; don't add content to it.

There is no automatic language detection or redirect by browser language.
Each page links to its other-language copy with a visible switch.

Links between pages: the Armenian home links to `hy/privacy.html`, the
English home to `/privacy.html`. Each privacy page's brand link goes to its
own language's home (`/` for Armenian, `/en/` for English). hreflang
`x-default` points at the Armenian copy.

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

The app's in-app Privacy sheet loads the English page. It keeps the page only
when the address matches exactly, and it checks every hop of a redirect.

- Tester builds up to iOS 53 / Android 46 load
  `https://nordram-am.github.io/privacy.html`. Since 2026-11-21 that address
  redirects to `https://nordram.am/privacy.html`, and those builds send the
  redirect out to the browser instead of showing the page in the sheet.
- Builds made after the app fix (nordram-am/Nordram#1126) load
  `https://nordram.am/privacy.html` directly.

Neither address may move. The github.io address must keep pointing at
`https://nordram.am/privacy.html`, and that page must answer at exactly that
address, with no redirect in front of it (not to `www.`, not to a trailing
slash). A new build would send any such hop to the browser too.
