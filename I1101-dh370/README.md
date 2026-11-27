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
