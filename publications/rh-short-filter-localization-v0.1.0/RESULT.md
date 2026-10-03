# Sharp short-filter obstruction and a paid local observation gate

## Observation and retained conditions

For the arithmetic application let M be even, Y=M/2, Y^(1/5)<=H<=Y^(1/4), and 8H<M. Let ψ be fixed, nonzero, real C_c^3((1,2)); let η be fixed, even, nonnegative C_c^infinity(R), supported where 1/2<=|t|<=4 and at least 1 where 1<=|t|<=2. The coefficients are

    c(m)=2 1_(2|m)(Λ(m/2)−1)−4(Λ(m)−1+(log 2)μ(m)),
    a_x=c(M+x)ψ(1+x/M)/(M+x),
    A_h=sum_x a_x exp(−2πi hx/M), E=sum_h η(h/H)|A_h|^2.

Here μ is the Möbius function and Λ is the von Mangoldt function, equal to log p at prime powers p^k and zero otherwise. The actual target E<<_epsilon H^4 M^(−1+epsilon) remains unproved. The finite obstruction below concerns arbitrary coefficients; the paid localization is conditional on fixed smooth weight, its stated H/γ range and quadratic coefficient mass. It provides an equivalent local target, not the arithmetic upper bound.

## Finite proposition: a sharp obstruction to exact local replacement

Let M≥2 be any integer, ζ=exp(2πi/M), and F a nonempty proper subset of Z/MZ with |F|=s. Give each h∈F a positive weight w_h. For a vector a=(a_x)_(x mod M), set

    â(h)=Σ_(x mod M) a_x ζ^(−hx),
    E_F(a)=Σ_(h∈F) w_h |â(h)|².

Let I be any interval of at least s+1 consecutive residues. A finite family of convolution filters q_j may depend arbitrarily on M. Each nonzero q_j is supported in some interval of K_j consecutive residues, with K_j≤M. Write

    V(a)=Σ_j ||q_j *_M a||²_(ℓ²(Z/MZ)).

**Proposition.** If a finite constant C can satisfy

    V(a) ≤ C E_F(a)                                            (1)

for every complex vector supported on I, then every nonzero filter has

    K_j ≥ M−s+1.                                               (2)

The threshold is sharp, even if (1) is required on the entire M-dimensional vector space: there is a nonzero filter supported in exactly M−s+1 consecutive residues for which (1) holds for some finite C. If F is symmetric under h↦−h and the filters are real, the obstruction already holds on real vectors. No primality assumption on M is used.

**Proof of necessity, including a constructive counterexample.** Form the polynomial

    P(z)=∏_(h∈F) (z−ζ^(−h)) = Σ_(r=0)^s p_r z^r.               (3)

Place its s+1 coefficients on consecutive residues inside I, starting at x_0, and zero elsewhere. Then

    â(h)=ζ^(−h x_0) P(ζ^(−h)),

so E_F(a)=0 exactly. Both endpoints of the coefficient block are nonzero: P is monic and its constant coefficient is a product of nonzero roots. In particular a≠0.

Consider any nonzero q_j with K_j<M−s+1. A cyclic shift of its support changes the output only by a cyclic shift, so take its polynomial Q(z)=Σ_(r=0)^(K_j−1) q_r z^r, trimming zero endpoints if needed. The cyclic convolution corresponds to the product Q(z)P(z) modulo z^M−1, together with the harmless shift z^(x_0). The nonzero product has degree at most K_j−1+s<M. It cannot be divisible by z^M−1; thus the cyclic convolution is nonzero. Consequently V(a)>0 but E_F(a)=0, contradicting (1). This same a obstructs every short nonzero member of the family; adding positive variances does not help.

When F is symmetric, the roots in (3) occur in conjugate pairs, possibly with real roots ±1. Thus P has real coefficients. The constructed a is real, proving the real assertion.

**Proof of sharpness.** Take

    Q_*(z)=∏_(h∉F) (z−ζ^(−h)).                                 (4)

Its degree is M−s and its first and last coefficients are nonzero, so it has a consecutive support representation of length M−s+1. Its multiplier vanishes off F and is nonzero on F. Cyclic Parseval gives

    ||q_* *_M a||² = M^(−1) Σ_(h∈F) |Q_*(ζ^(−h))|² |â(h)|²
                  ≤ [max_(h∈F) |Q_*(ζ^(−h))|²/(M w_h)] E_F(a).

