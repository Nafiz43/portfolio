"""Write data/scholar.json = citations, h-index and article count from the Google Scholar profile.

Scholar blocks GitHub runners (HTTP 403), so this runs daily on Nafiz's Mac through
tools/scholar_daily.sh (launchd job com.user.portfolio-scholar), which commits and pushes.

Scholar has no API, so this reads the public profile page. If Google blocks the request or the
page layout changes, the script exits 1 and leaves the old data/scholar.json untouched, so the
site never shows wrong numbers. Stdlib only.  Run: python3 tools/sync_scholar.py
"""
import json
import re
import sys
import urllib.request
from pathlib import Path

USER = "UDxK99QAAAAJ"
OUT = Path(__file__).resolve().parent.parent / "data/scholar.json"
PAGE = 100  # Scholar's max page size


def fetch(cstart):
    url = f"https://scholar.google.com/citations?user={USER}&hl=en&cstart={cstart}&pagesize={PAGE}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64)", "Accept-Language": "en"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8", "replace")


def parse_stats(html):
    # Stats table cells, in order: citations (all, since), h-index (all, since), i10 (all, since).
    cells = [int(x) for x in re.findall(r'class="gsc_rsb_std">(\d+)<', html)]
    if len(cells) != 6:
        title = re.search(r"<title>(.*?)</title>", html, re.S)
        raise ValueError(f"expected 6 stat cells, found {len(cells)}; page title: {title.group(1).strip() if title else html[:200]!r}")
    return {"citations": cells[0], "h_index": cells[2]}


def count_rows(html):
    return len(re.findall(r'<tr class="gsc_a_tr"', html))


def scholar():
    html = fetch(0)
    stats = parse_stats(html)
    articles, rows = 0, count_rows(html)
    while True:
        articles += rows
        if rows < PAGE:
            break
        rows = count_rows(fetch(articles))
    if articles == 0:
        raise ValueError("found 0 articles")
    return {**stats, "articles": articles}


def demo():
    row = '<tr class="gsc_a_tr"><td>x</td></tr>'
    html = "".join(f'<td class="gsc_rsb_std">{n}</td>' for n in (1641, 1635, 14, 14, 19, 19)) + row * 3
    assert parse_stats(html) == {"citations": 1641, "h_index": 14}
    assert count_rows(html) == 3
    try:
        parse_stats("<html>captcha</html>")
        raise AssertionError("should reject a page with no stats")
    except ValueError:
        pass


if __name__ == "__main__":
    demo()
    try:
        data = scholar()
    except Exception as e:
        print(f"::warning::Scholar fetch failed, kept old data/scholar.json: {e}")
        sys.exit(1)
    OUT.write_text(json.dumps(data, indent=2) + "\n")
    print(data)
