# Recorded clean-source and fresh-extraction checks

**Record date:** September 19, 2026
**Package version:** `v1.0.0-rc1`
**Intended public remote:** `https://github.com/swihart/minvol-degree3-contact-bound` (not yet created)

This document records reproducibility tests performed while constructing the
fresh-history public package. A final tagged-checkout test will be added before
release.

## Results at a glance

| Checkpoint | Source form | Result |
|---|---|---|
| Standalone certificate root | Git bundle at commit `21a175010fb18d74e11286ef0e1135cb32c47053` | Exact Python, binary64, ten tests, base R, checksums, and clean status passed |
| Adversarial mutation overlay | Clean clone of the standalone bundle plus overlay | Seven corruptions rejected; full Python path and checksums passed |
| Lean Paper v1 overlay | Clean clone of the preceding content plus overlay | Paper reconciliation, manuscript build, Markdown pairs, checksums, and construction-environment PDF preflight passed |
| Complete release-document overlay | Clean clone of the preceding content plus this checkpoint | Exact/reconciliation/document checks and fresh-extraction PDF build/preflight passed during packaging |

The later overlay checkpoints were constructed before their user-side commit
hashes were available to this document. They are identified by content and
archive checksums in the corresponding transfer records rather than by invented
Git identifiers.

## 1. Standalone certificate bundle

The first fresh-history commit was

```text
21a175010fb18d74e11286ef0e1135cb32c47053
Add standalone exact universal certificate
```

The named author verified the supplied ZIP checksum, initialized an empty
`main` repository, checked both SHA-256 manifests, installed NumPy 2.3.5 in a
Python 3.14 virtual environment, and ran the exact verifier, independent
binary64 audit, and ten tests. The independent base-R audit also ended with its
required pass marker.

After the transcript and manifests were refreshed, all checksums passed and
`git status --short` was empty before and after the root commit.

## 2. Mutation checkpoint

A clean clone of the bundle was used to apply the adversarial-test overlay. The
complete Python path passed and seven deliberately corrupted objects were all
rejected. Root and certificate checksum manifests passed before and after the
run. A second clean extraction of the final overlay reproduced the same result.

The theorem coefficient and authoritative certificate JSON did not change.

## 3. Paper checkpoint

The lean Paper v1 overlay was applied to the post-mutation tree. The following
passed in the construction environment:

- exact and binary64 certificate paths;
- ten reconstruction tests;
- seven mutation tests;
- paper/certificate reconciliation;
- clean LaTeX build;
- Markdown/PDF source pairing;
- Poppler page/font/text preflight;
- page-by-page visual inspection of the ten-page release-candidate manuscript;
- all nested checksum manifests.

On the named author's Mac, the manuscript and Markdown builds and pair checks
passed. Poppler was not installed locally, so `pdfinfo`, `pdffonts`, and
`pdftotext` preflight was correctly deferred to the hosted Ubuntu document job.
No repository change was needed for that local dependency difference.

The named author reported the Paper v1 commit complete with a clean working tree
at 1:41 PM Eastern time on September 19, 2026. The exact commit hash will be
recorded after the next repository bundle or before release.

## 4. Release-document checkpoint

The release-document checkpoint adds the reproducibility, trust-boundary,
claims, audit, source-ledger, exact-constants, proof-ledger, release-note, and
release-checklist materials. During construction it was applied to a clean
reconstruction of the committed content and tested as a fresh extraction.

The packaging audit requires:

- current root, certificate, paper, and rendered-document manifests;
- exact certificate and mutation suites;
- exact-constants generation check;
- release-document presence, claim-boundary, and relative-link checks;
- paper/certificate reconciliation;
- one PDF for every Markdown source;
- valid embedded-font and extractable-text preflight in the construction
  environment;
- clean staged-diff checks.

The exact results and archive hash are reported with the overlay transfer. The
named author's local base-R replay remains required after applying the overlay,
because R is unavailable in the construction container.

## Environment notes

### Construction environment

```text
Linux x86_64
Python 3.13.5
NumPy 2.3.5
Rscript unavailable
Pandoc, XeLaTeX, latexmk, and Poppler available
```

### Named-author Mac replay

```text
macOS
Python 3.14
NumPy 2.3.5
base R available
Poppler command-line tools not installed
```

The exact R version was not captured in the archived local transcript and is
therefore not inferred. The hosted workflow declares R 4.6.1.

## Interpretation

These checks show that the supplied source tree is self-contained, the finite
programs replay in multiple implementations, the documentation builds, and no
private repository is needed. They do not establish independent mathematical
review, peer review, novelty, or correctness of every conceptual reduction.

## Final release requirement

After public metadata is finalized, the project must repeat the following from
a fresh checkout of the exact release tag:

1. checksum verification;
2. full Python and base-R replay;
3. paper and Markdown builds;
4. hosted Poppler preflight;
5. metadata and release-asset verification;
6. final clean working-tree check.

The resulting commit, tag, environments, workflow URLs, and any harmless PDF
binary variation should be recorded here rather than silently omitted.

## Metadata and legal checkpoint

The release-candidate metadata gate fixes the sole named author, absence of an
asserted institutional affiliation, intended repository name and description,
preferred citation, and split CC BY 4.0/MIT license. `ci/preflight_metadata.sh`
checks those decisions against the paper, README, `CITATION.cff`, `LICENSE`,
`VERSION`, and `RELEASE_DATE`. A public-remote clone and hosted workflow record
remain pending and must be appended before release.
