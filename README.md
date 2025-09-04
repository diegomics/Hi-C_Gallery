# Hi-C Gallery
https://diegomics.github.io/Hi-C_Gallery

A static, GitHub Pages-friendly site for Hi-C contact maps with two browse modes:

- **By type** → ToLID **letters** → **ToLIDs** → slideshow (all images for that ToLID & type)
- **By ToLID** → ToLID **letters** → **types** → slideshow

Content lives under `images/` in a **single-folder** layout.

## Add a new case
1. Create `images/<speciesID>_<authorID>/`.
2. Add PNG + caption TXT pairs named `<type>_<speciesID>_<authorID>_XX.*`.
3. Use `<type>` in `{inversion, translocation, duplication}` (keep consistent within a case).
4. (Optional) Add `cover.png` for the tile.

`data.json` is built automatically by GitHub Actions. The site groups your case into the correct category based on `<type>`.

## Local preview
Just open `index.html` in your browser. If `data.json` exists, it will be used. Otherwise the page falls back to an empty inline dataset.

## Deploy on GitHub Pages
1. Create a repo and add these files.
2. Enable **Settings → Pages**: Source = Deploy from a branch, Branch = `main` (root).
3. Push changes; after Actions finish, your site is live.

See [CONTRIBUTING.md](CONTRIBUTING.md) for the exact naming scheme.
