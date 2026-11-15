# I427-mac: a second, independent implementation of the M = 5 start-value contraction, against the stored start set

Machine: mac (Apple M5 Mac, 10 cores, macOS 27.0.1), `.venv` of the main checkout (Python 3.13.15, python-flint 0.9.0
with FLINT 3.6.0), one process at nice 10. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/427. Code:
`solver/proof/fixed_point_M_b.py` (the proof code; it imports python-flint and the standard library only) and
`solver/proof/fixed_point_M_b_check.py` (a harness that imports both implementations), branch `wip/sa-427` (rebased onto main b268b553: the code at e9419653, the proposed notes at 4bea27cf).
All arithmetic is arb/acb ball arithmetic at 512 bits.

`run_i427.sh <python> <root of the raw-data clone>` ran everything from `solver/proof/`, in 94 s. `exits.txt` has each
run's command, its exit status and the status it must have: 18 checks exit 0 and 14 mutations exit 3. Each run's log is
`<name>.log`; the start sets are also stored as JSON (`start_M5*.json`, `start_M3_cert.json`: every ball of the values
and of the derivative columns, as strings).

## What is compared

The stored data are `I38-macm3/lemma6b1_runs_M5_cert/ray.json`, `sets["0"]`: the C¹ start set of lemma 6b₁(5) at
s₀ = 405e^{−3iπ/4} (z₀ = 1/s₀, |ξ₀| = 0.0497 on arg ξ = 3π/8). `lemma6b1_cover_M.start_data_u` made it from
`fixed_point_M.run_M` (diag splitting, r₀ = 0.07, sector 0.2, k = 40) at the centre p̂ (the file's `x`), from
`fixed_point_M.series_jet_M` over X = p̂ ± 10⁻¹⁸, and from Cauchy's estimate over X + 10⁻³(1 + i). The set has 21
complex components, [P_μ, V_μ, 100(C_ν − δ), w, A], and a 21 × 6 block of parameter derivatives.

The second implementation recomputes the 21 values at p̂ and the 126 derivative entries over X from its own series
recursion, residual, majorants, kernel bound, contraction test and jets. It reads from the stored file only the centre
p̂. Each of its balls must overlap the stored one in its real and its imaginary part.

## Results

**The M = 5 contraction** (`start_M5*.log`), N = 105 terms, R = r₀² = 0.0049.

| run | parameters | k | kernel rate a | contraction constant | sup \|η\| at \|z\| = R (p, v, c) | holds |
|---|---|---|---|---|---|---|
| start_M5 | the point p̂ | 103 | 0.35355 (the ray) | 0.1000 | 7.5×10⁻⁷⁵, 1.5×10⁻⁷², 1.5×10⁻⁷⁸ | yes |
| start_M5 | p̂ ± (10⁻¹⁸ + 10⁻³)(1 + i) | 103 | 0.35355 | 0.1002 | 6.9×10⁻¹⁷, 1.4×10⁻¹⁴, 1.3×10⁻²⁰ | yes |
| start_M5_sector | the point p̂ | 103 | 0.18796 (sector 0.2) | 0.1135 | 9.3×10⁻⁷⁵, 1.8×10⁻⁷², 1.6×10⁻⁷⁸ | yes |
| start_M5_sector | the complex box | 103 | 0.18796 | 0.1137 | 8.5×10⁻¹⁷, 1.7×10⁻¹⁴, 1.4×10⁻²⁰ | yes |
| start_M5_k40_sector | the point p̂ | 40 | 0.18796 | 0.2355 | 2.5×10⁻⁷⁴, 1.9×10⁻⁷², 6.4×10⁻⁷⁸ | yes |
| start_M5_k40_sector | the complex box | 40 | 0.18796 | 0.2360 | 2.3×10⁻¹⁶, 1.8×10⁻¹⁴, 5.8×10⁻²⁰ | yes |

The contraction constant is max_i (L w)_i / w_i for the vector w of the test (a rigorous upper bound). The first
implementation's constant for the stored data's configuration (sector 0.2, k = 40, its own weights) is 0.3671.

**The start set against the stored one** (`start_M5.log`; the sector and k = 40 runs give the same verdicts).

- Values: 21 of 21 overlap, and all 21 of the second implementation's balls lie inside the stored ones.
- Derivative columns: 126 of 126 overlap. The second implementation's radii are 1 to 2 times the stored ones (at most
  2.7×10⁻¹⁶ against 1.9×10⁻¹⁶); both are the variation of the jets over X in ball arithmetic.

