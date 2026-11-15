# I869-mac: the C² start data of the M = 5 point certificate, assembled a second time

Machine: mac (Apple M5 Mac, 10 cores, macOS 27.0.1), `.venv` of the main checkout (Python 3.13.15, python-flint 0.9.0
with FLINT 3.6.0), one process at nice 10. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/869. Code:
`solver/proof/fixed_point_M_b_check.py cert2` (new) and `fixed_point_M_b.start_data` (its `info` gains the
per-component bounds of η, `e_real` and `e_cauchy`; no bound changes), branch `wip/sa-869` on main 2283596e: the code at
95a4368a, the proposed notes (proof/A_lemmas_M.md §2.5) at e2ff6e17.

`run_i869.sh <python> <this folder> <runs>` ran each line of `exits.txt` from `solver/proof/`: 3 checks exit 0 and
2 mutations exit 3, about 165 s each. Each run's log is `<name>.log`, with one line per pair of the 21.

## What is compared

`certify_M2.start_data2` returns the C² start data of the second-order box run: the values at p̂, the first-derivative
columns V0_k = Dy⁺(ξ₀; p̂)T_k, and for every pair j ≤ k of the six chart coordinates the second-derivative column

    W0_jk = D²Y_N(p(x))[d_j, d_k] + (Cauchy bound of D²η) + Dy⁺(ξ₀; p(x)) Γ_jk    over the box.

`cert2` calls it as `box2_run` does and assembles the same three from the second implementation:

- D²Y_N over the hull: `fixed_point_M_b.formal_series` run on series of length 3 along the directions d_k and along
  d_j + d_k, combined by polarization;
- the Cauchy bound e_q(2ν/(c − hw))², with e_q the second implementation's bound of η on the Cauchy box at p̂ for state
  component q, ν the largest entry of the directions and hw the hull's half-width. The estimate is start_data2's: for
  x in the hull and directions of max norm ν, the bidisc of radius (c − hw)/(2ν) stays in the Cauchy box;
- the Γ term, for the pairs of outer coordinates, from the second implementation's derivatives over the hull.

The chart geometry is the certificate's own: T (`certify_M.T_matrix`), Γ and the directions (`certify_M2.dp_dirs`,
`gam`), the pair list (`certify_M2_lohner.pair_list`) and the four sets (`start_cover_M2.cert_data`).

## Results

| | h = 10⁻⁹ | h = 10⁻¹⁰ (the certificate's run) | h = 10⁻¹¹ |
|---|---|---|---|
| four contractions (p̂, its Cauchy box, the hull, its Cauchy box) | 0.0886, 0.0888, 0.0886, 0.0888 | the same | the same |
| values at p̂ | 19 of 19 overlap, all inside the first's | 19 of 19, all inside | 19 of 19, all inside |
| first-derivative columns V0 | 114 of 114 overlap, all inside | 114 of 114, all inside | 114 of 114, all inside |
| second-derivative columns W0 | 399 of 399 overlap, 21 of 21 pairs | 399 of 399, 21 of 21 pairs | 399 of 399, 21 of 21 pairs |
| largest radius of W0, second against first | 3.86×10⁻⁹ against 2.24×10⁻⁹ | 3.86×10⁻¹⁰ against 2.24×10⁻¹⁰ | 3.86×10⁻¹¹ against 2.24×10⁻¹¹ |
| largest midpoint distance in W0 | 6.8×10⁻¹⁹ | 6.7×10⁻²⁰ | 6.6×10⁻²¹ |
| bound of D²η, second against first | 7.7×10⁻²⁰ against 9.96×10⁻¹⁹ | the same | the same |

The largest entries of W0 are 0.289, in the pairs (1, 4) and (1, 5) (ω/ω∞ with B₅ and C₅). The midpoints of the pairs
without the direction of ω/ω∞ agree to 10⁻⁹⁷. Those with it differ by up to 6.7×10⁻²⁰ at h = 10⁻¹⁰, which is of the
order of the radius squared: the two recursions square the ω ball in different orders. The radii are the variation of
the jets over the hull in ball arithmetic, 1.7 times wider in the second implementation.

**Mutations** (on the h = 10⁻¹⁰ box; each must exit 3, and does).

| mutation | what fires |
|---|---|
| `--mutate=w0`: the second implementation's D²Y_N dropped | the values and V0 still overlap (19 of 19, 114 of 114); 0 of 399 entries of W0 overlap, the midpoints up to 0.289 apart |
| `--mutate=sign`: the sign of [G P] in the second implementation | four contractions hold for the other system; 0 of 19 values, 0 of 114 entries of V0 and 0 of 399 of W0 overlap |

## What this does not show

The comparison is an overlap of enclosures. The box run and the Krawczyk test of Theorem A(M = 5) were made from
`start_data2`'s columns; they were not repeated from the second implementation's, which are 1.7 times wider.

## Recommended tasks

1. **The M = 5 box run from the second implementation's start data.** What: a switch in `certify_M2.box2_run` that
   takes the values, V0 and W0 from `fixed_point_M_b` (the assembly of `cert2`), then the h = 10⁻¹⁰ run (about 40 min)
   and its Krawczyk test on the sub-box. Why: it would make the certificate's start data independent of
   `fixed_point_M.py`, and show whether the 1.7 times wider second-derivative columns still pass. Acceptance: the
   Krawczyk test passes on the same sub-box, and the zero's enclosure overlaps the stored one. Depends on: #869.
