# I866-mac: the point certificates' start data (M = 3 and M = 5) by the second implementation of the start-value lemma

Machine: mac (Apple M5 Mac, 10 cores, macOS 27.0.1), `.venv` of the main checkout (Python 3.13.15, python-flint 0.9.0
with FLINT 3.6.0), one process at nice 10. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/866. Code:
`solver/proof/fixed_point_M_b.py` (new function `start_data`) and `solver/proof/fixed_point_M_b_check.py` (new command
`cert`), branch `wip/sa-866` on main 51dceb1f: the code at d4765610, the proposed notes (proof/A_lemmas_M.md §2.5) at f81cfd66.

`run_i866.sh <python> <this folder>` ran everything from `solver/proof/`, in 297 s. `exits.txt` has each run's
command, its exit status and the status it must have: 2 checks exit 0 and 4 mutations exit 3. Each run's log is
`<name>.log`.

## What is compared

A point certificate calls `fixed_point_M.start_data_M` twice: at its centre p̂, for the start values and their
derivatives, and over the hull of its box, for the derivatives over the box. Each call proves the fixed point on its
real set and on that set's Cauchy box (real parts 10⁻³ beyond it, imaginary parts ±10⁻³). That makes four parameter
sets per certificate. `start_cover_M2.cert_data` (#484) rebuilds them from the stored box file.

The stored box files hold the η bounds of those calls but not the start values, so the first implementation is rerun
here by the certificate's own calls (as `start_cover_M2.py --rerun` does), and the second implementation,
`fixed_point_M_b.start_data`, is run on the same four sets. It gives the state (D, S, C) at ξ₀ = r₀e^{iθ} and its
derivatives in every parameter from its own series, residual, majorants, kernel bound, contraction test and jets.
The pass criteria were written on the issue before the first run.

## Results

| | M = 3, `data/A_M_box_M3_1e-10.json` | M = 5, `data/A_M2_box_M5_1e-10.json` |
|---|---|---|
| start ray, r₀ | arg ξ = 5π/16, 0.0741 | arg ξ = 5π/16, 0.0622 |
| N by the second implementation's rule (the certificate's), k | 95 (95), 93 | 132 (132), 130 |
| contraction constant at p̂, on its Cauchy box, over the hull, on its Cauchy box | 0.0984, 0.0987, 0.0984, 0.0987 | 0.0886, 0.0888, 0.0886, 0.0888 |
| the first implementation's constants (k = 40) on the real and the complex sets | 0.3159, 0.3168 | 0.3095, 0.3102 |
| sup\|η\| at \|z\| = R in (p, v, c): at p̂, over the hull, on the Cauchy boxes | 4.7×10⁻⁶⁵, 1.7×10⁻²⁵, 9.3×10⁻¹⁸ | 1.0×10⁻⁹⁶, 1.3×10⁻³², 4.6×10⁻²⁴ |
| the first implementation's sup\|η\| at p̂ and over the hull | 4.1×10⁻⁶⁴, 1.3×10⁻²⁴ | 8.0×10⁻⁹⁶, 1.0×10⁻³¹ |
| start values at p̂ | 13 of 13 overlap, all inside the first's; midpoints within 2.1×10⁻⁹⁵; radii 2.7×10⁻⁶⁷ against 3.3×10⁻⁶⁶ | 19 of 19 overlap, all inside; midpoints within 3.0×10⁻⁹⁵; radii 4.3×10⁻⁹⁹ against 6.1×10⁻⁹⁵ |
| derivative entries at p̂ | 52 of 52 overlap, all inside; radii 5.5×10⁻¹⁷ against 5.9×10⁻¹⁶ | 114 of 114 overlap, all inside; radii 1.9×10⁻²³ against 2.5×10⁻²² |
| derivative entries over the hull | 52 of 52 overlap; radii 3.2×10⁻¹¹ against 2.5×10⁻¹¹ | 114 of 114 overlap; radii 7.6×10⁻¹¹ against 5.4×10⁻¹¹ |
| values over the hull (not used by the certificates) | 13 of 13 overlap | 19 of 19 overlap |
| second-order jets of Y_N over the hull, 21 directions, orders 0 to 2 (against `certify_M2.series2`) | not applicable (first-order chart) | 1197 of 1197 overlap; radii 3.4×10⁻¹⁰ against 2.0×10⁻¹⁰ |

The radii at p̂ are η's (values) and its Cauchy part (derivatives). Over the hull they are the variation of the jets
over the hull in ball arithmetic, which is why neither implementation's balls lie inside the other's there.

**Mutations** (each must exit 3, and does).

| mutation | M = 3 | M = 5 |
|---|---|---|
| `--mutate=sign` (the sign of [G P] in the series, the residual and the jets) | four contractions hold for the other system (its own N is 94); 0 of 13 values and 0 of 52 + 52 derivative entries overlap, the midpoints 1.3×10⁻² away | four contractions hold; 0 of 19 values and 0 of 114 + 114 derivative entries overlap, the midpoints 7.2×10⁻³ away |
| `--mutate=radius` (r₀ = 0.3) | no contraction on any of the four sets: row sums 18.8 and 20.8 | no contraction: row sums 21.5 and 34.3 |

## What the comparison shares, and what it leaves out

- The sets come from `start_cover_M2.cert_data`, which rebuilds them by the certificate's own expressions. The
  directions of the second-order jets come from the chart helpers `certify_M.T_matrix`, `certify_M2.dp_dirs` and
  `certify_M2_lohner.pair_list`.
- The first implementation's side is a rerun of the certificate's calls, not the certificate's stored balls. The rerun
  reproduces the η bounds that the box files store (4.090×10⁻⁶⁴ and 8.014×10⁻⁹⁶ at p̂).
- The hand-proved steps, as in `I427-mac/README.md`: the formulation, the residual's structural vanishing, the
  identification with y⁺ and Cauchy's estimate.
- Not recomputed: the assembly of `start_data2`'s second-derivative columns (the jets above, the Cauchy bound of D²η
  and the chart's Γ term), and the M = 5 boxes with other outer half-widths (h = 10⁻⁹, 10⁻¹¹).

## Recommended tasks

1. **The second-derivative columns of `start_data2`, assembled a second time.** What: from `fixed_point_M_b.start_data`
   and its jets, rebuild W0cols (D²Y_N over the hull, the Cauchy bound of D²η from sup|η| on the Cauchy box at p̂, and
   the Γ term) and compare with `certify_M2.start_data2`'s, pair by pair. Why: the Krawczyk test of Theorem A(M = 5)
   uses those columns, and this folder compares only their largest input, the jets. Acceptance: every entry of the 21
   pairs overlaps; the mutation `w0` (second derivatives dropped) and the sign mutation miss. Depends on: #866.
2. **The other M = 5 boxes.** What: `fixed_point_M_b_check.py cert --box=…` for the h = 10⁻⁹ and h = 10⁻¹¹ runs that
   proof/A_M2.md §6.5 and §6.6 name. Why: §6.6 states them covered by the first implementation only. Acceptance: as
   here. Depends on: #866.
