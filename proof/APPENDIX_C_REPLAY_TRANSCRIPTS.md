# Appendix C: replay transcripts and expected markers

**Status:** summary of archived and transferred evidence
**Construction-transcript authority:** checksummed files under
`certificate/transcripts/`
**Remote-evidence index:** `certificate/evidence/rc1_remote_audit.json`

This appendix does not replace the transcript or log files. It identifies what
each record contains, what a successful run must show, and how the evidence
should be interpreted.

## C.1 Construction transcript inventory

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

## C.4 Base-R records

The archived construction transcript records a successful base-R audit. The
later remote fresh-clone transcript records the exact named-author environment:

```text
Rscript (R) version 4.6.1 (2026-06-24)
```

The hosted R job also installed R 4.6.1 and ended with:

```text
MINVOL UNIVERSAL CONTACT-BOUND BASE-R AUDIT: PASS
```

The program reports the four refined rows, fan census and minimum margin,
determinant lower bound, coordinate widths, cap totals, disjointness gap,
near-Jung value, theorem coefficient, and predecessor gain.

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

## C.7 Hosted and fresh-clone evidence

The audited release-candidate commit is

```text
892d4bc6fad07950e78da66e45b95063a6415af6
Add release-candidate citation and licensing metadata
```

The successful hosted workflow is
<https://github.com/swihart/minvol-degree3-contact-bound/actions/runs/35468019663>.
It contains three jobs: exact/Python verification, independent base R, and
paper/document build plus Poppler preflight.

The named-author fresh-clone transcript records Python 3.14.7, NumPy 2.3.5,
R 4.6.1, the complete replay pass marker, a ten-page paper build, 22 committed
and 22 rebuilt Markdown/PDF pairs, an empty final `git status --short`, and a
complete five-commit bundle.

The transferred evidence artifacts have these SHA-256 values:

```text
2c324230f02ba4cb2541e0d353cc7906ae460cac0a768267144f650a0278a1a3  minvol-degree3-contact-bound-v1.0.0-rc1-main.bundle
ce2abd06646fdf89d6e60b9069ee55451715a35970afedd24e4acf0d1d64de7f  minvol-degree3-contact-bound-v1.0.0-rc1-fresh-replay.txt
44fc68b36e05153fabd2a93aaa4b092b946016b9eb10bcecf37d7bf5c6b4ad3a  minvol-degree3-contact-bound-v1.0.0-rc1-github-actions-logs.zip
```

The transfer manifest itself has SHA-256
`3f958520e0e119cad4db97d60a2ac3702b8144a8f6228068bdfeb6d43124f57d`.
The action-log ZIP has 36 entries and passes ZIP integrity testing.

These raw artifacts are intended for the final replay-transcript release asset;
they are not theorem proof objects. Their machine-readable evidence summary is
`certificate/evidence/rc1_remote_audit.json`.

## C.8 Reproducing the records

Run the Python paths:

```sh
./run_python_checks.sh
```

A successful Python run now also includes:

```text
MINVOL REMOTE-EVIDENCE CHECK: PASS
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

## C.9 Interpretation

The transcript set demonstrates repeatability of the finite programs on the
recorded environments. Hosted CI and the named-author fresh clone broaden the
platform evidence but do not demonstrate:

- external subject-matter review;
- novelty;
- correctness of every mathematical reduction outside the finite checker;
- immunity to a common bug shared by multiple implementations;
- sharpness or a minimizing body; or
- peer-reviewed publication.

Those distinctions must remain visible in any release announcement.
