# Reproducibility guide

**Package status:** release `v1.0.0` (September 26, 2026)
**Prepared:** September 26, 2026
**Main certificate schema:** `minvol.universal_contact_bound.v1`

This guide explains how to reproduce the exact certificate, the independent
Python and base-R audits, the adversarial mutation tests, the paper/certificate
reconciliation, the manuscript build, and the paired Markdown/PDF
documentation.

The proposed theorem represented by the package is

$$
\mathrm{Vol}(K)\ge
\frac{26220940089713\pi}{200000000000000}\,d^3
=0.41187756378030227424817892598\ldots d^3
$$

for every convex body $K\subset\mathbb R^3$ of constant width $d>0$.

## Reproduction levels

The repository distinguishes four levels of reproduction.

| Level | What is reproduced | Required tools | Interpretation |
|---|---|---|---|
| Exact certificate | All theorem-bearing finite inequalities and byte-identical derived certificate files | Python and pinned NumPy | Finite proof authority |
| Independent audits | Binary64 Python and base-R reconstructions | Python/NumPy and base R | Independent numerical agreement, not proof authority |
| Paper reconciliation | The theorem coefficient, split radius, lower-row table, and paper-facing constants | Python | Prevents silent drift between paper and certificate |
| Document build | LaTeX paper and every Markdown-derived PDF | LaTeX, Pandoc, XeLaTeX; Poppler for full preflight | Presentation and release integrity |

## Tested environments

### Construction environment

The archived construction transcript records:

```text
Linux x86_64
Python 3.13.5
NumPy 2.3.5
Rscript unavailable
```

In that environment, the exact verifier, binary64 audit, ten reconstruction
tests, seven adversarial mutation tests, paper reconciliation, manuscript
build, Markdown/PDF build, and Poppler PDF preflight passed.

### Named-author remote fresh-clone replay

The named author cloned the private staging remote at audited commit
`892d4bc6fad07950e78da66e45b95063a6415af6` and reproduced the complete
package on macOS with:

```text
Python 3.14.7
NumPy 2.3.5
R 4.6.1
TeX Live 2023
```

The exact verifier, binary64 audit, ten reconstruction tests, seven mutation
tests, release-document and metadata checks, paper reconciliation, base-R
audit, paper build, and all 22 committed and rebuilt Markdown/PDF pair checks
passed. The final `git status --short` was empty, and the resulting bundle
recorded the complete five-commit history.

The local Mac did not have Poppler installed. Full `pdfinfo`, `pdffonts`, and
`pdftotext` preflight was therefore supplied by the successful hosted document
job rather than waived.

### Continuous integration

Workflow run
<https://github.com/swihart/minvol-degree3-contact-bound/actions/runs/35468019663>
checked out audited candidate commit
`892d4bc6fad07950e78da66e45b95063a6415af6` in all three jobs. The downloaded
logs contain all required pass markers for:

- exact certificate, binary64 audit, ten tests, seven mutation tests, metadata,
  release documents, and paper reconciliation;
- the independent base-R audit; and
- the paper, 22-document build, pair checks, and committed/rebuilt Poppler
  preflight.

The recorded hosted environment was:

- Ubuntu 24.04.5 LTS, runner image version `20260907.300.1`;
- CPython 3.13.15 and NumPy 2.3.5;
- R 4.6.1, using base R only;
- Pandoc 3.10.1;
- TeX Live 2023/Debian; and
- Poppler `pdfinfo`, `pdffonts`, and `pdftotext`.

The run passed three of three jobs. This is portability and reproducibility
evidence; it does not replace mathematical review.

### Remote-evidence record

The audit-transfer manifest and the bundle, fresh-replay transcript, and hosted
log archive were independently hashed after upload. Their exact SHA-256 values
and structural conclusions are recorded in
[`CLEAN_CLONE_CHECK.md`](CLEAN_CLONE_CHECK.md) and
[`certificate/evidence/rc1_remote_audit.json`](certificate/evidence/rc1_remote_audit.json).
The structural checker is `ci/verify_remote_evidence.py`.

## Fresh source-tree procedure

The canonical repository is
<https://github.com/swihart/minvol-degree3-contact-bound>. For a release replay,
check out the immutable `v1.0.0` tag or download the corresponding GitHub
Release assets and verify their `SHA256SUMS.txt` before execution.

Enter the repository root:

```sh
cd minvol-degree3-contact-bound
```

Verify that the generated checksum manifests are current:

```sh
python3 refresh_checksums.py --check
```

Verify the root manifest:

```sh
shasum -a 256 -c SHA256SUMS.txt
```

Verify the certificate manifest:

```sh
cd certificate
```

```sh
shasum -a 256 -c SHA256SUMS.txt
```

Verify the paper manifest:

```sh
cd ../paper
```

```sh
shasum -a 256 -c SHA256SUMS.txt
```

Return to the root:

```sh
cd ..
```

## Python exact path and audits

Create an isolated environment:

```sh
python3 -m venv .venv
```

Activate it on a POSIX shell:

```sh
. .venv/bin/activate
```

Install the pinned dependency:

```sh
python3 -m pip install -r requirements.txt
```

