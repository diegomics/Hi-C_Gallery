#!/usr/bin/env python3
"""Build data.json for the Hi-C Gallery (single-folder layout only).

Layout:
  images/<speciesID>_<authorID>/
    <type>_<speciesID>_<authorID>_01.png
    <type>_<speciesID>_<authorID>_01.txt
    <type>_<speciesID>_<authorID>_02.png
    <type>_<speciesID>_<authorID>_02.txt
    [cover.png]

Rules:
- <type> is one of: inversion, translocation, duplication
- XX is two digits (01, 02, ...). One caption .txt per image (same basename).
- All images in a case must share the same <type>.
- Case folder name: (case_)?<speciesID>_<authorID>
"""
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IMG_DIR = ROOT / "images"

TYPE_TO_SLUG = {
    "inversion": "inversions",
    "translocation": "translocations",
    "duplication": "duplications",
}
SLUG_ORDER = ["inversions", "translocations", "duplications"]

CASE_DIR_RE = re.compile(r"^(?:case_)?[A-Za-z0-9]+_[A-Za-z0-9]+$")
FILE_RE = re.compile(r"^(inversion|duplication|translocation)_([A-Za-z0-9]+)_([A-Za-z0-9]+)_(\d{2})\.png$")

def human_case_name(folder: str) -> str:
    base = re.sub(r"^case_", "", folder)
    sp, _, au = base.partition("_")
    return f"{sp} — {au}" if au else base

def rel(p: Path) -> str:
    return str(p.relative_to(ROOT)).replace("\\", "/")

def list_pngs_sorted(case_dir: Path):
    items = []
    for p in case_dir.glob("*.png"):
        m = FILE_RE.match(p.name)
        order = int(m.group(4)) if m else 9999
        items.append((order, p))
    return sorted(items, key=lambda t: (t[0], t[1].name.lower()))

def caption_for(png: Path) -> str:
    txt = png.with_suffix(".txt")
    return txt.read_text(encoding="utf-8").strip() if txt.exists() else ""

def validate_case(case_dir: Path) -> list[str]:
    problems = []
    if not CASE_DIR_RE.match(case_dir.name):
        problems.append(f"Bad case folder name: {case_dir.name} (expected <speciesID>_<authorID> or case_<speciesID>_<authorID>)")
        return problems

    base = re.sub(r"^case_", "", case_dir.name)
    types_seen = set()
    idx_seen = set()

    for _, png in list_pngs_sorted(case_dir):
        m = FILE_RE.match(png.name)
        if not m:
            problems.append(f"[{case_dir.name}] Bad file name: {png.name} (expected <type>_<speciesID>_<authorID>_XX.png)")
            continue
        t, sp, au, xx = m.groups()
        if f"{sp}_{au}" != base:
            problems.append(f"[{case_dir.name}] Folder and file disagree: {png.name}")
        types_seen.add(t)
        i = int(xx)
        if i in idx_seen:
            problems.append(f"[{case_dir.name}] Duplicate index {xx} in {png.name}")
        idx_seen.add(i)
        if not png.with_suffix(".txt").exists():
            problems.append(f"[{case_dir.name}] Missing caption TXT for {png.name}")

    if not types_seen:
        problems.append(f"[{case_dir.name}] No valid images found.")
    elif len(types_seen) > 1:
        problems.append(f"[{case_dir.name}] Mixed <type> values: {sorted(types_seen)} (use a single type per case)")

    return problems

def build_data():
    categories = {slug: {"slug": slug, "name": slug[:1].upper() + slug[1:], "description": "", "coverImage": None, "cases": []}
                  for slug in SLUG_ORDER}

    if not IMG_DIR.exists():
        raise SystemExit("images/ directory not found")

    for case_dir in sorted([p for p in IMG_DIR.iterdir() if p.is_dir()], key=lambda p: p.name.lower()):
        pngs = [p for _, p in list_pngs_sorted(case_dir) if FILE_RE.match(p.name)]
        if not pngs:
            continue
        m = FILE_RE.match(pngs[0].name)
        t = m.group(1)
        cat_slug = TYPE_TO_SLUG[t]

        images = []
        for _, png in list_pngs_sorted(case_dir):
            m2 = FILE_RE.match(png.name)
            if not m2:
                continue
            _, sp, au, xx = m2.groups()
            images.append({
                "src": rel(png),
                "alt": f"{sp}_{au} {xx}",
                "caption": caption_for(png)
            })
        if not images:
            continue

        cover = case_dir / "cover.png"
        cover_rel = rel(cover) if cover.exists() else images[0]["src"]

        categories[cat_slug]["cases"].append({
            "slug": case_dir.name,
            "name": human_case_name(case_dir.name),
            "description": "",
            "coverImage": cover_rel,
            "images": images
        })

    out_categories = []
    for slug in SLUG_ORDER:
        cat = categories[slug]
        cat["cases"].sort(key=lambda c: c["slug"].lower())
        if cat["cases"] and not cat["coverImage"]:
            cat["coverImage"] = cat["cases"][0]["coverImage"]
        out_categories.append(cat)

    data = {
        "title": "Hi-C Gallery",
        "tagline": "Explore Hi-C contact maps by category → case → annotated views.",
        "categories": out_categories,
    }

    (ROOT / "data.json").write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

if __name__ == "__main__":
    if "--check" in sys.argv:
        problems = []
        if not IMG_DIR.exists():
            problems.append("Missing images/ directory.")
        else:
            for case_dir in [p for p in IMG_DIR.iterdir() if p.is_dir()]:
                problems.extend(validate_case(case_dir))
        if problems:
            print("Validation failed:\n")
            for p in problems:
                print(" -", p)
            sys.exit(1)
        print("All good ✅")
        sys.exit(0)
    else:
        if IMG_DIR.exists():
            for case_dir in [p for p in IMG_DIR.iterdir() if p.is_dir()]:
                probs = validate_case(case_dir)
                if probs:
                    print("WARNING:")
                    for p in probs:
                        print(" -", p)
        build_data()
        print("Wrote data.json")
