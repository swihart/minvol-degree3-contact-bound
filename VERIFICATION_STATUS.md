# Verification status

**Version:** `v1.1.0`<br>
**Release date:** September 26, 2026<br>
**Status date:** September 26, 2026<br>
**Audited pre-release commit:** `892d4bc6fad07950e78da66e45b95063a6415af6`<br>
**Audited hosted workflow:** <https://github.com/swihart/minvol-degree3-contact-bound/actions/runs/35468019663>

## Proposed theorem

For every convex body $K\subset\mathbb R^3$ of constant width $d>0$, the
package represents the proposed universal inequality

$$
\boxed{
\mathrm{Vol}(K)\ge
\frac{26221074253\pi}{200000000000}\,d^3
=0.41187967121228637754323153860\ldots d^3
}.
$$

## Current designation

> **Proposed exact universal certificate - standalone release v1.1.0.**

The finite exact verifier, independent binary64 Python audit, independent
base-R audit, regression tests, adversarial mutation tests, manuscript
reconciliation, documentation checks, hosted three-job workflow, and named-
author fresh-clone replay pass in the recorded environments. The result has not
been externally reproduced, peer reviewed, or accepted for journal
publication.

## Publication metadata

- sole named author: Bruce J. Swihart;
- institutional affiliation: none asserted;
- canonical repository:
  <https://github.com/swihart/minvol-degree3-contact-bound>;
- versioned release:
  <https://github.com/swihart/minvol-degree3-contact-bound/releases/tag/v1.1.0>;
- version: `v1.1.0`;
- release date: September 26, 2026;
- prose license: CC BY 4.0;
- software license: MIT;
- archival DOI: none assigned or implied.

## Verification matrix

| ID | Verification item | Evidence | Status |
|---|---|---|---|
| E1 | Exact lower-row, fan, determinant, coordinate-width, cap, and handoff inequalities | `certificate/certify_universal_bound.py`; certificate JSON; exact transcript | Passed |
| E2 | Byte-identical reconstruction of final machine-readable certificate | Production exact verifier | Passed |
| N1 | Independent binary64 reconstruction | `certificate/audit_universal_bound.py` | Passed locally and hosted |
| R1 | Independent base-R reconstruction | `certificate/audit_universal_bound.R`; named-author and hosted transcripts | Passed locally and hosted |
| T1 | Reconstruction and regression suite | Ten Python tests | Passed locally and hosted |
| M1 | Deliberate corruption detection | Seven adversarial mutation tests | Passed locally and hosted |
| P1 | Paper coefficient, split, lower rows, and main constants match certificate | `paper/reconcile_certificate.py` | Passed locally and hosted |
| D1 | Exact-constants appendix matches certificate | `proof/generate_exact_constants.py` | Passed locally and hosted |
| D2 | Required release documents and relative links are present | `ci/verify_release_docs.py` | Passed locally and hosted |
| D2a | Author, repository, version, date, citation, and split-license metadata are internally consistent | `ci/preflight_metadata.sh`; `ci/preflight_release.sh`; `CITATION.cff`; `LICENSE` | Passed in release preparation |
| D3 | Every repository Markdown source has a checksummed PDF counterpart | `ci/verify_doc_pairs.py` | 22 of 22 passed locally and hosted |
| P2 | Paper and documentation PDFs are readable, have embedded fonts, and expose extractable text | Hosted Poppler preflight on committed and rebuilt PDFs | Passed on run `35468019663` before the final metadata transition; repeated by the tag workflow before publication |
| C1 | Fresh standalone replay with no private path dependency | Named-author remote clone of commit `892d4bc6...` | Passed; final status clean |
| C2 | Green hosted Python, R, and document jobs on the audited candidate | Three jobs on commit `892d4bc6...` | Passed on run `35468019663` |
| C3 | Complete public-history bundle and transfer hashes verified | Bundle and three transferred evidence artifacts | Passed |
| C4 | Hosted workflow and fresh-clone evidence are internally indexed | `certificate/evidence/rc1_remote_audit.json`; `ci/verify_remote_evidence.py` | Passed |
| C5 | Green hosted jobs and fresh replay on the immutable final tag | Final `v1.1.0` tag and release procedure | Publication gate |
| A1 | Deterministic release assets and SHA-256 manifest verify | `release/build_release_assets.py`; `release/verify_release_assets.py` | Preview-tested; tagged build required for publication |
| X1 | Independent mathematical reproduction by an outside reviewer | None yet | Pending |
| J1 | Peer review or journal acceptance | None yet | Pending |

