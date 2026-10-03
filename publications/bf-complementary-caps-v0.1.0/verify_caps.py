# SPDX-License-Identifier: Apache-2.0
# Derived finite checker: explicit checks remain active under python -O.
"""Independent read-only validation of parent's two universal true-cap certificates."""
import json
from collections import defaultdict
from itertools import combinations, product

def edge(a, b):
    return tuple(sorted((str(a), str(b))))
marks = {'X': (1, 3), 'Y': (2, 5), 'Z': (4, 6), 'W': (1, 6)}
rs = json.load(open('corrected-cap-two-tables.json'))
if not len(rs) == 2:
    raise AssertionError('finite diagnostic check failed')
results = []
for r in rs:
    S = r['allowed_S']
    Sedges = {edge(a, b) for a, b in zip(S, S[1:] + S[:1])}
    T = {edge(a, b) for a, b in combinations('eXYZW', 2)} - Sedges
    if not T == {edge(a, b) for a, b in r['physical_T_edges']}:
        raise AssertionError('finite diagnostic check failed')
    c = {}
    for a, b, col in r['edge_colours']:
        if b is None:
            b = 'e' if a == 'bare' else 'p' + a[1:]
        e = edge(a, b)
        if not e not in c:
            raise AssertionError('finite diagnostic check failed')
        c[e] = col
    expected = set()
    for i in range(1, 6):
        expected |= {edge(i, f'u{i}'), edge(i + 1, f'u{i}'), edge(f'u{i}', f'p{i}')}
    for j, (a, b) in marks.items():
        expected |= {edge(a, f't{j}'), edge(b, f't{j}'), edge(f't{j}', f'bar{j}')}
    expected |= {edge('bar' + a, 'bar' + b) for a, b in T} | {edge('bare', 'e')}
    if not set(c) == expected:
        raise AssertionError('finite diagnostic check failed')
    adj = defaultdict(list)
    for (a, b), col in c.items():
        adj[a].append(col)
        adj[b].append(col)
    internal = [v for v, cols in adj.items() if len(cols) > 1]
    if not len(internal) == 20:
        raise AssertionError('finite diagnostic check failed')
    if not all((sorted(adj[v]) == [1, 2, 3] for v in internal)):
        raise AssertionError('finite diagnostic check failed')
    signature = [adj[v][0] for v in ['e', 'p1', 'p2', 'p3', 'p4', 'p5']]
    if not signature == r['signature'] == [1, 2, 2, 1, 3, 3]:
        raise AssertionError('finite diagnostic check failed')
    pairs = [('p3', 'p4'), ('p3', 'p5')] + list(product(['e', 'p1', 'p2'], ['p4', 'p5']))
    for a, b in pairs:
        ca, cb = (adj[a][0], adj[b][0])
        if not sorted([ca, cb, 6 - ca - cb]) == [1, 2, 3]:
            raise AssertionError('finite diagnostic check failed')
    results.append({'allowed_S': S, 'physical_T_complement_verified': True, 'internal_vertices_checked': 20, 'signature': signature, 'joined_d_pairs_checked': pairs})
print(json.dumps(results, indent=2))
