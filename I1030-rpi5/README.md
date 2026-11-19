# I1030-rpi5: P6 route 3's certificates (#990's remainder bound, #1015's head) reproduced on aarch64

Machine: rpi5 (Raspberry Pi 5, aarch64, 4 cores, 8 GB, Linux 6.17.0-1021-raspi), agent claude-me2. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1030 (follows #990, #1015; as #1024 did for P2). Task named by the coordinator by message, 2026-11-19.

Code: main 82f87a33 (contains 4a056a28, the commit the issue names), worktree `~/Source/choptuik-large-d-964`, `solver/proof/`. Python 3.13.7 (venv-choptuik), python-flint 0.9.0, FLINT 3.6.0, mpmath 1.3.0, sympy 1.14.0, numpy 2.5.4, scipy 1.18.1. The Mac's runs used venv-314 (python-flint 0.9.0, FLINT 3.6.0, sympy 1.14.0 per notes/P6_route3.md §10.1). One process at a time, `nice -n 10`.

## Written down before the runs (the issue's pass criteria, verbatim)

- Each run's own verdict passes, and every control (`--mutate=...`) exits 1.
- `route3_bound.py --constants` prints C_(ν−2), C_ν, C_(ν+2) = 28.45, 56.87, 4.77×10⁶, and with `--J0=100` 1.60, 3.17, 3.63×10⁵, as quoted in §10.
- `route3_head.py`: every printed line equals I1015-mac's log of the same command (raw f30c95b0) with timings masked. Use or adapt `I1024-rpi5/compare1024.py`, and keep its control (a changed line must be reported).
- Any difference is reported with its size and left unfixed. Certified bounds built from upper bounds may differ in last digits between machines and still both pass (#111); say whether the conclusion is the same.

Decision it informs: agreement sends route 3's bound to its independent review with two machines' runs behind it; a control that passes, or a bound that fails on aarch64, reopens the certificate before any review.

## Runs (`run1030.sh`, the commands of notes/P6_route3.md §10.6 and §11.6, from `solver/proof/`)

Each log ends with a line `exit N` (as I1015-mac's); `logs/times.txt` has each run's wall seconds. The expected exit is 0 for the verdict runs and 1 for the five controls (plant and psi of the bound, demix of the tuned run, plant and gsmall of the head).

| log | command | expected exit |
|---|---|---|
| route3_bound_lemmas | `route3_bound.py --lemmas` | 0 |
| route3_bound_constants | `route3_bound.py --constants` | 0 |
| route3_bound_constants_J0100 | `route3_bound.py --constants --J0=100` | 0 |
| route3_bound_check | `route3_bound.py --check` | 0 |
| route3_bound_check_plant | `route3_bound.py --check --mutate=plant` | 1 |
| route3_bound_check_psi | `route3_bound.py --check --mutate=psi` | 1 |
| route3_tuned_7_800 | `route3_tuned.py 7 800` | 0 |
| route3_tuned_7_800_demix | `route3_tuned.py 7 800 --mutate=demix` | 1 |
| route3_head_scope | `route3_head.py --scope` | 0 |
| route3_head_lemmas | `route3_head.py --lemmas` | 0 |
| route3_head_check | `route3_head.py --check` | 0 |
| route3_head_check_plant | `route3_head.py --check --mutate=plant` | 1 |
| route3_head_check_gsmall | `route3_head.py --check --mutate=gsmall` | 1 |
| route3_head_certify | `route3_head.py --certify` | 0 |

Estimate: 55 min on the Mac by §10-11's times, so about 3 h here (a guess).

## Result (2026-11-19, run 16:09 to 17:33 UTC, 84 min of wall time; `logs/driver.log`, `logs/times.txt`)

All 14 runs ended with the expected exit (`logs/compare1030.log`: 0 checks differ, 0 missing; its control `logs/compare1030_mutate.log`: all three altered copies reported, exit 1).

| log | exit | verdict | rpi5 wall | Mac (notes' estimate) |
|---|---|---|---|---|
| route3_bound_lemmas | 0 | PASS | 2 s | |
| route3_bound_constants | 0 | PASS | 260 s | 2.5 min |
| route3_bound_constants_J0100 | 0 | PASS | 261 s | |
| route3_bound_check | 0 | PASS | 1073 s | 7.5 min |
| route3_bound_check_plant | 1 | FAIL (control) | 1071 s | |
| route3_bound_check_psi | 1 | FAIL (control) | 1078 s | |
| route3_tuned_7_800 | 0 | PASS | 574 s | 5 min |
| route3_tuned_7_800_demix | 1 | FAIL (control) | 575 s | |
| route3_head_scope | 0 | none printed | 1 s | 3 min |
| route3_head_lemmas | 0 | PASS | 1 s | |
| route3_head_check | 0 | PASS | 40 s | 2 min |
| route3_head_check_plant | 1 | FAIL (control) | 40 s | |
| route3_head_check_gsmall | 1 | FAIL (control) | 40 s | |
| route3_head_certify | 0 | none printed | 24 s | 10 min |

**Criteria**
1. Own verdicts and controls: every verdict run exits 0 and every control exits 1 (the table).
2. Constants: `--constants` prints C_(ν−2), C_ν, C_(ν+2) = 28.4491, 56.8735, 4.76610e+6 (28.45, 56.87, 4.77e6); with `--J0=100` 1.59898, 3.17310, 3.62864e+5 (1.60, 3.17, 3.63e5). Also at §10.2's digits: the seven sups (0.56382 to 2.6323) and their box-centre lower bounds, P 1.63995e+5, W 0.0004728, Cr 27.885 and 55.770.
3. The head: all six `route3_head_*.log` equal I1015-mac's (raw f30c95b0) line by line, and are in fact byte-identical (`cmp`, `exit N` line included). The control (one printed digit of `route3_head_check.log` changed) is reported.
4. Differences: none in any printed number.

**Other numbers against the notes (not criteria, no Mac logs exist for #990's runs):** `--check` worst ratios 1.335e-5, 1.763e-2, 2.682e-2 (§10.3: 1.3e-5, 1.8e-2, 2.7e-2), largest relative radius 6.1e-32 at ν = 21 among the rows shown; planted violation caught in all rows (ratios 3.000, 3.017, 3.014 at ν = 21); the ψ control fails for label ν at ν = 3, 5, 7 first at j = 680, 1135, 1590 (§10.3: the same); the tuned test table equals §10.4's at every printed digit, with the demix control failing all 7 rows, ratios 1.29 to 2.01.

**Things to know**
- The first version of `compare1030.py` required a PASS line before `exit N` in every verdict run, and reported two differences, `route3_head_scope` and `route3_head_certify`. Those two print no verdict line, and neither do I1015-mac's logs (their last line before `exit 0` is a table row). The script now requires only exit 0 for them. The criteria were not changed and no result changed.
- The head runs here took 1 s (scope), 40 s (check, each control) and 24 s (certify), against the notes' "about 3 min", "2 min" and "10 min" (§11.6), while the bound and tuned runs took 1.7 to 2.4 times the notes' estimates (4.3 vs 2.5 min, 17.9 vs 7.5, 9.6 vs 5). The printed output is byte-identical to the Mac's, so the numbers do not depend on it. I did not look for why the estimates differ (they may predate an optimization of the script).
- Bound arithmetic from upper bounds can move in last digits between machines (#111). Here no printed digit moved, so no such case arose.
- What the two machines share: the same scripts (main 82f87a33 here, the Mac's branch wip/p6-route3-head c9876111 for the head), python-flint 0.9.0 and FLINT 3.6.0, sympy 1.14.0 (the exact C_λ). They differ in CPU (Apple M5 vs Cortex-A76), OS, Python (3.13.7 here, venv-314 there) and numpy/scipy (not used by the bound runs; `route3_tuned.py` takes `amp_flint.py`, which uses mpmath 1.3.0).

Conclusion on the criteria: the rerun passes. Route 3's bound has a second machine's runs behind it for the review.
