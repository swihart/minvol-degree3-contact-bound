# Proof ledger

## Status vocabulary

- **ESTABLISHED IN MANUSCRIPT:** a complete derivation is present in the paper,
  subject to ordinary mathematical review.
- **EXACT-CERTIFIED:** the finite claim is checked with integer and rational
  arithmetic by the standalone verifier.
- **NUMERICAL AUDIT:** a separate floating-point implementation agrees.
- **RECONSTRUCTION-CHECKED:** an expected derived artifact is rebuilt byte for
  byte.
- **MUTATION-TESTED:** a targeted corrupted object is rejected.
- **SOURCE-CHECKED:** bibliographic or historical wording has been compared with
  an identified source.
- **RELEASE-PENDING:** technically prepared but awaiting a hosted workflow,
  immutable tag, release assets, or explicit approval.
- **EXTERNAL REVIEW NEEDED:** no independent subject-matter review has been
  recorded.

## Mathematical claims

| ID | Claim | Evidence | Status |
|---|---|---|---|
| M1 | Constant-width support identity and diameter-one normalization | Paper Section 2; classical references | ESTABLISHED IN MANUSCRIPT; SOURCE-CHECKED |
| M2 | Blaschke volume-surface identity | Paper Section 2; classical references | ESTABLISHED IN MANUSCRIPT; SOURCE-CHECKED |
| M3 | Minimum circumsphere contact balance and Jung range | Paper Section 2 | ESTABLISHED IN MANUSCRIPT |
| M4 | Opposite-point identity and radial support inequality | Paper Lemma 2.1 | ESTABLISHED IN MANUSCRIPT |
| L1 | Transport inequality and tangent-gap master inequality | Paper Section 3 | ESTABLISHED IN MANUSCRIPT |
| L2 | Rational propagation implications | Paper Section 3; exact lower-cell checks | ESTABLISHED IN MANUSCRIPT; EXACT-CERTIFIED |
| L3 | Four refined cells replace `O3A1` with positive margins | Refined NPZ cells and JSON | EXACT-CERTIFIED; NUMERICAL AUDIT |
| L4 | Complete lower partition is gap free and has unique bottleneck `O3B02` | Final JSON and exact verifier | EXACT-CERTIFIED; RECONSTRUCTION-CHECKED |
| N1 | Near-Jung four-contact deficiency budget | Paper Section 4 | ESTABLISHED IN MANUSCRIPT |
| N2 | Affine contact coordinates and Gram formulas | Paper Section 4 | ESTABLISHED IN MANUSCRIPT |
| N3 | Determinant transfer $\det H\ge1-S/2-S^2/2$ | Paper Proposition 4.1 | ESTABLISHED IN MANUSCRIPT; exact endpoint evaluation |
| N4 | Dominant-edge coordinate-width diagonal bounds | Paper Section 5 | ESTABLISHED IN MANUSCRIPT; exact endpoint evaluation |
| N5 | Adjusted 98,306-ray fan is feasible with positive exact margin | Fan NPZ, orbit TSV, exact verifier | EXACT-CERTIFIED; NUMERICAL AUDIT; MUTATION-TESTED |
| N6 | Forced-core volume lower bound | Exact fan volume and determinant transfer | EXACT-CERTIFIED; NUMERICAL AUDIT |
| N7 | Three axis-specific antipodal cap-pair bounds | Hull TSV and cap certificate fields | EXACT-CERTIFIED; NUMERICAL AUDIT; MUTATION-TESTED |
| N8 | Six cap interiors are pairwise disjoint | Paper and exact disjointness fields | ESTABLISHED IN MANUSCRIPT; EXACT-CERTIFIED; MUTATION-TESTED |
| N9 | Near-Jung lower bound exceeds theorem upper enclosure | Final JSON assembly | EXACT-CERTIFIED; NUMERICAL AUDIT |
| T1 | Universal coefficient is $26220940089713\pi/200000000000000$ | `O3B02` plus strict near-Jung handoff | EXACT-CERTIFIED; RECONSTRUCTION-CHECKED |
| T2 | Scaling gives the theorem for arbitrary width $d>0$ | Homogeneity | ESTABLISHED IN MANUSCRIPT |

## Verification and provenance claims

| ID | Claim | Evidence | Status |
|---|---|---|---|
| V1 | Standalone verifier has no private repository dependency | Path regression test and source inspection | EXACT-CERTIFIED |
| V2 | Final JSON is rebuilt byte identically | Exact verifier and unit test | RECONSTRUCTION-CHECKED |
| V3 | Exact TSV and CSV renderings are rebuilt byte identically | Exact verifier | RECONSTRUCTION-CHECKED |
| V4 | Binary64 implementation agrees on principal quantities | Binary64 transcript | NUMERICAL AUDIT |
| V5 | Base-R implementation agrees on principal quantities | Named-author machine R transcript | NUMERICAL AUDIT |
| V6 | Seven named proof-object mutations are rejected | Mutation transcript | MUTATION-TESTED |
| V7 | Paper-facing constants and lower table match the JSON | Paper reconciliation script | RECONSTRUCTION-CHECKED |
| V8 | Exact-constants appendix matches the JSON | Generator `--check` | RECONSTRUCTION-CHECKED |
| V9 | Required release documents exist and preserve claim language | Release-document checker | RECONSTRUCTION-CHECKED |
| V10 | Markdown/PDF pairs are complete | Pair checker | RECONSTRUCTION-CHECKED |
| V11 | PDFs are readable, have embedded fonts, and expose text | Poppler preflight | Passed in construction; hosted rerun pending |

## Publication and review claims

| ID | Claim | Status |
|---|---|---|
| P1 | Lean ten-page Paper v1 manuscript is present | Completed draft |
| P2 | Complete release-document set is present in Markdown and PDF | Completed in this checkpoint after local build |
| P3 | Release-candidate author list and no-affiliation statement are fixed | Completed for `v1.0.0-rc1` |
| P4 | Split license and release-candidate citation metadata are fixed | Completed for `v1.0.0-rc1` |
| P5 | Public remote, immutable tag, and release assets exist | RELEASE-PENDING |
| P6 | Hosted Python, R, and document jobs are green on the release candidate | RELEASE-PENDING |
| P7 | Fresh public-clone replay is recorded | RELEASE-PENDING |
| P8 | External subject-matter reviewer has checked the theorem | EXTERNAL REVIEW NEEDED |
| P9 | Peer review or journal acceptance exists | Not claimed |

## Claim boundary

The package does not establish equality, rigidity, sharpness, a minimizing
body, or Meissner extremality. It should not be described as independently
verified or formally verified while `P8` remains open.

## Current bottleneck

The mathematical, finite-certificate, authorship, citation, and licensing
packages are prepared for `v1.0.0-rc1`. The remaining release bottlenecks are
administrative, hosted, and external:

1. public remote and release-candidate push;
2. green hosted workflow on that exact commit;
3. final named-author copy edit and page approval;
4. final release date, `v1.0.0` tag, and fresh tagged-checkout replay;
5. immutable release assets and independent hash verification;
6. explicit approval of the final README, paper, release notes, tag, and
   announcement; and
7. external mathematical review after release.
