# Status and claim ledger

## ESTABLISHED INSIDE THIS AUDIT

- The existing terminal row generator was reproduced exactly against the
  archived `v1.0.0` `O3B02` arrays and coefficient.
- The new rows `O3B02A` and `O3B02B` are exact rational certificates on a
  gap-free split of the original `O3B02` interval.
- Every unchanged lower-branch row clears the proposed theorem coefficient.
- The unchanged exact near-Jung rational lower clears the proposed theorem
  coefficient.
- The proposed coefficient strictly exceeds the public `v1.0.0` coefficient.
- Two terminal subintervals are sufficient; 3-way, 4-way, and doubled-grid
  variants do not improve the universal minimum at the fixed handoff.
- All tested admissible left shifts of `R_*` lower the near-Jung branch.

## PROPOSED / NOT YET PROMOTED

$$
\mathrm{Vol}(K)
\ge
\frac{26221074253\pi}{200000000000}d^3
=0.4118796712122863775\ldots d^3.
$$

This is a repository-integration candidate for `v1.1.0`.

## NUMERICAL AUDIT

- Python binary64 audit: PASS.
- Matching base-R audit: prepared, not run in the construction environment.

## NOT ESTABLISHED BY THIS PACKAGE

- Public `v1.1.0` release status.
- A stronger theorem than the stated candidate coefficient.
- Equality, sharpness, a minimizing body, or Meissner extremality.
- Any benefit from redesigning the near-Jung fan or changing theorem
  architecture.