## Recorded pre-release evidence

The audited pre-release commit is

```text
892d4bc6fad07950e78da66e45b95063a6415af6
Add release-candidate citation and licensing metadata
```

The hosted workflow at
<https://github.com/swihart/minvol-degree3-contact-bound/actions/runs/35468019663>
checked out that commit in all three jobs. The downloaded log archive contains
the expected exact, binary64, ten-test, seven-mutation, release-document,
metadata, paper, base-R, Markdown/PDF-pair, and Poppler-preflight pass markers.

A separate fresh clone reproduced the complete Python and base-R path under
Python 3.14.7, NumPy 2.3.5, and R 4.6.1. It rebuilt the ten-page paper and all
22 Markdown/PDF pairs and ended with an empty `git status --short`.

The raw transfer artifacts are identified by SHA-256 in
[`CLEAN_CLONE_CHECK.md`](CLEAN_CLONE_CHECK.md) and the machine-readable evidence
index at
[`certificate/evidence/rc1_remote_audit.json`](certificate/evidence/rc1_remote_audit.json).
That record remains intentionally labeled `rc1`: it documents the audited
pre-release state rather than rewriting history after the final version
transition.

## What "exact" means here

The theorem-bearing finite comparisons use Python integers and
`fractions.Fraction`. The verifier reads immutable integer arrays, checks the
semantic inequalities, reconstructs derived artifacts byte for byte, and
compares exact rational coefficients. No binary floating-point inequality is
used as theorem authority.

"Exact" does not mean that the whole research claim has been independently
validated. The proof still depends on the correctness and completeness of the
mathematical reduction encoded in the manuscript and verifier, the trusted
software/hardware stack, and the absence of a shared conceptual error.

See [`certificate/TRUST_BOUNDARY.md`](certificate/TRUST_BOUNDARY.md).

## What is established inside the package

- gap-free circumradius coverage from $1/2$ to $\sqrt6/4$;
- lower-branch weakest row `O3B02B`; the universal bottleneck is the near-Jung branch;
- exact refinement of the formerly weak lower-row interval;
- final fan reconstruction with 98,306 rays;
- positive exact fan margin;
- determinant transfer and dominant-edge coordinate-width bounds;
- forced-core and three cap-pair lower bounds;
- exact six-cap disjointness;
- a near-Jung lower bound that sets the universal bottleneck;
- exact universal coefficient assembly;
- paper and appendix reconciliation with the certificate;
- rejection of seven representative proof-object corruptions; and
- successful hosted and fresh-clone replay of the audited pre-release state.

## What is not established

The package does not establish:

- sharpness, equality, or rigidity;
- the identity of a minimizing body;
- the Meissner conjecture;
- external independent mathematical reproduction;
- peer review, journal acceptance, or an archival DOI;
- an exhaustive priority or novelty determination.

The Meissner volume is used only as an explicit-body comparison value.

## Publication boundary

The repository is prepared for release `v1.1.0`. Publication of the GitHub
Release is conditioned on all of the following operational checks:

1. the final release commit is clean and receives three green hosted jobs;
2. the annotated `v1.1.0` tag points to that exact commit;
3. the tag-triggered Python, R, and document jobs are green;
4. a fresh tagged checkout completes the full replay and ends clean;
5. tagged release assets are built, hashed, downloaded, and reverified; and
6. the named author explicitly approves the visibility change, GitHub Release,
   and announcement text.

External review remains a scientific goal after release and must not be implied
by a green workflow, named-author fresh-clone replay, or exact certificate.
