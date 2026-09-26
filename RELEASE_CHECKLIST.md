# Release checklist

**Release version:** `v1.1.0`<br>
**Release date:** September 26, 2026<br>
**Checklist updated:** September 26, 2026<br>
**Audited pre-release commit:** `892d4bc6fad07950e78da66e45b95063a6415af6`<br>
**Audited hosted workflow:** <https://github.com/swihart/minvol-degree3-contact-bound/actions/runs/35468019663>

A checked item means that evidence exists in the current construction
checkpoint. It does not authorize publication by itself.

## A. Mathematical claim

- [x] Exact theorem numerator and denominator are fixed in the authoritative
      certificate.
- [x] Lower and near-Jung circumradius branches cover the full Jung interval.
- [x] `O3B02A/O3B02B` are exact terminal rows and both clear the theorem coefficient; the near-Jung branch is the universal bottleneck.
- [x] Near-Jung handoff margin is strictly positive in exact arithmetic.
- [x] Width scaling restores the factor $d^3$.
- [x] Paper states no sharpness, equality, minimizer, or Meissner-extremality
      claim.
- [ ] Independent subject-matter reviewer has checked the mathematical
      reduction.

The unchecked external-review item is not required to label the release as a
non-peer-reviewed research preprint, but its absence must remain prominent.

## B. Exact certificate and audits

- [x] Standalone verifier has no private-repository dependency.
- [x] Immutable proof objects have SHA-256 fingerprints.
- [x] Exact certificate reconstructs byte identically.
- [x] Independent binary64 Python audit passes.
- [x] Independent base-R audit passes on the named author's machine.
- [x] Independent base-R audit passes in hosted R 4.6.1.
- [x] Ten reconstruction/regression tests pass.
- [x] Seven adversarial mutations are rejected.
- [x] Export-equivalence record checks ten theorem-critical fields.
- [x] Complete replay passes from a fresh clone of the staging remote at
      commit `892d4bc6fad07950e78da66e45b95063a6415af6`.
- [ ] Complete replay passes from a fresh checkout of the immutable `v1.1.0`
      tag.

## C. Paper

- [x] Focused Paper v1 contains only the proof supporting this coefficient.
- [x] The theorem coefficient and proof-critical constants are generated from
      the certificate.
- [x] Paper/certificate reconciliation passes.
- [x] Reference PDF builds and has been visually inspected page by page during
      construction.
- [x] Table 3 row spacing was repaired and approved by the named author.
- [x] Paper limitations and computer-assisted status are explicit.
- [x] Sole author and author order approved: Bruce J. Swihart.
- [x] No institutional affiliation is asserted; correspondence is directed to
      the repository issue tracker; no ORCID is asserted.
- [x] Version, date, canonical repository, and versioned release URL inserted.
- [ ] Final ten-page PDF approved in full by the named author for publication.

## D. Documentation

- [x] Reproducibility guide.
- [x] Verification-status page.
- [x] Trust-boundary document.
- [x] Claims-and-limitations document.
- [x] Certificate specification.
- [x] Independent-audit record.
- [x] Mathematical overview.
- [x] Claim-dependency graph.
- [x] Proof ledger and internal proof audit.
- [x] Source ledger with dated literature check.
- [x] Exact-constants appendix generated from the certificate.
- [x] Certificate-architecture appendix.
- [x] Replay-transcript appendix.
- [x] AI-assistance and provenance disclosure.
- [x] Clean-source, hosted, and fresh-clone record.
- [x] Release notes and release checklist.
- [x] Every Markdown source has a checksummed PDF counterpart.
- [x] Remote evidence is indexed in
      `certificate/evidence/rc1_remote_audit.json`.
- [x] GitHub README math syntax uses supported `$$` and `\mathrm` forms.
- [x] Named author approved the README after hosted rendering repair.
- [ ] Final release notes and link review approved by the named author.

## E. Metadata and legal

- [x] Repository name confirmed:
      `swihart/minvol-degree3-contact-bound`.
- [x] Repository description confirmed.
- [x] Split license selected and `LICENSE` added: CC BY 4.0 for paper/prose and
      MIT for software/build infrastructure.
- [x] `CITATION.cff` added and checked by the metadata preflight.
- [x] Preferred paper citation finalized for version `v1.1.0`.
- [x] `RELEASE_DATE` is `2026-09-26`.
- [x] `VERSION` is `v1.1.0`.
- [ ] DOI or archival identifier added only after one exists.
- [x] Copyright and third-party license boundary reviewed and documented.

The unchecked DOI item is informational; no DOI is required for the initial
GitHub release, and none is implied.

## F. Continuous integration and portability

- [x] Workflow has separate Python, base-R, and document jobs.
- [x] Hosted document job installs Poppler and checks fonts, text, and page
      validity.
- [x] Local Mac without Poppler is documented rather than treated as a theorem
      failure.
- [x] PDF byte identity across platforms is not required.
- [x] Three hosted jobs are green on audited pre-release commit
      `892d4bc6fad07950e78da66e45b95063a6415af6`.
- [x] The successful pre-release run is recorded at
      <https://github.com/swihart/minvol-degree3-contact-bound/actions/runs/35468019663>.
- [x] A fresh clone of that commit completed the Python and base-R replay,
      rebuilt the paper and 22 documentation PDFs, and ended clean.
- [x] Three hosted jobs are green on the rendering-repair/evidence commit, as
      reported by the named author.
- [ ] Three hosted jobs are green on the final release commit.
- [ ] Three hosted jobs are green on the immutable `v1.1.0` tag.
- [ ] Clean tagged-checkout replay is completed and archived.

## G. Release assets

- [x] Deterministic release-asset builder and verifier are included.
- [x] Preview paper PDF asset builds and verifies.
- [x] Preview paper-source archive builds and verifies.
- [x] Preview standalone certificate archive builds and verifies.
- [x] Preview documentation archive builds and verifies.
- [x] Preview replay-transcript archive builds and verifies.
- [x] Preview release record and one asset `SHA256SUMS.txt` build and verify.
- [x] Release notes PDF is generated from the final Markdown source.
- [ ] All assets are rebuilt from the exact `v1.1.0` tagged checkout.
- [ ] Every downloaded tagged asset is reverified in a clean directory.

## H. Public wording and approval

- [x] Wording says "computer-assisted" and "not peer reviewed."
- [x] Wording does not say "sharp," "optimal," "proved Meissner," or
      "independently certified."
- [x] [Earlier public MinVol spectral repository](https://github.com/swihart/minvol-degree3-spectral-bound) is clearly separate.
- [x] Unreleased research results and private history are absent.
- [x] Named author approved creation and use of the private staging remote.
- [x] Named author approves the README.
- [x] Named author approves the theorem wording as displayed in the README.
- [ ] Named author approves the final PDF in full.
- [ ] Named author approves the final release notes.
- [ ] Named author approves the announcement text.
- [ ] Named author explicitly approves changing repository visibility to
      public.
- [ ] Named author explicitly approves creation of the GitHub Release.

## Release decision

Current decision:

> **PREPARED FOR THE FINAL TAG GATE - DO NOT PUBLISH YET.** Version/date
> metadata, final README rendering, Table 3 spacing, exact verification,
> documentation, release tooling, and pre-release reproducibility evidence are
> prepared. Publication still requires green final-commit and tag workflows, a
> clean tagged replay, tagged-asset verification, final PDF/release-note/
> announcement approval, and explicit approval of the visibility change and
> GitHub Release.