| component | \|mid − stored mid\| | radius | stored radius |
|---|---|---|---|
| P₋₅ | 6.37×10⁻⁸⁰ | 1.65×10⁻¹⁰⁵ | 1.81×10⁻⁷⁹ |
| P₋₃ | 4.50×10⁻⁷⁹ | 3.98×10⁻¹⁰⁶ | 1.44×10⁻⁷⁸ |
| P₋₁ | 2.25×10⁻⁷⁸ | 5.78×10⁻¹⁰⁷ | 7.94×10⁻⁷⁸ |
| P₊₁ | 2.17×10⁻⁷⁸ | 5.78×10⁻¹⁰⁷ | 7.86×10⁻⁷⁸ |
| P₊₃ | 4.15×10⁻⁷⁹ | 3.98×10⁻¹⁰⁶ | 1.44×10⁻⁷⁸ |
| P₊₅ | 5.67×10⁻⁸⁰ | 1.65×10⁻¹⁰⁵ | 1.87×10⁻⁷⁹ |
| V₋₅ | 3.50×10⁻⁷⁹ | 3.22×10⁻¹⁰³ | 6.63×10⁻⁷⁸ |
| V₋₃ | 1.24×10⁻⁷⁸ | 7.27×10⁻¹⁰⁴ | 3.42×10⁻⁷⁷ |
| V₋₁ | 5.34×10⁻⁷⁸ | 9.32×10⁻¹⁰⁵ | 8.33×10⁻⁷⁷ |
| V₊₁ | 5.03×10⁻⁷⁸ | 9.32×10⁻¹⁰⁵ | 8.08×10⁻⁷⁷ |
| V₊₃ | 1.19×10⁻⁷⁸ | 7.27×10⁻¹⁰⁴ | 3.35×10⁻⁷⁷ |
| V₊₅ | 3.17×10⁻⁷⁹ | 3.22×10⁻¹⁰³ | 6.71×10⁻⁷⁸ |
| 100 C₋₆ | 1.39×10⁻⁷⁹ | 1.45×10⁻¹⁰⁷ | 4.70×10⁻⁷⁹ |
| 100 C₋₄ | 1.35×10⁻⁷⁸ | 1.61×10⁻¹⁰⁷ | 4.10×10⁻⁷⁸ |
| 100 C₋₂ | 1.05×10⁻⁷⁷ | 3.99×10⁻¹⁰⁸ | 2.82×10⁻⁷⁷ |
| 100 (C₀ − 1) | 2.33×10⁻⁷⁷ | 9.89×10⁻¹⁰⁹ | 6.26×10⁻⁷⁷ |
| 100 C₊₂ | 1.00×10⁻⁷⁷ | 3.99×10⁻¹⁰⁸ | 2.81×10⁻⁷⁷ |
| 100 C₊₄ | 1.24×10⁻⁷⁸ | 1.61×10⁻¹⁰⁷ | 3.66×10⁻⁷⁸ |
| 100 C₊₆ | 1.25×10⁻⁷⁹ | 1.45×10⁻¹⁰⁷ | 3.94×10⁻⁷⁹ |
| w | 4.70×10⁻⁷⁷ | 1.02×10⁻¹⁵³ | 1.08×10⁻⁷⁶ |
| A | 8.61×10⁻⁷⁸ | 4.14×10⁻¹⁵⁵ | 8.67×10⁻⁷⁸ |

The stored radii are the rounding of the stored set at 256 bits (`validated_int.PREC`); the first implementation's own
η radius at z₀ is below 2×10⁻⁸³ (its `run_M` rerun at p̂).

