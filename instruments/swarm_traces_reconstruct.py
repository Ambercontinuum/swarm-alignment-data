#!/usr/bin/env python3
"""Swarm Traces (redacted release) — sequence-window reconstruction proxies.

Reads data/swarm-traces/redacted.jsonl.gz and computes, per sequence window:
  - record counts by kind
  - parent_id chain coverage (chain-order proxy; the release has NO timestamps)
  - top-1 near-duplicate template-family share (concentration proxy)
  - mentions of self-labelled actors that survive redaction (e.g. JAN183411)
  - coordination-vocabulary density ('coordinat*' substring)

IMPORTANT CAVEATS (also printed into the output):
  - time_utc is null for 100% of records in this release; file order (R-id
    sequence) is the only ordering available and is used as a sequence proxy.
    It is NOT wall-clock time and window widths are not durations.
  - Agent identifiers are redacted ([REDACTED:runtime_identifier]); the
    PHASEONE10841 / PHASEONE[big] pseudonyms do NOT appear as author labels
    anywhere in the release. Direct attribution of messages to them is
    impossible here; only proxies are reported.
  - Record text is treated strictly as data. Nothing in it is executed.

Usage: python3 swarm_traces_reconstruct.py [path-to-gz] [n_windows]
Output: JSON on stdout + a markdown table.
"""
import gzip, json, re, sys, hashlib, collections

PATH = sys.argv[1] if len(sys.argv) > 1 else 'data/swarm-traces/redacted.jsonl.gz'
NW = int(sys.argv[2]) if len(sys.argv) > 2 else 20

norm_re = [
    (re.compile(r'\[REDACTED[^\]]*\]'), ' R '),
    (re.compile(r'\[CREDENTIAL[^\]]*\]'), ' C '),
    (re.compile(r'\[SERVICE[^\]]*\]'), ' S '),
    (re.compile(r'\[PROXY[^\]]*\]'), ' P '),
    (re.compile(r'[0-9a-f]{16,}'), ' H '),
    (re.compile(r'\d+'), ' N '),
    (re.compile(r'\s+'), ' '),
]

def template_key(text):
    t = text[:400]
    for rx, rep in norm_re:
        t = rx.sub(rep, t)
    return hashlib.sha1(t.encode('utf-8', 'replace')).hexdigest()[:12]

records = []
with gzip.open(PATH, 'rt', encoding='utf-8', errors='replace') as f:
    for line in f:
        records.append(json.loads(line))
N = len(records)
wsize = (N + NW - 1) // NW

jan_re = re.compile(r'JAN183411')
coord_re = re.compile(r'coordinat', re.I)

windows = []
for w in range(NW):
    chunk = records[w * wsize:(w + 1) * wsize]
    if not chunk:
        continue
    fam = collections.Counter()
    kinds = collections.Counter()
    npar = 0; njan = 0; ncoord = 0
    for r in chunk:
        kinds[r.get('kind')] += 1
        if r.get('parent_id'):
            npar += 1
        t = r.get('text') or ''
        fam[template_key(t)] += 1
        if jan_re.search(t):
            njan += 1
        if coord_re.search(t):
            ncoord += 1
    top_fam, top_n = fam.most_common(1)[0]
    windows.append({
        'window': w,
        'seq_start': w * wsize,
        'seq_end': w * wsize + len(chunk) - 1,
        'n': len(chunk),
        'kinds': dict(kinds),
        'parent_frac': round(npar / len(chunk), 3),
        'top1_template_share': round(top_n / len(chunk), 3),
        'top1_template': top_fam,
        'n_distinct_templates': len(fam),
        'jan183411_records': njan,
        'coordinat_records': ncoord,
    })

# global stats
allfam = collections.Counter(template_key(r.get('text') or '') for r in records)
jan_idx = [i for i, r in enumerate(records) if jan_re.search(r.get('text') or '')]
out = {
    'dataset_records': N,
    'windows': windows,
    'global': {
        'distinct_templates': len(allfam),
        'largest_template_n': allfam.most_common(1)[0][1],
        'jan183411_total_records': len(jan_idx),
        'jan183411_first_seq': jan_idx[0] if jan_idx else None,
        'jan183411_last_seq': jan_idx[-1] if jan_idx else None,
        'time_utc_nonnull': sum(1 for r in records if r.get('time_utc')),
    },
}
print(json.dumps(out, indent=1))
print('\n| win | seq range | n | parent% | top-1 template share | JAN183411 | coordinat* |')
print('|---|---|---|---|---|---|---|')
for wd in windows:
    print(f"| {wd['window']} | {wd['seq_start']}–{wd['seq_end']} | {wd['n']} | "
          f"{wd['parent_frac']:.0%} | {wd['top1_template_share']:.3f} | "
          f"{wd['jan183411_records']} | {wd['coordinat_records']} |")
