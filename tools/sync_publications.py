"""Build data/publications.json = hand-curated entries + any new ORCID works.

Curated entries (data/publications.manual.json) always win field by field; ORCID only
adds works whose title isn't already there. Authors for new works come from Crossref.
Stdlib only, so it runs as-is in GitHub Actions.  Run: python3 tools/sync_publications.py
"""
import difflib
import json
import re
import urllib.request
from pathlib import Path

ORCID = "0000-0003-0149-6012"
ME = ("Nafiz", "Khan")
ROOT = Path(__file__).resolve().parent.parent
MANUAL = ROOT / "data/publications.manual.json"
OUT = ROOT / "data/publications.json"
PREPRINT_TYPES = {"preprint", "other", "working-paper"}


def get(url):
    req = urllib.request.Request(url, headers={"Accept": "application/json", "User-Agent": f"portfolio-sync (orcid {ORCID})"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def norm(t):
    return re.sub(r"[^a-z0-9]", "", t.lower())


def same(a, b):
    return difflib.SequenceMatcher(None, norm(a), norm(b)).ratio() >= 0.85


def crossref(doi):
    try:
        return get(f"https://api.crossref.org/works/{doi}")["message"]
    except Exception:
        return {}


def authors_of(cr):
    names = []
    for a in cr.get("author", []):
        n = f"{a.get('given', '')} {a.get('family', '')}".strip()
        if a.get("given", "").startswith(ME[0]) and a.get("family") == ME[1]:
            n = f"<b>{n}</b>"
        names.append(n)
    return ", ".join(names)


def orcid_works():
    works = []
    for g in get(f"https://pub.orcid.org/v3.0/{ORCID}/works")["group"]:
        w = g["work-summary"][0]
        ids = {e["external-id-type"]: e["external-id-value"] for e in (w.get("external-ids") or {}).get("external-id", [])}
        doi = re.sub(r"^https?://(dx\.)?doi\.org/", "", ids.get("doi", ""))
        works.append({
            "title": w["title"]["title"]["value"],
            "type": w["type"],
            "year": (((w.get("publication-date") or {}).get("year")) or {}).get("value", ""),
            "venue": (w.get("journal-title") or {}).get("value", ""),
            "doi": doi,
        })
    # A preprint is dropped when a published version of the same title exists.
    published = [w for w in works if w["type"] not in PREPRINT_TYPES]
    return published + [w for w in works if w["type"] in PREPRINT_TYPES and not any(same(w["title"], p["title"]) for p in published)]


def to_entry(w):
    cr = crossref(w["doi"]) if w["doi"] else {}
    preprint = w["type"] in PREPRINT_TYPES
    venue = w["venue"] or (cr.get("container-title") or [""])[-1] or (cr.get("institution") or [{}])[0].get("name", "")
    return {
        "title": re.sub(r"\s+", " ", w["title"]).strip(),
        # ponytail: works without a DOI get no author list; add them to the manual file if that matters.
        "authors": authors_of(cr),
        "venue": "" if preprint else venue,
        "year": "TBD" if preprint else w["year"],
        "link": f"https://doi.org/{w['doi']}" if w["doi"] else "",
        "doi": w["doi"],
        "source": "orcid",
    }


def merge(manual, works):
    out = [dict(e) for e in manual]
    for w in works:
        hit = next((e for e in out if same(e["title"], w["title"])), None)
        if hit:
            hit.setdefault("doi", w["doi"])
            # Once ORCID knows the published DOI, link that instead of the arXiv preprint.
            if w["doi"] and w["type"] not in PREPRINT_TYPES and "arxiv.org" in hit.get("link", ""):
                hit["link"] = f"https://doi.org/{w['doi']}"
        else:
            out.append(to_entry(w))
    return out


def order(entries):
    # Newest first; "TBD" (under review / preprint) sorts above every year.
    return sorted(entries, key=lambda e: e["year"] if e["year"].isdigit() else "9999", reverse=True)


def demo():
    manual = [{"title": "COVID-19 and Black Fungus: Analysis of Public Perceptions through Machine Learning", "year": "2022"}]
    works = [{"title": "COVID‐19 and black fungus: Analysis of the public perceptions through machine learning", "type": "journal-article", "year": "2022", "venue": "", "doi": "10.1/x"}]
    merged = merge(manual, works)
    assert len(merged) == 1 and merged[0]["doi"] == "10.1/x", merged
    assert [e["year"] for e in order([{"year": "2021"}, {"year": "TBD"}, {"year": "2026"}])] == ["TBD", "2026", "2021"]


if __name__ == "__main__":
    demo()
    manual = json.loads(MANUAL.read_text())
    merged = order(merge(manual, orcid_works()))
    new = [e["title"] for e in merged if e.get("source") == "orcid"]
    OUT.write_text(json.dumps(merged, indent=2, ensure_ascii=False) + "\n")
    print(f"{len(merged)} publications ({len(new)} from ORCID only)")
    for t in new:
        print("  +", t)
