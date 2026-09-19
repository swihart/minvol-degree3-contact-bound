# MinVol three-dimensional contact bound

**Public-package construction checkpoint - not yet released**

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

The current checkpoint contains a standalone exact certificate, independent
Python and base-R audits, adversarial rejection tests, and a lean Paper v1
manuscript reconciled automatically against the machine-readable certificate.
It is still an unreleased research draft. Final authorship, affiliation,
citation, license, repository, tag, and release metadata remain open.

## Paper

- [Reference PDF](paper/contact_geometric_bound.pdf)
- [LaTeX source](paper/contact_geometric_bound.tex)
- [Paper build and reconciliation guide](paper/README.md)
- [Rendered paper-guide PDF](rendered/markdown/paper/README.pdf)

The reference manuscript states the proof architecture and claim limitations in
nine pages. Its certificate-critical constants and lower-branch partition are
generated from the exact JSON rather than copied manually.

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
adversarial mutation tests, and paper/certificate reconciliation:

```sh
./run_python_checks.sh
```

Expected final markers include:

```text
MINVOL UNIVERSAL CONTACT-BOUND CERTIFICATE: EXACT
MINVOL UNIVERSAL CONTACT-BOUND BINARY64 AUDIT: PASS
MINVOL ADVERSARIAL MUTATION SUITE: PASS
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

- Certificate guide: [Markdown](certificate/README.md) |
  [PDF](rendered/markdown/certificate/README.pdf)
- Certificate status: [Markdown](certificate/STATUS.md) |
  [PDF](rendered/markdown/certificate/STATUS.pdf)
- Paper guide: [Markdown](paper/README.md) |
  [PDF](rendered/markdown/paper/README.pdf)
- This README: [Markdown](README.md) |
  [PDF](rendered/markdown/README.pdf)

## Scope

The package proposes a universal lower bound. It does not identify a minimizing
body, prove sharpness or equality, or prove the Meissner conjecture. The
Meissner value is an explicit-body comparison value, not a universal minimum
proved here. The result has not yet been externally reproduced, peer reviewed,
or publicly released.

The earlier public MinVol spectral announcement remains a separate repository:
[swihart/minvol-degree3-spectral-bound](https://github.com/swihart/minvol-degree3-spectral-bound).
Further universal refinements are under investigation but are outside this v1
package.
