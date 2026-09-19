# Source ledger and dated literature check

**Ledger date:** September 19, 2026
**Scope:** sources used to frame, derive, compare, and document the proposed
universal contact-geometric lower bound

This ledger separates three different roles:

1. **mathematical sources**, which supply published definitions, identities,
   historical results, or predecessor arguments;
2. **project proof objects**, which are the finite exact data and programs that
   carry the proposed theorem in this repository; and
3. **dated literature checking**, which is a targeted search for recent public
   results and bibliographic updates, not a systematic novelty review.

The exact verifier and machine-readable certificate are the proof authority for
this package. A citation records provenance or context; it does not transfer the
burden of checking this repository's new finite certificate to the cited author.

## Core mathematical sources

### Chakerian and Groemer: survey and classical identities

G. D. Chakerian and H. Groemer, “Convex Bodies of Constant Width,” in
*Convexity and Its Applications*, Birkhäuser, 1983, pp. 49–96.

Repository role:

- standard terminology for support functions, widths, volumes, and surface
  areas;
- classical characterizations of constant width;
- the three-dimensional relation between volume and surface area;
- historical context for the Chakerian lower bound and Meissner bodies.

The survey is background authority, not a source for this repository's new
coordinate-width or cap-allocation certificate.

### Chakerian: historical universal lower bound

G. D. Chakerian, “Sets of Constant Width,” *Pacific Journal of Mathematics*
19 (1966), no. 1, 13–21.

Repository role:

- historical universal coefficient
  $\frac{\pi}{3}(3\sqrt6-7)=0.364916122595\ldots$;
- baseline for the long-standing three-dimensional lower-bound problem.

### Harrell: variational structure

E. M. Harrell II, “A Direct Proof of a Theorem of Blaschke and Lebesgue,”
*Journal of Geometric Analysis* 12 (2002), no. 1, 81–88.

Repository role:

- analytical formulation of the constant-width minimization problem;
- extreme-point or “bang-bang” structure in curvature variables;
- explanation of why the higher-dimensional problem requires geometric
  constraints beyond the relaxed scalar curvature problem.

Harrell's paper is conceptual background. The present proof uses a different
contact-geometric finite certificate.

### Kawohl and Weber: Meissner comparison value and problem status

B. Kawohl and C. Weber, “Meissner's Mysterious Bodies,” *The Mathematical
Intelligencer* 33 (2011), no. 3, 94–101.

Repository role:

- construction and historical description of the two Meissner bodies;
- exact explicit-body volume

  $$
  V_M=\frac{\pi}{12}
  \left(8-3\sqrt3\arccos\frac13\right)d^3
  =0.419860045965080\ldots d^3;
  $$

- the distinction between an explicit comparison body and a proved universal
  minimizer;
- Blaschke's identity relating volume and surface area for constant-width
  bodies in three dimensions.

This repository does not claim to prove Meissner extremality.

### Martini, Montejano, and Oliveros: modern reference text

H. Martini, L. Montejano, and D. Oliveros, *Bodies of Constant Width: An
Introduction to Convex Geometry with Applications*, Birkhäuser, 2019.
DOI: `10.1007/978-3-030-03868-7`.

Repository role:

- modern reference for support functions, circumspheres, constant-width
  identities, smooth approximation, mixed volumes, and geometric inequalities;
- terminology and broad literature orientation;
- background for passage from smooth calculations to arbitrary convex bodies.

### Lachand-Robert and Oudet: constant-width characterizations

T. Lachand-Robert and E. Oudet, “Bodies of Constant Width in Arbitrary
Dimension,” *Mathematische Nachrichten* 280 (2007), no. 7, 740–750.
DOI: `10.1002/mana.200510512`.

Repository role:

- reverse-Gauss-map and opposite-point characterizations;
- the spherical-intersection viewpoint;
- dimensional constructions and geometric context for Meissner bodies.

### Nishioka: spectral and support-function predecessor

A. Nishioka, “An Improved Lower Bound for the Three-Dimensional
Blaschke–Lebesgue Problem from Spectral and Dual Perspectives,” *Journal of
Mathematical Analysis and Applications* 566 (2027), no. 1, article 131038.
DOI: `10.1016/j.jmaa.2026.131038`; arXiv:2606.01754.

