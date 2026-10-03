# A common six-port colouring for two complementary pentagon caps

A self-contained explicit finite colouring lemma. Authorized human contribution credit: Li Hongmin; AI derivation and same-model review are disclosed separately. No novelty or external scientific acceptance claim.

## Statement

Start with the path 1–2–3–4–5–6. Subdivide its edge i(i+1) at u_i for i=1,...,5, and attach a dangling edge p_i at u_i. Subdivide the four other edges X=13, Y=25, Z=46, W=16 at t_X,t_Y,t_Z,t_W. Add five new vertices b_e,b_X,b_Y,b_Z,b_W. Join t_M to b_M for M=X,Y,Z,W, and attach a dangling edge e at b_e.

For either cycle S_1=e–X–Y–W–Z–e or S_2=e–X–W–Y–Z–e on these five labels, join the b vertices along the complementary cycle T_i=K_5−S_i. Explicitly,

T_1=e–Y–Z–X–W–e, and T_2=e–Y–X–Z–W–e.

Each resulting cubic six-pole has a proper three-edge-colouring with boundary signature

(e,p_1,p_2,p_3,p_4,p_5)=(1,2,2,1,3,3).

Consequently, removing any two dangling edges whose positions are one in {e,p_1,p_2,p_3} and one in {p_4,p_5}, joining their incident vertices to one new vertex d, and adding a new dangling edge at d, gives a three-edge-colourable cubic five-pole. This statement concerns these explicit fixed graphs, with no assumption about BF support, minimum counterexamples, or general cubic graphs.

## Explicit proof

The following table gives the colours on the two halves of each subdivided core edge in the displayed endpoint order. At its subdivision vertex the third edge receives the unique colour absent from the two halves.

| Core edge | T_1 halves | T_2 halves |
|---|---|---|
|u_1:12|1,3|1,3|
|u_2:23|1,3|1,3|
|u_3:34|2,3|2,3|
|u_4:45|1,2|2,1|
|u_5:56|1,2|2,1|
|t_X:13|2,1|2,1|
|t_Y:25|2,3|2,3|
|t_Z:46|2,3|1,3|
|t_W:16|3,1|3,2|

Colour the cap edges in their stated cycle order as follows:

| Physical cap | Successive edge colours |
|---|---|
|T_1=e–Y–Z–X–W–e|2,3,2,1,3|
|T_2=e–Y–X–Z–W–e|3,2,1,3,2|

Give e colour 1. At each original vertex 1,...,6 the three half-edge colours are 1,2,3. At every u_i or t_M the third colour is defined to complete that set. At the four b_M vertices, its spoke colour and its two cap-edge colours are distinct; at b_e its two cap-edge colours are 2,3. Thus all twenty internal vertices see exactly 1,2,3, proving a proper colouring. The five u_i third colours are 2,2,1,3,3, yielding the displayed six-port signature.

For the joining operation, its two retained edge colours are distinct: the first is 1 or 2 and the second is 3. Keep these colours, colour the new dangling edge by the remaining colour, and keep every other edge unchanged. All three colours occur at d, and its neighbours retain their original incident colours. This proves the consequence for all eight permitted joins and both caps without a case-by-case search.

## Why the cap distinction matters

In a cubic five-pole's BF boundary notation, [ij] denotes a type with two colours missing the same pair of positions i,j; it is a loop in the auxiliary support graph. A physical pentagon has such ordinary loops on its adjacent terminal pairs. For the complementary Case-XII side, the allowed ordinary loops lie on the complementary cycle instead. The cycle of allowed ordinary loops therefore must not be substituted for the physical cap cycle. The distinction follows from Definition 4.1, Figure 5 and Appendix XII of Máčajová, Mazzuoccolo and Tabarelli, *Cycle separating cuts in possible counterexamples to the cycle double cover and the Berge–Fulkerson conjectures*, Ars Mathematica Contemporanea 26 (2026), #P2.03, [DOI](https://doi.org/10.26493/1855-3974.3409.c13).

This explicit colouring lemma repairs that possible substitution at the fixed prism fragment. It does not independently certify any pole's exact BF support, force this fragment in a minimum counterexample, or resolve Berge–Fulkerson.

## Reproduction and review boundary

The proof is the two displayed tables and the vertex-wise colour check. `corrected-cap-two-tables.json` records every proper and dangling edge with its colour. `verify_caps.py` reconstructs the two graphs, verifies T_i=K_5−S_i, checks all twenty vertex partitions, confirms the common signature, and checks each of the eight joins.

Reproduce in this package with `python3 -B verify_caps.py` or `python3 -B -O verify_caps.py`; the certificate is at the top level. The standard-library checker prints JSON to stdout and never writes the frozen package. Its explicit runtime checks remain active under optimization. This verification does not call the colouring search or depend on the private BF project.

The producer reported an additional separately implemented check of all sixteen joined five-poles; that unselected search program is not a dependency or artifact of this package. This is supporting finite verification, not necessary for the explicit table proof. A fresh-context reviewer used the same model as the derivation agent; this is not independent human scientific acceptance or an independent-model external review. Novelty beyond this local correction has not been claimed or assessed. There is no counterexample to the stated colouring lemma; the failed earlier proof attempt used the wrong physical cap.


## Retained correction and later boundary

The rejected earlier local attempt substituted the allowed-loop cycle S for the physical complementary pentagon T=K5−S. Its 642-labelled colouring certificate is not evidence for this result. The displayed actual-T tables replace that attempt. The later compatible-pair distance example shows that minimizing arbitrary actual matching pairs does not preserve BF cooccurrence; it is not needed by this explicit colouring lemma. General exact-XII support, minimum-host configuration forcing, and a guarantee that a permitted pair attains difference eight remain outside the result. Neither this package nor the later example is a BF counterexample.
