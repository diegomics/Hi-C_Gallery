# Hi-C Gallery
https://diegomics.github.io/Hi-C_Gallery

A static, GitHub Pages–friendly gallery for Hi-C contact maps related to **assembly curation**, with two browse modes:

- **By type** → ToLID **prefix** → **ToLIDs** → slideshow (all images for that ToLID & type)
- **By ToLID** → ToLID **prefix** → **types** → slideshow

Content lives under `images/` in a **single-folder** layout. 
`data.json` is built automatically by GitHub Actions; the site groups each case into the correct category based on `<type>`.


## Contribute your cases!
We keep contributions simple. You don’t need to follow any strict file naming

1. Open a Pull Request that adds **a new folder** under `inbox/`
   - Pick a sensible name, e.g. `asm123_Genoscope` or `fValHis_Tom`
2. Inside that folder, place:
   - all your **PNG** images (any filenames)
   - one **text file** (e.g. `notes.txt`) that lists each image, its **type** (currently we are using`inversion`, `translocation`, `duplication`, but you can add other types), and a short **caption** explaining the feature.



### Example submission in `inbox/` 
```
inbox/
 ├── mEleMax_Genoscope/
 │    ├── contactmap_inv.png
 │    ├── transloc_1.png
 │    └── notes.txt
```
**Example `notes.txt` (free format, just keep it clear):**
```
mEleMax assembly; HiFi + Hi-C; hifiasm 0.25; dual-hap curation mode.
Curator: Lola from Genoscope. More info: https://github.com/ERGA-consortium/EARs

contactmap_inv.png: inversion. Corner-like contact enrichment between gaps; increased repetitive coverage.
transloc_1.PNG: translocation. Off-diagonal stripe suggests inter-chromosomal contact.
```
That’s it! We’ll review the PR. After merge, **maintainers** will place files into `images/<speciesID>_<authorID>/` with the required naming scheme for the site and remove the processed `inbox/<...>` folder.

---

## Local preview
Just open `index.html` in your browser. 
If `data.json` exists, it will be used; otherwise the page falls back to an empty inline dataset.