**Beyond the issue: two more stored sets** (`start_M5_vs_win2.log`, `start_M3_cert.log`).

| stored set | values overlap | derivative entries overlap | contraction constant (point, complex box) |
|---|---|---|---|
| win2's reproduction of the same set, `I121-win2/lemma6b1_runs_M5_cert/ray.json` (#121) | 21 of 21 | 126 of 126 | 0.1000, 0.1002 |
| the M = 3 certificate's start set at 262e^{−3iπ/4}, `solver/proof/lemma6b1_runs_M3_cert/ray.json` (p̂ ± 1.1×10⁻⁹, r₀ = 0.1, N = 53, k = 51) | 15 of 15 | 60 of 60 | 0.1674, 0.1681 |

With the sign mutation the M = 3 run misses its stored set in all 13 state values and all 52 of their derivative
entries (`start_M3_cert_mut_sign.log`).

**Planted truth and controls** (each ran before the M = 5 start set was looked at).

| check | what must hold | result |
|---|---|---|
| planted_M1, M3, M5 and the three `_edge` runs | the linear problem (no gravity): the enclosure must contain 2F_μ x^α U(α, ½, x), Kummer's U by arb, at z₀ and near the edge of the domain (\|u\| = 204.1, \|z\| = 0.99996 R) | pass; the radius is 3.2 to 3.4 times the true distance at z₀ and 1.05 to 1.16 times at the edge |
| check_m1 | M = 1 with gravity: the 7 enclosures of (D, S, C)(ξ₀) must overlap `fixed_point.py`'s start values | pass; midpoints equal to 6×10⁻⁹⁷, radii 7 to 81 times smaller |
| lip_M1, M3, M5, M5_sector | the two Lipschitz matrices at the first's N, k and ball, with the kernel bound of A_certify.md §4.4: every entry of the second ≤ the first's and ≥ 0.8 of it; the same for the forcing | pass; ratios 0.88–1.00 (M = 1), 0.86–1.00 (M = 3), 0.81–1.00 (M = 5); forcing ratios 0.99995, 0.99985, 0.99998; contraction constants in the first's weights 0.2143 against 0.2145, 0.3354 against 0.3359, 0.25000 against 0.25004, and 0.3668 against 0.3671 on the sector |
| two_M5_60_105, 95_105 | the full M = 5 problem at p̂ with two truncations: the enclosures must overlap at z₀ and at \|z\| = R | pass; the difference uses 0.83 and 0.68 of the summed radii at \|z\| = R, 0.26 and 0.27 at z₀ |

The lowest Lipschitz ratios (0.81) are the entries p ← c and v ← c. The second implementation bounds Q_N from its own
coefficients, the first by \|V_N\| + \|1 + s\|\|P_N\|.

**Mutations** (each must exit 3, and does).

| mutation | what it changes | what fires |
|---|---|---|
| start_M5_mut_radius | r₀ = 0.3 | no contraction: weighted row sums 19.3 (point) and 31.6 (complex box) |
| start_M5_mut_coef | d₅ of harmonic 5 times 1 + 10⁻⁶ | the residual no longer vanishes below its structural orders |
| start_M5_mut_sign | the sign of [G P], in the series, the residual and the jets | the contraction holds (another system), and none of the 19 state values and none of their 114 derivative entries overlaps the stored set (the rows w and A are parameters and still agree) |
| start_M5_mut_scale | [G P] times 1 + 10⁻⁹, likewise | the same: 0 of 19 and 0 of 114 |
| start_M5_mut_rho0 | the start point at \|u\| = 404 | 0 of 19 and 0 of 114 |
| planted_M5_mut_truth | Kummer's α times 1 + 10⁻¹² | the enclosure misses the mutated truth by 2.3×10⁻¹³ |
| planted_M5_mut_coef, radius | as above, in the linear problem | the residual check, and no contraction (row sums 2.49) |
| check_m1_mut_coef, sign, scale | as above, at M = 1 | the residual check; C₀ misses `fixed_point.py`'s by 3.1×10⁻³ and by 1.7×10⁻¹² |
| lip_M5_mut_drop | the second implementation's majorant without the [c̃ W] term of Φ_V | criterion (b): the v rows fall to half of the first's |
| two_M5_60_105_mut_forcing | the N = 60 forcing divided by 1000 | the N = 60 enclosure misses the N = 105 one by a factor 820 |

