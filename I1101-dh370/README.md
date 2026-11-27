# I1101-dh370: does re-solving the accepted k_c 127 D 23.0 state at the same k_c and kappa move the root lambda_1? Four evaluations at lambda 0.045 and 0.050 on two states

Machine `dh370-fedora` (Fedora, i7-8700, 6 cores / 12 threads, 31 GB), session claude-me2. Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1101 (depends on #1025). Coordinator t5. Written 2026-11-27 01:59 UTC by the clock, before any run of this folder (the pins, the worktree, the scripts and a planted test of `results.py` came first; no evaluation has run).

## Order (t5's hc, 2026-11-27 01:57 UTC), verbatim
"Next task, a #1101 follow-up. R0 showed that re-solving the accepted k_c 127 D 23.0 state at the same k_c and kappa moves Delta by 4.2e-7 at the same |F|. Measure whether it moves the root lambda_1 too. States, from raw: (A) winb's original I1025-win/kc127_d23/sol_l1kc127wind23_D23.0000.npy (blob 7a1b150c, record eea03461); (B) win2's re-solve I1101-win2/R0/sol_l1kc127k070w2_D23.0000.npy (blob 90d3e655, record d1a3a641). Run d18_secant.py scan (92b9bf53, eb1396ad, your scan worktree) on each state at lambda 0.045 and 0.050, which bracket the root (winb's scan: + at 0.04, - at 0.05). That is 4 evaluations, 2 processes, nice 19 beside D 5555, 1 thread each, --pin per state. Report per state: signs, ln|det| and dln at both lambda, and the det-linear root from the two points. The difference of the two states' det-linear roots is the root's solve scatter (the estimator's bias cancels to first order). Also give |Delta_B - Delta_A| from the records. Bars, written before the start into a new folder I1101-dh370/README.md: the four points noise-robust; the scatter reported as measured. Read it against the k_c steps of the root (+0.0055 at 111 to 119 at D 23.0): below 1e-4 means the thresholds are unaffected; above 1e-3 means they need a tighter solve. Push the README first and the records at the end, and post the table on #1101. ETA about 2.5-3 h."

## Inputs (raw origin/main a58b0324a at 01:57 UTC; copies in `inputs/A` and `inputs/B`; the driver refuses any other blob)
| state | what | raw path | state blob | record blob |
|---|---|---|---|---|
| A | winb's accepted k_c 127 at D 23.0, kappa 0.7 | I1025-win/kc127_d23/ (`sol_l1kc127wind23_D23.0000.npy`, `l1kc127wind23.jsonl`) | **7a1b150c** | **eea03461** |
| B | win2's R0 re-solve of A at the same k_c 127 and kappa 0.7 | I1101-win2/R0/ (`sol_l1kc127k070w2_D23.0000.npy`, `l1kc127k070w2.jsonl`) | **90d3e655** | **d1a3a641** |
| | records: A: |F| 3.1939646372e-10, 4179 steps, psi-constraint 1.463841e-03, Delta 1.174322923415951; B: |F| 3.1949266444e-10, 4179 steps, psi-constraint 1.463819e-03, Delta 1.1743225027439044 (F_start 3.198e-10: a re-solve from A) | | | |
Scanner: `solver/matter/d18_secant.py` of wip/ell1-speed at **92b9bf53**, blob **eb1396ad**, my worktree `~/Source/choptuik-large-d-1025v` (the k_c 119 and 127 scans' and secant's); reader `read_lower.py` 89309d3c and its change finder 7c9d400f (`in/`); python `~/Source/choptuik-large-d-1058b/.venv` (3.14.10, multidouble avx2). **|Delta_B - Delta_A| from the records: 4.2067e-07** (4.206720465e-07).

## Commands (`run_1101.sh`, unit `i1101a` under systemd-inhibit; `steps.txt`; stops at the first failure, `STOP.txt`)
1. Pins (the four input blobs, the worktree and `d18_secant.py`, the reader); selftests: `d18_secant.py selftest` exit 0 and its three mutations `half`, `norobust`, `nosigncheck` exit 1 each; `read_lower.py selftest` exit 0 and its mutations `shift`, `round2` exit 1 each. All logged.
2. Scan, one process per state (so each loads its state once): `d18_secant.py scan RECORD STATE 23.0 0.045,0.050 scan_<X>/scan_D23.0_p0.jsonl --pin=<state blob>,<record blob>` in the worktree, **2 processes, 1 thread each (OMP, OPENBLAS, MKL, VECLIB, RAYON = 1), nice 19** (the yield rule's level: D 5555 runs beside), under `/usr/bin/time -v`. The evaluations are the secant tool's: fast float64 blocks 0-11, double-double block 12, the 1e-15 noise test with two seeds, dln = the largest change of ln|det| under it; **robust** = both noise signs equal the hybrid sign **and** dln <= 0.1.
3. Reading: `read_lower.py` on each state's two points (window 0.045 to 0.050): its det-linear estimate and range; and `results.py` (`results.md`): the table, the det-linear root of each state from its two points by the straight line through f = sign * exp(ln|det| - ref) (the reader's definition; planted test: two planted roots 0.0462 and 0.0467 are recovered exactly, scatter +5.000e-04), **root_B - root_A**, and |Delta_B - Delta_A|. If a state's two hybrid signs are equal there is no root between its points and I report that as measured (nothing widened).

## Bars (t5's; written before the start)
- **The four points noise-robust** (all four robust in the sense above). If one is not, I report it and read the scatter only from what is robust, saying so.
- **The scatter is reported as measured:** |root_B - root_A|, from the two det-linear roots (the estimator's bias cancels to first order). Read against the k_c steps of the root at D 23.0 (+0.0341, +0.0178, +0.0091, +0.0055; the last one 111 to 119): **below 1e-4: the thresholds are unaffected by the solve; above 1e-3: they need a tighter solve**; between 1e-4 and 1e-3: not decided by t5's two statements; I report it as such and give the ratio to the last k_c step (0.0055) and to the next one (about 0.003, t5's registered step for 119 to 127).
- The comparison is of two states of the same discretization (same k_c, kappa, steps 4179): it measures the solve's scatter, not the truncation in k_c, kappa or the steps (that is the other runs of #1101).

## Predictions (mine; information, not pass rules)
- The hybrid signs are + at 0.045 and - at 0.050 for both states (t5: the points bracket the root; winb's scan had + at 0.04 and - at 0.05): 80% (a state with equal signs: the root of that state is outside (0.045, 0.050), 15%).
- All four evaluations robust: 85% (dln near this root grew from 1e-5 at 0.01 away to 0.3 within 1e-5 of it at k_c 127, D 22.875; 0.045 and 0.050 are probably about 1e-3 from the root).
- Scatter |root_B - root_A|: below 1e-4: 30%; between 1e-4 and 1e-3: 50%; above 1e-3: 20%. Basis, rough: the Delta change per k_c step at 119 to 127 (-2.05e-6) went with a root step of about +0.003 (t5's registration), a ratio of about -1.5e3 root per unit of Delta; the re-solve moved Delta by 4.2e-7, which at that sensitivity is about 6e-4; but the sensitivity to a solve error need not equal that to a k_c step.
- Each evaluation about 4500 to 6500 s on one process at nice 19 beside D 5555; the two processes take 2 evaluations each: **2.5 to 3.5 h** (t5's ETA 2.5 to 3 h).
- |Delta_B - Delta_A| = 4.2067e-07 is read from the records and needs no prediction.

## Status
- 2026-11-27 01:59 UTC: folder, inputs, scripts, pins and bars written before any evaluation; the unit `i1101a` starts next.

## Result (27 Nov 01:59:42 to 05:45:17 UTC = 13535 s = 3.76 h; unit `i1101a`; 2 processes, 1 thread each, nice 19; `results.md`, `read_lower_A.txt`, `read_lower_B.txt`, `scan_A/`, `scan_B/`)
Both processes printed the pin check and the record system (A: |F| 3.1987864632e-10 against the record's 3.1939646372e-10; B: 3.1911792672e-10 against 3.1949266444e-10; 4179 steps each) and exited 0; the selftest exits (secant 0 1 1 1, reader 0 1 1) are in `steps.txt`; peak RSS 4.46 GiB (A: 4674432 kB) and 4.28 GiB (B: 4488060 kB).
| state | lambda | hybrid sign | noise-robust | robust (dln <= 0.1) | dln | float64 sign | ln of abs det | seconds |
|---|---|---|---|---|---|---|---|---|
| A | 0.045 | + | True | True | 1.30e-05 | + | -3902.3590984513 | 7186 |
| A | 0.050 | - | True | True | 2.52e-06 | - | -3901.1429061235 | 6305 |
| B | 0.045 | + | True | True | 1.54e-05 | - | -3902.5303054577 | 6818 |
| B | 0.050 | - | True | True | 2.50e-06 | - | -3901.1035170558 | 6678 |
- **The four points are noise-robust and robust** (the first bar: met). Both states have the hybrid sign + at 0.045 and - at 0.050, so the points bracket a root in each. The float64 sign differs from the hybrid at B's 0.045 only (not used).
- **Det-linear root from the two points** (my formula in `results.py`, equal to the reader's, 0.046143 and 0.045968): **A 0.046143036**, **B 0.045967998**. **Root scatter root_B - root_A = -1.750e-04** (|.| 1.75e-04).
- **|Delta_B - Delta_A| from the records = 4.2067e-07** (Delta_A 1.174322923415951, Delta_B 1.1743225027439044; B is the lower, by the same sign as the root).
- **Read against t5's bars:** below 1e-4: no; above 1e-3: no; **between 1e-4 and 1e-3, which t5's two statements do not decide.** As numbers: the scatter is 3.2% of the last k_c step of the root (+0.0055 at 111 to 119 at D 23.0) and 5.8% of the next step as registered (+0.003 at 119 to 127). The ratio of the root's scatter to Delta's is +416 per unit of Delta; the k_c step 119 to 127 carried a Delta change of -2.05e-6 with a root step of about +0.003 (t5's registered value for it; the measured one is not at hand here), a ratio of about -1.5e3 of the opposite sign: arithmetic on those numbers, which does not say whether the two are related.
- **Caveats:** the root of each state is the det-linear value of two points 0.005 apart (a crude estimator: winb's scan at this D gave + at 0.04 and - at 0.05, det-linear 0.048098, and t5 registered the root at 0.0444 +- 0.003, so the two-point values 0.0461 and 0.0460 are probably above the true root; I did not measure the bias); it cancels to first order in the difference, not exactly. One re-solve (B) of one state (A): this is one measurement of the scatter, not a distribution.

### Predictions scorecard (mine, registered before the run)
| prediction | result |
|---|---|
| hybrid signs + at 0.045 and - at 0.050 for both states (80%) | right |
| all four evaluations robust (85%) | right (dln 2.5e-06 to 1.5e-05) |
| scatter below 1e-4 (30%); between 1e-4 and 1e-3 (50%); above 1e-3 (20%) | the middle one: 1.75e-04 |
| 2.5 to 3.5 h (t5's ETA 2.5 to 3 h) | WRONG: 3.76 h (each evaluation 6305 to 7186 s on one process at nice 19, against my 4500 to 6500 s) |

## Status
- 2026-11-27 05:45 UTC: done. The scatter is 1.75e-04 (between t5's 1e-4 and 1e-3); records pushed; the table is posted on #1101.

# R1 (kappa 0.5) on dh370: the order of the step error, from the root

Machine `dh370-fedora`, session claude-me2, coordinator t5. Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1101, comment 7212257601 (R1 on dh370; its bars below, verbatim) and 7211909730 (R2's root scan, which goes to dh170). Written 2026-11-27 07:25 UTC by the clock (the stamp first pushed, 07:26, was a guess), **before R1 starts**: this README section went to raw as e3364429 and R1 started at 07:25:36 (`R1/steps.txt`). Files: `R1/` (script `run_R1.sh`, unit `i1101r1`, `R1/steps.txt`).

## Order (t5's hc, 2026-11-27 ~07:19 UTC, the task part, verbatim)
"1. R1: in your scan worktree ~/Source/choptuik-large-d-1025v (92b9bf53; check ell_refine.py blob 631e5801 and dss_ell.py 5d28c19e), with winb's k_c 127 state and record (raw I1025-win/kc127_d23/, blobs 7a1b150c and eea03461) copied into solver/matter/data/ under their own names and blob-checked, from solver/matter: python ell_refine.py l1kc127wind23 127 l1kc127k050dh370 127 1 23.0 2.0992182200 --kappa 0.5 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma. Python ~/Source/choptuik-large-d-1058b/.venv. 6 threads (OMP, OPENBLAS, MKL, RAYON = 6) beside D 5555's unit i1088a-d5555b (never touch it), nice 10, a systemd user unit, cap 57600 s on the exact pid, no retry. Pilot: when it prints its steps, they must be 5851 +- 2% (5734-5968); otherwise stop it and report.
2. When R1 ends: bar 1 (|F| <= 5e-10, steps in range), its record, log and state into I1101-dh370/R1/ and pushed.
3. Root scan of R1's state with your #1102 build: worktree ~/Source/choptuik-large-d-1102 (d4b6b6ce), PYTHONPATH=~/Source/ellrs-site-1102, d18_secant.py scan --b12=rust --b12_threads=1 at lambda 0.045, 0.050, 0.060, 0.070, 4 processes, 1 thread each, nice 10, --pin of R1's state and record blobs, with the reader and robustness test of your I1101-dh370 scatter run.
4. Reading per comment 7212257601: delta_1 = root(R1) - 0.045967998 from the bracketing pair; with delta_2 from dh170's R2 scan when it is posted, r = delta_1/(delta_2 - delta_1) and its bar (kappa^4 predicts 3.74; [3.0, 4.6] confirms). Report delta_1 at once even if delta_2 is not in yet.
Raw: a new section in I1101-dh370/README.md with these bars, written and pushed before R1 starts. No code changes. Report to me when R1 starts (with its steps), when it ends, and when the scan ends; post on #1101 at each."

## Bars (comment 7212257601, verbatim; written by t5 before the run)
> **Bars, written before the run.**
> 1. R1 converges: |F| ≤ 5e-10, steps 5851 ± 2% (5734–5968).
> 2. Δ_R1 is reported beside Δ_R0 = 1.174322502744 and Δ_R2. r for Δ is formed only if |Δ_R1 − Δ_R2| ≥ 2e-6.
> 3. δ₁ = root(R1) − root(B) and δ₂ = root(R2) − root(B), with root(B) = 0.045967998 (`I1101-dh370/`), each from the
>    bracketing pair (the 0.045/0.050 pair if it brackets).
> 4. If |δ₂| ≥ 3e-3 (R2's bar: the step error is real): r = δ₁/(δ₂ − δ₁). κ⁴ predicts 3.74. r in [3.0, 4.6] (about 3σ
>    at the scatter) confirms κ⁴; outside it, the measured order p, from (0.7ᵖ − 0.5ᵖ)/(0.5ᵖ − 0.35ᵖ) = r, is reported.
> 5. If |δ₂| ≤ 1e-3, |δ₁| ≤ 1e-3 is expected, and a larger δ₁ is a discrepancy to report.
> 

The bars are t5's; mine are the gates and predictions below.

## Inputs and pins (all blob-checked; `R1/inputs/` holds copies, the worktree's `solver/matter/data/` the same files)
| what | blob | where |
|---|---|---|
| winb's k_c 127 D 23.0 state (kappa 0.7, 4179 steps, Delta 1.174322923415951) | **7a1b150c** | `inputs/A/` = raw `I1025-win/kc127_d23/sol_l1kc127wind23_D23.0000.npy` (the copy made for the scatter run) |
| its record | **eea03461** | `inputs/A/l1kc127wind23.jsonl` |
| scan worktree `~/Source/choptuik-large-d-1025v` | **92b9bf53**; `ell_refine.py` **631e5801**, `dss_ell.py` **5d28c19e** | R1 (`ell_refine.py`) |
| Rust worktree `~/Source/choptuik-large-d-1102` (wip/ell1-rust-b12, bd424726 is an ancestor) | **d4b6b6ce**; `d18_secant.py` **9706e506**, `ell_b12rs.py` **a1fff74f**, `ellrs/build.sh` **e6254c9b**; the build `~/Source/ellrs-site-1102` (`ellrs avx2`) | the scan |
| reader and its change finder | `in/read_lower.py` **89309d3c**, `in/d185_scan_read.py` **7c9d400f** | the scatter run's (this folder) |
| state B's root, the reference | root(B) = **0.045967998** (this README, the scatter run; det-linear from B's (0.045, 0.050) pair) | |
Python `~/Source/choptuik-large-d-1058b/.venv` (3.14.10, multidouble 5.1.0 avx2). R1's own output names (`sol_l1kc127k050dh370_D23.0000.npy`, `l1kc127k050dh370.jsonl`) did not exist before the start.

## Commands (`R1/run_R1.sh`, unit `i1101r1` under systemd-inhibit; each step stamped in `R1/steps.txt`; stops at the first failure with `R1/STOP.txt`)
1. R1, from `solver/matter` of the scan worktree: `nice -n 10 /usr/bin/time -v timeout -k 120 57600 python -u ell_refine.py l1kc127wind23 127 l1kc127k050dh370 127 1 23.0 2.0992182200 --kappa 0.5 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma > R1/R1.log`, `OMP/OPENBLAS/MKL/RAYON_NUM_THREADS=6`. `timeout` signals its child, the python pid; no retry.
2. When it exits: copy record, state and log into `R1/`; bar 1 by `R1/gate_R1.py` (D 23.0, k_c 127, kappa 0.5, |F| <= 5e-10, steps 5734 to 5968); push the folder to raw (`push_1101.sh`) **whatever the gate says**; the scan runs only if the gate passes.
3. Selftests of the 1102 build on its first use: `d18_secant.py selftest` (0) and `--mutate=half|norobust|nosigncheck` (1 each), `ell_b12rs.py selftest` (0) and `--mutate=nolam|harm` (1 each), `read_lower.py selftest` (0) and `--mutate=shift|round2` (1 each).
4. The scan: `d18_secant.py scan R1/l1kc127k050dh370.jsonl R1/sol_l1kc127k050dh370_D23.0000.npy 23.0 <lambda> R1/scan/scan_D23.0_p<i>.jsonl --b12=rust --b12_threads=1 --pin=<state blob>,<record blob>`, `P4_WT_MATTER=<1102>/solver/matter`, `PYTHONPATH=~/Source/ellrs-site-1102`, one process per lambda (0.045, 0.050, 0.060, 0.070), 1 thread each (OMP, OPENBLAS, MKL, VECLIB, RAYON = 1), nice 10. Robust = both noise signs equal the hybrid sign and dln <= 0.1 (the scatter run's test).
5. Reading: `read_lower.py R1/scan 0.045 0.070` and `R1/results_R1.py` (`R1/results_R1.md`): the table, the bracketing pair (the (0.045, 0.050) one if it brackets, else the robust sign change; several: all listed, none chosen), root(R1) det-linear from it, delta_1 = root(R1) - 0.045967998, Delta_R1 beside Delta_R0 = 1.1743225027439044 (win2's R0, record d1a3a641, = state B), and, when given (`--delta2=`, `--root2=`, `--dR2=`), bars 2 and 4 (r, and the order p from (0.7^p - 0.5^p)/(0.5^p - 0.35^p) = r).

## Gates run before the start (all in `R1/pre/`, `R1/steps_check.txt`)
| check | result |
|---|---|
| step counts from `freeze_from` on the state (`steps_check.py`: ell_refine's first freeze, same constructor) at kappa 0.7 / 0.5 / 0.35 and a 0.6 control | **4179** (the record's) / **5847** (in 5734-5968; 5851 is 4179 x 0.7/0.5 rounded) / 8351 (R2: 8190-8525) / 4871 (the control, outside the R1 range, as it must be) |
| `d18_secant.py selftest` (9706e506) and `--mutate=half`, `norobust`, `nosigncheck` | exit 0, 1, 1, 1 |
| `ell_b12rs.py selftest`, `--mutate=nolam`, `--mutate=harm` | exit 0, 1, 1 (block 12 at lambda 0.9: 3666 of 3666 entries bit for bit) |
| `read_lower.py selftest`, `--mutate=shift`, `--mutate=round2` | exit 0, 1, 1 |
| a scan command with a wrong state pin (`--pin=deadbeef,...`, `--b12=rust --b12_threads=1`) | refused, exit 3 (the command line parses and the pin gate fires) |
| `gate_R1.py` on the kappa 0.7 records A and B; on a planted passing record; with `--mutate=f|steps` | exit 1, 1; 0; 1, 1 |
| `results_R1.py selftest` (planted root 0.061 read as 0.060996; planted kappa^4 deltas read r 3.7394 and p 4.000; planted cubic read p 3.000) and `--mutate=r|pair` | exit 0; 1, 1 |
The pilot in the order, "when it prints its steps": `ell_refine.py` prints one JSON line, with the steps, only when it ends; the first `freeze_from` is checked above (5847), and bar 1 holds the final count (R0's steps did not move in its re-solve: 4179 before and after).

## Notes and conflicts named
- **Nice (changed by t5's order at 07:27 UTC):** the order said nice 10 beside D 5555, my standing yield rule says nice 19 while an `i1088a-*` unit runs. I named the conflict at the start; t5 ruled **the yield rule wins** (D 5555 serves #1098) and asked for nice 19 on every thread, for R1 and for its root scan. R1 ran at nice 10 from 07:25:36 to 07:27; at 07:27 every thread of every process of the unit (python 11 of 11 threads, `time`, `timeout`, the script's bash, `systemd-inhibit`) was raised to 19 with `renice_threads.sh` (verified by `ps -L`). The script's bash is at 19, so its later `nice -n 10` children (the selftests, the four scan processes, the pushes) start at 19: nice is capped at 19 (tested: `nice -n 19 bash -c 'nice -n 10 bash -c "ps -o ni= -p \$\$"'` prints 19). The scan's commands above read nice 10 as written in the script and run at 19. D 5555 (nice 10, 6 threads) is not touched.
- **Reading bias:** root(B) is the det-linear value of the (0.045, 0.050) pair, which may sit above the true root (the scatter run's caveat). If root(R1) comes from another pair, delta_1 carries the difference of the two windows' estimator biases, which I did not measure. I give delta_1 as the order says and report the pair; the estimator range of the reader (`read_lower_R1.txt`) is given beside it.
- Raw output is never written outside this folder, except `ell_refine.py`'s own `solver/matter/data/` files, which are copied here at the end and pushed (R1 writes its state only at its end).

## Predictions (mine, registered before R1 starts; information, not pass rules)
| prediction | probability |
|---|---|
| R1 converges (bar 1: \|F\| <= 5e-10, steps in 5734-5968) | 85% (steps 97%; \|F\| near the floor of R0's 3.2e-10, 12% it lands above 5e-10) |
| R1 wall time (6 threads, nice 10, beside D 5555's 6 threads on 6 cores / 12 threads; R0 took 4.6 h on win2 with 4179 steps) | 8 to 14 h, median 10 h (60%); under 8 h: 20%; t5's 6-8 h holds only if D 5555 is in a serial phase |
| root(R1) bracketed by one robust pair | 85% (the pairs (0.050, 0.060) and (0.060, 0.070) are the likely ones: 45% together; (0.045, 0.050): 15%; above 0.070: 5%) |
| delta_1 >= 3e-3 / between 1e-3 and 3e-3 / <= 1e-3 | 55% / 20% / 25% (#1103's inference gives about 0.015) |
| all four scan points robust (dln <= 0.1) | 80% (a point within 1e-3 of the root can carry dln up to 0.3) |
| scan wall time (4 processes, 1 thread, Rust block 12) | 1.0 to 2.0 h (60%); the Rust block was 678 s on 4 threads at lambda 0.046 and kappa 0.7, and R1 has 1.4x the steps |
| r in [3.0, 4.6] once delta_2 is in and \|delta_2\| >= 3e-3 | 45% |

## Status
- 2026-11-27 07:25 UTC: bars, pins, gates and scripts written and pushed (raw e3364429) before any R1 evaluation.
- 2026-11-27 07:25:36 UTC: R1 started (unit `i1101r1`, python pid 2984071 under `timeout`, nice 10, 11 threads of the process, OMP/OPENBLAS/MKL/RAYON = 6). Steps: the first `freeze_from` gives 5847 (in 5734-5968); the record's final count follows at the end.
- 2026-11-27 07:27 UTC: all threads of the unit raised to nice 19 on t5's order (see Notes); the scan will run at 19.
