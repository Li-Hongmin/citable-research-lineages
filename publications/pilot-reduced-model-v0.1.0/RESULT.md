# A two-row countermodel in an explicitly reduced boundary-support language

Status: analytically checked and reproduced within the reduced model stated below; broader marked-type realizability unverified. Human contributor: Li Hongmin. New mathematical text: CC BY 4.0. New verification code: Apache-2.0. Actual Codex roles and source boundaries are recorded in rights-and-attribution.json. This is not a graph counterexample to the Barnette conjecture.

## Objects and assumptions

Let R be a finite set of abstract row identities. A row has a unary type label, an exterior defect class, a parent-admission flag, a parent-state-11 flag, and a sector bit. For every ordered pair of rows record its endpoint labels, an equality bit, and a crossing-bond bit. Require endpoint consistency, equality exactly on the diagonal, transpose consistency, and a false crossing-bond bit on every diagonal. These are the complete axioms of this **reduced language**; no graph, perfect-matching family, or full marked partition alphabet is assumed.

Define ParentKill as the conjunction of: an admitted state-11 row exists; an admitted crossing bond between different sectors exists; and every such bond has at least one state-11 endpoint.

For a standard four-vertex patch, let its internal edges be ab, bc, cd, da and its connectors be ua, bv, xc, dy. Its internal vertices must each be matched once; each old exterior endpoint is used at most once. A compatible exterior defect is the set of old endpoints used by the patch. Direct finite enumeration, or the vertex-degree constraints, give seven patterns: two with no exterior defect and one each with uv, xy, uvxy, uy, vx. The uvxy pattern is uniquely the four connectors and is denoted C11. The three new cells R00, Xuy, Xvx have defects empty, uy, vx, respectively. A child supplement is an admitted child bond with at least one endpoint in these new cells.

## Proposition and proof

In this language, ParentKill does not imply child supplementation. The minimum number of rows for a countermodel with the nonempty-bond antecedent is two.

Take R = {r0,r1}. Both rows have exterior defect uvxy, are parent-admitted and state-11, and have different sector bits. Give them different unary labels. Give each diagonal pair the appropriate endpoint labels, equality true, and crossing-bond false. Give both off-diagonal ordered pairs consistent endpoint labels, equality false, and crossing-bond true, with one the transpose of the other. All axioms hold. The state-11 slice and the crossing graph are nonempty, and every crossing bond has both endpoints in the slice. ParentKill is therefore true.

Each row has only the compatible C11 child pattern. Thus every child row has cell label C11, with no endpoint in R00, Xuy, Xvx. The child-supplement existential formula is false for **every** choice of child-admission and child-bond flags. No partition-join calculation is needed for this conclusion.

With zero rows there is no admitted state-11 row or crossing bond. With one row every ordered pair is diagonal and its bond flag must be false. Consequently ParentKill fails in both cases, proving minimum nonvacuous size two.

## Exact boundary

This is a self-contained theorem about the declared reduced language. Source note 134 phrases its countermodel using complete unary and pair-deletion types. The present verifier does not construct those full types or check their partition joins. Therefore it reproduces a precise projection of that argument and its local patch premise, not every stronger assertion in the source. It does not prove the original state graph-realizable, reachability under CEN/UV, a counterexample to actual rooted split-bond supplementation, or a solution of Barnette.

## Reproduction and sources

Run `python3 reproduce.py` in this directory. It uses only the Python standard library, examines all 256 patch edge subsets, verifies the seven compatible patterns, checks the two-row quantifiers, exhausts all 64 child admission/bond assignments, and checks all singleton flag combinations under the stated diagonal axiom. It also rejects malformed equality, endpoint and transpose data and an empty-bond antecedent.

The source lineage is the fixed Barnette notes 132–134, indexed by content hashes in `sources.json`. No original private note is included in this contribution. Notes 132–133 motivated the language/table; all definitions needed for this narrowed theorem are supplied above. Their CEN/UV iteration theorems and computational bundles are not dependencies of this theorem and are not claimed reproduced here. The review in `REVIEW.md` must travel with this result.

License: CC BY 4.0 for this new text; see rights-and-attribution.json.
