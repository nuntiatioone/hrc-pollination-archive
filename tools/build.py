"""Build and validate the bounded transcription using only Python's standard library.

The hand-entered TSVs are the inputs, not generated OCR. SQLite/CSV/JSON are
derived companions; no ambiguous handwritten physical cell becomes a seed count.
"""
from pathlib import Path
import csv
import hashlib
import json
import re
import sqlite3
import sys

ROOT = Path(__file__).resolve().parents[1]
SOURCE_SHA = 'e6d76c5d41e013a193667914ffbeace5e3e9875262686df74ad940c9a646b298'


def read_tsv(name):
    with (ROOT / 'data' / name).open(encoding='utf-8', newline='') as stream:
        rows = list(csv.DictReader(stream, delimiter='\t'))
    if any(None in row or None in row.values() for row in rows):
        raise ValueError(f'Misaligned or incomplete TSV row in {name}')
    return rows


def number(raw):
    if raw == '':
        return None
    if not re.fullmatch(r'\d+', raw):
        raise ValueError(f'Not a plain nonnegative integer: {raw!r}')
    return int(raw)


def transform(raw):
    seq = int(raw['sequence'])
    cross = raw['cross_raw']
    if ' x ' in cross:
        parent1, parent2 = cross.split(' x ', 1)
        mode = 'paired_parents_recorded'
    elif cross.endswith(' open'):
        parent1, parent2, mode = cross[:-5], None, 'explicit_open'
    else:
        parent1, parent2, mode = cross, None, 'unspecified_in_typed_cross'
    date = raw['date_pol_raw']
    date_iso = None
    if re.fullmatch(r'\d{1,2}/\d{1,2}', date):
        month, day = map(int, date.split('/'))
        from datetime import date as Date
        date_iso = Date(1950, month, day).isoformat()
    annotations = json.loads((ROOT/'data/annotations.json').read_text(encoding='utf-8'))
    flags = [n['kind'] for n in annotations['row_notes'] if n['sequence'] == seq]
    flags += [n['kind'] for n in annotations['group_notes'] if seq in n['sequences']]
    return {
        'record_id': f'hrc-apricot-1950-{seq:02}',
        'sequence': seq, 'crop_recorded': 'Apricot', 'year_pollinated': 1950,
        'breeding_no': raw['breeding_no_raw'].replace(' ', '').upper(),
        'breeding_no_raw': raw['breeding_no_raw'], 'cross_raw': cross,
        'recorded_parent_1': parent1, 'recorded_parent_2': parent2,
        'pollination_mode': mode,
        'date_pol_raw': date, 'date_pol_iso': date_iso,
        'flowers_pollinated': number(raw['flowers_pol_raw']),
        'fruit_matured_typed': number(raw['fruit_matured_raw']),
        'plump_seed_typed': number(raw['plump_seed_raw']),
        'germinated_typed': number(raw['germinated_raw']),
        'nursery_typed': number(raw['nursery_raw']),
        'annotation_codes': ';'.join(flags),
        'typed_pdf_page': int(raw['pdf_page']), 'typed_page_row': int(raw['page_row']),
        'handwritten_pdf_page': 17 if seq <= 20 else 19 if seq <= 40 else 20,
        'source_handle': 'https://hdl.handle.net/11299/206557',
        'source_sha256': SOURCE_SHA,
        'source_pdf_link': f'../sources/pollination-1950-1955.pdf#page={raw["pdf_page"]}',
    }


