# Verification status

**Version:** `v1.0.0-rc1`
**Release date:** unreleased
**Status date:** September 19, 2026

## Proposed theorem

For every convex body $K\subset\mathbb R^3$ of constant width $d>0$, the
package represents the proposed universal inequality

$$
\boxed{
\operatorname{Vol}(K)\ge
\frac{26220940089713\pi}{200000000000000}\,d^3
=0.41187756378030227424817892598\ldots d^3
}.
$$

## Current designation

> **Proposed exact universal certificate — standalone internal replay.**

The finite exact verifier, independent binary64 Python audit, independent
base-R audit, regression tests, adversarial mutation tests, manuscript
reconciliation, and documentation checks pass in the recorded environments.
The result is not yet externally reproduced, peer reviewed, accepted, tagged,
or publicly released.

## Candidate publication metadata

- sole named author: Bruce J. Swihart;
- institutional affiliation: none asserted;
- intended repository:
  <https://github.com/swihart/minvol-degree3-contact-bound>;
- candidate version: `v1.0.0-rc1`;
- target final tag: `v1.0.0`;
- prose license: CC BY 4.0;
- software license: MIT;
- final release date and archival identifier: pending.

## Verification matrix

| ID | Verification item | Evidence | Status |
|---|---|---|---|
| E1 | Exact lower-row, fan, determinant, coordinate-width, cap, and handoff inequalities | `certificate/certify_universal_bound.py`; certificate JSON; exact transcript | Passed |
| E2 | Byte-identical reconstruction of final machine-readable certificate | Production exact verifier | Passed |
| N1 | Independent binary64 reconstruction | `certificate/audit_universal_bound.py` | Passed |
| R1 | Independent base-R reconstruction | `certificate/audit_universal_bound.R`; archived user-machine transcript | Passed |
| T1 | Reconstruction and regression suite | Ten Python tests | Passed |
| M1 | Deliberate corruption detection | Seven adversarial mutation tests | Passed |
| P1 | Paper coefficient, split, lower rows, and main constants match certificate | `paper/reconcile_certificate.py` | Passed |
| D1 | Exact-constants appendix matches certificate | `proof/generate_exact_constants.py` | Passed |
| D2 | Required release documents and relative links are present | `ci/verify_release_docs.py` | Passed in this checkpoint |
| D2a | Candidate author, repository, citation, and split-license metadata are internally consistent | `ci/preflight_metadata.sh`; `CITATION.cff`; `LICENSE` | Passed in this checkpoint |
| D3 | Every repository Markdown source has a checksummed PDF counterpart | `ci/verify_doc_pairs.py` | Passed in construction environment |
| P2 | Paper and documentation PDFs are readable, have embedded fonts, and expose extractable text | Poppler preflight in construction environment and hosted workflow definition | Passed in construction; hosted run pending |
| C1 | Fresh standalone replay with no private path dependency | Clean extraction/bundle tests | Passed for recorded checkpoints |
| C2 | Green hosted Python, R, and document jobs on final public commit/tag | `.github/workflows/verification.yml` | Pending |
| X1 | Independent mathematical reproduction by an outside reviewer | None yet | Pending |
| J1 | Peer review or publication acceptance | None yet | Pending |

## What “exact” means here

The theorem-bearing finite comparisons use Python integers and
`fractions.Fraction`. The verifier reads immutable integer arrays, checks the
semantic inequalities, reconstructs derived artifacts byte for byte, and
compares exact rational coefficients. No binary floating-point inequality is
used as theorem authority.

“Exact” does not mean that the whole research claim has been independently
validated. The proof still depends on the correctness and completeness of the
mathematical reduction encoded in the manuscript and verifier, the trusted
software/hardware stack, and the absence of a shared conceptual error.

See [`certificate/TRUST_BOUNDARY.md`](certificate/TRUST_BOUNDARY.md).

## What is established inside the package

- gap-free circumradius coverage from $1/2$ to $\sqrt6/4$;
- unique lower-branch bottleneck `O3B02`;
- exact refinement of the formerly weak lower-row interval;
- final fan reconstruction with 98,306 rays;
- positive exact fan margin;
- determinant transfer and dominant-edge coordinate-width bounds;
- forced-core and three cap-pair lower bounds;
- exact six-cap disjointness;
- a near-Jung lower bound strictly above the bottleneck;
- exact universal coefficient assembly;
- paper and appendix reconciliation with the certificate;
- rejection of seven representative proof-object corruptions.

## What is not established

The package does not establish:

- sharpness, equality, or rigidity;
- the identity of a minimizing body;
- the Meissner conjecture;
- external independent reproduction;
- peer review, journal acceptance, or publication;
- an exhaustive priority or novelty determination.

The Meissner volume is used only as an explicit-body comparison value.

## Release boundary

Before this release candidate can become an immutable public release, the
project still requires:

1. creation of the intended public remote and push of the exact candidate;
2. final author copy edit and approval;
3. green hosted Python, R, and document jobs on that commit;
4. assignment of the final release date and transition to tag `v1.0.0`;
5. a fresh tagged-checkout replay and release-asset hash audit; and
6. explicit approval before the tag, release, or announcement.

External review remains a scientific goal after release and must not be implied
by a green workflow.
