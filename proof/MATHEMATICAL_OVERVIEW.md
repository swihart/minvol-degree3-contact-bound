# Mathematical overview

## The problem

A convex body $K\subset\mathbb R^3$ has constant width $d$ when the distance
between every pair of parallel supporting planes with opposite normals is
$d$. The three-dimensional Blaschke-Lebesgue problem asks for the least
possible volume among all such bodies.

The two classical Meissner bodies have volume

$$
V_M(d)=\frac{\pi}{12}
\left(8-3\sqrt3\arccos\frac13\right)d^3
=0.419860045965080\ldots d^3,
$$

and are conjectured to minimize volume. That conjecture remains separate from
the theorem proposed here.

The present package represents the universal lower bound

$$
\mathrm{Vol}(K)\ge
\frac{26221074253\pi}{200000000000}\,d^3
=0.4118796712122863775\ldots d^3.
$$

## Normalize the width

Volume scales cubically. It is therefore enough to prove the result for width
one and multiply the answer by $d^3$.

For a width-one body, the support function satisfies

$$
h_K(u)+h_K(-u)=1.
$$

Equivalently,

$$
K+(-K)=B(0,1),
$$

so the diameter is one. In three dimensions, Blaschke's identity gives

$$
S(K)=2\mathrm{Vol}(K)+\frac{2\pi}{3}.
$$

This converts a surface-area estimate into a volume estimate.

## Minimum circumsphere and the circumradius split

Place the origin at the center of a minimum circumscribed ball $B(0,R)$. The
contact points with the ball balance around the origin. Caratheodory's theorem
reduces this balance to at most four contacts, and the diameter-one condition
gives Jung's range

$$
\frac12\le R\le\frac{\sqrt6}{4}.
$$

The proof splits this interval at the exact rational number

$$
R_*=\frac{305695601}{500000000}=0.611391202.
$$

The two branches use different geometric information.

## Branch I: lower circumradius

Suppose $R\le R_*$. An outer support point $x$ with unit normal $n$ has an
opposite point $x-n\in K$. Since $K\subset B(0,R)$,

$$
\langle x,n\rangle\ge\frac{|x|^2+1-R^2}{2}.
$$

This inequality controls how the radial function $\rho$ can change across the
sphere.

A divergence estimate with

$$
F_m(x)=\frac{2x}{|x|^2+m}
$$

gives

$$
3V=\int_{\mathbb S^2}\rho^3\,d\sigma,
\qquad
S\le\int_{\mathbb S^2}\frac{2\rho^3}{\rho^2+m}\,d\sigma.
$$

The integrand is majorized by a tangent line in the variable $X=\rho^3$.
The nonnegative tangent gap can be recovered on spherical caps where the
radial function is forced above or below explicit values.

All cap angles are represented by a rational tangent-half-angle grid. After
one square root is cleared, every propagation, cap, disjointness, and
integration condition becomes an integer inequality. A gap-free finite table
covers $[1/2,R_*]$. Its terminal row is split into `O3B02A` and `O3B02B`; `O3B02B` is the weakest lower row, while the near-Jung branch sets the theorem coefficient. The former exact terminal coefficient
of $\pi$ is the final theorem coefficient.

## Branch II: near the Jung endpoint

Suppose $R\ge R_*$. Four circumsphere contacts are required and are close to a
regular tetrahedral configuration.

Let $p_i=Ru_i$ be the contact points and define the six edge deficiencies

$$
e_{ij}=1-|p_i-p_j|^2\ge0,
\qquad
S=\sum_{i<j}e_{ij}.
$$

The weighted balance equations imply the scalar budget

$$
S\le\frac{3-8R^2}{4R^2-1}.
$$

Because the right side decreases with $R$, the split radius gives one exact
universal deficiency budget on the entire near-Jung branch.

## Affine tetrahedral coordinates

Use the four sign vectors

$$
(1,1,1),\quad(1,-1,-1),\quad(-1,1,-1),\quad(-1,-1,1)
$$

as a regular tetrahedral reference. An affine map sends this reference
configuration to the actual contact tetrahedron. Its normalized Gram matrix
$H$ is an explicit linear function of the six deficiencies.

The proof obtains the determinant transfer

$$
\det H\ge1-\frac S2-\frac{S^2}{2}.
$$

Thus any certified volume in reference coordinates transfers to physical
coordinates with a controlled loss.

## High-resolution forced fan

The four contacts and the diameter-one ball constraints force a radial
polyhedral core. The canonical fan contains:

- 98,306 vertices;
- 196,608 triangular faces;
- 294,912 edges; and
- 24,833 orbits under the distinguished-edge stabilizer.

The fan rays carry exact integer radial data and dyadic S-procedure
multipliers. The minimum exact fan margin is

$$
2.8889042070928578767\times10^{-10}>10^{-12}.
$$

After determinant transfer, the forced core contributes at least

$$
V_{\rm core}\ge0.4117357103127771735489695\ldots.
$$

## Dominant-edge coordinate-width lemma

Relabel a maximum-deficiency edge as `01`. The normalized Gram diagonal obeys

$$
H_{00}\le1+\frac S2,
\qquad
H_{11},H_{22}\le1+\frac S6.
$$

For a positive-definite matrix,

$$
(H^{-1})_{jj}\ge\frac1{H_{jj}}.
$$

These inequalities give three different lower bounds for the physical widths
of transformed coordinate sections. The two transverse directions receive a
stronger estimate than the dominant-edge direction. This anisotropic
coordinate-width step is the main analytic sharpening that separates the
present handoff from the predecessor certificate.

## Six additional cone caps

For each coordinate axis, one cap lies on the positive side and one on the
negative side. Exact section polygons, support values, cap depths, and
allocation brackets give three separately optimized antipodal cap-pair lower
bounds. Their sum is

$$
V_{\rm caps}\ge
0.00014396090205525818382845\ldots.
$$

An exact transformed-ellipsoid argument proves that the interiors of all six
caps are pairwise disjoint, so their volumes may be added to the forced core.

## Near-Jung assembly

The near-Jung branch yields

$$
V_{\rm near}\ge
0.41187967121483243173279798\ldots.
$$

This exceeds the upper enclosure of the lower-branch theorem value by

$$
0.000002107434530157484619055\ldots>0.
$$

Therefore the split terminal rows clear the theorem coefficient, the unchanged near-Jung branch is the universal bottleneck, and the
two branches together cover the complete Jung interval.

## What the computer checks

The exact verifier checks the finite rational objects produced after the
mathematical reductions:

- lower-row propagation chains;
- fan-ray inequalities and multipliers;
- section hulls and exact areas;
- determinant and coordinate-width inputs;
- cap allocations and disjointness;
- branch handoff; and
- the exact final coefficient.

The mathematical derivation connecting arbitrary constant-width bodies to
those finite conditions is written in the paper and remains subject to human
review. The division is detailed in
[`../certificate/TRUST_BOUNDARY.md`](../certificate/TRUST_BOUNDARY.md).

## Reading path

A reviewer can proceed in this order:

1. `paper/contact_geometric_bound.pdf`;
2. this overview;
3. [`CLAIM_DEPENDENCIES.md`](CLAIM_DEPENDENCIES.md);
4. [`../certificate/CERTIFICATE_SPECIFICATION.md`](../certificate/CERTIFICATE_SPECIFICATION.md);
5. [`APPENDIX_A_EXACT_CONSTANTS.md`](APPENDIX_A_EXACT_CONSTANTS.md); and
6. the exact verifier and proof objects under `certificate/`.
