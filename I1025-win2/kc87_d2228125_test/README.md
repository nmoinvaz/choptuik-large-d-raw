# I1025-win2/kc87_d2228125_test: registered zero-versus-pole test at lambda -0.1990, -0.1985, -0.1965 (macm3's k_c 87 part b2 state at D 22.28125)

Machine win2 (Windows 11, 20 logical CPUs, 95.5 GB RAM; runner win2 claude-me2, Sonnet 5.5). Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1025. Written 2026-11-25 10:27 UTC, **before the three points are evaluated** (the driver `kc87_testscan.sh`, the checker `predict_check.py` with its selftest, and the dry run, which stops before the scan, are here).

## Order (coordinator t5, hc, 25 Nov ~10:30 UTC), verbatim
"good report; both readings stand as reported. Decide it with a test registered now: lambda -0.1990, -0.1985 and -0.1965 on the 3 free threads. Prediction from your zero fit (lc -0.1976, background slope -79.6, q -3.1), written in the README before the start: ln|det| at each point = the fit's background + ln|l - lc| within 0.05;
a pole predicts the opposite sign of that term (a rise of about the same size). Pass for 'zero' when all three are within 0.05 of the zero model and the sign changes between -0.1985 and -0.1965; 'pole' when they follow the pole model; else undecided. No refit before reading."

## The registered prediction (fixed here, before any of the three points exists)
The fit (`../kc87_d2228125_fine/fit_zero_pole.py`, `fit_zero_pole_output.txt`; hybrid ln|det| at -0.20, -0.19, -0.18, -0.17, -0.16, -0.12, -0.08 of D 22.28125, k_c 87): best lc = **-0.1976** (grid 1e-4), a = -2397.4451203178, s = -79.6113350583, q = -3.0581771034, background B(l) = a + s (l + 0.18) + q (l + 0.18)^2; rms residual 0.0012.
Zero model: ln|det|(l) = B(l) + ln|l - lc|. Pole model: ln|det|(l) = B(l) - ln|l - lc|.

| lambda | background B | ln|l - lc| | zero model | pole model |
|---|---|---|---|---|
| -0.1990 | -2395.9336 | -6.5713 | **-2402.5049** | -2389.3623 |
| -0.1985 | -2395.9734 | -7.0131 | **-2402.9865** | -2388.9602 |
| -0.1965 | -2396.1324 | -6.8124 | **-2402.9448** | -2389.3199 |

