#!/usr/bin/env python3
"""Check that the English and Armenian privacy policies move together.

Founder decision 2026-11-21: privacy.html and hy/privacy.html change in the
same commit and the same PR, say the same thing, and carry the same
"Last updated" date. See .claude/CLAUDE.md.

Run from anywhere:   python3 -I _checks/policy_pair.py [--base origin/main]

Prints one PASS or FAIL line per check. Exits 0 only if every check passes.
Standard library only.
"""

import argparse
import datetime
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EN = "privacy.html"
HY = "hy/privacy.html"

EN_MONTHS = {
    "january": 1, "february": 2, "march": 3, "april": 4, "may": 5, "june": 6,
    "july": 7, "august": 8, "september": 9, "october": 10, "november": 11,
    "december": 12,
}
# Armenian month names in the genitive, as a date is written ("նոյեմբերի 20").
HY_MONTHS = {
    "հունվարի": 1, "փետրվարի": 2, "մարտի": 3, "ապրիլի": 4, "մայիսի": 5,
    "հունիսի": 6, "հուլիսի": 7, "օգոստոսի": 8, "սեպտեմբերի": 9,
    "հոկտեմբերի": 10, "նոյեմբերի": 11, "դեկտեմբերի": 12,
}

COMMENT = re.compile(r"<!--.*?-->", re.S)
DATE_P = re.compile(r'<p class="date">(.*?)</p>', re.S)
# "Last updated 20 November 2026"
EN_DATE = re.compile(r"^Last updated\s+(\d{1,2})\s+([A-Za-z]+)\s+(\d{4})$")
# "Վերջին թարմացումը՝ 2026 թ. նոյեմբերի 20" (the abbreviation point may be
# a full stop or the Armenian one, U+2024).
HY_DATE = re.compile(r"^Վերջին թարմացումը՝\s*(\d{4})\s*թ[.․]\s*(\S+)\s+(\d{1,2})$")
H2 = re.compile(r"<h2\b")


def page(rel):
    """The page's markup with HTML comments removed (they are not page text)."""
    return COMMENT.sub("", (ROOT / rel).read_text(encoding="utf-8"))


def parse_date(rel, text, pattern, months, order):
    """Return (date, None) or (None, reason). order maps groups to (d, m, y)."""
    found = DATE_P.findall(text)
    if not found:
        return None, f'{rel}: no <p class="date"> paragraph found'
    raw = " ".join(found[0].split())
    m = pattern.match(raw)
    if not m:
        return None, f"{rel}: date not understood: {raw!r}"
    day, month, year = (m.group(i) for i in order)
    month_no = months.get(month.lower())
    if month_no is None:
        return None, f"{rel}: month not understood: {month!r}"
    try:
        return datetime.date(int(year), month_no, int(day)), None
    except ValueError as e:
        return None, f"{rel}: not a real date ({raw!r}): {e}"


def check_date(en, hy):
    en_date, en_err = parse_date(EN, en, EN_DATE, EN_MONTHS, (1, 2, 3))
    hy_date, hy_err = parse_date(HY, hy, HY_DATE, HY_MONTHS, (3, 2, 1))
    errors = [e for e in (en_err, hy_err) if e]
    if errors:
        return False, "could not compare: " + "; ".join(errors)
    if en_date != hy_date:
        return False, f"English says {en_date.isoformat()}, Armenian says {hy_date.isoformat()}"
    return True, f"both say {en_date.isoformat()}"


def check_sections(en, hy):
    n_en, n_hy = len(H2.findall(en)), len(H2.findall(hy))
    detail = f"{n_en} <h2> in English, {n_hy} in Armenian"
    return n_en == n_hy, detail


def git(*args):
    return subprocess.run(
        ["git", "-C", str(ROOT), *args],
        capture_output=True, text=True, encoding="utf-8",
    )


def check_together(base):
    verify = git("rev-parse", "--verify", "--quiet", f"{base}^{{commit}}")
    if verify.returncode != 0:
        return False, f"base ref {base!r} not found (fetch it, or pass --base <ref>)"
    changed = set()
    for args in (("diff", "--name-only", "-z", f"{base}...HEAD"),
                 ("diff", "--name-only", "-z", "HEAD")):
        r = git(*args)
        if r.returncode != 0:
            return False, f"git {' '.join(args)} failed: {r.stderr.strip()}"
        changed.update(p for p in r.stdout.split("\0") if p)
    en_changed, hy_changed = EN in changed, HY in changed
    if en_changed and hy_changed:
        return True, f"both policies changed relative to {base}"
    if not en_changed and not hy_changed:
        return True, f"neither policy changed relative to {base}"
    only, missing = (EN, HY) if en_changed else (HY, EN)
    return False, f"only {only} changed relative to {base}; {missing} must change with it"


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--base", default="origin/main",
                    help="ref to compare against (default: origin/main)")
    args = ap.parse_args()

    en, hy = page(EN), page(HY)
    results = [
        ("Same date", *check_date(en, hy)),
        ("Same sections", *check_sections(en, hy)),
        ("Changed together", *check_together(args.base)),
    ]
    for name, ok, detail in results:
        print(f"{'PASS' if ok else 'FAIL'}  {name}: {detail}")
    failed = sum(1 for _, ok, _ in results if not ok)
    print("All checks passed." if not failed else f"{failed} check(s) failed.")
    return 0 if not failed else 1


if __name__ == "__main__":
    sys.exit(main())
