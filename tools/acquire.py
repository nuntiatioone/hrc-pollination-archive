"""Verify preserved originals; --fetch retrieves only missing files via public URLs.

Existing files are never overwritten. Changed repository metadata is a version
change requiring review, not an excuse to silently replace the recorded snapshot.
"""
from pathlib import Path
import argparse
import hashlib
import json
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--fetch', action='store_true')
args = parser.parse_args()
manifest = json.loads((ROOT/'sources/manifest.json').read_text(encoding='utf-8'))
for item in manifest['files']:
    path = ROOT / item['path']
    if not path.exists():
        if not args.fetch:
            raise SystemExit(f'Missing {item["path"]}; use --fetch to retrieve.')
        request = urllib.request.Request(item['url'], headers={'User-Agent': 'HRC-archive-transcription/0.1 (bounded public-source retrieval)'})
        with urllib.request.urlopen(request, timeout=90) as response:
            content = response.read()
        if hashlib.sha256(content).hexdigest() != item['sha256']:
            raise SystemExit(f'Source changed: {item["path"]}; not saved. Review the version.')
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open('xb') as output:
            output.write(content)
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    if digest != item['sha256']:
        raise SystemExit(f'Hash mismatch: {item["path"]}')
    print(f'OK {item["path"]} {digest}')