## What the two implementations share

- The hand-proved formulation of A_certify.md §4.4 and A_lemmas_M.md §2.2: the variables (P, V, C) in z = ξ², the
  diag splitting of the fast row, the integral operator and the component norms. The second implementation re-derives
  them from `inner_np.py`'s equations, but it is the same operator.
- The hand-proved steps that no code checks: the vanishing of the residual below its structural orders (both codes
  only test that the balls contain 0), the identification of the fixed point with y⁺ (Braaksma's theorem), and
  Cauchy's estimate on the complex box.
- The centre p̂, the box half-width 10⁻¹⁸ and the Cauchy radius 10⁻³, read from the stored file and the issue.
- The rule for N (the smallest term at |z| = R among the first 1/(2R) + 30), which gives N = 105 in both.
- python-flint 0.9.0 with FLINT 3.6.0 (arb), on an Apple-silicon Mac in both cases.

Not shared: the series recursion (the first uses `series_arb.SeriesArb`), the residual, the majorants and their
derivative calculus, the kernel bound (∫ ≤ r^{m+2}/(a + (m + 1 + e)r) here), the contraction test (componentwise here,
Perron-weighted there), the weight exponent (k = N − 2 here, 40 there), the jets and the evaluation at z₀.

Of `start_data_u`'s pipeline the second implementation replaces `run_M` at the point and on the Cauchy box,
`series_jet_M`, the evaluation at z₀ and the η discs. It does not replace `lohner_c1`, which turns the values and
columns into the stored Lohner set at 256 bits; the comparison is made after that step, with the stored set.

## Discrepancy with the issue's text

The issue calls the start-value fixed point "the one input of both lemmas' flows". Only lemma 6b₁(5)'s ray starts
from the data at s₀. Lemma 6a(5)'s backward flow (`lemma6_jump_M.py`) starts at ξ₁ = 0.3 from the point certificate's
state box, and the certificate (`certify_M2.py`) takes its own start values from `fixed_point_M.start_data_M` on its
own ray and radius. That third use of the lemma is not covered here (task 1 below).

## Recommended tasks

1. **The point certificate's start data, a second time.** What: run `fixed_point_M_b.py` on the ray, radius and box
   that `certify_M2.py` passes to `fixed_point_M.start_data_M` (#484 states them), and compare with the certificate's
   stored start values and derivatives. It needs a `--start` variant in the (D, S, C) variables at ξ₀ = r₀e^{iθ}, about
   20 lines. Why: lemma 6a(5)'s flow and the Krawczyk test rest on that start data, and no second rigorous code has
   checked it. Acceptance: the contraction holds at the point and on the Cauchy box; every component overlaps the
   stored one; the sign mutation misses it. Depends on: #427, #484.
2. **Write the second implementation into the proof notes.** What: merge the proposed §2.5 of proof/A_lemmas_M.md
   (branch `wip/sa-427`) and name `fixed_point_M_b.py` where the README and PROOF.md list what has a second
   implementation. Why: the notes still say the start-value lemma has one code. Acceptance: `check_numbers.py
   --selftest` passes, and the §2.5 commands run as written from a clean checkout. Depends on: #427.
3. **An independent review of `fixed_point_M_b.py`.** What: a reader who has not seen this work checks the derivation
   in its docstring (the system in z, the diag splitting, the kernel bound ∫ ≤ r^{m+2}/(a + (m + 1 + e)r), the
   componentwise test) and the majorant calculus line by line. Why: AGENTS.md asks for a review of new certificate
   code before its claim is relied on; its author wrote both the code and its checks. Acceptance: a written list of
   findings, each with a mutation or a counterexample where it claims an error. Depends on: #427.
