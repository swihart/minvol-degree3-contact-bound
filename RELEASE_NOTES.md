# Release notes

## Release candidate `v1.0.0-rc1` (unreleased)

This is the release-candidate record for a proposed computer-assisted
universal lower bound in the three-dimensional Blaschke–Lebesgue problem. The
candidate metadata and licensing are fixed, but no public release or immutable
tag is asserted yet.

## Proposed result

For every convex body $K\subset\mathbb R^3$ of constant width $d>0$, the
package represents the proposed inequality

$$
\operatorname{Vol}(K)\ge
\frac{26220940089713\pi}{200000000000000}\,d^3
=0.4118775637803022742481789259828398710\ldots d^3.
$$

The result is universal: no symmetry, smoothness, contact-type, or fixed
circumradius assumption appears in the final theorem.

## Included in the draft package

- a ten-page LaTeX manuscript and reference PDF;
- one standalone exact-rational certificate;
- immutable JSON, NPZ, TSV, and CSV proof objects;
- an independent NumPy binary64 audit;
- an independent base-R audit;
- ten reconstruction and regression tests;
- seven adversarial proof-object mutation tests;
- automatic paper/certificate and appendix/certificate reconciliation;
- reproducibility, trust-boundary, claims, source, audit, and proof ledgers;
- paired Markdown/PDF documentation;
- SHA-256 manifests for the repository, certificate, paper, and rendered docs;
- a three-job GitHub Actions workflow for Python, R, and PDF/document checks;
- final candidate authorship, repository, citation, and split-license metadata.

## Proof architecture

The proof splits the normalized circumradius interval at

$$
R_*=\frac{305695601}{500000000}=0.611391202.
$$

The lower branch is a gap-free exact radial certificate whose unique bottleneck
is `O3B02`. In the near-Jung branch, four circumsphere contacts force a
98,306-ray core. An exact determinant transfer, a dominant-edge
coordinate-width estimate, and three optimized antipodal cap pairs give

```text
near-Jung lower = 0.4118796712148324317327979810531508741628745212952960018
handoff margin  = 0.0000021074345301574846190550703110031602996750911392740
```

so the lower-row coefficient is the universal bottleneck.

## Verification status

Completed in recorded environments:

- exact finite verification and byte-identical certificate reconstruction;
- independent Python binary64 audit;
- independent base-R audit on the named author's machine;
- ten regression tests and seven mutation tests;
- paper/certificate and exact-appendix reconciliation;
- manuscript and Markdown/PDF builds;
- construction-environment Poppler preflight and visual PDF inspection;
- clean-source/fresh-extraction checks.

Still required before release:

- creation of the intended public repository and push of this candidate;
- green hosted jobs on the exact release-candidate commit;
- final release date and transition from `v1.0.0-rc1` to `v1.0.0`;
- clean tagged-checkout replay;
- immutable release assets and hashes;
- explicit named-author approval of the final paper, README, release notes,
  tag, and announcement.

## Candidate publication metadata

- sole named author: Bruce J. Swihart;
- no institutional affiliation asserted;
- intended canonical repository:
  <https://github.com/swihart/minvol-degree3-contact-bound>;
- preferred citation: `CITATION.cff`;
- paper and prose license: CC BY 4.0;
- software and build-infrastructure license: MIT;
- candidate version: `v1.0.0-rc1`;
- target final tag: `v1.0.0`;
- final release date and archival identifier: not yet assigned.

## Scope and limitations

This draft does not prove:

- sharpness or equality;
- rigidity;
- the identity of a minimizing body;
- the Meissner conjecture;
- independent reproduction or peer review.

The Meissner value is an explicit-body comparison value, not a universal
minimum established here.

## Relationship to prior work

The package builds on classical constant-width geometry, the support-function
and spectral perspective developed in recent work, and the direct
contact-geometric exact-rational architecture of the public HYRA predecessor.
The repository has fresh history and does not alter the earlier public MinVol
spectral-bound repository.

A dated source and recent-literature check is recorded in
[`proof/SOURCE_LEDGER.md`](proof/SOURCE_LEDGER.md). It is targeted rather than
exhaustive, so this draft avoids an unqualified “best known” claim.

## Corrections and versioning

A change to any theorem-bearing proof object, exact verification rule, radius
partition, or coefficient requires a new version and explicit mathematical
comparison. Corrections must be recorded in release notes; released history
must not be silently rewritten.
