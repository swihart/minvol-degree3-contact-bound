# MinVol three-dimensional contact bound

**Public-package construction checkpoint — not yet released**

This fresh-history repository scaffold is being prepared for a computer-assisted
preprint and exact reproducibility package for the proposed universal bound

$$
\operatorname{Vol}(K)\ge
\frac{26220940089713\pi}{200000000000000}\,d^3
=0.41187756378030227424817892598\ldots d^3
$$

for every convex body `K` in `R^3` of constant width `d`.

The current checkpoint contains the standalone exact certificate export, an
archived successful base-R audit, and adversarial rejection tests for seven
theorem-critical mutation classes. It does not yet contain the final paper,
final authorship/citation metadata, license, rendered Markdown PDFs, or release
assets. It must not yet be described as a public release.

## Replay

```sh
python3 -m pip install -r requirements.txt
```

```sh
./run_python_checks.sh
```

The Python path runs the exact verifier, the binary64 audit, ten reconstruction
tests, and seven adversarial mutation tests. With base R installed, the complete
all-language replay is:

```sh
./run_all.sh
```

To refresh the archived base-R transcript deliberately, run:

```sh
./run_r_checks.sh 2>&1 | tee certificate/transcripts/base_r_audit.txt
```

After changing an archived transcript or any other protected file, refresh and
verify both checksum manifests:

```sh
python3 refresh_checksums.py
```

```sh
python3 refresh_checksums.py --check
```

The exact certificate and its claim boundaries are documented in
[`certificate/README.md`](certificate/README.md) and
[`certificate/STATUS.md`](certificate/STATUS.md).

## Scope

The package proposes a universal lower bound. It does not identify a minimizing
body, prove sharpness, or prove the Meissner conjecture. The Meissner value is an
explicit-body comparison value, not a theorem supplied by this repository.

Further universal refinements are under investigation but are outside this v1 package.
