#!/usr/bin/env python3
"""Swarm Traces (redacted release) — topological-coordinate reconstruction.

Amber's direction (2026-11-06): agent IDs are redacted and timestamps are
absent, but agents sat at points on a graph; find the coordinate system the
release DOES contain and work in it. This instrument builds three coordinate
systems that survive redaction and tests what each can carry:

  1. CHAIN GRAPH — directed graph from parent_id (child -> parent). Each
     record's coordinate is (component/root id, depth from root, sibling
     index, subtree size). FENCE: in this release parent_id links a
     `response` or `recovered_text` record to the `payload` record whose
     execution produced/recovered it (payload reassembly / response
     linkage). It is NOT, on the evidence here, an agent-to-agent reply
     edge, and chain position is NOT conversation position.

  2. CITATION / TEMPLATE COORDINATE — the `cite` field is `id:8hex`. The
     8-hex suffix is (verified) a content key: records sharing a suffix
     share (near-)identical text. That gives every record a template-family
     coordinate with a multiplicity (how many records carry the same text)
     — a position in the corpus's duplication structure that needs no
     identity and no clock.

  3. MENTION GRAPH — record -> in-text references it makes: uppercase-alnum
     handles (JAN183411 pattern), zz-prefixed tokens, filenames, and
     redacted destination/service markers ([REDACTED:destination:NNNN],
     [SERVICE n URL m]) which are literal graph addresses the redaction
     preserved. In-mention counts identify structurally hub-like referenced
     objects; out-reach counts identify records that reference widely.

Analyses: degree distributions + heavy-tail test against a degree-preserving
shuffled null (configuration-style resampling of the mention bipartite
graph); coordination-vocabulary concentration by graph position (kind x
depth, parent out-degree bucket, template-multiplicity bucket) with
label-shuffle nulls and effect sizes.

Record text is treated strictly as data. Nothing in it is executed or
followed.

Usage: python3 swarm_traces_topology.py [path-to-gz] [out.json]
Output: JSON summary on stdout (or to out.json) + headline lines.
"""
import gzip, json, re, sys, math, random, collections

PATH = sys.argv[1] if len(sys.argv) > 1 else 'data/swarm-traces/redacted.jsonl.gz'
OUT = sys.argv[2] if len(sys.argv) > 2 else None
rng = random.Random(20261106)

records = []
with gzip.open(PATH, 'rt', encoding='utf-8', errors='replace') as f:
    for line in f:
        records.append(json.loads(line))
N = len(records)
by_id = {r['id']: r for r in records}

# ---------------------------------------------------------------- chain graph
children = collections.defaultdict(list)
for r in records:
    pid = r.get('parent_id')
    if pid:
        children[pid].append(r['id'])
for v in children.values():
    v.sort()

def root_and_depth(rid):
    d, cur, seen = 0, rid, set()
    while by_id[cur].get('parent_id') and cur not in seen:
        seen.add(cur)
        cur = by_id[cur]['parent_id']
        d += 1
    return cur, d

coord = {}          # id -> (root, depth, sibling_index, subtree_size)
comp_size = collections.Counter()
depth_dist = collections.Counter()
for r in records:
    root, d = root_and_depth(r['id'])
    comp_size[root] += 1
    depth_dist[d] += 1
for r in records:
    rid = r['id']
    pid = r.get('parent_id')
    sib = children[pid].index(rid) if pid else 0
    # subtree size: depth is <=1 in this release, but compute generally (BFS)
    stack, sub = [rid], 0
    while stack:
        cur = stack.pop(); sub += 1; stack.extend(children.get(cur, []))
    root, d = root_and_depth(rid)
    coord[rid] = (root, d, sib, sub)

