# Claim dependencies

## Purpose

This document exposes the logical dependency structure of the proposed theorem.
It separates sourced classical facts, human mathematical reductions, and finite
machine-checked claims.

## Status labels

- **Sourced:** imported from an identified mathematical reference.
- **Paper proof:** derived in `paper/contact_geometric_bound.tex`.
- **Exact certificate:** checked with integer and rational arithmetic.
- **Independent audit:** checked by a separately organized numerical path.
- **Release infrastructure:** checks consistency, provenance, or presentation.
- **External review needed:** no independent subject-matter review has been
  recorded.

## Dependency graph

```text
C0 constant-width identities and scaling
 |
 +--> C1 minimum-circumsphere contact balance and Jung range
       |
       +--> L0 lower-branch radial transport and tangent-gap reduction
       |     |
       |     +--> L1 exact rational propagation cells and row partition
       |           |
       |           +--> L2 weakest lower row O3B02B / near-Jung theorem bottleneck
       |
       +--> N0 four-contact near-Jung deficiency budget
             |
             +--> N1 affine tetrahedral coordinates
             |     |
             |     +--> N2 determinant transfer
             |     +--> N3 dominant-edge coordinate-width lemma
             |
             +--> N4 exact forced fan
             |     |
             |     +--> N5 physical forced-core lower bound
             |
             +--> N6 three antipodal cap-pair bounds
                   |
                   +--> N7 exact six-cap disjointness
                         |
                         +--> N8 near-Jung lower bound and strict handoff

L2 + N8 + gap-free partition --> T0 universal coefficient
```

## Claim ledger by dependency

| ID | Claim | Evidence | Verification class | Depends on |
|---|---|---|---|---|
| C0 | Width-one support identity, difference body, diameter one, cubic scaling | Paper Section 2; classical sources | Sourced; paper proof | - |
| C1 | Minimum-ball contacts balance; $1/2\le R\le\sqrt6/4$; four contacts for $R^2>1/3$ | Paper Section 2 | Sourced; paper proof | C0 |
| C2 | Opposite-point identity $x-n\in K$ and support inequality | Paper Lemma 2.1 | Paper proof | C0 |
| L0 | Divergence transport inequality and tangent majorant | Paper Section 3 | Paper proof | C0, C2 |
| L1 | Rational propagation, exact cap rings, and complete lower row table | Four NPZ cells, reference handoff JSON, exact verifier | Exact certificate | L0 |
| L2 | `O3B02B` is the weakest lower-branch row at $R_*$, while the near-Jung branch is the universal bottleneck | Final JSON and byte-identical row reconstruction | Exact certificate | L1 |
| N0 | Four-contact deficiency budget $S\le(3-8R^2)/(4R^2-1)$ | Paper Section 4 | Paper proof | C1 |
| N1 | Affine tetrahedral reference coordinates and explicit Gram formulas | Paper Section 4 | Paper proof | N0 |
| N2 | $\det H\ge1-S/2-S^2/2$ | Paper Proposition 4.1; exact assembly inputs | Paper proof; exact evaluation | N1 |
| N3 | Dominant-edge diagonal bounds and three coordinate-width lower bounds | Paper Section 5; certificate JSON | Paper proof; exact evaluation | N0, N1 |
| N4 | 98,306-ray fan satisfies every exact margin and inherited multiplier condition | Fan NPZ files, orbit audit TSV, exact verifier | Exact certificate | N0 |
| N5 | Determinant-transferred forced-core volume lower bound | Fan volume and determinant fields | Exact certificate | N2, N4 |
| N6 | Three optimized antipodal cap-pair lower bounds | Section hull TSV, cap fields, exact verifier | Exact certificate | N3, N4 |
| N7 | Interiors of all six caps are pairwise disjoint | Cross-axis disjointness fields and exact verifier | Paper proof; exact certificate | N3, N6 |
| N8 | Near-Jung branch exceeds the theorem upper enclosure by a strict positive margin | Final JSON and exact branch assembly | Exact certificate | N5, N6, N7 |
| T0 | Universal coefficient is set just below the near-Jung branch and is cleared by both split terminal rows | Gap-free split and exact branch comparison | Exact certificate plus paper reduction | L2, N8 |
| A0 | Binary64 Python agrees with principal exact values | `audit_universal_bound.py` and transcript | Independent audit | L1, N4-N8, T0 |
| A1 | Base-R implementation agrees with principal values | `audit_universal_bound.R` and transcript | Independent audit | L1, N4-N8, T0 |
| A2 | Seven corrupted objects are rejected | Mutation suite and transcript | Adversarial audit | L1, N4, N6-N8, T0 |
| D0 | Paper theorem constants and lower table match the JSON | `paper/reconcile_certificate.py` | Release infrastructure | L1, T0 |
| D1 | Exact-constants appendix is generated from JSON | `proof/generate_exact_constants.py` | Release infrastructure | L1, N4-N8, T0 |
| E0 | Full theorem independently reviewed | No record yet | External review needed | C0-T0 |

## Universal theorem assembly

The theorem uses the closed partition

$$
\left[\frac12,R_*\right]
\cup
\left[R_*,\frac{\sqrt6}{4}\right].
$$

The lower branch proves a coefficient strictly above the displayed theorem value throughout the first interval via the split terminal rows `O3B02A/O3B02B`.
The near-Jung branch proves a strictly larger coefficient throughout the second
interval. The common endpoint causes no gap because both branch conditions are
valid there.

The finite certificate checks the exact comparison. The manuscript must still
justify that every width-one body has a circumradius in the Jung interval and
falls under the corresponding branch reduction.

## Audit dependencies are not proof dependencies

The numerical audits, PDF checks, and continuous-integration jobs do not feed
into the logical proof of `T0`. They are error-detection and release-integrity
layers. A failed audit blocks release because it indicates a discrepancy, but a
passing audit does not substitute for the exact path or the paper proof.

## Highest-value external review points

The most consequential points for independent mathematical review are:

1. passage from arbitrary bodies to the regularized radial inequality;
2. completeness and direction of each lower-branch propagation implication;
3. the deficiency budget and determinant transfer;
4. the dominant-edge coordinate-width lemma;
5. the geometric interpretation of the fan and section hulls;
6. the cap-volume formula and pairwise-disjointness argument; and
7. the final universal quantifier across the branch split.
