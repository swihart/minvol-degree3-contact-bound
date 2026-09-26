# Paper v1 manuscript

## Status

This directory contains the focused Paper v1 manuscript for the proposed exact
universal contact-geometric lower bound

$$
\mathrm{Vol}(K)\ge
\frac{26221074253\pi}{200000000000}\,d^3
=0.41187967121228637754323153860\ldots d^3
$$

for every three-dimensional convex body `K` of constant width `d`.

The manuscript is version `v1.1.0` of an **AI-assisted, computer-assisted,
non-peer-reviewed research preprint**. Bruce J. Swihart is the sole named
author, and no institutional affiliation is asserted. It does not establish
sharpness or equality, identify a minimizer, or prove the Meissner conjecture.

## Files

- `contact_geometric_bound.tex` is the editable LaTeX manuscript.
- `contact_geometric_bound.pdf` is the checksum-protected reference PDF.
- `reconcile_certificate.py` reads the authoritative certificate JSON and
  generates/checks the theorem-critical TeX includes.
- `certificate_constants.tex` is the generated exact-constant include.
- `lower_branch_table.tex` is the generated gap-free lower-branch table.
- `build.sh` performs a non-destructive local build in `paper/build/`.
- `SHA256SUMS.txt` authenticates the archived paper sources and reference PDF.

The reference PDF is committed for review. A local build is written to
`paper/build/contact_geometric_bound.pdf` and does not overwrite the reference
artifact.

## Certificate reconciliation

The paper does not maintain independent hand-entered copies of the main
coefficient, circumradius split, lower-branch table, fan census, core and cap
bounds, near-Jung lower bound, or handoff margin. Those values are generated
from

```text
certificate/certificates/universal_contact_bound_certificate.json
```

Run the reconciliation check from the repository root:

```sh
python3 paper/reconcile_certificate.py --check
```

The required marker is:

```text
MINVOL PAPER-CERTIFICATE RECONCILIATION: PASS
```

To deliberately regenerate the two TeX includes after an authorized
certificate change:

```sh
python3 paper/reconcile_certificate.py --write
```

A certificate change is a mathematical change and requires explicit review,
new checksums, and a new public version. Ordinary paper editing should use
`--check`, not `--write`.

## Build

Required tools are Python 3, `latexmk`, and a PDFLaTeX installation containing
the standard AMS, Latin Modern, `microtype`, `geometry`, `hyperref`, `xurl`,
`enumitem`, and table packages used in the source.

From the repository root:

```sh
./build_paper.sh
```

Expected final markers:

```text
MINVOL PAPER-CERTIFICATE RECONCILIATION: PASS
MINVOL PAPER BUILD: PASS
```

The build uses a fixed source-date epoch and canonicalizes the PDF trailer ID.
Equivalent PDF bytes are nevertheless not required across all TeX engines,
font maps, operating systems, or compression libraries. The mathematical proof
authority is the exact certificate and verifier, not PDF serialization.

## Manuscript boundary

Paper v1 explains only the proof needed for the coefficient above:

1. constant-width identities and minimum-circumsphere contacts;
2. the lower-circumradius radial certificate;
3. affine contact coordinates and determinant transfer;
4. the high-resolution forced fan;
5. the dominant-edge coordinate-width estimate;
6. six optimized pairwise-disjoint antipodal cone caps;
7. universal branch assembly; and
8. the certificate architecture and trust boundary.

Later private circumradius-local and contact-atlas research is not included.
The manuscript contains only a general sentence noting that further refinements
may be investigated.

## Visual review

The reference PDF was rendered page by page and checked for clipped text,
overlapping tables, broken glyphs, and missing references. Table 3 uses local
row-height controls so that stacked exact fractions do not overlap. The author,
no-affiliation statement, citation, split license, version, release date, and
repository URL are checked automatically. The hosted document workflow rebuilds
the ten-page paper and performs Poppler readability, embedded-font, and
extractable-text preflight.

## Publication metadata

- **Sole named author:** Bruce J. Swihart
- **Institutional affiliation:** none asserted
- **Version:** `v1.1.0`
- **Release date:** September 26, 2026
- **Canonical repository:**
  <https://github.com/swihart/minvol-degree3-contact-bound>
- **Versioned release:**
  <https://github.com/swihart/minvol-degree3-contact-bound/releases/tag/v1.1.0>
- **Audited pre-release workflow:**
  <https://github.com/swihart/minvol-degree3-contact-bound/actions/runs/35468019663>
- **Paper/prose license:** CC BY 4.0
- **Software/build license:** MIT
- **Preferred citation:** repository-root `CITATION.cff`

The recorded hosted workflow and named-author fresh clone are reproducibility
evidence, not peer review or external mathematical verification. No DOI or
other archival identifier is asserted unless one is assigned later.
