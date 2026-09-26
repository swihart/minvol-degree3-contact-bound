# Internal proof audit for the universal contact-geometric bound

**Audit date:** September 19, 2026
**Status:** internal project audit; not independent subject-matter review

## Audit conclusion

No contradiction was found between the mathematical manuscript, the exact
finite certificate, the machine-readable theorem fields, the independent
binary64 and base-R audits, or the adversarial mutation tests.

The exact package reconstructs the proposed coefficient

$$
\frac{26221074253\pi}{200000000000}
=0.4118796712122863775432315385981549189\ldots
$$

and verifies that both split terminal rows `O3B02A` and `O3B02B` strictly
clear the theorem coefficient. The unchanged near-Jung branch is therefore the
universal bottleneck within the certified gap-free circumradius partition.

This conclusion is limited in four ways:

- the audit was performed inside the same project that produced the proof;
- much of the construction and exposition was AI-assisted;
- it is not a systematic novelty review;
- it does not establish peer review, external reproduction, sharpness, or
  Meissner extremality.

The public status remains:

> Proposed exact universal certificate — standalone internal replay.

## 1. Audit layers

| Layer | Object checked | Method | Result |
|---|---|---|---|
| Exact finite proof | Lower rows, fan, multipliers, determinant transfer, coordinate widths, caps, disjointness, assembly | Python integers and `fractions.Fraction` | Pass |
| Derived authority | Assembled certificate JSON and exact audit tables | Byte-identical reconstruction | Pass |
| Numerical implementation | Full theorem assembly | Independent NumPy binary64 path | Pass |
| Independent language | Archived decimals, cap allocations, and assembly | Base R only | Pass on named author's machine |
| Regression | Reconstruction and public-path invariants | Ten Python unit tests | Pass |
| Adversarial | Seven deliberately corrupted proof objects | Production semantic and byte-identity gates | All rejected |
| Manuscript | Coefficient, split, partition, and main constants | Generated TeX and reconciliation checker | Pass |
| Documentation | Required files, claim language, links, paired PDFs | Release-document and pair checkers | Pass in this checkpoint |

The exact and numerical layers are intentionally separate. Agreement between
them is evidence against implementation error, but only the exact path carries
the finite inequality claims.

## 2. Geometric reduction audit

### A1. Constant width and scaling

The proof normalizes the width to one and restores the factor $d^3$ by dilation.
The support-function identity, diameter-one consequence, and Blaschke volume–
surface relation agree with the standard sources listed in
[`SOURCE_LEDGER.md`](SOURCE_LEDGER.md).

**Status:** source-checked and manuscript-checked.

### A2. Minimum circumsphere and contact balance

The origin is placed at the center of a minimum circumscribed ball. Contact
balance and Carathéodory's theorem reduce the relevant near-Jung regime to four
contact directions. The circumradius range terminates at Jung's value
$\sqrt6/4$.

Audit focus:

- no symmetry assumption is introduced;
- the four-contact conclusion is used only in the stated radius regime;
- the lower and near-Jung intervals meet exactly at
  $R_*=305695601/500000000$.

**Status:** manuscript derivation and exact partition checked.

### A3. Opposite-point and radial inequalities

The opposite-point identity converts constant width into pointwise support and
ball bounds. These feed a divergence inequality and a concave tangent majorant
for the radial function.

Audit focus:

- normal orientation and inequality direction;
- admissible parameter ranges;
- use of regularization when the boundary is not smooth;
- no floating-point quantity is used to certify a row.

**Status:** source comparison, manuscript check, and exact-row replay passed.

## 3. Lower-branch certificate audit

The lower interval is covered by thirteen rows. Four refined cells replace the
formerly weak `O3A1` interval. Their endpoints match exactly and the full table
covers

$$
\left[\frac12,\frac{305695601}{500000000}\right]
$$

without a gap or overlap affecting the argument.

The exact verifier checks each rational step certificate, cap bound,
disjointness condition, and coefficient comparison. It then proves that
`O3B02B` is the weakest lower-branch row, while the near-Jung branch sets the theorem coefficient.

High-risk items checked:

- exact endpoint adjacency;
- angular and radial grid denominators;
- sign conditions before squaring inequalities;
- downward rounding directions;
- coefficient-of-$\pi$ versus decimal-volume columns;
- unique-bottleneck logic.

The first adversarial test changes a lower-row endpoint and is rejected by the
semantic verifier after bypassing only the immutable-file fingerprint.

**Status:** exact replay, independent numerical audit, and mutation rejection
passed.

## 4. Near-Jung fan audit

The final fan contains 98,306 rays, 196,608 triangular faces, 294,912 edges,
and 24,833 distinguished-edge stabilizer orbits. The exact minimum fan margin
is positive and exceeds the package threshold.

High-risk items checked:

- fan-array fingerprints and integer dtypes;
- edge-stabilizer orbit census;
- inherited and revised radial numerators;
- exact S-procedure multipliers;
- active-bound classification;
- strict positivity of every accepted margin.

Two adversarial tests alter a fan radial numerator and an S-procedure
multiplier. Each mutation is rejected by the underlying exact semantic checks,
not merely by a checksum mismatch.

**Status:** exact reconstruction and mutation rejection passed.

## 5. Determinant and coordinate-width audit

The determinant transfer uses the total edge deficiency $S$ and the exact
bound

