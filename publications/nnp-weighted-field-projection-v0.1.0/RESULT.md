# Weighted finite-field projections and a canonical cancellation toy

## Objects and exact projection

Let u=2^mu>=8, K=GF(u), F=GF(u^6), Q=u^6,
M=1+u+u^2+u^3+u^4+u^5, U_4=u+u^2+u^3+u^4, B=4U_4 and kappa=4u^5.
Define L_b(Z)=1+(Z+b)^(u-1) for b in K. For a_o in K^times set s=1+X^(u-1), ell=1+(X+a_o)^(u-1), and v=X^(u-1).
For arbitrary fixed coefficients k, a, b, c_0,c_2,c_kappa,c_T in F define the ordinary, denominator-cleared polynomial

    W(X)=(1+k v^4)^(U_4) {
       a[c_0 s^(4M)+c_2 s^(4M-2)ell^2+c_kappa s^(4M-kappa)ell^kappa+c_T s^(4M-kappa-2)ell^(kappa+2)]
       +b v^kappa[c_0 s^(4M)+c_2 s^(4M-2)ell^2+c_T s^(4M-kappa-2)ell^(kappa+2)] }.

Put P_0(z)=c_0+c_2z^2+c_kappa z^kappa+c_T z^(kappa+2) and P_5(z)=c_0+c_2z^2+c_T z^(kappa+2).
Then

    sum_(X in F) W(X)=(1+k)^(U_4)[a P_0(1)+b P_5(1)].

The off-grid sum over F\K adds a c_0 to this expression in characteristic two: only X=0 contributes on the grid. These two sums must not be conflated. The weights include s^2; forgetting this factor gives a different projection. Every coefficient is held fixed while X varies. Arbitrary coefficients are permitted for this algebraic identity, not as arbitrary advice in an actual RW application.

## General mixed moment and proof


Scale X=a_o x. Since a_o^(u-1)=1, this is a bijection of F preserving v, and it sends ell to L_1(x), s to L_0(x). It suffices to prove the identity for a_o=1. In this section only, X denotes this normalized variable.

Take the unique fourth root r of k, and define the **product**
\[
H=s(1+rv)=1+(1+r)v+rv^2.
\]
Then deg H<=2u-2, [X^(u-1)]H=1+r, and
\[
H^B=s^B(1+kv^4)^{U_4}.
\]
The product is essential: replacing H by s+rv drops a factor and is incorrect.

For arbitrary polynomials L,H,R of degree at most 2u-2, define
\[
\lambda=[X^{2u-2}]L,\quad \nu=[X^{2u-3}]L,\quad
h=[X^{u-1}]H,\quad a_R=[X^{u-1}]R,\quad b_R=[X^{3u/2-1}]R.
\]
The following general moment is valid:
\[
\sum_{X\in F} L(X)^2H(X)^B R(X)^\kappa
=h^B(\lambda^2 a_R^\kappa+\nu^2 b_R^\kappa).                           \tag{7}
\]

To prove it, the summand has degree at most
\[
4(u-1)+2B(u-1)+2\kappa(u-1)=8Q-4u-4<8(Q-1).
\]
Every exponent is even. Full-field power summation in characteristic two keeps only positive multiples of Q-1; hence the only possibilities are 2(Q-1), 4(Q-1), 6(Q-1). The constant term sums to Q=0.

All exponents in H^B R^kappa are divisible by 4u, whereas deg L^2<=4u-4. The residue for 2(Q-1) is 4u-2, outside this range. The other two residues are 4u-4 and 4u-6, selecting the coefficients lambda^2 and nu^2 of L^2 respectively.

For the 4(Q-1) case, removing low exponent 4u-4 and dividing by 4u leaves target u^5-1. Write the four H factors as H^(4u), H^(4u^2), H^(4u^3), H^(4u^4), followed by R^(4u^5). The target's five base-u digits are all u-1. At its lowest digit a selected H exponent lies in [0,2u-2]. Congruence to u-1 forces precisely u-1; the alternative 2u-1 is unavailable. There is no carry. Repeat through the lower four positions, and the R exponent is u-1. The product coefficient is h^B a_R^kappa.

For 6(Q-1), removing 4u-6 and dividing by 4u gives (3/2)u^5-1. Its lower four digits are again u-1 and its top digit is 3u/2-1. The same no-carry argument gives h^B b_R^kappa. Adding the two terms proves (7).

