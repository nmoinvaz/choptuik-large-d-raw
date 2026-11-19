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
