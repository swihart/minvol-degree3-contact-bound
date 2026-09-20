# Recorded clean-source, hosted, and fresh-clone checks

- **Record date:** September 19, 2026
- **Current package version:** `v1.0.0`
- **Audited pre-release package:** `v1.0.0-rc1`
- **Canonical repository:**
  <https://github.com/swihart/minvol-degree3-contact-bound>
- **Visibility during this audit:** private
- **Audited candidate commit:**
  `892d4bc6fad07950e78da66e45b95063a6415af6`
- **Hosted workflow:**
  <https://github.com/swihart/minvol-degree3-contact-bound/actions/runs/35468019663>

This document preserves the clean-source, hosted continuous-integration, and
fresh-clone evidence for the audited pre-release state. The final `v1.0.0` tag
uses the same replay requirements and must pass its own hosted and tagged-clone
gates before the GitHub Release is published.

## Results at a glance

| Checkpoint | Result |
|---|---|
| Standalone certificate (`21a1750`) | Exact Python, binary64, ten tests, base R, checksums, and clean status passed |
| Adversarial mutation suite (`068be1f`) | Seven representative corruptions rejected |
| Focused Paper v1 (`b11a13a`) | Paper reconciliation, builds, paired documents, and PDF checks passed |
| Complete release documentation (`dc4017a`) | Release-document, exact-constants, link, checksum, and PDF checks passed |
| Release-candidate metadata (`892d4bc`) | Author, citation, repository, version, and split-license metadata passed |
| Hosted candidate workflow | Three of three jobs completed successfully on `892d4bc` |
| Remote fresh-clone replay | Full Python/R replay, paper build, 22 document pairs, complete bundle, and clean status passed |

## 1. Curated fresh history

The audited bundle contains exactly five fresh-history commits. The labels below
identify their public audit roles; the hashes are authoritative:

```text
21a175010fb18d74e11286ef0e1135cb32c47053 Standalone exact-certificate checkpoint
068be1ff4bd7d815714445ec24549715eef0e5aa Adversarial mutation-test checkpoint
b11a13a145ebb09218dca542057b1d44700cb48e Focused Paper v1 checkpoint
dc4017ae564f8680eddbb9f1b4407ff1bd45991e Complete release-document checkpoint
892d4bc6fad07950e78da66e45b95063a6415af6 Release-candidate metadata checkpoint
```

The literal historical subject of commit `b11a13a` used lower-case *lean* in
the ordinary sense of *concise*. Public documentation uses **focused** to avoid
confusion with the Lean theorem prover. No proof-assistant formalization is
claimed.

`git fsck --full` passed, the bundle records a complete SHA-1 history, and no
private research branch or private repository history is present.

## 2. Transfer integrity

The four audit-transfer files were checked against the uploaded manifest. The
manifest itself has SHA-256

```text
3f958520e0e119cad4db97d60a2ac3702b8144a8f6228068bdfeb6d43124f57d
```

The three transferred evidence artifacts are:

**Main-branch bundle**

```text
filename: minvol-degree3-contact-bound-v1.0.0-rc1-main.bundle
SHA-256: 2c324230f02ba4cb2541e0d353cc7906ae460cac0a768267144f650a0278a1a3
```

**Fresh-clone replay transcript**

```text
filename: minvol-degree3-contact-bound-v1.0.0-rc1-fresh-replay.txt
SHA-256: ce2abd06646fdf89d6e60b9069ee55451715a35970afedd24e4acf0d1d64de7f
```

**GitHub Actions log archive**

```text
filename: minvol-degree3-contact-bound-v1.0.0-rc1-github-actions-logs.zip
SHA-256: 44fc68b36e05153fabd2a93aaa4b092b946016b9eb10bcecf37d7bf5c6b4ad3a
```

The GitHub Actions ZIP contains 36 entries, passes ZIP integrity testing, and
expands to 564,330 bytes. These raw transfer artifacts are audit inputs rather
than tracked theorem objects. Their hashes and conclusions are indexed in
`certificate/evidence/rc1_remote_audit.json`.

## 3. Hosted workflow on the audited candidate

Workflow run
<https://github.com/swihart/minvol-degree3-contact-bound/actions/runs/35468019663>
checked out commit
`892d4bc6fad07950e78da66e45b95063a6415af6` in all three jobs.
The named author reported all three jobs green, and the downloaded logs contain
all required pass markers with no error marker or nonzero command exit.

