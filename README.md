# MinVol three-dimensional contact bound

**Release candidate `v1.0.0-rc1` - not yet public**

This fresh-history repository is being prepared for a computer-assisted
preprint and exact reproducibility package for the proposed universal bound

$$
\boxed{
\operatorname{Vol}(K)\ge
\frac{26220940089713\pi}{200000000000000}\,d^3
=0.41187756378030227424817892598\ldots d^3
}
$$

for every convex body `K` in `R^3` of constant width `d`.

The release candidate contains a standalone exact certificate, independent
Python and base-R audits, adversarial rejection tests, and a lean Paper v1
manuscript reconciled automatically against the machine-readable certificate.
Publication metadata is now fixed for this candidate: Bruce J. Swihart is the
sole named author, no institutional affiliation is asserted, prose is licensed
CC BY 4.0, and software is licensed MIT. The intended canonical repository is
<https://github.com/swihart/minvol-degree3-contact-bound>. The public remote,
hosted workflow, final release date and tag, immutable assets, and announcement
remain pending.

## Paper

- [Reference PDF](paper/contact_geometric_bound.pdf)
- [LaTeX source](paper/contact_geometric_bound.tex)
- [Paper build and reconciliation guide](paper/README.md)
- [Rendered paper-guide PDF](rendered/markdown/paper/README.pdf)

The reference manuscript states the proof architecture and claim limitations in
ten pages. Its certificate-critical constants and lower-branch partition are
generated from the exact JSON rather than copied manually.

## Publication metadata

- **Author:** Bruce J. Swihart
- **Institutional affiliation:** none asserted in this release candidate
- **Correspondence and verification reports:** the intended repository issue
  tracker at <https://github.com/swihart/minvol-degree3-contact-bound/issues>
- **Candidate version:** `v1.0.0-rc1`
- **Target final tag:** `v1.0.0`
- **Release date:** not yet assigned
- **License:** CC BY 4.0 for paper/prose; MIT for software/build infrastructure
- **Citation metadata:** [`CITATION.cff`](CITATION.cff)
- **Licensing text:** [`LICENSE`](LICENSE)

The repository description approved for the intended public remote is:

> Paper, exact certificate, and reproducibility materials for a
> contact-geometric universal lower bound in the three-dimensional
> Blaschke-Lebesgue problem.

## Reviewer path

1. Read the [paper PDF](paper/contact_geometric_bound.pdf).
2. Read the [certificate status](certificate/STATUS.md) and
   [certificate guide](certificate/README.md).
3. Verify the checksum manifests.
4. Run the exact and independent Python paths with `./run_python_checks.sh`.
5. With base R installed, run the complete replay with `./run_all.sh`.
6. Build the paper and Markdown documentation in a clean environment.

## Replay

Install the pinned Python dependency:

```sh
python3 -m pip install -r requirements.txt
```

Run the exact verifier, binary64 audit, ten reconstruction tests, seven
adversarial mutation tests, exact-constants and release-document checks, and
paper/certificate reconciliation:

```sh
./run_python_checks.sh
```

Expected final markers include:

```text
MINVOL UNIVERSAL CONTACT-BOUND CERTIFICATE: EXACT
MINVOL UNIVERSAL CONTACT-BOUND BINARY64 AUDIT: PASS
MINVOL ADVERSARIAL MUTATION SUITE: PASS
MINVOL EXACT-CONSTANTS APPENDIX: CURRENT
MINVOL RELEASE-DOCUMENT CHECK: PASS
MINVOL CITATION METADATA CHECK: PASS
MINVOL METADATA PREFLIGHT: PASS
MINVOL PAPER-CERTIFICATE RECONCILIATION: PASS
```

With base R installed, run all language paths:

```sh
./run_all.sh
```

To refresh the archived base-R transcript deliberately:

```sh
./run_r_checks.sh 2>&1 | tee certificate/transcripts/base_r_audit.txt
```

After changing a protected source, transcript, or reference artifact, refresh
and verify the checksum manifests:

```sh
python3 refresh_checksums.py
```

```sh
python3 refresh_checksums.py --check
```

## Build documentation

Build the paper without overwriting its committed reference PDF:

```sh
./build_paper.sh
```

Build local PDFs for every Markdown source under `build/markdown/`:

```sh
./build_markdown_pdfs.sh
```

The committed Markdown/PDF pairs are under `rendered/markdown/`. Their pairing
and PDF preflight checks are run by continuous integration and can also be run
locally.

## Proof architecture

The proof splits the normalized circumradius interval at

$$
R_*=\frac{305695601}{500000000}=0.611391202.
$$

Below the split, a gap-free exact radial-propagation certificate has unique
bottleneck `O3B02`. Above the split, four balanced circumsphere contacts force
a 98,306-ray polyhedral core. An exact determinant transfer, a dominant-edge
coordinate-width estimate, and three optimized antipodal cap pairs produce a
near-Jung lower bound strictly above the bottleneck. Exact integer and rational
arithmetic supplies the finite proof authority; binary64 Python and base R are
independent audits.

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
- Draft release notes: [Markdown](RELEASE_NOTES.md) |
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
proved here. The result has not yet been externally reproduced or peer reviewed. This
release candidate has not yet been pushed to the intended public repository.

The earlier public MinVol spectral announcement remains a separate repository:
[swihart/minvol-degree3-spectral-bound](https://github.com/swihart/minvol-degree3-spectral-bound).
Further universal refinements are under investigation but are outside this v1
package.