The two models differ by about 13 at each point. Predicted hybrid signs for a zero (and for a pole at the same place): - at -0.1990, - at -0.1985, + at -0.1965 (the sign change between -0.1985 and -0.1965, at lc = -0.1976).
**Classification, PRIMARY (the order's)**: `zero` if all three hybrid ln|det| are within 0.05 of the zero model and the signs are -, -, +; `pole` if all three are within 0.05 of the pole model (the signs are printed; no sign condition is added); else `undecided`. `predict_check.py` computes it from the scan rows; no refit comes before the reading.
**Classification, SECONDARY (mine, registered with the primary, with a reason)**: the primary's 0.05 is below the prediction's own uncertainty: lc sits on a 1e-4 grid, and the zero model moves by 714, 1111 and 909 per unit lc at the three points (0.07, 0.11 and 0.09 per 1e-4), the fit allows lc in [-0.1977, -0.1975] at rms <= 0.02 and in [-0.1979, -0.1973] at rms <= 0.05, i.e. the model predicts each value only to about +-0.1 to +-0.2. So a real zero may land outside 0.05 and read `undecided`. The secondary says which model the values are near: `zero-like` if all three are within 0.5 of the zero model, each at least 5 from the pole model, and the signs are -, -, +; `pole-like` if all three are within 0.5 of the pole model and each at least 5 from the zero model; else `neither`. Reported beside the primary, never instead of it.
Reading of the result, stated now: primary `zero` = the order's pass for a zero; primary `pole` = the order's pass for a pole; primary `undecided` with secondary `zero-like` or `pole-like` = a decision only in the sense of the secondary and reported as that; anything else is undecided. After the reading (not before), the values are refit for the record and a new lc is reported.
Not covered: a root pair or a feature narrower than 0.0005 near lc; lambda printed by `read_lower.py` to three decimals (-0.1985 shows as -0.198 or -0.199: the keys and the scan files carry four decimals).

## Inputs (pinned; the driver refuses any other)
As `../kc87_d2228125_low/README.md`: macm3's part b2 k_c 87 state at D 22.28125 (raw `I1025-macm3/kc87_leg2/b2/sol_l1kc87Lmacm3b2_D22.281250.npy`, blob 3ce8bc2e) and its record row (sha1 0eb8d22e), the k_c 87 check (6df5d960, must accept; controls 1 1) and the k_c 95 check (d487e628, must refuse), `d18_hybsign.py` e089207a, `read_lower.py` 89309d3c, `d185_scan_read.py` 7c9d400f, `d18c_read.py` 1383470f, `repeat_check.py` aaf598a9, `pair2025.py` e692c61d. Code: worktree `D:/choptuik-i1025k79` at 48c36355, python 3.14 with multidouble 5.1.0 (`venv-md510`).

## Commands (`kc87_testscan.sh`, one driver started through `cim_start.ps1`)
1. Pins and selftests (read_lower with its two mutations, repeat_check, pair, kc95 and kc87 checks, fetch, `predict_check.py --selftest` 0 and `--mutate` 1); the source fetched, state blob and row hash pinned, the k_c 87 check accepts (controls 1 1), the k_c 95 check refuses (dry run first).
2. Scan, now (the D 22.5 wide scan's last evaluation runs beside it): three processes of one thread, caps 28800 s by the exact root pids: P1 -0.1990 | P2 -0.1985 | P3 -0.1965 (no repeat is ordered).
3. Reading: `predict_check.py` (the primary and secondary classification and the table of values against both models), `read_lower.py` over -0.1990 to -0.1965, then `joint/` with the three previous scans over -0.50 to 0.10 and the ln|det| table.

## Acceptance (fixed before the run)
Source accepted with controls 1 1 and the k_c 95 check refusing it (dry run); every scan process prints "the record system"; the classification is the one `predict_check.py` prints, whatever it is; the values, the table and the refit are reported in full. A pin that differs, a selftest or control that does not read as written, or a scan process that fails stops the lane and I report it.

## Status
- 2026-11-25 10:27 UTC: README (the registered prediction) and `predict_check.py` (selftest 0; `--mutate` 1) written; the driver is dry-run next, then started.
- 2026-11-25 10:29 UTC: dry run passed (`dry_stdout.txt`, `exits_testscan.txt`, `selftest_exits.txt` = 0 1 1 0 0 1 0 0 0 1 0 1): pins and selftests, macm3's state fetched (blob 3ce8bc2e, row hash 0eb8d22e) and accepted (controls 1 1), the k_c 95 check refuses. The driver starts next.
- 2026-11-25 10:29 UTC: the scan started by itself (the driver run through `cim_start.ps1`): three processes, root pids 40532, 37032, 29660, caps 28800 s (18:29 UTC at the latest); about 1900 s per evaluation: the three points ~11:01 UTC.
- 2026-11-25 10:54 UTC: scan done (three processes exit 0 in 1465 to 1489 s; the third round of nothing else running but the wide scan's last evaluation). Every process printed the record system (|F| 3.8875e-10 against the record's 3.8769e-10, steps 2865 = 2865).

## Result (D 22.28125, k_c 87, macm3's part b2 state; `read_lower.txt`, `joint/`, `summary_testscan.txt`)
`predict_check.py` (registered before the scan; selftest 0, mutation 1):

| lambda | hybrid sign | hybrid ln|det| | zero model (registered) | difference | pole model (registered) | difference |
|---|---|---|---|---|---|---|
| -0.1990 | - | -2402.5099 | -2402.5049 | -0.0050 | -2389.3623 | -13.1476 |
| -0.1985 | - | -2402.9950 | -2402.9865 | -0.0085 | -2388.9602 | -14.0348 |
| -0.1965 | + | -2402.9352 | -2402.9448 | +0.0096 | -2389.3199 | -13.6152 |

**PRIMARY (the order's, tolerance 0.05): `zero`** (all three within 0.01 of the zero model, signs -, -, +: the sign changes between -0.1985 and -0.1965). **SECONDARY (registered with it): `zero-like`.** Not noise-robust: none. **Flag: the float64 sign differs from the hybrid sign at -0.1965** (float64 -1, hybrid +1; float64 ln|det| -2401.6045 against the hybrid -2402.9352, a difference of 1.33; at -0.1990 and -0.1985 the signs agree and the ln|det| differ by 1.45 and 1.20): the plain float64 determinant has lost its precision beside the zero, the double-double block carries the sign there. The hybrid is the quantity read throughout.
`read_lower.py` on these three points (it prints lambda to three decimals, so -0.1990 and -0.1985 show as -0.199 and -0.1965 as -0.197): one robust change `- to +` in (-0.1985, -0.1965), det-linear -0.197530, range [-0.197613, -0.197530] (a spread over estimator choices, not an enclosure). The joint reading with the low, neg and fine scans (`joint/read_lower_joint.txt`, 23 distinct lambdas, -0.50 to 0.10): the same single change, sign - below it and + above it, no other change. `joint/ln_table.txt` prints lambda to three decimals (merging -0.1990 and -0.1985); `joint/ln_table4.txt` (written by `refit_after.py`) has four.
Refit AFTER the reading (`refit_after.py`, `refit_after_output.txt`; the same model functions as `../kc87_d2228125_fine/fit_zero_pole.py`; the ten hybrid values -0.20, -0.1990, -0.1985, -0.1965, -0.19, -0.18, -0.17, -0.16, -0.12, -0.08; lc on a 1e-5 grid): **zero: best lc -0.19761, rms residual 0.00045** (a -2397.4448, s -79.68, q -2.4; the first fit had -2397.4451, -79.61, -3.06 and lc -0.1976); **pole: rms 1.00** (best lc -0.19752, residuals up to 1.4); zero rms <= 0.01 for lc in [-0.19762, -0.19759], <= 0.03 for [-0.19767, -0.19755]. The registered prediction (lc -0.1976) held to 1e-5 in lc and 0.01 in ln|det| at three points that lie 0.0003 to 0.0014 from the root; the model-class comparison (zero 0.00045 against pole 1.0 on ten points, with planted controls) and the registered test agree.
**Reading for the report: branch S at D 22.28125 (k_c 87) is a simple zero of det M(lambda) at lambda_S = -0.1976 (fit; det-linear -0.19753), a `- to +` sign change (- below it, + above it), not a pole.** Its motion since D 22.25 (0.108387, macm3's det-linear): -9.8 per unit D. Not settled by this scan: whether S's zero is the continuation of the root macm3 reads at 0.108 at D 22.25 (the sign pattern, the orientation and the ln|det| profile say it is; no point at D 22.265625 exists to follow it).