The maximum is finite. Necessity already rules out a shorter cyclic support representation, so this proves sharpness. Symmetric F also yields a real sharpness filter. □

## Application and its exact limits

Take x=m−M and a_x=c(M+x)ψ(1+x/M)/(M+x). Any nonzero continuous ψ has a closed interval inside (1,2) on which its absolute value is bounded below. For sufficiently large M its integer samples include s+1 consecutive positions. Every vector constructed in (3) supported there can be realized by some real or complex test coefficient c, using division by the nonzero weight. The active η weights give E_F=E. Thus a nonzero convolution filter with span o(M), including a difference filter whose order grows with M but whose total span stays o(M), cannot satisfy an **exact**, observation-only domination (1) on this arbitrary-coefficient class. Its necessary span is at least M−O(H), and the elementary bound is attained by a global filter.

This is stronger in scope than merely testing a fixed-order adjacent-window difference, but narrower in conclusion than a quantitative arithmetic obstruction. The constructed coefficients need not be μ, Λ, multiplicative, prime-supported, or satisfy their inversion identities. Scaling a can meet any prescribed strictly positive pointwise or interval-sum upper bounds on this finite window, provided no fixed normalization or nonzero lower bound is imposed; scaling does not make the coefficients arithmetic. More crucially, the proof does not quantify V(a) relative to H^4/M as M grows. It excludes exact domination with no additive remainder, even with an M-dependent finite C; it does not exclude a short-filter estimate with a separately paid additive error, or a gate proved only for the true c. It therefore must not be cited as ruling out fixed-power estimates, growing-order Haar methods on the true sequence, or RH.

## A concrete approximate local replacement with a paid error

The exact obstruction does not force the usable gate to be global. Here is a second, positive proposition which keeps an explicitly controlled error. It applies to the actual observation under its known quadratic mass bound, without assuming any new cancellation.

Fix the fixed smooth, even, nonnegative η declared above, with the stated support. Put f_h=√η(h/H) on the centered residue representatives. Fix 1/10<γ<1/5 and set

    K=ceil((M/H) M^γ),
    q_n=(1−|n|/K) M^(−1) Σ_(h mod M) f_h e(hn/M)  (|n|<K),
    q_n=0 otherwise,
    E_loc(a)=M ||q *_M a||².

For sufficiently large M, K<M/2 and the filter has consecutive support at most 2K−1=o(M). Suppose

    Σ_x |a_x|² ≤ C_0 (log M)/M.                                 (5)

Then, uniformly over the original H range,

    |√E_loc(a)−√E_F(a)| ≪_(η,C_0) M^(−γ) (log M)^(3/2),         (6)
    (right-hand side)² = o(H^4/M).                              (7)

Consequently E_loc≪_ε H^4 M^(−1+ε) if and only if E_F has the same bound. This is an equivalence of target-scale upper bounds; it does not claim their unconditional difference is o(H^4/M).

**Proof.** The square root of a nonnegative C_c^2 function is Lipschitz. Indeed Taylor's upper bound with C=||η''||_∞>0 and displacement −η'(t)/C gives 0≤η(t)−η'(t)²/(2C). Wherever η>0, |(√η)'|≤√(C/2); extension across its zeros preserves the Lipschitz bound. The periodic continuous function θ↦√η(Mθ/H), −1/2≤θ≤1/2, is therefore Lipschitz with constant O_η(M/H), and vanishes near the periodic seam.

The filter multiplier Q(h)=Σ_n q_n e(−hn/M) is the discrete Fejér average of f:

    Q(h)=M^(−1) Σ_(j mod M) f_j F_K((j−h)/M),
    F_K(t)=Σ_(|n|<K)(1−|n|/K)e(nt)
          =K^(−1)|Σ_(r=0)^(K−1)e(rt)|².

This kernel is nonnegative, and M^(−1)Σ_j F_K(j/M)=1 since K<M. Its discrete first moment obeys

    M^(−1) Σ_j dist(j/M,Z) F_K(j/M) ≪ log(2K)/K.

