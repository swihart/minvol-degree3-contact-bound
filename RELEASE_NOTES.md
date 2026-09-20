# Release notes: v1.0.0

**Release date:** September 20, 2026<br>
**Author:** Bruce J. Swihart<br>
**Status:** AI-assisted, non-peer-reviewed computer-assisted research preprint seeking independent mathematical verification

**Canonical repository:**
[github.com/swihart/minvol-degree3-contact-bound](https://github.com/swihart/minvol-degree3-contact-bound)

**Versioned release:**
[v1.0.0](https://github.com/swihart/minvol-degree3-contact-bound/releases/tag/v1.0.0)

**Main manuscript:**
[PDF](paper/contact_geometric_bound.pdf) | [LaTeX source](paper/contact_geometric_bound.tex)

## Purpose of this release

Version `v1.0.0` is the initial public research release of a proposed
computer-assisted universal lower bound in the three-dimensional
Blaschke-Lebesgue problem.

For every convex body $K\subset\mathbb R^3$ of constant width $d>0$, the
package represents the proposed inequality

$$
\mathrm{Vol}(K)\ge
\frac{26220940089713\pi}{200000000000000}\,d^3
=0.4118775637803022742481789259828398710\ldots d^3.
$$

The result is universal: no symmetry, smoothness, contact-type, or fixed
circumradius assumption appears in the final theorem.

## Included materials

This release contains:

- a ten-page LaTeX manuscript and compiled PDF;
- a standalone exact-rational certificate;
- immutable JSON, NPZ, TSV, and CSV proof objects;
- an independent NumPy binary64 audit;
- an independent base-R audit;
- ten reconstruction and regression tests;
- seven adversarial proof-object mutation tests;
- automatic paper/certificate and appendix/certificate reconciliation;
- reproducibility, trust-boundary, claims, source, audit, and proof ledgers;
- 22 paired Markdown/PDF documents;
- SHA-256 manifests for the repository, certificate, paper, and rendered docs;
- deterministic release-asset build and verification scripts; and
- a three-job GitHub Actions workflow for Python, R, and PDF/document checks.

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

Before the final version transition, audited release-candidate commit
`892d4bc6fad07950e78da66e45b95063a6415af6` passed:

- the exact finite verifier and byte-identical certificate reconstruction;
- the independent Python binary64 audit;
- the independent base-R audit on the named author's machine and hosted R 4.6.1;
- ten regression tests and seven mutation tests;
- paper/certificate and exact-appendix reconciliation;
- the manuscript and all 22 Markdown/PDF builds;
- hosted Poppler preflight of committed and rebuilt PDFs;
- three green hosted jobs at
  <https://github.com/swihart/minvol-degree3-contact-bound/actions/runs/35468019663>;
- a complete named-author fresh-clone replay under Python 3.14.7, NumPy 2.3.5,
  and R 4.6.1; and
- a clean fresh-clone working tree and complete five-commit bundle.

The exact `v1.0.0` tag must pass the same three hosted jobs before the GitHub
Release is published. Release assets are then built from that tagged checkout,
verified against one SHA-256 manifest, downloaded, and reverified in a clean
directory.

These checks establish reproducibility of the supplied computations and
documents. They do not constitute peer review or external subject-matter
verification of the complete mathematical argument.

## Release assets

The tagged asset builder produces:

```text
minvol-contact-bound-paper-v1.0.0.pdf
minvol-contact-bound-paper-source-v1.0.0.zip
minvol-contact-bound-certificate-v1.0.0.zip
minvol-contact-bound-docs-v1.0.0.zip
minvol-contact-bound-replay-transcripts-v1.0.0.zip
minvol-contact-bound-release-record-v1.0.0.json
RELEASE_NOTES.md
RELEASE_NOTES.pdf
SHA256SUMS.txt
```

## Publication metadata

- sole named author: Bruce J. Swihart;
- no institutional affiliation asserted;
- canonical repository:
  <https://github.com/swihart/minvol-degree3-contact-bound>;
- preferred citation: `CITATION.cff`;
- paper and prose license: CC BY 4.0;
- software and build-infrastructure license: MIT;
- version: `v1.0.0`;
- release date: September 20, 2026;
- archival DOI: none assigned or implied.

## Scope and limitations

This release does not prove:

- sharpness or equality;
- rigidity;
- the identity of a minimizing body;
- the Meissner conjecture;
- independent external reproduction or peer review.

The Meissner value is an explicit-body comparison value, not a universal
minimum established here. The dated literature check in
[`proof/SOURCE_LEDGER.md`](proof/SOURCE_LEDGER.md) is targeted rather than
exhaustive, so this release avoids an unqualified "best known" claim.

## Relationship to prior work

The package builds on classical constant-width geometry, Nishioka's
support-function and spectral perspective, and the direct contact-geometric
exact-rational architecture of the public HYRA predecessor. The repository has
fresh Git history and does not alter the [earlier public MinVol spectral-bound
repository](https://github.com/swihart/minvol-degree3-spectral-bound).

## Preferred citation

Bruce J. Swihart, *A Certified Contact-Geometric Lower Bound for the
Three-Dimensional Blaschke-Lebesgue Problem*, version v1.0.0,
computer-assisted preprint, September 20, 2026.

The machine-readable citation is in [`CITATION.cff`](CITATION.cff).

## Corrections and versioning

A change to any theorem-bearing proof object, exact verification rule, radius
partition, or coefficient requires a new version and explicit mathematical
comparison. Corrections must preserve the `v1.0.0` record and must not silently
rewrite released history.