Repository role:

- exact support-function formulation at the level of the infimum;
- volume-energy identity and support-tensor box constraint;
- spherical-harmonic/Bochner lower bound
  $\mathrm{Vol}(K)\ge 4\pi d^3/33$;
- comparison point for subsequent MinVol results.

Publisher metadata and the final article identifier were checked on September
19, 2026. The volume year is 2027 even though the publisher record and DOI were
available in 2026.

### HYRA: direct contact-geometric predecessor

HYRA, “A Certified Geometric Lower Bound for the Three-Dimensional
Blaschke–Lebesgue Problem,” public artifact in the Tencent Hunyuan
`Hyra-results` repository, manuscript dated August 15, 2026.

Public artifact:
`https://github.com/Tencent-Hunyuan/Hyra-results/tree/main/AI4Science/3d_blaschke_lebesgue`

Repository role:

- minimum-circumsphere contact geometry;
- opposite-point and radial-divergence inequalities;
- tangent-gap recovery on disjoint spherical caps;
- exact-rational certificate architecture;
- predecessor coefficients
  $0.404120778796972\ldots$ analytically and
  $0.411040473721188\ldots$ by finite exact verification.

This project cites HYRA as an external predecessor. The present repository has
fresh Git history, a standalone verifier, a different final coefficient, and a
new dominant-edge coordinate-width handoff. It does not claim authorship of the
HYRA artifact.

### Bogosel: Meissner-polyhedron volume computations

B. Bogosel, “Volume Computation for Meissner Polyhedra and Applications,”
*Discrete & Computational Geometry* 75 (2026), no. 1, 48–72.
DOI: `10.1007/s00454-024-00688-0`.

Repository role:

- current explicit-body and Meissner-polyhedron context;
- comparison between universal lower-bound work and construction/volume work
  for particular bodies.

The publisher page records online publication in 2024 and the final 2026 volume
assignment.

## Project proof authority

The theorem claimed by this draft is not inherited from any one source above.
Its finite proof authority is local to this repository:

```text
certificate/certificates/universal_contact_bound_certificate.json
certificate/certificates/*.npz
certificate/certificates/*.tsv
certificate/certify_universal_bound.py
certificate/exact_geometry.py
```

The proof-object graph, exact arithmetic boundary, and derived artifacts are
specified in
[`certificate/CERTIFICATE_SPECIFICATION.md`](../certificate/CERTIFICATE_SPECIFICATION.md)
and
[`certificate/TRUST_BOUNDARY.md`](../certificate/TRUST_BOUNDARY.md).

The paper-facing constants are generated from the certificate JSON by
`paper/reconcile_certificate.py` and `proof/generate_exact_constants.py`.

## Dated recent-literature check

A targeted web check was performed on **September 19, 2026** using publisher,
arXiv, and official repository records. It checked:

- final bibliographic metadata for Nishioka's article;
- the public HYRA artifact and its stated universal coefficient;
- the final publication record for Bogosel's Meissner-polyhedron article;
- recent arXiv results using the phrases “three-dimensional
  Blaschke–Lebesgue,” “constant width volume lower bound,” “Meissner
  polyhedra,” and close variants.

The check located related 2026 work on extremal-diameter graphs and particular
constant-width constructions, but did not locate a later public claim of a
universal coefficient exceeding the one proposed here.

That statement is intentionally narrow. It is **not** a guarantee of novelty,
priority, completeness, or absence of unpublished work. Search-engine coverage,
indexing delays, terminology differences, and nonpublic manuscripts can all
hide relevant results. Accordingly:

- the paper should avoid an unqualified “best known” claim;
- any precedence statement should be dated and attributed;
- the search should be repeated immediately before public release and again
  before journal submission; and
- external subject-matter reviewers should be asked specifically about
  omitted or competing lower bounds.

## Citation discipline

Public prose should distinguish the following forms of statement:

- **Published fact:** cite the published or official source.
- **Source interpretation:** say that the cited source states or implies it.
- **Project computation:** cite a local proof object, transcript, or verifier.
- **Project inference:** identify it as an inference and state its inputs.
- **Open status:** use dated language and avoid claiming exhaustive knowledge.

No bibliography entry, web-search result, or AI-generated summary is accepted
without human verification against a primary or official record.