For completeness, use F_K(t)≲min(K,1/(K dist(t,Z)²)). The indices 1≤j≤M/K cost O(1/K); the remainder up to M/2 is bounded by K^(−1)Σ_(M/K<j≤M/2)1/j=O(log(2K)/K). Reflect negative indices; j=0 contributes zero. Thus

    max_h |Q(h)−f_h| ≪_η (M/H)log(2K)/K
                         ≪_η M^(−γ)log M =: ε_M.               (8)

Cyclic Parseval and the reverse triangle inequality in frequency ℓ² give

    |√E_loc−√E_F|
      ≤ [Σ_h |Q(h)−f_h|² |â(h)|²]^(1/2)
      ≤ ε_M √(M Σ_x|a_x|²),

which proves (6). Since H^4/M≳M^(−1/5) and 2γ>1/5, (7) follows. Also K/M≲M^(γ−1/5)→0, establishing short relative support. This proves the proposition. □

For the actual a_x=c(M+x)ψ(1+x/M)/(M+x), (5) follows from Σ_(M<m<2M)|c(m)|²≪M log M. To see that mass bound, square the displayed three-channel formula, use |μ|≤1, and use Σ_(n≤2M)Λ(n)²≤log(2M)Σ_(n≤2M)Λ(n)≪M log M (Chebyshev's bound suffices); the doubled Λ channel is bounded the same way. No prime-pair or Möbius-pair cancellation enters this step.

Because ψ is supported away from both window endpoints and K=o(M), for sufficiently large M the correlations in E_loc have no cyclic wraparound. Its exact physical form is

    E_loc = M Σ_(|n|,|m|<K) q_n overline(q_m) C_a(n−m),
    C_a(k)=Σ_(x∈Z) a_x overline(a_(x+k)),

where a is extended by zero. Only ordinary displacements |k|≤2K−2 enter. The weights keep the signs of the complete three-channel correlations. The explicitly specified mean-square bound E_loc≪_ε H^4 M^(−1+ε) is now a concrete necessary and sufficient local gate at the target scale. It remains unproved. At γ=3/20 and H≍M^(1/5), its spatial span is O(M^(19/20)); this is much longer than a single observation length M/H, and still o(M). The short support comes from a paid approximation error, so it does not contradict the exact proposition.

This resolves the finite localization obligation while preserving the scientific gap: a direct joint signed Gram estimate, or the displayed E_loc estimate, must still gain the missing arithmetic power. Source-normal-form manipulations and one-point bounds must be tested at that interface rather than declared sufficient from names or numbering.


## Elementary mass input

For completeness, the Chebyshev upper bound used only for quadratic mass follows from central binomial coefficients. For integer n>=1, each prime power p^k in (n,2n] contributes log p to ψ_Λ(2n)−ψ_Λ(n), while its exponent contributes at least one to the p-adic valuation of binomial(2n,n); the other valuation terms are nonnegative. Thus ψ_Λ(2n)−ψ_Λ(n)<=log binomial(2n,n)<=2n log 2. Summing over dyadic n and using monotonicity yields ψ_Λ(x)=sum_(m<=x)Λ(m)=O(x). Therefore sum_(m<=2M)Λ(m)^2<=log(2M) ψ_Λ(2M)=O(M log M). The displayed three-channel c and |μ|<=1 then imply the quadratic mass used above. This is not a correlation-cancellation estimate.

## Reproduction, objections and novelty

`python3 -B verify_filters.py` or `python3 -B -O verify_filters.py` prints small standard-library diagnostics without changing the package. The polynomial and analytic proofs establish the claims; floating-point residues and the toy Fejér parameters do not establish the asymptotic H/K regime. No third-party paper or uninspected theorem is a load-bearing dependency of these two propositions.

The exact obstruction does not exclude an estimate with an additive error or a gate valid only for true arithmetic coefficients. The paid proposition certifies a square-root energy difference and target-bound equivalence, not unconditional E−E_loc=o(H^4/M). Its actual E_loc arithmetic bound, joint signed Gram fixed-power input, all-scale Weil conclusion and RH remain open. Earlier modulation/Haar ideas were excluded as duplicate local candidates. No new uncertainty principle, priority, external human review or heterogeneous acceptance is claimed.
