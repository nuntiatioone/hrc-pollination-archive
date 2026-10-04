"""Read-only example queries against the reproducible SQLite companion."""
from pathlib import Path
import argparse
import json
import sqlite3

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('command', choices=['demo','search','sql'], nargs='?', default='demo')
parser.add_argument('text', nargs='?')
args = parser.parse_args()
path = ROOT/'.local/apricot-1950.sqlite'
if not path.exists():
    raise SystemExit('Run tools/build.py first.')
db = sqlite3.connect(path.as_uri()+'?mode=ro', uri=True)
db.row_factory = sqlite3.Row


def query(sql, parameters=()):
    return [dict(row) for row in db.execute(sql, parameters)]


selection = '''SELECT breeding_no, cross_raw, flowers_pollinated,
fruit_matured_typed, typed_pdf_page, typed_page_row, annotation_codes
FROM records'''
if args.command == 'search':
    if args.text is None:
        parser.error('search requires a text fragment')
    result = query(selection+' WHERE instr(lower(cross_raw),lower(?)) > 0 ORDER BY sequence', (args.text,))
elif args.command == 'sql':
    if args.text is None:
        parser.error('sql requires a query string')
    result = query(args.text)
else:
    result = {
        'question': 'Which recorded crosses mention Golden Glow, and which outcomes are actually recorded?',
        'golden_glow_records': query(selection+" WHERE instr(cross_raw,'Golden Glow') > 0 ORDER BY sequence"),
        'missingness': query('''SELECT COUNT(*) AS records, COUNT(flowers_pollinated) AS flower_cells_recorded,
COUNT(fruit_matured_typed) AS fruit_cells_recorded,
COUNT(*)-COUNT(fruit_matured_typed) AS fruit_cells_blank,
COUNT(plump_seed_typed) AS plump_seed_cells_recorded,
COUNT(germinated_typed) AS germinated_cells_recorded FROM records'''),
        'typed_cross_descriptions': query('SELECT pollination_mode, COUNT(*) AS records FROM records GROUP BY pollination_mode ORDER BY pollination_mode'),
        'interpretation': 'These are statements about the preserved typed record, not biological success or genetically verified parents. Blank fruit cells remain null. See annotations.json for handwritten divergences.',
    }
print(json.dumps(result, indent=2))
db.close()
