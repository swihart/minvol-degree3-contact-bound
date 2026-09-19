# AI assistance and provenance

**Repository status:** public-release construction checkpoint
**Current named author:** Bruce J. Swihart
**Primary AI system used:** OpenAI ChatGPT (GPT-5.6 Sol Pro)
**Primary access period:** August-September 2026

## Scope of AI assistance

OpenAI ChatGPT was used extensively during this project to:

- read and compare the supplied literature on bodies of constant width;
- discuss candidate proof strategies and failure modes;
- derive, reorganize, and check mathematical calculations;
- write and execute exact-rational Python verifiers;
- prepare an independently organized binary64 Python audit;
- prepare a matching base-R audit;
- design adversarial mutation tests;
- flatten the private proof dependency closure into a standalone public-format
  certificate;
- draft and revise the paper, Markdown documentation, build scripts, and
  continuous-integration workflow;
- inspect rendered manuscript and documentation PDFs; and
- organize claim boundaries, release gates, and reproducibility records.

The AI system is not listed as an author and is not represented as an
independent reviewer. Its mathematical, computational, bibliographic, and
expository output can be wrong. Every AI-proposed artifact intended for the
repository is subject to deterministic checks and human review.

## Human contribution and responsibility

Bruce J. Swihart selected the research problem and project goals, supplied and
reviewed the source materials, chose which proposed directions to pursue, ran
the independent base-R checks locally, maintained the private and fresh-history
repositories, reviewed the manuscript and supporting documents, and decides
whether and when a version is made public.

The named author is responsible for:

- the mathematical claims and their wording;
- the accuracy of the provenance and verification record;
- the final author list, affiliations, acknowledgments, and license;
- preserving corrections and superseded versions;
- not presenting the work as peer reviewed or independently verified before
  such review occurs; and
- ensuring that no private research history or unrelated private work is
  exposed in the public repository.

## Relationship to the HYRA predecessor

The direct contact-geometric predecessor used by this project is the public
HYRA artifact titled *A Certified Geometric Lower Bound for the
Three-Dimensional Blaschke-Lebesgue Problem*. It is treated as an external
source and cited as such. This repository does not claim authorship of that
artifact. The current package develops and independently restructures its
contact-geometric route, adds a new coordinate-width handoff, and provides a
separate fresh-history verifier and release record.

## Verification boundary

The repository contains several layers:

1. exact integer and rational verification of the finite certificate;
2. immutable machine-readable proof objects with SHA-256 fingerprints;
3. independent binary64 Python and base-R audits;
4. reconstruction, regression, and adversarial mutation tests;
5. automatic reconciliation of paper-facing constants against the certificate;
6. reproducible paper and documentation builds; and
7. human-readable derivations and claim ledgers.

These layers improve traceability and make discrepancies easier to detect.
They do not turn an AI-assisted draft into an independently reviewed theorem.
The current designation is:

> AI-assisted, non-peer-reviewed computer-assisted research draft seeking
> independent mathematical verification.

## AI output that is not proof authority

No natural-language answer from an AI system is a proof object. In particular,
the following are not theorem authority:

- chat transcripts;
- hidden model reasoning;
- prose summaries of calculations;
- model confidence statements;
- web-search summaries;
- floating-point candidate searches; and
- AI-generated bibliography entries that have not been checked against primary
  sources.

The finite proof authority is described in
[`certificate/TRUST_BOUNDARY.md`](certificate/TRUST_BOUNDARY.md).

## Model-identification note

The model designation records the hosted system used during this phase of the
project. Hosted systems can change over time, and their behavior is not
reproducible merely from a model name. The designation and access period are
included for provenance, not as a claim that future model outputs will match
those used here.

## Disclosure in the paper and release

Before release, the paper and repository metadata should include a concise AI
assistance disclosure consistent with this document. Any later material change
in the role of AI systems should be recorded in a new version rather than
silently rewriting the history of the released package.
