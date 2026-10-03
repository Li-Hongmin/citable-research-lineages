# Square splicing with zero, two or four arbitrary terminals



## Statement

Let \(H\) be a finite simple graph and \(F\) a spanning subgraph with degree one exactly at a terminal set \(T\), degree two at every other vertex, and \(|T|\in\{0,2,4\}\). For each \(i\) choose four distinct vertices \(h_i,x_i,y_i,j_i\); assume these four-vertex supports are pairwise disjoint and

\[
h_ix_i,y_ij_i\in E(F),\qquad
e_i=x_iy_i\in E(H)\setminus E(F),\qquad h_ij_i\in E(H).
\]

Put \(E=\{e_i\}\). Assume \(F\cup E\) is connected. Then \(H\) has a spanning subgraph obtained only by square switches

\[
\{h_ix_i,y_ij_i\}\longmapsto\{h_ij_i,x_iy_i\},
\]

which is (i) one Hamilton cycle if \(|T|=0\); (ii) one spanning path with endpoints \(T\) if \(|T|=2\); or (iii) a two-path spanning cover with endpoints \(T\) if \(|T|=4\). In case (iii) two distinct terminal pairings are obtainable.

Every edge of \(F\) outside the set of the displayed removable rails \(\{h_ix_i,y_ij_i\}\) is retained. In particular, prescribed matching edges or root anchors disjoint from the rails are protected. There is no condition \(T\subseteq\{x_i,y_i\}\), no cycle-base assumption, and no planarity or bipartiteness assumption.

## Proof

The components of \(F\) are cycles and exactly \(|T|/2\) paths. Contract these components and retain one quotient edge for each \(e_i\), allowing loops. Call the connected quotient \(Q\). If \(e_i\) is a nonloop, its endpoints are in different current components, with \(h_ix_i\) and \(y_ij_i\) respectively in those two components. The chord \(h_ij_i\) cannot already be in the current subgraph, since it would connect them. The square switch therefore produces a simple spanning subgraph with the same degree at each vertex.

Cutting one edge in each of two cycles and joining crosswise produces one cycle. Cutting one edge in a path and one in a cycle produces one path with the same endpoints. Cutting one edge in each of two paths produces two paths with a different terminal pairing: the two halves of each original path now join halves of the other. These statements also hold when a removed rail meets a terminal, leaving a one-vertex half-path. Supports are disjoint, so switches at other supports change none of the rails or added chords under consideration.

For zero terminals, take a spanning tree of \(Q\), choose one cycle component as root, and absorb all other cycles along its tree edges. At each step a tree edge joins the growing cycle to one as-yet-unabsorbed subtree component. Only cycle-cycle switches occur, leaving one spanning cycle.

For two terminals, root a spanning tree at the unique path component and absorb cycles by the same argument. This leaves one spanning terminal path.

For four terminals, \(F\) initially has exactly two path components. Take a spanning tree of \(Q\) and choose an edge \(e_*\) on the tree path joining them. Removing \(e_*\) leaves two subtrees, each rooted at one path component. Absorb every cycle in each subtree into its rooted path, without using \(e_*\). This gives a spanning two-path cover. The support of \(e_*\) is untouched, and its endpoints lie on the two different resulting paths. Applying its switch produces another spanning two-path cover with a different pairing. All switches remove only the specified rails, which proves the protection statement. \(\square\)

The same statement applies separately to every connected component \(X\) of \(F\cup E\) with 0, 2 or 4 terminals: any support incident with an \(e_i\) inside \(X\) lies wholly in \(X\), because its rails belong to \(F\). Terminal counts in such components are even since they are unions of \(F\)-paths and cycles. No quotient-degree parity assumption is required.

An explicit illustration is \(F=(a,b,c,d)\dot\cup(e,f,g,h)\), with added edges \(cf,bg\). Use the square support \((b,c,f,g)\), removable rails \(bc,fg\), and \(E=\{cf\}\). All terminals \(a,d,e,h\) lie outside the endpoints of E. The quotient has two vertices and one edge, so both quotient degrees are odd. Switching gives paths \((a,b,g,h)\) and \((d,c,f,e)\), changing \((a,d)(e,h)\) into \((a,h)(d,e)\). Thus neither the old terminal restriction nor an Eulerian quotient is necessary for this generalized result.


## Scope and correction

The terminals need not be endpoints of the added square edges; the component quotient need not be Eulerian. The stated disjoint supports, degree pattern and connectivity are essential. All rails-external protected edges survive. Overlapping supports, arbitrary four-port networks and an arbitrary Barnette graph are not covered.

The earlier local tree-switch statement used in a chord-model application restricted terminal positions. This proof states the more general interface explicitly instead of applying that restricted statement literally. It does not establish any application-specific profile, component classification or exterior closure. The subsequent two-four-special-leaf profile theorem is not a second result in this package. No priority claim or solution of Barnette is made. The eight-vertex illustration is a direct hand-check, not a graph census.