| Hosted job | Principal evidence | Result |
|---|---|---|
| Exact certificate, audits, metadata, release docs, and paper reconciliation | Exact verifier; binary64 audit; 10 regression tests; 7 mutation tests; metadata, release-doc, and paper checks | PASS |
| Independent base-R audit | Base R reconstruction on R 4.6.1 | PASS |
| Build and preflight paper and documentation PDFs | Ten-page paper; 22 Markdown/PDF pairs; committed and rebuilt Poppler preflight | PASS |

The hosted runners used Ubuntu 24.04.5 LTS, runner image
`ubuntu-24.04` version `20260907.300.1`. The Python job used CPython 3.13.15
and NumPy 2.3.5. The R job used R 4.6.1. The document job used Pandoc 3.10.1,
TeX Live 2023/Debian, and Poppler.

The document job also uploaded a temporary typeset-PDF artifact. Its recorded
run-scoped URL is
<https://github.com/swihart/minvol-degree3-contact-bound/actions/runs/35468019663/artifacts/10591743752>.
That artifact is not an immutable release asset and may expire.

## 4. Fresh clone from the staging remote

The named author cloned the private staging remote and began the audit at
`2026-09-19 16:58:42 EDT`. The fresh clone reported:

```text
branch: main
HEAD: 892d4bc6fad07950e78da66e45b95063a6415af6
origin/main: 892d4bc6fad07950e78da66e45b95063a6415af6
public-history commits: 5
Python: 3.14.7
NumPy: 2.3.5
R: 4.6.1
TeX Live: 2023
```

Before execution, the root, certificate, paper, and rendered-document checksum
manifests passed. The fresh-clone transcript then records all of the following:

```text
MINVOL UNIVERSAL CONTACT-BOUND CERTIFICATE: EXACT
MINVOL UNIVERSAL CONTACT-BOUND BINARY64 AUDIT: PASS
Ran 10 tests
OK
Ran 7 tests
OK
MINVOL ADVERSARIAL MUTATION SUITE: PASS
MINVOL EXACT-CONSTANTS APPENDIX: CURRENT
MINVOL RELEASE-DOCUMENT CHECK: PASS
MINVOL CITATION METADATA CHECK: PASS
MINVOL METADATA PREFLIGHT: PASS
MINVOL PAPER-CERTIFICATE RECONCILIATION: PASS
MINVOL UNIVERSAL CONTACT-BOUND BASE-R AUDIT: PASS
MINVOL UNIVERSAL CONTACT-BOUND REPLAY: PASS
MINVOL PAPER BUILD: PASS
MINVOL MARKDOWN PDF BUILD: PASS
MINVOL MARKDOWN/PDF PAIR CHECK: PASS
```

The paper rebuilt to ten pages. Both the 22 committed Markdown/PDF pairs and
the 22 local rebuild pairs passed. The Mac did not run Poppler locally; the
successful hosted document job supplies that required page/font/text preflight.

After all replay and build steps, `git status --short` was empty. The bundle
created from that fresh clone points `refs/heads/main` to the audited candidate
and records complete history.

## 5. Interpretation

This evidence shows that the audited pre-release state is self-contained,
replays from the actual remote on the named author's machine, and passes the
three-job hosted workflow. It also confirms that the public-format history is the intended
five-commit history and that the replay leaves tracked source unchanged.

It does **not** establish external mathematical reproduction, peer review,
novelty, correctness of every conceptual reduction, sharpness, a minimizing
body, or Meissner extremality. The fresh-clone audit was performed by the named
author, and the hosted jobs execute project-supplied programs.

## 6. Tagged-release follow-up

The historical audit above is complete and intentionally retains its `rc1`
filenames and commit identifiers. Publication of `v1.0.0` additionally requires:

1. a green three-job hosted run on the final release commit;
2. an annotated `v1.0.0` tag pointing to that exact commit;
3. a green three-job workflow triggered by the immutable tag;
4. a complete replay from a fresh checkout of the tag with clean final status;
5. deterministic release assets built from the tagged checkout and verified
   against `SHA256SUMS.txt` after download; and
6. explicit named-author approval before changing visibility, publishing the
   GitHub Release, or announcing the result.
