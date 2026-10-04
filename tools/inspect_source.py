"""Inspect the preserved PDF and render contact sheets from embedded page images."""
from pathlib import Path
import hashlib
import json
from pypdf import PdfReader
from PIL import Image, ImageOps, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
source = ROOT / 'sources/pollination-1950-1955.pdf'
reader = PdfReader(source)
out = ROOT / '.local/contact'
out.mkdir(parents=True, exist_ok=True)
thumbs = []
for n, page in enumerate(reader.pages, 1):
    images = list(page.images)
    image_file = max(images, key=lambda x: x.image.width*x.image.height)
    im = image_file.image.convert('RGB')
    thumb = ImageOps.contain(im, (290, 415))
    thumbs.append((n, thumb))
    # Save encoded source image, avoiding expensive recompression of large scans.
    (out / f'page-{n:03}{Path(image_file.name).suffix}').write_bytes(image_file.data)
    if n % 20 == 0:
        print(f'Inspected {n}/{len(reader.pages)} pages', flush=True)
for start in range(0, len(thumbs), 20):
    sheet = Image.new('RGB', (1500, 1800), 'white')
    draw = ImageDraw.Draw(sheet)
    for i, (n, im) in enumerate(thumbs[start:start+20]):
        x, y = (i % 5)*300, (i//5)*450
        draw.text((x+5, y+4), f'PDF page {n}', fill='black')
        sheet.paste(im, (x, y+25))
    sheet.save(out / f'contact-{start+1:03}-{min(start+20,len(thumbs)):03}.jpg')
result = {
    'source': str(source.relative_to(ROOT)).replace('\\','/'),
    'sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
    'bytes': source.stat().st_size,
    'pages': len(reader.pages),
    'nonspace_extracted_text_by_page': [len(''.join((p.extract_text() or '').split())) for p in reader.pages],
    'method': 'pypdf text extraction; embedded images rendered with Pillow for visual inspection',
}
(ROOT/'evidence/source-inspection.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8', newline='\n')
print(json.dumps({k:v for k,v in result.items() if k!='nonspace_extracted_text_by_page'},indent=2))