def validate(typed, handwritten, rows):
    expected = list(range(1, 56))
    assert [int(r['sequence']) for r in typed] == expected
    assert [int(r['sequence']) for r in handwritten] == expected
    assert len({r['breeding_no'] for r in rows}) == 55
    comparisons = []
    for raw, witness, row in zip(typed, handwritten, rows):
        assert int(witness['pdf_page']) == row['handwritten_pdf_page']
        seq = row['sequence']
        assert int(raw['pdf_page']) == (34 if seq <= 20 else 35 if seq <= 40 else 36)
        assert int(raw['page_row']) == (seq if seq <= 20 else seq - 20 if seq <= 40 else seq - 40)
        expr = witness['cross_column_expression']
        if expr:
            assert re.fullmatch(r'\d+( \+ \d+)+', expr)
            value = sum(int(part) for part in expr.split(' + '))
            basis = 'arithmetic correspondence only; cross-column semantics unresolved'
        else:
            value = number(witness['fruit_cell_raw'])
            basis = 'literal count or blank'
        assert value == row['fruit_matured_typed'], f'Count disagreement at {seq}'
        if seq <= 16:
            assert number(witness['flowers_pol_raw']) == row['flowers_pollinated']
        comparisons.append({'sequence': seq, 'typed_fruit': row['fruit_matured_typed'],
                            'handwritten_comparison': value, 'basis': basis})
    # Independent totals explicitly written in the original, not synthetic ranges.
    assert sum(r['flowers_pollinated'] or 0 for r in rows[:16]) == 3719
    assert sum(r['fruit_matured_typed'] or 0 for r in rows[:16]) == 280
    assert sum(r['fruit_matured_typed'] for r in rows[16:]) == 4556
    # Actual failure risks encountered during recovery.
    assert rows[1]['fruit_matured_typed'] is None  # blank is not zero
    assert rows[16]['date_pol_raw'] == '3' and rows[16]['date_pol_iso'] is None
    assert rows[16]['breeding_no'] == 'ATO5017'  # O is not a zero
    assert rows[32]['pollination_mode'] == 'unspecified_in_typed_cross'
    assert all(r['plump_seed_typed'] is None and r['germinated_typed'] is None for r in rows)
    assert rows[19]['fruit_matured_typed'] == 1106
    return comparisons


def build():
    source = ROOT / 'sources/pollination-1950-1955.pdf'
    if hashlib.sha256(source.read_bytes()).hexdigest() != SOURCE_SHA:
        raise ValueError('Source PDF hash differs from reviewed version')
    reviewed = json.loads((ROOT/'evidence/reviewed-inputs.json').read_text(encoding='utf-8'))
    for relative_path, expected_hash in reviewed['sha256'].items():
        if hashlib.sha256((ROOT/relative_path).read_bytes()).hexdigest() != expected_hash:
            raise ValueError(f'Reviewed input changed: {relative_path}; re-review before updating the review manifest')
    typed = read_tsv('typed-apricot-1950.tsv')
    handwritten = read_tsv('handwritten-count-witness.tsv')
    rows = [transform(r) for r in typed]
    comparisons = validate(typed, handwritten, rows)
    (ROOT/'data/apricot-1950.json').write_text(json.dumps(rows, indent=2)+'\n', encoding='utf-8', newline='\n')
    with (ROOT/'data/apricot-1950.csv').open('w', newline='', encoding='utf-8') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]), lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)
    output = ROOT / '.local/apricot-1950.sqlite'
    output.parent.mkdir(exist_ok=True)
    with sqlite3.connect(output) as db:
        db.execute('DROP TABLE IF EXISTS records')
        columns = ', '.join('"'+k+'" '+('INTEGER' if isinstance(v, int) or k in
            ['plump_seed_typed','germinated_typed','nursery_typed'] else 'TEXT') for k,v in rows[0].items())
        db.execute('CREATE TABLE records ('+columns+')')
        db.executemany('INSERT INTO records VALUES ('+','.join('?' for _ in rows[0])+')',
                       [list(r.values()) for r in rows])
    evidence = {
        'validation_scope': 'Structural checks, source hash, comparison to a separately read handwritten witness, and source-written totals. Not external scientific validation.',
        'source_sha256': SOURCE_SHA, 'records': 55,
        'input_hashes': {p: hashlib.sha256((ROOT/'data'/p).read_bytes()).hexdigest()
                         for p in ['typed-apricot-1950.tsv','handwritten-count-witness.tsv','annotations.json']},
        'flowers_known_first_16': 3719, 'fruit_known_first_16': 280,
        'fruit_typed_ATO_series_39_rows': 4556, 'fruit_sum_recorded_cells_across_55_rows': 4836,
        'sum_limitation': '44 recorded typed cells summed; 11 blanks excluded. This is not complete cohort yield or independent biological validation.',
        'blank_fruit_cells': 11, 'cross_column_expressions': 4,
        'comparisons': comparisons,
    }
    (ROOT/'evidence/validation.json').write_text(json.dumps(evidence, indent=2)+'\n', encoding='utf-8', newline='\n')
    print(json.dumps({k:v for k,v in evidence.items() if k not in ['comparisons','input_hashes']},indent=2))


if __name__ == '__main__':
    if sys.flags.optimize:
        raise SystemExit('Run without -O: validation assertions are required.')
    build()
