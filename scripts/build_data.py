#!/usr/bin/env python3
"""Build data.json for the Hi-C Gallery (single-folder layout).

Layout:
  images/<speciesID>_<authorID>/
    <type>_<speciesID>_<authorID>_01.png
    <type>_<speciesID>_<authorID>_01.txt
    <type>_<speciesID>_<authorID>_02.png
    <type>_<speciesID>_<authorID>_02.txt
    [cover.png]
    [cover_inversion.png]
    [cover_translocation.png]
    [cover_duplication.png]

- <type> is one of: inversion, translocation, duplication
- XX is two digits (01, 02, ...). One caption .txt per image (same basename).
- Case folder name: (case_)?<speciesID>_<authorID>
- Mixed types in the same folder are allowed; the builder emits one case per type.
"""
import json, re, sys
from itertools import chain
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
FILE_RE = re.compile(
    r"^(inversion|duplication|translocation)_([A-Za-z0-9]+)_([A-Za-z0-9]+)_(\d{2})\.(?:png|PNG)$"
)

def human_case_name(folder: str) -> str:
    base = re.sub(r"^case_", "", folder)
    sp, _, au = base.partition("_")
    return f"{sp} — {au}" if au else base

def rel(p: Path) -> str:
    return str(p.relative_to(ROOT)).replace("\\", "/")

def list_pngs_sorted(case_dir: Path):
    items = []
    for p in chain(case_dir.glob("*.png"), case_dir.glob("*.PNG")):
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
    for _, png in list_pngs_sorted(case_dir):
        m = FILE_RE.match(png.name)
        if not m:
            problems.append(f"[{case_dir.name}] Bad file name: {png.name} (expected <type>_<speciesID>_<authorID>_XX.png)")
            continue
        t, sp, au, xx = m.groups()
        if f"{sp}_{au}" != base:
            problems.append(f"[{case_dir.name}] Folder and file disagree: {png.name}")
        if not png.with_suffix(".txt").exists():
            problems.append(f"[{case_dir.name}] Missing caption TXT for {png.name}")
    return problems  # mixed types are fine

def build_data():
    categories = {slug: {"slug": slug, "name": slug[:1].upper() + slug[1:], "description": "", "coverImage": None, "cases": []}
                  for slug in SLUG_ORDER}

    if not IMG_DIR.exists():
        raise SystemExit("images/ directory not found")

    for case_dir in sorted([p for p in IMG_DIR.iterdir() if p.is_dir()], key=lambda p: p.name.lower()):
        # group images by type within the folder
        images_by_type = {"inversion": [], "translocation": [], "duplication": []}
        for _, png in list_pngs_sorted(case_dir):
            m = FILE_RE.match(png.name)
            if not m: 
                continue
            t, sp, au, xx = m.groups()
            t = t.lower()
            images_by_type[t].append({
                "src": rel(png),
                "alt": f"{sp}_{au} {xx}",
                "caption": caption_for(png),
                "order": int(xx),
            })

        # emit one case per type present
        for t, images in images_by_type.items():
            if not images:
                continue
            cat_slug = TYPE_TO_SLUG[t]

            cover_typed = case_dir / f"cover_{t}.png"
            cover_generic = case_dir / "cover.png"
            if cover_typed.exists():
                cover_rel = rel(cover_typed)
            elif cover_generic.exists():
                cover_rel = rel(cover_generic)
            else:
                cover_rel = images[0]["src"]

            for img in images:
                img.pop("order", None)

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

    # summary in CI logs
    for cat in out_categories:
        print(f"[{cat['slug']}] {len(cat['cases'])} case(s)")
        for cs in cat["cases"]:
            print(f"  - {cs['slug']}: {len(cs['images'])} image(s)")

if __name__ == "__main__":
    if "--check" in sys.argv:
        problems = []
        if not IMG_DIR.exists():
            problems.append("Missing images/ directory.")
        else:
            for case_dir in [p for p in IMG_DIR.iterdir() if p.is_dir()]:
                problems.extend(validate_case(case_dir))
        if problems:
            print("Validation failed:\\n")
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