For a_o=1,
\[
s=1+X^{u-1},\qquad
\ell=X+X^2+\cdots+X^{u-1}.
\]
The relevant boundary coefficients are:

| L | lambda | nu |
|---|---:|---:|
| s^2 | 1 | 0 |
| s ell | 1 | 1 |

| R | a_R | b_R |
|---|---:|---:|
| s | 1 | 0 |
| ell | 1 | 0 |
| s v | 1 | 0 |
| ell v | 0 | 1 |

Indeed s ell has coefficient one at every power 1 through 2u-2. The seven terms of W correspond, in order, to
\[
(L,R)=(s^2,s),(s\ell,s),(s^2,\ell),(s\ell,\ell),
       (s^2,sv),(s\ell,sv),(s\ell,\ell v).
\]
Formula (7) makes every one of their sums equal h^B. Finally
\[
h^B=(1+r)^{4U_4}=(1+k)^{U_4}.
\]
Collecting the same c_j coefficients proves the full-field identity. The direct grid evaluation above proves the off-grid correction. This proof includes the public s^2 weight and does not assume that an unweighted sum has the same value.


## Canonical Boolean-grid toy

A stronger toy than a freely prescribed coefficient list obeys the canonical paired source form. Assume mu is even and at least four, so K contains F4. Choose omega with omega^2+omega+1=0, take endpoint labels p=0,q=1, and let
\[
V_0=0,\qquad V_1=L_0,\qquad O=L_\omega.
\]
All three sections have Boolean grid values and degree below u; O(p)=O(q)=0, and V_1+V_0 has endpoint difference one.

For a section T define its four moments
\[
a_T=[Z^{u-1}]T,\quad
g_T=[Z^{2u-3}]L_0T,\quad
h_T=T(0)+T(1),\quad
t_T=[Z^{3u/2-1}](L_0+L_1)T.
\]
The moments of V_1 are (1,0,1,1), and those of O are (1,omega,0,1). To verify the last entry directly, L_0+L_1 has all coefficients one in degrees 0 through u-2, while [Z^j]L_omega=omega^(u-1-j) for j>0. The relevant convolution is
\[
t_O=\sum_{e=0}^{u/2-2}\omega^e=1:
\]
u=4^m makes the last exponent divisible by three and each full triple has sum zero.

Define the following paired canonical coefficient model by its displayed moments; the finite counterexample below is about this explicit algebraic model:
\[
\begin{aligned}
c_0&=\sum_i(a_i^2h_i^{B+\kappa}+g_i^2h_i^Bt_i^\kappa),\\
c_2&=a_O^2\sum_i h_i^{B+\kappa}+g_O^2\sum_i h_i^Bt_i^\kappa,\\
c_\kappa&=t_O^\kappa\sum_i g_i^2h_i^B,\\
c_T&=g_O^2t_O^\kappa(h_1^B+h_0^B).
\end{aligned}
\]
Substitution gives
\[
(c_0,c_2,c_\kappa,c_T)=(1,\omega,0,\omega^2),\qquad
P_0=P_5=1+\omega z^2+\omega^2 z^{\kappa+2}.
\]
Hence c_T!=0 but P_0(1)=P_5(1)=0. The weighted seven-basis sum vanishes for this coefficient model, for every fixed background satisfying the displayed polynomial interface.


## Exact application boundary

This is a theorem of finite-field polynomial algebra and an explicitly synthetic canonical example. A nonzero highest coefficient alone does not imply nonzero complete-coordinate average. It does not exhibit an actual reachable RW cancellation or prove an actual-source survival theorem, an efficient evaluator, the complete JK response, or P versus NP.

An application must supply the same actual source sections and keep the same permitted third remainder and all other coefficients fixed while X varies. The public-weight identity must also hold; the theorem does not establish the original route/checker chain. There is a further conditional obstruction to using this entire singleton toy as an actual section: if an actual source difference has hard-suffix grid support equal to a specified word with at least two nonzero positions, through a nonzero ledger multiplier, it cannot equal the one-point grid-supported difference L_p. This comparison requires equality of the entire canonical section, not matching only moments or one endpoint pair. No actual source is certified here to meet these premises, and other vanishing projections are not excluded.

The review's initial substitution H=s+rv was wrong and was corrected to H=s(1+rv). That correction, the s-squared public weight and the off-grid distinction are retained. The two finite checkers test formal polynomial bases and synthetic F4 sections only. Novelty and external scientific acceptance are not claimed.
