# I881-mac: Theorem A(5)'s set X_c taken strictly inside the covering's ball X_b

Machine: mac (Apple M5 Mac), `.venv` of the main checkout (Python 3.13.15, python-flint 0.9.0 with FLINT 3.6.0), one
process at nice 10. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/881. Code:
`solver/proof/theorem_A_sets_M.py`, branch `wip/sa-881` on main 1dee59e4. It continues `I871-mac/`. RAW in the logs
is the root of this repository.

X_c is now the decimal box p(X), X = [−9×10⁻¹⁹, 9×10⁻¹⁹]² × [−10⁻²⁶, 10⁻²⁶]² × [−10⁻²⁷, 10⁻²⁷]² in the chart around
p̂. The ball of radii (10⁻¹⁸, 10⁻²⁶, 10⁻²⁷), rounded up, stays the certificate's Krawczyk sub-box and the box of lemma
6a's state set.

| log | run | result |
|---|---|---|
| `sets_M5.log` | `theorem_A_sets_M.py --M=5 --raw=RAW` | HOLD, exit 0 |
| `sets_M5_mut_decimal.log` | `--mutate=decimal`, X_b's radius the decimal 10⁻¹⁸ | HOLD, exit 0, as it must |
| `sets_M5_mut_old.log` | `--mutate=old`, the X_c of #871 with the decimal radius | FAIL at (2) by 4.613×10⁻³⁹ in A, exit 1 |
| `sets_M5_mut_centre.log` | `--mutate=centre` | FAIL at (2), exit 1 |
| `sets_M5_mut_kbox.log` | `--mutate=kbox` | FAIL at (1), exit 1 |
| `sets_M5_mut_six_a.log` | `--mutate=six_a`, X_c wider than the ball | FAIL at (2) and (3), exit 1 |
| `sets_M5_selftest.log` | `--selftest` | PASS, exit 0 |
| `sets_M3.log`, `sets_M3_selftest.log` | `--M=3`, unchanged by this task | HOLD and PASS, exit 0 |

| check at M = 5 | result |
|---|---|
| (0) the Krawczyk test on the ball | K(X) ⊂ int X, relative margins 1.000, 1.000, 0.980, 0.980, 0.932, 0.932 |
| (1) K(X) inside X_c | \|K\| ≤ 6.08×10⁻²⁴ and 4.96×10⁻²⁴ against 9×10⁻¹⁹, slack 9.000×10⁻¹⁹; the inner coordinates as in `I871-mac/` |
| (2) X_c inside X_b | slack 10⁻¹⁹ + 2.193×10⁻²⁷ in A and in ω/ω∞; 6.296×10⁻¹⁹, 9.582×10⁻¹⁹, 9.606×10⁻¹⁹, 9.926×10⁻¹⁹ in B₃, C₃, B₅, C₅ |
| (2) with X_b's decimal radius | slack 10⁻¹⁹ − 4.613×10⁻³⁹ in A and 10⁻¹⁹ − 8.493×10⁻⁴¹ in ω/ω∞: it holds |
| (3) X_c inside the ball | slack 10⁻¹⁹ in the outer coordinates. In the inner ones the half-widths are the ball's own decimals |
