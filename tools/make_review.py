"""Generate an offline, read-only reviewer view with exact source-page images.

No contacts, tracking, network requests, uploads, or inferred plant identifiers.
Generated files live under ignored build/review and can be regenerated from Git.
"""
from pathlib import Path
import csv
import hashlib
import io
import json
from collections import defaultdict
from PIL import Image
from pypdf import PdfReader
from build import read_tsv, transform

if not __debug__:
    raise RuntimeError('Run without -O: source integrity checks are required.')

ROOT = Path(__file__).resolve().parents[1]
out = ROOT/'build/review'
(out/'assets').mkdir(parents=True, exist_ok=True)
manifest = json.loads((ROOT/'sources/manifest.json').read_text())
source = ROOT/'sources/pollination-1950-1955.pdf'
expected = next(f['sha256'] for f in manifest['files'] if f['path'].endswith('.pdf'))
assert hashlib.sha256(source.read_bytes()).hexdigest() == expected
reviewed = json.loads((ROOT/'evidence/reviewed-inputs.json').read_text())
for name, digest in reviewed['sha256'].items():
    assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest() == digest
reader = PdfReader(source)
pages = {}
# Pixel coordinates are approximate context strips, not authoritative cell boxes.
# All strips link to the complete, unmodified embedded image for interpretation.
grid = {17:(426,2299,20),19:(390,2260,20),20:(396,1811,15),
        34:(377,2252,20),35:(369,2239,20),36:(406,1812,15)}
for number, (top, bottom, count) in grid.items():
    embedded = max(reader.pages[number-1].images, key=lambda x: len(x.data))
    filename = f'page-{number:03}{Path(embedded.name).suffix}'
    (out/'assets'/filename).write_bytes(embedded.data)
    w,h = Image.open(io.BytesIO(embedded.data)).size
    pages[str(number)] = dict(file='assets/'+filename,width=w,height=h,
                              top=top,step=(bottom-top)/count)
rows = json.loads((ROOT/'data/apricot-1950.json').read_text())
assert rows == [transform(raw) for raw in read_tsv('typed-apricot-1950.tsv')], 'Derived records differ from reviewed input'
with (ROOT/'data/handwritten-count-witness.tsv').open(newline='') as f:
    witness = {r['sequence']:r for r in csv.DictReader(f,delimiter='\t')}
payload = dict(rows=rows,witness=witness,pages=pages,
               annotations=json.loads((ROOT/'data/annotations.json').read_text()))
template = (ROOT/'tools/review-template.html').read_text(encoding='utf-8')
html = template.replace('__DATA__',json.dumps(payload).replace('<','\\u003c'))
(out/'index.html').write_text(html,encoding='utf-8',newline='\n')
# Exact textual labels only. Repeated labels are not proof of plant identity;
# different labels are not proof of different plants. No accession is inferred.
labels = defaultdict(list)
for row in rows:
    for position in (1,2):
        label = row[f'recorded_parent_{position}']
        if label:
            labels[label].append((row['record_id'],position))
fields = ['raw_parent_label','occurrences','record_ids','parent_positions',
          'mapping_status','candidate_accession_id','mapping_evidence','curator_note']
with (ROOT/'data/parent-label-review.csv').open('w',encoding='utf-8',newline='') as f:
    writer = csv.DictWriter(f,fieldnames=fields,lineterminator='\n')
    writer.writeheader()
    for label, occurrences in sorted(labels.items()):
        writer.writerow(dict(raw_parent_label=label,occurrences=len(occurrences),
            record_ids=';'.join(x[0] for x in occurrences),
            parent_positions=';'.join(str(x[1]) for x in occurrences),
            mapping_status='unresolved',candidate_accession_id='',mapping_evidence='',curator_note=''))
print(json.dumps({'html':'build/review/index.html','records':len(rows),
                  'source_images':len(pages),'source_sha256':expected,
                  'distinct_text_labels':len(labels),
                  'parent_occurrences':sum(map(len,labels.values()))}))
