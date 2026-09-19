# Claims and limitations

## Main claim represented by the package

The exact certificate and manuscript represent the universal statement

$$
\boxed{
\mathrm{Vol}(K)\ge
\frac{26220940089713\pi}{200000000000000}\,d^3
=0.41187756378030227424817892598\ldots d^3
}
$$

for every convex body $K\subset\mathbb R^3$ of constant width $d>0$.

The claim is universal: it is not restricted by symmetry, smoothness, contact
type, prescribed circumradius, or proximity to a Meissner body. Scaling from
width one supplies the factor $d^3$.

## Current verification classification

> **Proposed exact universal certificate - standalone internal replay.**

This means:

- the finite certificate is represented by exact integer and rational objects;
- the standalone exact verifier accepts those objects;
- the assembled theorem certificate is reconstructed byte for byte;
- independent binary64 Python and base-R audits agree;
- ten reconstruction/regression tests pass;
- seven targeted corruptions are rejected;
- paper-facing constants and the lower-row table are generated or reconciled
  against the certificate JSON; and
- the package is still an AI-assisted, non-peer-reviewed research draft.

The word **exact** refers to the arithmetic of the finite certificate. It does
not mean that the full proof has been formalized in a proof assistant or
independently reviewed.

## Claims established inside the finite package

Subject to the mathematical reductions in the manuscript, the exact package
checks:

- gap-free circumradius coverage from $1/2$ through $\sqrt6/4$;
- the exact split
  $R_*=305695601/500000000$;
- the unique lower-branch bottleneck `O3B02`;
- four exact replacement cells for the old `O3A1` interval;
- reconstruction of a 98,306-vertex near-Jung fan;
- all exact fan-margin and inherited-multiplier inequalities;
- the determinant transfer and forced-core lower bound;
- the dominant-edge coordinate-width estimate on all three axes;
- three optimized antipodal cap-pair contributions;
- exact six-cap disjointness;
- a strict near-Jung handoff surplus; and
- the exact theorem coefficient and decimal enclosure.

## What is not claimed

The package does **not** establish any of the following:

- that the bound is sharp;
- an equality case;
- rigidity or stability near equality;
- the identity or uniqueness of a minimizing body;
- that either Meissner body minimizes volume;
- the Meissner conjecture;
- a classification of all extremal contact configurations;
- a proof in Lean, Coq, Isabelle, or another proof assistant;
- external independent reproduction;
- peer review, journal acceptance, or publication;
- a systematic priority or novelty guarantee; or
- correctness of every statement merely because it was generated or checked by
  an AI system.

The explicit Meissner value

$$
\frac{\pi}{12}
\left(8-3\sqrt3\arccos\frac13\right)d^3
=0.419860045965080\ldots d^3
$$

is used only as an explicit-body comparison value. It is not asserted here as
the universal minimum.

## Relationship to earlier bounds

The certificate coefficient exceeds, by direct arithmetic comparison, the
public HYRA coefficient

$$
\frac{130838246407123\pi}{10^{15}}
>0.411040473721188.
$$

It also exceeds Nishioka's $4\pi/33$ coefficient and Chakerian's historical
coefficient. These comparisons do not by themselves establish priority or
publication status. The dated source review is recorded in
[`../proof/SOURCE_LEDGER.md`](../proof/SOURCE_LEDGER.md).

## Smoothness and approximation

The final theorem is stated for all convex bodies of constant width, including
nonsmooth bodies. The analytic divergence step is first justified on a regular
class and then passed to arbitrary bodies by the regularization and continuity
argument stated in the manuscript. The finite verifier assumes that reduction;
it does not independently formalize geometric measure theory or Hausdorff
continuity.

## Status words that may be used

Before public release and external review, acceptable descriptions include:

- proposed exact universal certificate;
- computer-assisted research draft;
- exact-rational finite verification;
- independently audited in Python and base R; and
- seeking independent mathematical verification.

Descriptions that should not be used at this stage include:

- peer reviewed;
- independently verified;
- formally verified;
- sharp or optimal;
- proof of the Meissner conjecture;
- identification of the minimizer; and
- final accepted theorem.

## Corrections policy

A mathematical or certificate correction must be visible. It should receive a
new commit and, after release, a new version or release tag. The old tagged
artifact should remain available with a clear correction notice rather than
being silently rewritten.

A change to the exact theorem coefficient, branch partition, proof objects, or
verifier semantics requires:

1. a new certificate schema or documented schema revision;
2. regenerated exact and audit transcripts;
3. renewed adversarial tests;
4. paper and documentation reconciliation;
5. fresh-machine replay; and
6. explicit release notes comparing the old and new claims.
