# Schema and transcription conventions

`data/typed-apricot-1950.tsv` is the agent-authored reading of every occupied row in the typed section. It includes the eight printed data fields plus sequence and source location. `raw` means the visible field content is preserved as a reading, including abbreviations and incomplete dates; it does not reproduce spacing, underlines, overtyping or every incidental pen mark. Blank TSV cells represent blank cells, not zero.

`data/handwritten-count-witness.tsv` contains a separate reading of the numeric/date columns of the corresponding handwritten section. `[ditto]` marks visible ditto notation; `-` is a dash. It is not a full diplomatic transcription of the handwritten cross names. In the four overflow cases it preserves physical printed-cell placement and the whole apparent arithmetic expression; no separate biological measurements are inferred from those positions.

| Normalized field | Meaning |
|---|---|
| `record_id`, `sequence` | Local stable ID and 1–55 position, not an accession identifier. |
| `crop_recorded`, `year_pollinated` | Section headings: Apricot, 1950. No taxonomic harmonization. |
| `breeding_no`, `breeding_no_raw` | Uppercase, space-free query key plus source reading; `ATO` contains letter O. No added zero-padding. |
| `cross_raw` | Typed cross description, with spellings and abbreviations retained. |
| `recorded_parent_1`, `recorded_parent_2` | Text to left/right of ` x `, or sole named parent when no `x` appears. Tree/pot numbers remain in the text. These are labels, not authenticated genotypes or modern accessions; no sex assignment beyond source order is asserted. |
| `pollination_mode` | Syntactic category: `paired_parents_recorded`, `explicit_open`, or `unspecified_in_typed_cross`. The last is retained for eight ATo rows lacking an explicit open label. |
| `date_pol_raw`, `date_pol_iso` | Literal typed cell; ISO date only for complete month/day, using section year. Literal `3` remains raw with null ISO value. |
| `flowers_pollinated` | Integer count in typed No. Flrs. Pol., or null. |
| `fruit_matured_typed` | Integer under typed No. Fruit Matured, or null. Four historical aggregates are flagged; their semantic assignment is not newly verified. |
| `plump_seed_typed`, `germinated_typed`, `nursery_typed` | Typed field counts, all null in this section. No meaning is manufactured from handwritten overflow. |
| `annotation_codes` | Semicolon-separated kinds from `data/annotations.json`; join using sequence for full notes, including group notes. |
| `typed_pdf_page`, `typed_page_row`, `handwritten_pdf_page` | One-based PDF page and occupied-row positions. |
| `source_handle`, `source_sha256`, `source_pdf_link` | Institutional provenance, exact source version and relative file link with PDF page fragment. |

JSON uses null, CSV uses an empty field, and SQLite uses SQL NULL for missing normalized values. Count columns are integers; dates are text. No zeros are inferred. The source-written totals are transcription constraints, not guarantees of historical accuracy or completeness.

Input SHA-256 values are frozen in `evidence/reviewed-inputs.json`. Changing an input requires source review, documented adjudication and deliberate manifest update; a normal build refuses modified inputs. Git records versions. Original source hashes are independently fixed in `sources/manifest.json`; the builder checks the PDF version.
