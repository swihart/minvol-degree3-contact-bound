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
- **HOSTED-REPLAYED:** the named three-job hosted workflow passed on the stated
  commit.
- **FRESH-CLONE-REPLAYED:** a new clone of the remote passed the stated replay
  and ended clean.
- **RELEASE-PENDING:** technically prepared but awaiting a final evidence run,
  immutable tag, release assets, visibility change, or explicit approval.
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
| T1 | Universal coefficient equals the exact theorem coefficient | `O3B02` plus strict near-Jung handoff; exact value in the certificate and paper | EXACT-CERTIFIED; RECONSTRUCTION-CHECKED |
| T2 | Scaling gives the theorem for arbitrary width $d>0$ | Homogeneity | ESTABLISHED IN MANUSCRIPT |

## Verification and provenance claims

| ID | Claim | Evidence | Status |
|---|---|---|---|
| V1 | Standalone verifier has no private repository dependency | Path regression test and source inspection | EXACT-CERTIFIED |
| V2 | Final JSON is rebuilt byte identically | Exact verifier and unit test | RECONSTRUCTION-CHECKED |
| V3 | Exact TSV and CSV renderings are rebuilt byte identically | Exact verifier | RECONSTRUCTION-CHECKED |
| V4 | Binary64 implementation agrees on principal quantities | Binary64 transcript | NUMERICAL AUDIT |
| V5 | Base-R implementation agrees on principal quantities | Named-author and hosted R transcripts | NUMERICAL AUDIT |
| V6 | Seven named proof-object mutations are rejected | Mutation transcript | MUTATION-TESTED |
| V7 | Paper-facing constants and lower table match the JSON | Paper reconciliation script | RECONSTRUCTION-CHECKED |
| V8 | Exact-constants appendix matches the JSON | Generator `--check` | RECONSTRUCTION-CHECKED |
| V9 | Required release documents exist and preserve claim language | Release-document checker | RECONSTRUCTION-CHECKED |
| V10 | Markdown/PDF pairs are complete | Pair checker | RECONSTRUCTION-CHECKED |
| V11 | PDFs are readable, have embedded fonts, and expose text | Hosted Poppler preflight on run `35468019663` | HOSTED-REPLAYED |
| V12 | Exact, Python-audit, test, mutation, metadata, and paper paths pass on Ubuntu | Workflow run `35468019663`, commit `892d4bc6fad07950e78da66e45b95063a6415af6` | HOSTED-REPLAYED |
| V13 | Independent base-R audit passes on hosted R 4.6.1 | Workflow run `35468019663` | HOSTED-REPLAYED; NUMERICAL AUDIT |
| V14 | Remote fresh clone reproduces all language paths and builds | Named-author transcript for commit `892d4bc6...` | FRESH-CLONE-REPLAYED |
| V15 | Fresh-clone working tree remains clean and bundle has complete five-commit history | Fresh transcript and verified transfer bundle | FRESH-CLONE-REPLAYED; RECONSTRUCTION-CHECKED |
| V16 | Hosted/fresh-clone evidence fields and claim boundaries are indexed consistently | `certificate/evidence/rc1_remote_audit.json`; `ci/verify_remote_evidence.py` | RECONSTRUCTION-CHECKED |

The hosted evidence above refers to
<https://github.com/swihart/minvol-degree3-contact-bound/actions/runs/35468019663>.

## Publication and review claims

| ID | Claim | Status |
|---|---|---|
| P1 | Lean ten-page Paper v1 manuscript is present | Completed draft |
| P2 | Complete release-document set is present in Markdown and PDF | Completed; 22 paired documents |
| P3 | Release-candidate author list and no-affiliation statement are fixed | Completed for `v1.0.0-rc1` |
| P4 | Split license and release-candidate citation metadata are fixed | Completed for `v1.0.0-rc1` |
| P5 | Private staging remote exists and the audited candidate was pushed | Completed at commit `892d4bc6...` |
| P6 | Hosted Python, R, and document jobs are green on the audited candidate | Completed on run `35468019663` |
| P7 | Fresh staging-remote clone replay is recorded | Completed; final status clean |
| P8 | Evidence-bearing commit receives its own hosted run | RELEASE-PENDING |
| P9 | Immutable final tag and release assets exist | RELEASE-PENDING |
| P10 | Repository visibility is public and GitHub Release is published | RELEASE-PENDING |
| P11 | External subject-matter reviewer has checked the theorem | EXTERNAL REVIEW NEEDED |
| P12 | Peer review or journal acceptance exists | Not claimed |

## Claim boundary

The package does not establish equality, rigidity, sharpness, a minimizing
body, or Meissner extremality. It should not be described as independently
verified or formally verified while `P11` remains open. The named-author fresh
clone and hosted CI are reproducibility evidence, not external mathematical
review.

## Current bottleneck

The mathematical, finite-certificate, authorship, citation, licensing, hosted-
candidate, and fresh-clone gates are complete for audited commit
`892d4bc6fad07950e78da66e45b95063a6415af6`. The remaining release bottlenecks
are:

1. green hosted jobs on this evidence-bearing commit;
2. final named-author copy edit and page approval;
3. final release date and transition to `v1.0.0`;
4. immutable release assets and independent asset-hash verification;
5. annotated `v1.0.0` tag, green tag workflow, and fresh tagged-checkout replay;
6. explicit approval of the final README, paper, release notes, tag, visibility
   change, release, and announcement; and
7. external mathematical review after release.
