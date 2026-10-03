"""Independent finite check of the declared reduced relational model.

SPDX-License-Identifier: Apache-2.0
Copyright 2026 Li Hongmin. Standard-library only, no network or writes.
This does not implement complete marked partition joins or graph realizability.

Derived local publication candidate, 2026-10-03: assert checks are explicit runtime failures, including under Python -O. Finite definitions unchanged.
"""
import itertools
import json
import platform

def patch_rows():
    internal = frozenset('abcd')
    boundary = frozenset('uvxy')
    edges = ('ua', 'bv', 'xc', 'dy', 'ab', 'bc', 'cd', 'da')
    answer = []
    for bits in itertools.product((0, 1), repeat=len(edges)):
        chosen = tuple((e for e, bit in zip(edges, bits) if bit))
        degree = {v: sum((v in e for e in chosen)) for v in internal | boundary}
        if all((degree[v] == 1 for v in internal)) and all((degree[v] <= 1 for v in boundary)):
            answer.append({'patch_edges': sorted(chosen), 'old_exterior_defect': ''.join(sorted((v for v in boundary if degree[v])))})
    return sorted(answer, key=lambda r: (r['old_exterior_defect'], r['patch_edges']))

def transpose(pair):
    return {**pair, 'first': pair['second'], 'second': pair['first']}

def coherent(rows, pairs):
    expected = set(itertools.product(range(len(rows)), repeat=2))
    if set(pairs) != expected:
        return False
    for (i, j), pair in pairs.items():
        if pair['first'] != rows[i]['type'] or pair['second'] != rows[j]['type']:
            return False
        if pair['equal'] != (i == j) or pairs[j, i] != transpose(pair):
            return False
        if i == j and pair['crossing_bond']:
            return False
    return True

def parent_kill(rows, pairs):
    admitted = [r['parent_admitted'] for r in rows]
    bonds = [(i, j) for (i, j), p in pairs.items() if p['crossing_bond'] and admitted[i] and admitted[j] and (rows[i]['sector'] != rows[j]['sector'])]
    return any((a and r['parent_state11'] for a, r in zip(admitted, rows))) and bool(bonds) and all((rows[i]['parent_state11'] or rows[j]['parent_state11'] for i, j in bonds))

def child_supplement(rows, table, child_admission, child_bonds):
    children = [(i, cell) for i, row in enumerate(rows) for cell in table[row['defect']]]
    new = {'R00', 'Xuy', 'Xvx'}
    return any((child_admission.get(a, False) and child_admission.get(b, False) and child_bonds.get((a, b), False) and (a[1] in new or b[1] in new) for a in children for b in children))

def check():
    local = patch_rows()
    expected_counts = {'': 2, 'uv': 1, 'xy': 1, 'uvxy': 1, 'uy': 1, 'vx': 1}
    counts = {d: sum((r['old_exterior_defect'] == ''.join(sorted(d)) for r in local)) for d in expected_counts}
    if not (len(local) == 7 and counts == expected_counts):
        raise AssertionError('Finite model validation failed')
    full_defect = [r for r in local if r['old_exterior_defect'] == ''.join(sorted('uvxy'))]
    if not full_defect[0]['patch_edges'] == sorted(['ua', 'bv', 'xc', 'dy']):
        raise AssertionError('Finite model validation failed')
    table = {'uvxy': ['C11']}
    rows = [{'type': f'a{i}', 'defect': 'uvxy', 'parent_admitted': True, 'parent_state11': True, 'sector': i} for i in range(2)]
    pairs = {(i, j): {'first': rows[i]['type'], 'second': rows[j]['type'], 'equal': i == j, 'crossing_bond': i != j} for i in range(2) for j in range(2)}
    if not (coherent(rows, pairs) and parent_kill(rows, pairs)):
        raise AssertionError('Finite model validation failed')
    children = [(i, 'C11') for i in range(2)]
    admission_assignments = bond_assignments = combinations_checked = 0
    for admission_bits in itertools.product((False, True), repeat=2):
        admission = dict(zip(children, admission_bits))
        admission_assignments += 1
        for bond_bits in itertools.product((False, True), repeat=4):
            bonds = dict(zip(itertools.product(children, repeat=2), bond_bits))
            if not child_supplement(rows, table, admission, bonds) is False:
                raise AssertionError('Finite model validation failed')
            combinations_checked += 1
    bond_assignments = 16
    singleton_cases = coherent_singletons = 0
    for admitted, state11, sector, diagonal_bond in itertools.product((False, True), repeat=4):
        singleton_cases += 1
        one = [{'type': 'a', 'defect': 'uvxy', 'parent_admitted': admitted, 'parent_state11': state11, 'sector': int(sector)}]
        diagonal = {(0, 0): {'first': 'a', 'second': 'a', 'equal': True, 'crossing_bond': diagonal_bond}}
        if coherent(one, diagonal):
            coherent_singletons += 1
            if not not parent_kill(one, diagonal):
                raise AssertionError('Finite model validation failed')
    if not not parent_kill([], {}):
        raise AssertionError('Finite model validation failed')
    bad = {k: dict(v) for k, v in pairs.items()}
    bad[0, 1]['equal'] = True
    if not not coherent(rows, bad):
        raise AssertionError('Finite model validation failed')
    bad = {k: dict(v) for k, v in pairs.items()}
    bad[0, 1]['first'] = 'wrong'
    if not not coherent(rows, bad):
        raise AssertionError('Finite model validation failed')
    bad = {k: dict(v) for k, v in pairs.items()}
    bad[1, 0]['crossing_bond'] = False
    if not not coherent(rows, bad):
        raise AssertionError('Finite model validation failed')
    no_bonds = {k: {**v, 'crossing_bond': False} for k, v in pairs.items()}
    if not (coherent(rows, no_bonds) and (not parent_kill(rows, no_bonds))):
        raise AssertionError('Finite model validation failed')
    return {'status': 'PASS', 'python': platform.python_version(), 'coverage': 'declared reduced finite relational model and one local patch', 'patch_subsets_examined': 256, 'patch_rows': local, 'two_row_parent_kill': True, 'child_supplement': False, 'admission_assignments': admission_assignments, 'bond_assignments_per_admission': bond_assignments, 'child_combinations_checked': combinations_checked, 'singleton_assignments_examined': singleton_cases, 'coherent_singletons': coherent_singletons, 'minimum_nonvacuous_row_count': 2, 'full_marked_partition_types_checked': False, 'graph_realizability_checked': False, 'barnette_conjecture_resolved': False}
if __name__ == '__main__':
    print(json.dumps(check(), indent=2, sort_keys=True))
