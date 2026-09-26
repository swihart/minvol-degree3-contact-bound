# MinVol three-dimensional contact bound

**Release:** [v1.1.0](https://github.com/swihart/minvol-degree3-contact-bound/releases/tag/v1.1.0) (September 26, 2026)<br>
**Author:** Bruce J. Swihart<br>
**Status:** AI-assisted, non-peer-reviewed computer-assisted research preprint seeking independent mathematical verification<br>
**Canonical repository:** [github.com/swihart/minvol-degree3-contact-bound](https://github.com/swihart/minvol-degree3-contact-bound)<br>
**AI system disclosed:** OpenAI ChatGPT (GPT-5.6 Sol Pro), accessed August-September 2026

This repository is the paper, exact certificate, and reproducibility package for
the proposed universal bound

$$
\boxed{
\mathrm{Vol}(K)\ge
\frac{26221074253\pi}{200000000000}\,d^3
=0.41187967121228637754323153860\ldots d^3
}
$$

for every convex body `K` in `R^3` of constant width `d`.

The package contains a standalone exact-rational certificate, independent
binary64 Python and base-R audits, ten reconstruction tests, seven adversarial
proof-object mutation tests, a ten-page manuscript, and paired Markdown/PDF
documentation. Bruce J. Swihart is the sole named author; no institutional
affiliation is asserted. The paper and prose are licensed CC BY 4.0, while the
software and build infrastructure are licensed MIT.

## Paper

- [Reference PDF](paper/contact_geometric_bound.pdf)
- [LaTeX source](paper/contact_geometric_bound.tex)
- [Paper build and reconciliation guide](paper/README.md)
- [Rendered paper-guide PDF](rendered/markdown/paper/README.pdf)

The manuscript explains the geometric reduction, the two circumradius
branches, and the finite certificate architecture. Every theorem-critical
constant and the complete lower-branch partition are generated from the
machine-readable certificate rather than copied manually.

## Publication metadata

- **Author:** Bruce J. Swihart
- **Institutional affiliation:** none asserted
- **Correspondence and verification reports:**
  <https://github.com/swihart/minvol-degree3-contact-bound/issues>
- **Version:** `v1.1.0`
- **Release date:** September 26, 2026
- **Versioned release:**
  <https://github.com/swihart/minvol-degree3-contact-bound/releases/tag/v1.1.0>
- **License:** CC BY 4.0 for paper/prose; MIT for software/build infrastructure
- **Citation metadata:** [`CITATION.cff`](CITATION.cff)
- **Licensing text:** [`LICENSE`](LICENSE)

## Verification record

Before the final version transition, the release-candidate commit
`892d4bc6fad07950e78da66e45b95063a6415af6` passed a three-job hosted workflow
covering exact/Python verification, independent base R, and paper/document
builds with Poppler preflight. A separate fresh clone of that commit reproduced
the complete Python and R replay under Python 3.14.7, NumPy 2.3.5, and R 4.6.1;
rebuilt the ten-page paper and all 22 Markdown/PDF pairs; and ended with an
empty `git status --short`.

The archived evidence and exact transfer hashes are in
[`CLEAN_CLONE_CHECK.md`](CLEAN_CLONE_CHECK.md) and
[`certificate/evidence/rc1_remote_audit.json`](certificate/evidence/rc1_remote_audit.json).
The final `v1.1.0` tag is required to pass the same three hosted jobs before the
GitHub Release is published. These are reproducibility checks, not peer review
or external mathematical verification.

## Reviewer path

1. Read the [paper PDF](paper/contact_geometric_bound.pdf).
2. Read the [certificate status](certificate/STATUS.md) and
   [certificate guide](certificate/README.md).
3. Verify the checksum manifests.
4. Run the exact and independent Python paths with `./run_python_checks.sh`.
5. With base R installed, run the complete replay with `./run_all.sh`.
6. Consult the proof ledger, source ledger, and trust-boundary document.

## Replay

Install the pinned Python dependency:

```sh
python3 -m pip install -r requirements.txt
```

Run the exact verifier, binary64 audit, ten reconstruction tests, seven
adversarial mutation tests, exact-constants and release-document checks,
release metadata preflight, and paper/certificate reconciliation:

```sh
./run_python_checks.sh
```

Expected markers include:

```text
MINVOL UNIVERSAL CONTACT-BOUND CERTIFICATE: EXACT
MINVOL UNIVERSAL CONTACT-BOUND BINARY64 AUDIT: PASS
MINVOL ADVERSARIAL MUTATION SUITE: PASS
MINVOL EXACT-CONSTANTS APPENDIX: CURRENT
MINVOL REMOTE-EVIDENCE CHECK: PASS
MINVOL RELEASE-DOCUMENT CHECK: PASS
MINVOL CITATION METADATA CHECK: PASS
MINVOL METADATA PREFLIGHT: PASS
MINVOL RELEASE PREFLIGHT: PASS
MINVOL PAPER-CERTIFICATE RECONCILIATION: PASS
```

With base R installed, run all language paths:

```sh
./run_all.sh
```

After changing a protected source, transcript, or reference artifact, refresh
and verify the checksum manifests:

```sh
python3 refresh_checksums.py
```

```sh
python3 refresh_checksums.py --check
```

## Build documentation and release assets

Build the paper without overwriting its committed reference PDF:

```sh
./build_paper.sh
```

Build local PDFs for every Markdown source under `build/markdown/`:

```sh
./build_markdown_pdfs.sh
```

The committed Markdown/PDF pairs are under `rendered/markdown/`. Their pairing
and PDF preflight checks run in continuous integration.

Preview and verify the deterministic release-asset set before tagging:

```sh
./build_release_assets.sh --preview
```

```sh
./verify_release_assets.sh
```

From the exact tagged checkout, omit `--preview`. The resulting release bundle
contains the paper PDF, paper source, standalone certificate, paired
documentation, replay records, release notes in Markdown/PDF, a machine-readable
release record, and one SHA-256 manifest.

## Proof architecture

The proof splits the normalized circumradius interval at

$$
R_*=\frac{305695601}{500000000}=0.611391202.
$$

Below the split, a gap-free exact radial-propagation certificate has unique
weakest terminal row `O3B02B`. Above the split, four balanced circumsphere contacts force
a 98,306-ray polyhedral core. An exact determinant transfer, a dominant-edge
coordinate-width estimate, and three optimized antipodal cap pairs produce a
near-Jung lower bound that is the universal bottleneck, while both split terminal rows clear the theorem coefficient. Exact integer and rational
arithmetic supplies the finite proof authority; binary64 Python and base R are
independent numerical audits.

## Documentation

The editable sources are Markdown. Checksummed reference PDFs mirror the same
repository-relative tree under `rendered/markdown/`.

### Status, release, and provenance

- Verification status: [Markdown](VERIFICATION_STATUS.md) |
  [PDF](rendered/markdown/VERIFICATION_STATUS.pdf)
- Reproducibility guide: [Markdown](REPRODUCIBILITY.md) |
  [PDF](rendered/markdown/REPRODUCIBILITY.pdf)
- Clean-source record: [Markdown](CLEAN_CLONE_CHECK.md) |
  [PDF](rendered/markdown/CLEAN_CLONE_CHECK.pdf)
- AI assistance and provenance: [Markdown](AI_ASSISTANCE.md) |
  [PDF](rendered/markdown/AI_ASSISTANCE.pdf)
- Release notes: [Markdown](RELEASE_NOTES.md) |
  [PDF](rendered/markdown/RELEASE_NOTES.pdf)
- Release checklist: [Markdown](RELEASE_CHECKLIST.md) |
  [PDF](rendered/markdown/RELEASE_CHECKLIST.pdf)

### Certificate documentation

- Certificate specification:
  [Markdown](certificate/CERTIFICATE_SPECIFICATION.md) |
  [PDF](rendered/markdown/certificate/CERTIFICATE_SPECIFICATION.pdf)
- Trust boundary: [Markdown](certificate/TRUST_BOUNDARY.md) |
  [PDF](rendered/markdown/certificate/TRUST_BOUNDARY.pdf)
- Claims and limitations:
  [Markdown](certificate/CLAIMS_AND_LIMITATIONS.md) |
  [PDF](rendered/markdown/certificate/CLAIMS_AND_LIMITATIONS.pdf)
- Independent-audit record:
  [Markdown](certificate/INDEPENDENT_AUDIT.md) |
  [PDF](rendered/markdown/certificate/INDEPENDENT_AUDIT.pdf)
- Certificate guide: [Markdown](certificate/README.md) |
  [PDF](rendered/markdown/certificate/README.pdf)
- Certificate status: [Markdown](certificate/STATUS.md) |
  [PDF](rendered/markdown/certificate/STATUS.pdf)

### Mathematical proof documentation

- Mathematical overview: [Markdown](proof/MATHEMATICAL_OVERVIEW.md) |
  [PDF](rendered/markdown/proof/MATHEMATICAL_OVERVIEW.pdf)
- Claim dependencies: [Markdown](proof/CLAIM_DEPENDENCIES.md) |
  [PDF](rendered/markdown/proof/CLAIM_DEPENDENCIES.pdf)
- Proof ledger: [Markdown](proof/PROOF_LEDGER.md) |
  [PDF](rendered/markdown/proof/PROOF_LEDGER.pdf)
- Internal proof audit: [Markdown](proof/PROOF_AUDIT.md) |
  [PDF](rendered/markdown/proof/PROOF_AUDIT.pdf)
- Source ledger: [Markdown](proof/SOURCE_LEDGER.md) |
  [PDF](rendered/markdown/proof/SOURCE_LEDGER.pdf)
- Appendix A, exact constants:
  [Markdown](proof/APPENDIX_A_EXACT_CONSTANTS.md) |
  [PDF](rendered/markdown/proof/APPENDIX_A_EXACT_CONSTANTS.pdf)
- Appendix B, certificate architecture:
  [Markdown](proof/APPENDIX_B_CERTIFICATE_ARCHITECTURE.md) |
  [PDF](rendered/markdown/proof/APPENDIX_B_CERTIFICATE_ARCHITECTURE.pdf)
- Appendix C, replay transcripts:
  [Markdown](proof/APPENDIX_C_REPLAY_TRANSCRIPTS.md) |
  [PDF](rendered/markdown/proof/APPENDIX_C_REPLAY_TRANSCRIPTS.pdf)
- Paper guide: [Markdown](paper/README.md) |
  [PDF](rendered/markdown/paper/README.pdf)
- This README: [Markdown](README.md) |
  [PDF](rendered/markdown/README.pdf)

## Citation and license

Use [`CITATION.cff`](CITATION.cff) for the preferred preprint citation. The
paper and prose documentation are licensed under CC BY 4.0; software and build
infrastructure are licensed under MIT. See [`LICENSE`](LICENSE) for the full
split-license notice.

## Scope

The package proposes a universal lower bound. It does not identify a minimizing
body, prove sharpness or equality, or prove the Meissner conjecture. The
Meissner value is an explicit-body comparison value, not a universal minimum
proved here. The result has not been externally reproduced or peer reviewed. The finite
certificate is not a Lean theorem-prover formalization; here, **exact** means
exact integer and rational arithmetic checked by the included programs.

The earlier public MinVol spectral announcement remains a separate repository:
[swihart/minvol-degree3-spectral-bound](https://github.com/swihart/minvol-degree3-spectral-bound).
Further universal refinements are under investigation but are outside this
version.
