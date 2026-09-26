# MinVol terminal-handoff optimization audit

## Result

This package records a bounded parameter audit of the public MinVol `v1.0.0`
contact-geometric certificate.  It does not introduce a new theorem
architecture.

The audit found a genuine exact improvement.  Split the terminal lower-branch
row `O3B02` at

$$
R_m=\frac{611382837}{10^9}=0.611382837
$$

and retune the tangent radius independently on the two subintervals.  The exact
row bounds become

$$
\begin{aligned}
\mathrm{O3B02A}:&\quad
\frac{131107875849897}{10^{15}}\pi
 =0.411887539597799\ldots,\\
\mathrm{O3B02B}:&\quad
\frac{131105572993743}{10^{15}}\pi
 =0.411880304961823\ldots.
\end{aligned}
$$

Both exceed the unchanged near-Jung branch

$$
0.4118796712148324317327979810\ldots.
$$

Thus the near-Jung branch, rather than the lower radial partition, becomes the
bottleneck.  A conservative presentable theorem coefficient is

$$
\boxed{
\frac{\mathrm{Vol}(K)}{d^3}
\ge
\frac{26221074253\pi}{200000000000}
=0.4118796712122863775432315385\ldots
}
$$

for every three-dimensional convex body of constant width $d$, conditional only
on integrating these two new exact rows into the already released `v1.0.0`
proof package.  Its exact safety margins are:

- gain over public `v1.0.0`: more than
  `0.000002107431984103295052612615315...`;
- unchanged near-Jung branch over the candidate: more than
  `0.000000000002546054189566442454995...`;
- weakest split row over the candidate: more than
  `0.000000633749537026703427624968302...`.

The coefficient is deliberately rounded down far enough to preserve a useful
cross-language numerical audit margin.  The exact unchanged near-Jung rational
lower is slightly larger.

## Bounded search findings

| Test | Exact outcome | Universal consequence |
|---|---:|---|
| Local `s_0` retune, unsplit `O3B02` | `0.411877563780308...` | Only a `6.28e-15` gain; negligible |
| Split `O3B02` into 2 cells | minimum `0.411880304961823...` | Near-Jung becomes bottleneck |
| Split into 3 cells | minimum `0.411881218927344...` | No further universal gain |
| Split into 4 cells | minimum `0.411881675993877...` | No further universal gain |
| Double angular resolution, unsplit | `0.411878272868567...` | Improves v1.0 but remains below near-Jung |
| Double angular resolution, 2 cells | minimum `0.411881014196832...` | No further universal gain |
| Shift `R_*` left by up to `4e-11` | near-Jung value decreases at every tested shift | No handoff improvement |

The unchanged fan can move left only about
`4.3639089872663e-11` before its archived exact margin target is exhausted.
Every tested left shift lowered the near-Jung branch while the retuned split
lower branch stayed above it.  Larger shifts would require changing the fan
proof object and are outside this audit's parameter-only scope.

## Proof authority and audits

- `terminal_handoff_v11_exact.py` is the proof authority for the two promoted
  split rows and the proposed universal comparison.  It regenerates the radial
  chains and checks all accepted steps, adjacent grid extremality,
  cap-disjointness, tangent-gap sums, inherited-row comparisons, pi bounds, and
  the unchanged near-Jung rational lower using integer and rational arithmetic.
- `terminal_handoff_v11_exploration.py` replays the archived bounded search and
  reconstructs the near-Jung branch and left-shift behavior exactly from the
  public `v1.0.0` fan.
- `terminal_handoff_v11_binary64.py` is an independent numerical audit.
- `terminal_handoff_v11_audit.R` is a matching base-R numerical audit.  It was
  prepared but was not executed in the construction environment because
  `Rscript` was unavailable.

The row generator was also regression-tested against the original immutable
`O3B02` arrays: it reproduced all 6,309 positive steps, all 18,562 antipodal
steps, and the exact `v1.0.0` coefficient element-for-element.  The transcript
is archived under `transcripts/reference_generator_validation.txt`.

## Replay

From this directory:

```sh
./run_all.sh
```

The exact proof objects can be regenerated deliberately with:

```sh
python3 terminal_handoff_v11_exact.py --write
```

Normal replay refuses stale or manually divergent JSON or arrays.

## Claim boundary

This package establishes a **proposed exact `v1.1.0` candidate**, not yet a new
public release.  Promotion still requires integration into the public
repository, updated reconstruction and mutation tests, the base-R replay on a
machine with R, checksum/document regeneration, and a green hosted workflow.
The public `v1.0.0` tag and release should remain immutable.
