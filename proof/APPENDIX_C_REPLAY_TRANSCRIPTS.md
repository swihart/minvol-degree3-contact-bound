# Appendix C: replay transcripts and expected markers

**Status:** summary of archived evidence
**Transcript authority:** checksummed files under `certificate/transcripts/`

This appendix does not replace the transcript files. It identifies what each
file records, what a successful run must contain, and how the records should be
interpreted.

## C.1 Transcript inventory

| File | Path exercised | Required terminal marker |
|---|---|---|
| `exact_certificate.txt` | Production exact-rational verifier | `MINVOL UNIVERSAL CONTACT-BOUND CERTIFICATE: EXACT` |
| `binary64_audit.txt` | Independent NumPy binary64 audit | `MINVOL UNIVERSAL CONTACT-BOUND BINARY64 AUDIT: PASS` |
| `python_unittest.txt` | Ten reconstruction/regression tests | `Ran 10 tests` followed by `OK` |
| `adversarial_mutations.txt` | Seven deliberate corruptions | `MINVOL ADVERSARIAL MUTATION SUITE: PASS` |
| `base_r_audit.txt` | Independent base-R audit | `MINVOL UNIVERSAL CONTACT-BOUND BASE-R AUDIT: PASS` |
| `export_equivalence.txt` | Private-source/public-export theorem-field comparison performed during construction | `PUBLIC EXPORT EQUIVALENCE: PASS` |
| `environment.txt` | Construction-environment versions and platform | no theorem marker; provenance only |

Exact SHA-256 values for these files are recorded in
`certificate/SHA256SUMS.txt` and the root `SHA256SUMS.txt`.

## C.2 Exact transcript

The exact transcript should report, among other values:

```text
split radius:                  0.61139120200000000000
weakest lower row:            O3B02
changed fan vertices:         18229
minimum exact fan margin:     0.0000000002888904207092857876733697822441644655792123744
near-Jung handoff margin:     0.0000021074345301574846190550703110031602996750911392740
universal coefficient lower: 0.4118775637803022742481789259828398710025748462041567278
```

The exact output is a human-readable projection of integer and rational
computations. The production program also requires byte-identical reconstruction
of the authoritative certificate and exact audit artifacts.

## C.3 Binary64 transcript

The numerical audit should reconstruct the same geometry with ordinary
floating-point operations and report values agreeing at the documented scale.
It is expected to differ in the last displayed digits from exact decimal
renderings.

A pass means the independent numerical implementation agrees within its stated
tolerances. It is not a substitute for the exact finite proof.

## C.4 Base-R transcript

The base-R implementation was run on the named author's Mac. It reports the
four refined rows, fan census and minimum margin, determinant lower bound,
coordinate widths, cap totals, disjointness gap, near-Jung value, theorem
coefficient, and predecessor gain.

The archived transcript did not record the exact R version. This omission is
reported rather than filled by inference. Hosted continuous integration uses
the declared R version in `.github/workflows/verification.yml`.

## C.5 Mutation transcript

A successful mutation transcript shows seven tests and ends with:

```text
Ran 7 tests
OK
MINVOL ADVERSARIAL MUTATION SUITE: PASS
```

The test succeeds only when every corrupted object is rejected. A mutation that
passes through the verifier is a test failure, even if the final coefficient is
numerically unchanged.

## C.6 Export-equivalence transcript

The standalone public package was compared semantically with the authoritative
private theorem package during construction. Ten theorem-critical fields were
checked, including the coefficient, split, lower rows, bottleneck, fan minimum,
core, cap total, near-Jung value, and handoff margin.

This transcript records construction provenance. The public release does not
require access to the private repository to replay its own proof.

## C.7 Reproducing the records

Run the Python paths:

```sh
./run_python_checks.sh
```

Run the independent R path:

```sh
./run_r_checks.sh
```

Run both language paths:

```sh
./run_all.sh
```

To refresh a transcript deliberately, capture the program output, review it,
refresh checksum manifests, and commit the source and new record together.
Never edit a transcript to manufacture a pass marker.

## C.8 Interpretation

The transcript set demonstrates repeatability of the finite programs on the
recorded environments. It does not demonstrate:

- external subject-matter review;
- novelty;
- correctness of every mathematical reduction outside the finite checker;
- immunity to a common bug shared by multiple implementations;
- peer-reviewed publication.

Those distinctions must remain visible in any release announcement.