Run the exact verifier, independent binary64 audit, ten reconstruction tests,
seven mutation tests, exact-constants appendix check, release-document check,
and paper reconciliation:

```sh
./run_python_checks.sh
```

A successful run contains all of these markers:

```text
MINVOL UNIVERSAL CONTACT-BOUND CERTIFICATE: EXACT
PROPOSED UNIVERSAL LOWER BOUND ABOVE 0.4118775: EXACTLY CERTIFIED BY THIS PACKAGE
MINVOL UNIVERSAL CONTACT-BOUND BINARY64 AUDIT: PASS
Ran 10 tests
OK
Ran 7 tests
OK
MINVOL ADVERSARIAL MUTATION SUITE: PASS
MINVOL EXACT-CONSTANTS APPENDIX: CURRENT
MINVOL REMOTE-EVIDENCE CHECK: PASS
MINVOL RELEASE-DOCUMENT CHECK: PASS
MINVOL METADATA PREFLIGHT: PASS
MINVOL RELEASE PREFLIGHT: PASS
MINVOL PAPER-CERTIFICATE RECONCILIATION: PASS
```

On tested machines, the complete Python path usually finishes in under one
minute. Runtime is informative only; a slower run is not a failure.

## Independent base-R audit

The R program uses base R only:

```sh
./run_r_checks.sh
```

The required marker is:

```text
MINVOL UNIVERSAL CONTACT-BOUND BASE-R AUDIT: PASS
```

To deliberately refresh the archived transcript:

```sh
./run_r_checks.sh 2>&1 | tee certificate/transcripts/base_r_audit.txt
```

After changing a protected transcript, refresh both generated manifests:

```sh
python3 refresh_checksums.py
```

Then rerun all checksum checks. A transcript should never be edited to add a
pass marker that was not produced by the program.

## Complete language replay

When both Python and R are available:

```sh
./run_all.sh
```

The final marker is:

```text
MINVOL UNIVERSAL CONTACT-BOUND REPLAY: PASS
```

## Paper build

The committed paper PDF is a reference artifact. A local build is written to
`paper/build/` and does not overwrite the reference PDF:

```sh
./build_paper.sh
```

Required final markers:

```text
MINVOL PAPER-CERTIFICATE RECONCILIATION: PASS
MINVOL PAPER BUILD: PASS
```

A locally rebuilt PDF need not have the same SHA-256 as the committed PDF on a
different TeX installation. Mathematical content, page validity, embedded
fonts, extractable text, and reconciliation with the certificate are the
portable requirements.

## Markdown/PDF documentation build

Build all Markdown sources into a local mirror under `build/markdown/`:

```sh
./build_markdown_pdfs.sh
```

Verify the committed pairs:

```sh
python3 ci/verify_doc_pairs.py --pdf-root rendered/markdown
```

Verify the local rebuild pairs:

```sh
python3 ci/verify_doc_pairs.py --pdf-root build/markdown
```

The committed reference PDFs are in `rendered/markdown/`; Markdown remains the
editable source.

## PDF preflight

On a system with Poppler installed, preflight the committed artifacts:

```sh
./ci/preflight_pdfs.sh rendered/markdown paper/contact_geometric_bound.pdf
```

Preflight the local rebuilds:

```sh
./ci/preflight_pdfs.sh build/markdown paper/build/contact_geometric_bound.pdf
```

If Poppler is not available locally, record that fact and rely on the hosted
document job. Do not weaken or delete the preflight script merely to make a
local command return success.

## Release-asset build and verification

Before the immutable tag exists, exercise the deterministic packager in preview
mode:

```sh
./build_release_assets.sh --preview
```

Verify every generated file, archive member, and SHA-256 entry:

```sh
./verify_release_assets.sh
```

From the exact `v1.0.0` tagged checkout, build the release assets without the
preview flag:

```sh
./build_release_assets.sh
```

The tagged mode refuses a dirty tree and refuses a `HEAD` that is not tagged
`v1.0.0`. The output under `release/build/` contains the paper PDF, paper-source
archive, standalone certificate archive, paired-documentation archive, replay
records, release notes in Markdown and PDF, a machine-readable release record,
and one `SHA256SUMS.txt`. Downloaded GitHub Release assets should be reverified
with the same verifier in a clean directory.

## Clean-tree check

After all replay steps and deliberate builds:

```sh
git status --short
```

A release replay should leave the tracked source tree clean. Local
outputs under ignored `build/`, `.venv/`, and `ci-artifacts/` directories do
not count as tracked changes.

## Disk and network requirements

The checked proof objects occupy only a few megabytes. The largest cost is the
local TeX/Pandoc toolchain rather than the certificate itself. The exact
verifier requires no network access after the repository and Python dependency
are present. Continuous integration may access package mirrors only to install
its declared tools.

## Reproducibility is not peer review

Successful replay shows that the supplied programs deterministically accept
the supplied exact objects and that two numerical implementations agree. It
does not independently prove the geometric reductions in the manuscript,
establish novelty, identify a minimizer, or replace expert mathematical review.
See [`certificate/TRUST_BOUNDARY.md`](certificate/TRUST_BOUNDARY.md) and
[`certificate/CLAIMS_AND_LIMITATIONS.md`](certificate/CLAIMS_AND_LIMITATIONS.md).