$$
D(e)\ge 1-\frac S2-\frac{S^2}{2}.
$$

After relabeling a maximum-deficiency edge as `01`, the new analytic handoff
uses

$$
H_{00}\le1+\frac S2,
\qquad
H_{11},H_{22}\le1+\frac S6,
$$

and positive definiteness to infer reciprocal coordinate-width lower bounds.

Audit focus:

- the relabeling is exhaustive rather than a symmetry assumption;
- the dominant-edge inequality applies to the selected maximum edge;
- the two nondominant axes use the weaker but valid $S/6$ diagonal estimate;
- the inverse-diagonal inequality
  $(H^{-1})_{jj}\ge 1/H_{jj}$ has the correct direction;
- the coordinate factors are combined with the same core geometry used in the
  certificate.

The exact JSON, binary64 audit, paper-generated constants, and human-readable
appendix agree on all three coordinate-width lower bounds.

**Status:** algebraically reviewed and exact-code checked. This is a priority
for independent mathematical review because it is the main analytic step that
separates the proposed coefficient from the predecessor certificate.

## 6. Cap allocation and disjointness audit

Three positive/negative coordinate-axis pairs are optimized separately. Their
exact lower bounds sum to

```text
0.0001439609020552581838284512468198759823427280084172919
```

The six open cap interiors are pairwise disjoint by exact transformed-ellipsoid
inequalities. The smallest stored strict gap is positive.

High-risk items checked:

- cap bracket orientation;
- section-hull vertex order and exact polygon area;
- cap-pair summation;
- strict versus non-strict disjointness statements;
- no cap contribution is counted twice;
- the cap total is added to, rather than substituted for, the forced core.

Four mutation tests alter a section-hull vertex, cap bracket, disjointness
threshold, and final theorem digit. The full reconstruction gate rejects every
case.

**Status:** exact replay and mutation rejection passed.

## 7. Universal assembly audit

The exact near-Jung branch gives

```text
0.4118796712148324317327979810531508741628745212952960018
```

and exceeds the upper enclosure of the lower-branch bottleneck by

```text
0.0000021074345301574846190550703110031602996750911392740
```

Therefore both split terminal rows clear the displayed coefficient across the lower branch, while the near-Jung certificate supplies the universal bottleneck across the two
closed intervals. The proof restores $d^3$ by scaling.

Audit focus:

- strict handoff direction;
- use of an upper enclosure for the bottleneck in the comparison;
- exact endpoint coverage;
- no interpolation across an uncertified radius interval;
- exact numerator and denominator in every public location.

**Status:** byte-identical certificate reconstruction, exact arithmetic,
binary64 audit, base-R audit, and paper reconciliation agree.

## 8. Portability and release repairs

The following nonmathematical defects or risks were found and addressed during
public-package construction:

- private parent-package imports were flattened into a standalone public tree;
- private branch names, commit hashes, and unrelated unreleased research material were removed;
- a seven-case mutation suite was added to ensure that proof-object corruption
  is detected;
- theorem-critical manuscript constants were moved to generated TeX includes;
- an early paper table with visual overlap was redesigned before packaging;
- the first generated exact-constants PDF used tables too wide for the page;
  the generator was changed to vertical row records, large exact fractions are
  identified by certificate field, and every lower-row volume decimal is now
  recomputed uniformly from its exact coefficient and the certificate's exact
  rational lower bound for $\pi$;
- PDF byte identity across platforms was explicitly separated from
  mathematical validity;
- the local Mac's missing Poppler tools were documented, with full font/text
  preflight delegated to the hosted Ubuntu document job;
- Markdown/PDF one-to-one pairing and checksums were automated.

No repair silently changed the theorem. A future change to the authoritative
certificate requires a new version and explicit coefficient comparison.

## 9. Literature and precedence audit

The source ledger was checked against official publisher, arXiv, and public
repository records on September 26, 2026. That targeted search did not locate a
later public universal coefficient exceeding the proposed one. This is not a
systematic novelty review and should not be reported as one.

The targeted search was repeated on September 26, 2026, immediately before
release. Independent experts should still be asked specifically about:

- unpublished or recently accepted universal lower bounds;
- alternate contact-geometric certificates;
- changes to the final bibliographic status of recent papers;
- precedence for the dominant-edge coordinate-width lemma.

## 10. Priority questions for external reviewers

1. Does the minimum-circumsphere reduction cover every nonsmooth constant-width
   body after the stated regularization?
2. Are all sign and monotonicity hypotheses in the lower-row propagation
   certificates stated strongly enough in the manuscript?
3. Is the dominant-edge coordinate-width lemma valid under every allowed
   contact labeling, including ties?
4. Does the determinant transfer use exactly the Gram normalization declared in
   the paper and JSON?
5. Do the transformed section hulls and cap-disjointness inequalities exclude
   all cross-axis overlaps?
6. Is the exact handoff comparison made against the correct enclosure of the
   lower bottleneck?
7. Are any recent universal bounds or relevant predecessor lemmas missing from
   the source ledger?

## 11. Current scientific boundary

The audit supports releasing the package, after the remaining metadata and
hosted-CI gates, as an **AI-assisted, non-peer-reviewed computer-assisted
research draft seeking independent mathematical verification**.

It does not support describing the result as independently certified, accepted,
sharp, or a solution of the Meissner conjecture.