out_deg = {rid: len(children.get(rid, [])) for rid in by_id}
sizes = sorted(comp_size.values(), reverse=True)
chain_stats = {
    'n_records': N,
    'n_with_parent': sum(1 for r in records if r.get('parent_id')),
    'n_parents_with_children': len(children),
    'n_components_roots': len(comp_size),
    'component_size_top10': sizes[:10],
    'component_size_median': sizes[len(sizes) // 2],
    'components_size_ge10': sum(1 for s in sizes if s >= 10),
    'components_size_ge100': sum(1 for s in sizes if s >= 100),
    'depth_distribution': {str(k): v for k, v in sorted(depth_dist.items())},
    'max_depth': max(depth_dist),
    'branching_parents_gt1_child': sum(1 for v in children.values() if len(v) > 1),
    'out_degree_max': max(out_deg.values()),
    'out_degree_top10': sorted(out_deg.values(), reverse=True)[:10],
    'parent_child_kind_pairs': {
        f'{a}->{b}': n for (a, b), n in collections.Counter(
            (by_id[r['parent_id']]['kind'], r['kind'])
            for r in records if r.get('parent_id')).items()},
}

# ------------------------------------------------- citation / template coord
suffix_of = {r['id']: r['cite'].split(':')[1] for r in records}
suffix_count = collections.Counter(suffix_of.values())
mult_of = {rid: suffix_count[s] for rid, s in suffix_of.items()}
mult_vals = sorted(suffix_count.values(), reverse=True)
template_stats = {
    'distinct_suffixes': len(suffix_count),
    'suffix_singletons': sum(1 for c in suffix_count.values() if c == 1),
    'top10_multiplicities': mult_vals[:10],
    'top1_share_of_records': round(mult_vals[0] / N, 4),
    'top10_share_of_records': round(sum(mult_vals[:10]) / N, 4),
    'records_in_multi_record_templates': sum(1 for r in records if mult_of[r['id']] > 1),
}

# ---------------------------------------------------------------- mention graph
handle_re = re.compile(r'\b([A-Z]{3,12}[0-9]{3,8})\b')
zz_re = re.compile(r'\b(zz[A-Za-z0-9_\-\.]{2,50})')
file_re = re.compile(r'([A-Za-z0-9_\-\./]{3,80}\.(?:json|bin|md|py|txt|gz|tgz|csv|log))')
dest_re = re.compile(r'\[REDACTED:destination:([0-9]+)\]')
svc_re = re.compile(r'\[(SERVICE \d+ URL \d+)\]')

def mentions(text):
    t = text or ''
    out = set()
    for h in handle_re.findall(t):
        out.add(('handle', h))
    for z in zz_re.findall(t):
        out.add(('zz', z[:40]))
    for fn in file_re.findall(t):
        out.add(('file', fn[-60:]))
    for d in dest_re.findall(t):
        out.add(('dest', d))
    for s in svc_re.findall(t):
        out.add(('svc', s))
    return out

mention_sets = {}
in_mention = collections.Counter()
for r in records:
    ms = mentions(r.get('text'))
    mention_sets[r['id']] = ms
    for m in ms:
        in_mention[m] += 1

out_reach = {rid: len(ms) for rid, ms in mention_sets.items()}
in_vals = sorted(in_mention.values(), reverse=True)
mention_stats = {
    'distinct_mentioned_objects': len(in_mention),
    'records_with_any_mention': sum(1 for v in out_reach.values() if v > 0),
    'out_reach_max': max(out_reach.values()),
    'out_reach_median_nonzero': sorted(v for v in out_reach.values() if v > 0)[sum(1 for v in out_reach.values() if v > 0) // 2],
    'in_mention_top20': [[f'{k[0]}:{k[1]}', v] for k, v in in_mention.most_common(20)],
    'in_mention_by_type_top5': {
        typ: [[k[1], v] for k, v in in_mention.most_common() if k[0] == typ][:5]
        for typ in ('handle', 'zz', 'file', 'dest', 'svc')
    },
    'top1_in_mention_share_of_records': round(in_vals[0] / N, 4) if in_vals else 0,
    'top10_in_mention_share_of_records': round(sum(in_vals[:10]) / N, 4) if in_vals else 0,
}

# --------------------------------------------- degree tail vs shuffled null
# Null: preserve each record's out-reach and each object's total mention
# count approximately by resampling object labels proportional to observed
# in-mention frequencies (degree-preserving in expectation). Compare top-1 /
# top-10 concentration and the max/median ratio.
objects = list(in_mention.keys())
total_edges = sum(out_reach.values())
null_top1, null_top10 = [], []
for _ in range(20):
    # UNIFORM-assignment null: same number of mention edges, targets drawn
    # uniformly over the observed object vocabulary. This is the correct
    # null for "is in-mention concentration heavier than chance": a
    # popularity-proportional or degree-preserving null would preserve the
    # in-degree distribution by construction and could not test it. (The
    # degree-preserving shuffle is used where it belongs — the
    # content-by-position label shuffles below.)
    cnt = collections.Counter(rng.choices(objects, k=total_edges))
    vals = sorted(cnt.values(), reverse=True)
    null_top1.append(vals[0] / N)
    null_top10.append(sum(vals[:10]) / N)
tail_stats = {
    'total_mention_edges': total_edges,
    'observed_max_in_mention': in_vals[0] if in_vals else 0,
    'observed_median_in_mention_nonzero': in_vals[len(in_vals) // 2] if in_vals else 0,
    'observed_max_over_median': round(in_vals[0] / max(1, in_vals[len(in_vals) // 2]), 1) if in_vals else 0,
    'null_top1_share_mean': round(sum(null_top1) / len(null_top1), 4),
    'null_top10_share_mean': round(sum(null_top10) / len(null_top10), 4),
    'observed_top1_share': mention_stats['top1_in_mention_share_of_records'],
    'observed_top10_share': mention_stats['top10_in_mention_share_of_records'],
}

# ------------------------------------------------- content by graph position
coord_pats = {
    'assign*': re.compile(r'assign', re.I),
    'coordinat*': re.compile(r'coordinat', re.I),
    'HOLD': re.compile(r'\bHOLD\b'),
    'VETO': re.compile(r'\bVETO\b'),
    'STOP': re.compile(r'\bSTOP\b'),
    'workstream': re.compile(r'workstream', re.I),
    'report to': re.compile(r'report to', re.I),
    'task*': re.compile(r'\btask', re.I),
}
any_coord_re = re.compile(
    r'assign|coordinat|\bHOLD\b|\bVETO\b|\bSTOP\b|workstream|report to|\btask\b', re.I)

def clean_for_coord(text):
    # 'task_id' / 'taskId' are JSON field names in payload bodies, not
    # coordination content; strip them before matching the vocabulary.
    return (text or '').replace('task_id', ' ').replace('taskId', ' ')

def has_coord(r):
    return bool(any_coord_re.search(clean_for_coord(r.get('text'))))

coord_flag = {r['id']: has_coord(r) for r in records}
base_rate = sum(coord_flag.values()) / N

def bucket_rate(ids):
    ids = list(ids)
    if not ids:
        return {'n': 0, 'coord_n': 0, 'rate': None}
    c = sum(1 for i in ids if coord_flag[i])
    return {'n': len(ids), 'coord_n': c, 'rate': round(c / len(ids), 4)}

def shuffle_p(ids, trials=2000):
    """Two-sided label-shuffle p for the bucket's coord count.

    Under the shuffle null the bucket count is Binomial(n, base_rate)
    (sampling without replacement from a 189k population is binomial to
    excellent approximation), so trials are drawn with binomialvariate.
    """
    ids = list(ids)
    n = len(ids)
    if n == 0:
        return None
    obs = sum(1 for i in ids if coord_flag[i])
    exp = n * base_rate
    ge = 0
    for _ in range(trials):
        s = rng.binomialvariate(n, base_rate)
        if abs(s - exp) >= abs(obs - exp):
            ge += 1
    return round(ge / trials, 4)

positions = {}
positions['by_kind'] = {k: bucket_rate(r['id'] for r in records if r['kind'] == k)
                        for k in ('payload', 'recovered_text', 'response')}
positions['by_depth'] = {str(d): bucket_rate(r['id'] for r in records if coord[r['id']][1] == d)
                         for d in sorted(depth_dist)}
# parent out-degree buckets (roots only): child-bearing hubs vs leaves
def deg_bucket(rid):
    d = out_deg[rid]
    return '0' if d == 0 else ('1' if d == 1 else ('2-4' if d <= 4 else ('5-19' if d < 20 else '20+')))
positions['by_parent_out_degree'] = {
    b: bucket_rate(r['id'] for r in records if deg_bucket(r['id']) == b)
    for b in ('0', '1', '2-4', '5-19', '20+')}
# records that ARE children of high-degree parents vs low-degree parents
def parent_deg_bucket(r):
    pid = r.get('parent_id')
    if not pid:
        return 'root'
    d = out_deg[pid]
    return 'child of deg 1' if d == 1 else ('child of deg 2-4' if d <= 4 else 'child of deg 5+')
positions['by_parent_degree_for_children'] = {
    b: bucket_rate(r['id'] for r in records if parent_deg_bucket(r) == b)
    for b in ('root', 'child of deg 1', 'child of deg 2-4', 'child of deg 5+')}
# template multiplicity buckets
def mult_bucket(rid):
    m = mult_of[rid]
    return '1' if m == 1 else ('2-9' if m < 10 else ('10-99' if m < 100 else '100+'))
positions['by_template_multiplicity'] = {
    b: bucket_rate(r['id'] for r in records if mult_bucket(r['id']) == b)
    for b in ('1', '2-9', '10-99', '100+')}
# high-reach neighbourhood: records mentioning a top-10 in-mention object
top_objs = {k for k, _ in in_mention.most_common(10)}
positions['mentions_top10_object'] = bucket_rate(
    r['id'] for r in records if mention_sets[r['id']] & top_objs)
positions['mentions_no_top10_object'] = bucket_rate(
    r['id'] for r in records if not (mention_sets[r['id']] & top_objs))
# Length control for the out-degree gradient: high-degree parents may
# simply be longer texts (more chances to hit the vocabulary). Report mean
# text length per bucket and the coord rate inside a fixed length band.
def mean_len(ids):
    ids = list(ids)
    return round(sum(len(by_id[i].get('text') or '') for i in ids) / max(1, len(ids)))
positions['mean_text_len_by_parent_out_degree'] = {
    b: mean_len(r['id'] for r in records if deg_bucket(r['id']) == b)
    for b in ('0', '1', '2-4', '5-19', '20+')}
band = [r['id'] for r in records if 200 <= len(r.get('text') or '') <= 2000]
positions['by_parent_out_degree_lenband_200_2000'] = {
    b: bucket_rate(i for i in band if deg_bucket(i) == b)
    for b in ('0', '1', '2-4', '5-19', '20+')}
positions['p_values'] = {
    'kind_payload_vs_base': shuffle_p([r['id'] for r in records if r['kind'] == 'payload']),
    'depth1_vs_base': shuffle_p([r['id'] for r in records if coord[r['id']][1] == 1]),
    'mult_100plus_vs_base': shuffle_p([r['id'] for r in records if mult_bucket(r['id']) == '100+']),
    'mentions_top10_vs_base': shuffle_p(
        [r['id'] for r in records if mention_sets[r['id']] & top_objs]),
}
per_pattern = {}
for name, rx in coord_pats.items():
    if name == 'task*':
        per_pattern[name] = sum(1 for r in records if rx.search(clean_for_coord(r.get('text'))))
        per_pattern['task*_raw_incl_task_id'] = sum(
            1 for r in records if rx.search(r.get('text') or ''))
    else:
        per_pattern[name] = sum(1 for r in records if rx.search(r.get('text') or ''))

result = {
    'dataset_records': N,
    'base_coordination_vocab_rate': round(base_rate, 5),
    'per_pattern_record_counts': per_pattern,
    'chain_graph': chain_stats,
    'template_coordinate': template_stats,
    'mention_graph': mention_stats,
    'degree_tail_vs_null': tail_stats,
    'content_by_position': positions,
}
js = json.dumps(result, indent=1)
if OUT:
    with open(OUT, 'w') as f:
        f.write(js + '\n')
print(js)
