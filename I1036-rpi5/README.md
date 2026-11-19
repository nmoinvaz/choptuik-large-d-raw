# I1036-rpi5: #1010's c2 = -lambda_1 (the l = 2 mode in the M-harmonic truncation) reproduced on aarch64

Machine: rpi5 (Raspberry Pi 5, aarch64, 4 cores, 8 GB, Linux 6.17.0-1021-raspi), agent claude-me2. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1036 (follows #1010; as #1024 and #1030 did for P2 and route 3). Task named by the coordinator by message, 2026-11-19. The Mac's logs: `I1010-mac/` of this repository (525f445f).

Code: main 2df76651 (the commit the issue names), a fresh worktree `~/Source/cl-1036`, `solver/inner_pert/`. Python 3.13.7 (venv-choptuik), numpy 2.5.4, scipy 1.18.1, mpmath 1.3.0, sympy 1.14.0. The Mac's runs: venv-314 (sympy 1.14.0), `wip/l2-c2-calc` cafa2971 for the p = q runs (I1010-mac/README.md). One process at a time, `nice -n 10`. The c2 runs read the stored zeros `data/first_order_hier_M{1,3,5}_xi0.2.json` and write their result JSONs to `data/` of the worktree, where main tracks the Mac's `l2_c2_*.json`; the rpi5 JSONs are copied to `json/` here and compared leaf by leaf with the tracked ones (an extra check, not a criterion).

## Written down before the runs (the issue's pass criteria, verbatim)

- Each command exits as §10 says. `l2_c2.py --checks` exits 1 by design (its control's check 3, §9.3), and every `--mutate` run exits as listed.
- Every printed number equals the same command's log in I1010-mac with timings masked. Adapt `I1030-rpi5/compare1030.py`, and keep its control (a changed line must be reported).
- Any difference is reported with its size and left unfixed. Say whether c2's sign and the c2 = -lambda_1 relation hold at M = 1, 3 and 5.

Decision it informs: agreement sends #1010 to its independent review with two machines' runs behind it; a difference in a verdict reopens #1010 before any review.

## Runs (`run1036.sh`: every command of notes/L2_MODE.md §10, as written, in its order, from `solver/inner_pert/`)

Each log ends with a line `exit N` (as I1010-mac's); `logs/times.txt` has each run's wall seconds. Expected exits from §10: 0 for every line except `--checks` (1, by design), the three `--checks --mutate=` runs (1: the mutation's check fails), and `l2_c2.py 5 --forcing=l0,sym --mutate=gsign` (1: "BAD").

| log | command | expected exit | Mac log in I1010-mac |
|---|---|---|---|
| l2_mode_flat | `l2_mode.py --flat` | 0 | none |
| l2_mode_check | `l2_mode.py --check` | 0 | none |
| l2_mode_check_curv | `l2_mode.py --check --mutate=curv` | 1 | none |
| l2_mode_first_order | `l2_mode.py --first-order` | 0 | none |
| l2_mode_first_order_print | `l2_mode.py --first-order --print` | 0 | none |
| l2_c2_forcing | `l2_c2_forcing.py` | 0 | l2_c2_forcing.log |
| l2_c2_forcing_p1 | `l2_c2_forcing.py --p1` | 0 | l2_c2_forcing_p1.log |
| l2_c2_checks_main | `l2_c2.py --checks` | 1 | l2_c2_checks_main.log (and the first section of l2_c2_checks.log) |
| l2_c2_checks_ident | `l2_c2.py --checks --mutate=ident` | 1 | section of l2_c2_checks.log |
| l2_c2_checks_series | `l2_c2.py --checks --mutate=series` | 1 | section of l2_c2_checks.log |
| l2_c2_checks_force | `l2_c2.py --checks --mutate=force` | 1 | section of l2_c2_checks.log |
| l2_c2_M1_planted | `l2_c2.py 1 --planted-lam` | 0 | l2_c2_M1_planted.log |
| l2_c2_M{1,3,5} | `l2_c2.py M --forcing=l2,l2_ctrl,l0,sym --lamcheck` | 0 | l2_c2_M{1,3,5}.log |
| l2_c2_M{1,3,5}_G | `l2_c2.py M --forcing=l2,l0,G,sym --lamcheck` | 0 | l2_c2_M{1,3,5}_G.log |
| l2_c2_M5_mutate_gsign | `l2_c2.py 5 --forcing=l0,sym --mutate=gsign` | 1 | l2_c2_M5_mutate_gsign.log |
| l2_c2_summary | `l2_c2_summary.py` | 0 | l2_c2_summary.log |

The five `l2_mode.py` commands have no log in I1010-mac (they belong to #1001's and earlier work), so for them only the exit is a criterion. Estimate: 45 to 60 min on the Mac, so about 2 to 3 h here (a guess).

## Result (2026-11-19 17:39 to 20:22 UTC, 2 h 43 min wall; one process at a time at nice 10; main 2df76651, no file of the code edited)

Verdict on the issue's criteria (`python3 compare1036.py <raw checkout> --wt=<code worktree>`, log `logs/compare1036.log`; its control
`--mutate` reports 3 of 3 altered copies, `logs/compare1036_mutate.log`; the sizes of the differences are `numdiff1036.py`,
`logs/numdiff1036.log`, control `logs/numdiff1036_mutate.log`):

| criterion | verdict | number |
|---|---|---|
| every command exits as §10 says (and prints the verdict line) | met | 20 of 20: the 4 `--checks` runs and `--mutate=curv` exit 1 with FAIL, the gsign run exits 1 (BAD), the other 14 exit 0 with PASS |
| every printed number equals the same command's log in I1010-mac, timings masked | not met | 2 of 12 logs equal line by line (`l2_c2_forcing`, `l2_c2_forcing_p1`), 0 of the 4 sections of `l2_c2_checks.log`; the others differ, sizes below |
| control: a changed line is reported | met | `compare1036.py --mutate`: 3 of 3 (a digit of c2 in l2_c2_M1.log, a digit of l2_c2_summary.log, the exit line of l2_c2_checks_main.log) |
| c2 < 0 at M = 1, 3, 5 | holds | -7.9591, -2.4825, -3.0458 (the Mac's, to the printed digits) |
| c2 = -lambda_1 | as the Mac's | c2 + lambda_1 (l0) = -0.1496, +0.0216, -0.0016 (1.92%, 0.86%, 0.05% of lambda_1); the Mac's -0.1496, +0.0216, -0.0016; its slice-spread ranges and the summary's PASS the same |

### Sizes of the differences (left as they are)

1. **Numbers that are equal.** c2, c2_ctrl, lambda_1 (l0), lambda_1 (SymForce) at M = 1 and M = 3 equal the Mac's at all six printed digits (the `_G` logs too, with G = c2 + lambda_1 = -0.149648, +0.021617), and so do `l2_c2_forcing`, `l2_c2_forcing_p1` and the planted lambda* of M = 1 to the printed 10 digits (its iterations differ from the 9th digit on, e.g. `lam it 2` 1.804689528 against 1.804689534, and its g by 1e-6 relative).
2. **M = 5.** c2 -3.045765 against the Mac's -3.045841 (relative 2.5e-5), c2_ctrl -25.562085 against -25.562628 (2.1e-5), lambda_1 l0 3.044200 against 3.044279 (2.6e-5), SymForce 3.041506 against 3.041583 (2.5e-5); c2 + lambda_1 -0.001565 against -0.001562. The `_G` run: c2 -3.045820 against -3.045839 (6.2e-6), G -0.001562 against -0.001561. The gsign run: lambda_1 l0 -3.044284 against -3.044257 (8.9e-6). The summary table differs only in the fourth decimal of the M = 5 row's range (-3.0474 to -3.0437 against -3.0475 to -3.0438), lambda_1 (3.0442 against 3.0443) and SymForce (3.0415 against 3.0416), in its mode-jump column (M = 1 5.1e-11 against 5.0e-11, M = 3 4.2e-11 against 4.6e-11, M = 5 3.1e-07 against 8.2e-07, all under the bar 1e-5), and in the planted-lambda_1 line (3.0442 against 3.0443, both 0.39%, bar 1%). The two M = 5 runs of this folder (`l2_c2_M5` and `_G`, the same background zero) differ by 1.8e-5 in c2 and the Mac's two by 2e-6.
3. **Where the M = 5 difference starts.** The background zero's Sch matrix: entries differ by at most 1.6e-11 (M = 1), 1.3e-10 (M = 3), 1.1e-6 (M = 5); its smaller singular value by 1.7e-11, 1.5e-8, 4.3e-4 (the larger by 0, 5e-11, 2.1e-7); the last deflation residual r_H is 1.4e-9 against 1.1e-9 at M = 3 and 4.8e-5 against 4.0e-5 at M = 5. The M = 5 zero is solved to that tolerance, so a different build lands at a different point inside it (a reading, not tested: I did not vary the stopping tolerance). The ranges of the slices (e1, e2, f2) are +-6e-4 at M = 5, 25 times the 2.5e-5.
4. **Noise diagnostics.** The corrected jump of d_s Z0 (printed against |Sch| |f2|, bar 1e-5): M = 1 5.41e-05 against 5.24e-05 (3.1%), M = 3 3.55e-04 against 3.86e-04, `_G` 1.57e-04 against 3.47e-04, M = 5 2.31 against 6.11 (`_G` 3.89 against 9.15, gsign 2.91 against 8.54), at |Sch| |f2| 1.05e6, 8.43e6, 7.50e6, so 5e-11, 4e-11 and 3e-7 to 8e-7 of the scale. The deflation residuals by iteration differ by up to a factor 6 at M >= 3 (M = 3: 2.8e-04 against 4.4e-05) (M = 5: 4.1e+03, 3.9e+01, 4.5e+01 against 2.0e+03, 4.6e+01, 3.5e+01), and the `--checks` residuals by up to 3x at 1e-12 to 1e-15 (series y 1.7e-15 against 1.8e-15, rhs 6.8e-13 against 4.7e-13, dropped 4.5e-14 against 6.7e-14, the control's 2.2e-10 against 1.7e-10 at the bar 1e-10); every "(as required)" and "NOT AS REQUIRED" tag is the same as the Mac's.
5. **Text that differs, from the code, not the machine (checked in git, not by a rerun).** I1010-mac's `l2_c2_M{1,3,5}.log` were made with `l2_c2.py` as of 4a391a20 or an earlier working copy of the Mac: they print `F_lambda forcing ...: relative difference 1.46e-01` and `wrote .../l2_c2_M1_xi0.2.json`, and main prints `raw difference 1.46e-01; after the local field's homogeneous part 9.83e-02; ell projections differ by 5.58e-02` and `wrote .../l2_c2_M1_xi0.2_l2-l2_ctrl-l0-sym.json` (both changed by 3de4637e: at 4a391a20 the line and the file name are the Mac's). Its `_G` and summary logs have the later printing (the same `wrote` name as mine). Main also prints the two planted-lambda_1 lines of M = 5 (e75ba9fa), which no Mac log of M = 5 has, and the radius diagnostic of `--checks` (f2626f7d), which the Mac's `l2_c2_checks.log` sections predate (its `l2_c2_checks_main.log` has it). `git diff 4a391a20 e75ba9fa -- l2_c2.py` changes only printing, the diagnostics, the file names, G in the check loop and the planted bar: the solve is not touched. Hence `l2_c2_M{1,3,5}` differ from the Mac's in 2 to 4 lines of text plus the numbers above.
6. **One verdict differs from the Mac's log.** `l2_c2_M5_mutate_gsign`: the Mac's log ends `PASS`, `exit 0` (no bar existed); mine prints `planted lambda_1 (M = 5), l0: -3.0443 against 3.0324, 200.39%: BAD (bar 1%)`, `FAIL`, `exit 1`, which is what §10 lists. Both logs show lambda_1 flipped to -3.044, as the mutation intends. The bar and the exit code are e75ba9fa's, after the Mac's log.
7. **Result JSONs against the tracked ones** (`json/`, leaf by leaf, extra): `l2_c2_forcing_p1.json` identical, `l2_c2_forcing.json` differs only in two description strings, `planted_lam` in lam by 2.0e-12; the others differ in 28 to 45 numeric leaves (largest relative 6.8e-3 to 3.3e-1 at M = 1, up to 1.0 at M = 3 and 5, in quantities that are noise or near zero: `mode_jump`, `deflation_hist`, `gk`, the control's `lamcheck`) and the control JSONs' `corr_l2_lam`, absent from the tracked ones. The headline leaves (`ell`, `c2`) follow items 1 and 2.

### Times (rpi5, wall seconds; the Mac's last stage in brackets where its log has one)

`l2_mode.py --first-order` 1551 s and `--print` 1568 s (about 2.2x the Mac's estimate), `l2_c2_forcing.py` 1003 s, the `--checks` runs 386 to 391 s each, M = 1 97 s (20 s), M = 3 693 s (165 s), M = 5 1802 s (446 s), `_G` 39, 279 and 699 s (Mac M3_G 62 s, M5_G 164 s), gsign 286 s, summary 0 s; all in `logs/times.txt`. About 4 to 5 times the Mac's.

### Recommended tasks (for the coordinator; not opened by me)

1. **Regenerate I1010-mac's `l2_c2_M{1,3,5}.log` and the gsign log at main's `l2_c2.py`** (Mac, about 15 min), so the logs match §10's code. Accept when each log's text equals mine except numbers.
2. **M = 5's cross-machine scatter.** Run `l2_c2.py 5 --forcing=l2,l2_ctrl,l0,sym --lamcheck` three times on the Mac (7 min each) with the same stopping tolerance, then once with the background zero's tolerance tightened until Sch(2) at M = 5 stops moving in its 7th digit. Accept when the scatter of c2 is under 3e-5 relative or its cause is named. Depends on #1036.
