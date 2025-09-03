# Contributing to Hi-C Gallery

## Folder layout (single-folder only)
Create one folder per case directly under `images/`:

```
images/
 └ <speciesID>_<authorID>/
    ├ <type>_<speciesID>_<authorID>_01.png
    ├ <type>_<speciesID>_<authorID>_01.txt
    ├ <type>_<speciesID>_<authorID>_02.png
    ├ <type>_<speciesID>_<authorID>_02.txt
    └ (optional) cover.png
```

- `<type>` is one of: `inversion`, `translocation`, `duplication`.
- All images in a case must share the same `<type>`.
- `XX` is a two-digit index (`01`, `02`, …) that controls gallery order.
- The `.txt` file must have the same base name as the image and contain the caption.
- Optional `cover.png` sets the case thumbnail.

## PR checklist
- [ ] Case folder named `<speciesID>_<authorID>` (or `case_<speciesID>_<authorID>`)
- [ ] PNG files named `<type>_<speciesID>_<authorID>_XX.png`
- [ ] Matching caption files `<type>_<speciesID>_<authorID>_XX.txt`
- [ ] All images use the **same `<type>`**

On pull requests, CI validates the above. On merge to `main`, `data.json` is rebuilt and the site updates.
