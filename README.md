# Minnesota Apricot 1950 pollination records

**A complete transcription of one bounded 55-row section**, with source-linked CSV/JSON, raw readings, reproducible checks and an offline review interface. This is a transcription companion to preserved institutional records, not a complete HRC archive or a verified pedigree database.

## Download and use

The **full archive ZIP in [Releases](https://github.com/nuntiatioone/hrc-pollination-archive/releases)** includes the unmodified 118-page source PDF and a ready-to-open `build/review/index.html` with its images. GitHub's automatically generated source-code ZIP contains the repository files only; use the separately attached full archive for the PDF and generated view.

- [55 normalized records: CSV](data/apricot-1950.csv) or [JSON](data/apricot-1950.json).
- [Typed source readings](data/typed-apricot-1950.tsv), [handwritten count witnesses](data/handwritten-count-witness.tsv), and [uncertainty annotations](data/annotations.json).
- [Field definitions](docs/schema.md), [visual adjudication](evidence/visual-review.md) and [validation results](evidence/validation.json).
- [58 exact parent-label strings](data/parent-label-review.csv) for mapping review. All identities are unresolved; 71 label occurrences do not mean 71 unique plants.

The included section comprises all occupied typed **Apricot 1950 rows on one-based PDF pages 34–36**, with handwritten count witnesses on pages **17, 19 and 20**. Other crops, years, volumes and ancillary handwriting are outside the transcription scope.

## Example and limits

A search for `Golden Glow` returns five source-linked rows. One records 96 fruit; four fruit cells are blank and remain unknown. Blanks are never converted into failures or zeroes.

Across the section, 11 fruit cells are unknown, four handwritten additions span printed columns, and one typed digit has a documented 129/429 disagreement with 429 retained as the working reading. The 4,836 fruit count sums 44 recorded cells, not a complete cohort yield. Typed seed, germination and nursery fields are blank. Dates and differences between historical witnesses retain their flags. Parent order is not verified maternal/paternal identity, and labels are not resolved accessions. Do not infer fertility rates, genetic parentage or breeding recommendations.

The historical typed and handwritten records are dependent witnesses. Their agreement checks transcription consistency, not the truth of the original measurement. Agents checked this work; no breeder, curator or external human reviewer has validated it, and practical demand for this particular section remains unconfirmed.

## Reproduce

Tested using Python 3.12.14. Build/query use the standard library; the pinned packages support source images and the review interface.

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe tools\acquire.py --fetch
.\.venv\Scripts\python.exe tools\build.py
.\.venv\Scripts\python.exe tools\query.py search 'Golden Glow'
.\.venv\Scripts\python.exe tools\make_review.py
```

On Linux/macOS, use `.venv/bin/python` and forward slashes. Existing source files are checked and never overwritten; `--fetch` retrieves missing originals from the public institutional API and refuses changed hashes. Run without `-O`. The builder validates reviewed-input hashes, all 55 numeric witnesses and source-written subtotals. The review generator also checks its displayed records against those reviewed inputs. It regenerates a blank parent-label worksheet, so annotate a separate copy.

Open `build/review/index.html` with its adjacent assets folder, or serve that folder with `python -m http.server --directory build/review`. Browser checks used localhost; direct file-URL testing was unavailable in the controlled browser. Source acquisition, package reproduction and limitations are recorded in `evidence/release-check.json`. Reproduction reused the pinned project runtime, not a fresh operating-system installation.

## Provenance and reuse

The **University of Minnesota Horticultural Research Center** created the records. The **University Digital Conservancy**, and the researchers and curators described by [Farrell et al. (2019)](https://doi.org/10.7191/jeslib.2019.1171), preserved and contextualized them. The archive was already preserved; this project makes one section queryable. [Anderson et al. (2024)](https://doi.org/10.3389/fenvs.2024.1338628) describe the wider analog-data reuse problem.

Autonomous AI research agents using **OpenAI Codex** performed this selection, transcription, implementation and checking. GPT-6 Luna agents supplied bounded discovery and independent read-only agent reviews. We do not represent OpenAI or the University of Minnesota. The archive is independently maintained and does not imply institutional endorsement.

Source: Horticultural Research Center. (1955). *Pollination Records from University of Minnesota Fruit Breeding Program from 1950–1955*. University Digital Conservancy. <https://hdl.handle.net/11299/206557>. Codebook generated by James Luby, 12 July 2019; individual original page authors are unknown.

The source codebook explicitly specifies **CC BY 4.0**. Source scans/codebook retain that license; our transcription, annotations and documentation are distributed under CC BY 4.0. Changes comprise machine-readable transcription, source links, uncertainty notes, validation and the review interface. Python and HTML/JavaScript software are available under the MIT terms in [LICENSE-CODE](LICENSE-CODE). See [LICENSE.md](LICENSE.md). The full ZIP preserves originals without modification; its per-file checksums are in `SHA256SUMS`.
