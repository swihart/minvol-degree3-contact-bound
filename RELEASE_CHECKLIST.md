# Release checklist

**Candidate version:** `v1.0.0-rc1`
**Candidate date:** unreleased
**Checklist updated:** September 19, 2026

A checked item means that evidence exists in the current construction
checkpoint. It does not authorize publication by itself.

## A. Mathematical claim

- [x] Exact theorem numerator and denominator are fixed in the authoritative
      certificate.
- [x] Lower and near-Jung circumradius branches cover the full Jung interval.
- [x] `O3B02` is the exact lower-branch bottleneck.
- [x] Near-Jung handoff margin is strictly positive in exact arithmetic.
- [x] Width scaling restores the factor $d^3$.
- [x] Paper states no sharpness, equality, minimizer, or Meissner-extremality
      claim.
- [ ] Independent subject-matter reviewer has checked the mathematical
      reduction.

The unchecked external-review item is not required to label a release as a
non-peer-reviewed research draft, but its absence must remain prominent.

## B. Exact certificate and audits

- [x] Standalone verifier has no private-repository dependency.
- [x] Immutable proof objects have SHA-256 fingerprints.
- [x] Exact certificate reconstructs byte identically.
- [x] Independent binary64 Python audit passes.
- [x] Independent base-R audit passes on the named author's machine.
- [x] Ten reconstruction/regression tests pass.
- [x] Seven adversarial mutations are rejected.
- [x] Export-equivalence record checks ten theorem-critical fields.
- [ ] Complete replay passes from the final release tag on a fresh machine.

## C. Paper

- [x] Lean Paper v1 contains only the proof supporting this coefficient.
- [x] The theorem coefficient and proof-critical constants are generated from
      the certificate.
- [x] Paper/certificate reconciliation passes.
- [x] Reference PDF builds and has been visually inspected page by page.
- [x] Paper limitations and computer-assisted status are explicit.
- [x] Sole author and author order approved: Bruce J. Swihart.
- [x] No institutional affiliation is asserted; correspondence is directed to
      the intended repository issue tracker; no ORCID is asserted.
- [x] Candidate repository URL and version inserted; final release date and any
      archival identifier remain intentionally unassigned.
- [ ] Final PDF approved by every named author.

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
- [x] Clean-source/fresh-extraction record.
- [x] Draft release notes and release checklist.
- [x] Every Markdown source has a checksummed PDF counterpart in the prepared
      overlay.
- [ ] Final copy edit and link review by the named author.

## E. Metadata and legal

- [x] Intended public repository name confirmed:
      `swihart/minvol-degree3-contact-bound`.
- [x] Repository description confirmed.
- [x] Split license selected and `LICENSE` added: CC BY 4.0 for paper/prose and
      MIT for software/build infrastructure.
- [x] `CITATION.cff` added and checked by the metadata preflight.
- [x] Preferred paper citation finalized for the release candidate.
- [x] Candidate version changed to `v1.0.0-rc1`.
- [ ] `RELEASE_DATE` changed from `UNRELEASED` to the approved final date.
- [ ] Candidate version changed from `v1.0.0-rc1` to final tag `v1.0.0`.
- [ ] DOI or archival identifier added only after one exists.
- [x] Copyright and third-party license boundary reviewed and documented.

The unchecked date, final-tag, and archival items cannot be completed before a
successful hosted candidate replay and explicit release approval.

## F. Continuous integration and portability

- [x] Workflow has separate Python, base-R, and document jobs.
- [x] Hosted document job installs Poppler and checks fonts/text/page validity.
- [x] Local Mac without Poppler is documented rather than treated as a theorem
      failure.
- [x] PDF byte identity across platforms is not required.
- [ ] Three hosted jobs are green on the final `main` commit.
- [ ] Three hosted jobs are green on the immutable release tag.
- [ ] Clean tagged-checkout replay is recorded in `CLEAN_CLONE_CHECK.md`.

## G. Release assets

- [ ] Paper PDF asset built from the tagged checkout.
- [ ] Paper-source archive built from the tagged checkout.
- [ ] Standalone certificate archive built from the tagged checkout.
- [ ] Documentation archive built from the tagged checkout.
- [ ] Replay-transcript archive built from the tagged checkout.
- [ ] One release-asset `SHA256SUMS.txt` generated and independently checked.
- [ ] Every downloaded asset reverified in a clean directory.
- [ ] Release notes PDF generated from the final Markdown source.

## H. Public wording and approval

- [x] Draft wording says “computer-assisted” and “not peer reviewed.”
- [x] Draft wording does not say “sharp,” “optimal,” “proved Meissner,” or
      “independently certified.”
- [x] Earlier public spectral repository is clearly separate.
- [x] Private sequel results and history are absent.
- [ ] Named author approves README.
- [ ] Named author approves theorem wording.
- [ ] Named author approves release notes.
- [ ] Named author approves announcement text.
- [ ] Named author explicitly approves creation of the public remote.
- [ ] Named author explicitly approves publication of the GitHub release.

## Release decision

Current decision:

> **DO NOT RELEASE YET.** The mathematical, documentation, authorship,
> citation, and licensing packages are prepared. The public remote, hosted-CI,
> final date/tag, tagged replay, release assets, and explicit publication
> approvals remain open.
