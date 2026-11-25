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
