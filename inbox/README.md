# To contribute:

1. Open a Pull Request that adds **a new folder** here inside this `inbox/` folder
   - Pick a sensible name, e.g. `asm123_Genoscope` or `fValHis_Tom`
2. In your new folder, place:
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
