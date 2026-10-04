# Visual review and adjudication

Reviewed 4 October 2026. This is review by autonomous agents, **not external human validation**. Original source: `sources/pollination-1950-1955.pdf`, SHA-256 in the manifest. PDF page numbers are one-based.

The lead agent read all six relevant page images: handwritten 17, 19, 20 and historical typed 34–36. Page 18 contains crossed-out plum notes and is not an apricot continuation. Typed pages contain 20 + 20 + 15 occupied rows; the corresponding handwritten pages have the same row sequence. The scope is this section of this volume, not every surviving 1950 apricot record in all HRC volumes.

The lead authored the 55-row typed TSV and separately read the handwritten count witness. A GPT-6 Luna agent (`biology_gap_scan`) independently returned all 55 typed rows without reading the lead's TSV. Another GPT-6 Luna agent (`history_gap_scan`) compared the original images with the historical typed copies, again without reading the lead's TSV. The source copies are historically dependent, so agreement between them is not independent biological corroboration.

## Disagreements and limits

- **Ato 5054, fruit:** lead reads 429; typed-only agent reads 129, including after a crop recheck; comparative agent reads 429 and recognizes ambiguity. The lead retains **429** because the typewriter's open `4` matches `435` immediately below and other `4` glyphs, the handwritten value is clearly 429, and the original ATo subtotal 4556 matches all 39 typed values with 429 (using 129 would give 4256). This is an explicit adjudication, not unanimous agent agreement. The row remains flagged in machine-readable annotations.
- **Ato 5022, parent label:** the independent typed read initially omitted the final `c` in `Apric`. Original-pixel crop confirms `Apric #28 open`; agent accepted correction. The TSV retains the source's unusual abbreviation.
- **Ato 5017:** the typed-only agent's response contained an extra tab; agent confirmed 57 is Fruit Matured, Flowers Pollinated is blank, and date text is just `3`. The authored TSV has the correct fields. The handwritten date is a dash; the full date remains null.
- **Ato 5020:** the comparison agent's preliminary response omitted the final `+ 35`, reading 1071. Reinspection confirmed handwritten `318 + 753 + 35` and typed 1106. Final count comparison agrees. Preliminary numbers are not promoted to data.
- **Ato 5024:** the handwritten separator between 74 and 193 is less clear than the other plus signs. The witness represents the apparent additive expression `74 + 193` but its interpretation remains flagged; the historical typed result is unambiguously 267.
- The comparison agent's general statement that all dates and parents matched was too broad: the lead explicitly retains the isolated `3` versus dash, the N2644 `(Tub)` versus `(P. armeniaca)` description, and missing `open` labels. Do not use the broad statement as validation of those differences.
- Faint ancillary handwriting is uncertain: the short note above CROSS and parts of the left margin are not required to compute the typed table. Readings in annotations are tentative and do not become normalized values.

The four cross-column expressions are stored as physical cell readings plus expressions. A printed column location does not establish that an overflow number measures plump seeds or germination. Conversely, a historical typist's sum does not prove the intended field semantics. The normalized count is therefore explicitly named `fruit_matured_typed`, and source differences remain inspectable.

The original totals support transcription consistency: 3719 flowers and 280 recorded matured fruit for the first 16 rows; 4556 for the 39 ATo entries. The eleven blank fruit cells are not zero. No rate of failed crosses, seed germination rate, or germplasm recommendation is justified by this pilot.

A third GPT-6 Luna agent (`economics_gap_scan`) checked conversion read-only: all 55 normalized records matched the existing CSV, JSON and SQLite, with missing values preserved. It requested clearer wording for the 4836 sum and stronger version checks on transcription inputs. The lead renamed the evidence field to identify a sum of recorded cells, explicitly stated the eleven excluded blanks, and added a frozen reviewed-input hash manifest. This audit did not supply biological validation or another independent reading of every source cell.
