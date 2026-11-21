# I1054-dh610: PR #1054's exact 1/k (`--exact_recip`, #1043): the flag off against the main build, and the re-solves at D 73, 241.96 and 251.88, on dh610

Machine dh610 (Fedora 45, i7-12700, 20 threads, 62 GB). Pull request https://github.com/nmoinvaz/choptuik-large-d/pull/1054 (branch `feat/exact-recip-1043`, head 5f488e2b when this was written, based on main 6f401e0b),
the coordinator's order of 20 Nov 2026 (about 11:40 UTC), queued after #1052's A/B (unit `i1052`): the runner commands of `notes/EXACT_RECIP.md` section 3, in order.

Builds: the new one is a worktree `~/Source/choptuik-large-d-1054` at the PR head with a new venv `~/Source/venv-i1054` and `hp/build.sh` (`PIP_NO_CACHE_DIR=1 python -m pip uninstall -y multidouble` first, as the note says); the
comparison build ("main") is `~/Source/venv-i1050`, the #1050 build at 1c02b15b. Between 1c02b15b and main 6f401e0b (the PR's merge base) `hp/src`, `hp/python`, `hp/Cargo.toml`, `hp/Cargo.lock`, `hp/pyproject.toml` and `hp/build.sh` are
identical (checked: empty `git diff --stat`), so venv-i1050 is main's build for this comparison. The PR changes `hp/src/{model,python,series_split,split_tests,qd_residual,lib}.rs`, `hp/modecount_cx/src/lib.rs`, `hp/python/hpkernel/driver.py`,
`hp/anm_run.py`, `hp/arclength.py`, `hp/reseed.py` and adds `hp/exact_recip_check.py`, `hp/src/recip_tests.rs` and the note.

Steps (cheapest first within the coordinator's order; each under timeout, 3 times its estimate, on its exact pid; nice 10):
0. venv and worktree; 1. `hp/build.sh` (est. 31 min, 24 GB; cap 93 min);
(1) bit identity with the flag off: `highm_check.py` ref, scaled, jets and `jets --mutate=kappa` (the #1034 step 5 commands) on the new build, compared row by row with `../I1050-dh610/step5_*.log` (the venv-i1050 build; `compare1050.py` copy, with its control);
and `exact_recip_check.py bits $RAW/I461-win2/crawlJ/anm_pin3_D242.3642.npz --threads 10`: `--save=$OUT/bits242_main.json` with venv-i1050's python, then `--compare` with venv-i1054 (expect 0 of 6 differ), and `--compare ... --mutate=on` (control, exit 1) (est. 5 min each);
(2) the re-solves, `anm_run.py` with `--steps 0 --save_base 1 --exact_recip 0` and `1`: D 73 (`T81/conv_pin5_D73.0000_D73.000000.npz`, est. 5-15 min a run), D 241.96 (`I603-win2/chain/anm_pin3_D241.9602.npz`, 5-20 min), D 251.88
(`I966-dh370/ks_chain3b/leg06_D251.2845_ks293/anm_pin3_D251.8782.npz`, 1-3 h); (3) `exact_recip_check.py delta` on each pair. Pass criterion of the D 73 control, fixed before the runs (#1043): |Delta(exact) - Delta(recip_int)| < 1e-25.
The Mac's D 73 pair gave +1.74e-25 (a miss) and its D 241.96 pair about +3.3e-13 (note section 3.3); a polish that is not adopted is reported, not rerun with `--base_adopt 1`.

Inputs not in the live raw clone (`I603-win2/.../anm_pin3_D241.9602.npz`, `I966-dh370/.../anm_pin3_D251.8782.npz`) were taken from origin/main by `git archive`. `exits_1054.txt` and `summary_1054.txt` hold the exits and walls.

## Files

| file | what |
|---|---|
| `common1054.sh`, `run1054.sh`, `compare1050.py` | paths, the driver, the row-by-row comparator (a copy of I1050-dh610's) |
| `resolve73_r{0,1}/`, `resolve241_r{0,1}/`, `resolve251_r{0,1}/` (+ `.log`) | the re-solves with `--exact_recip 0` and `1`; each folder holds the saved `base_pin<k>_D<D>.npz` |
| `delta73.json`, `delta241.json` (`delta*_early.log`) | `exact_recip_check.py delta` on the D 73 and D 241.96 pairs, run by hand at 15:05 UTC while the D 251.88 pair ran (the driver reruns them after that pair, same inputs); D 73: Delta(on) - Delta(off) = +1.743109e-25 (a miss against 1e-25), D 241.96: +3.290002e-13 |
| `delta251.log` | `exact_recip_check.py delta` at D 251.88 failed (exit 1, FileNotFoundError): the flag-on polish saved no base, see below |
| `delta73.log`, `delta241.log`, `delta*.json` | the driver's own runs of the deltas, after the D 251.88 pair; the same values as the by-hand runs (`*_early.log`) |

## Results (16:13 UTC, 20 Nov)

| D | flag off (`--exact_recip 0`) | flag on (`1`) | Delta(on) - Delta(off) |
|---|---|---|---|
| 73.0 (T81) | exit 0, 121 s, 3 Newton steps, max\|F\| 2.6e-34 to 2.3e-83 | exit 0, 125 s, 4.4e-30 to 2.0e-73 | +1.743109e-25, a miss against the 1e-25 bound |
| 241.96 (I603) | exit 0, 70 s, converged at once (2.0e-65) | exit 0, 2948 s, stalled at max\|F\| 6.8e-51 after 12 steps, base saved | +3.290002e-13 |
| 251.88 (I966-dh370 leg 6) | exit 0, 3857 s, 7 steps, 4.55e-35 to 7.2e-82, base saved | exit 0, 320 s: "the start's projection failed, attempt stopped", no step, no base | none |

D 251.88, flag on: the log says `elim projections {'u0': 0, 'u0q': 0, 'ladder': 0, 'failed': 1, 'skipped': 0}: the start's projection failed, attempt stopped`. From `hp/octo_corrector.py` (`ElimO.project`) that error is raised only when the start's
pinned quad-double max|F| is above `--elim_switch` (1e-15) and above `start_F` (1e-6), so with the flag on the stored state's residual is above 1e-6 (flag off: 4.55e-35, its start was skipped by the switch). The log does not print that value (a reading of the code, not tested).
There is no "base polish not adopted" line and no "base polish saved" line: in `anm_run.py` the stopped attempt leaves no `od_F` and no `z8`, so the adoption branch saves nothing and prints nothing. Reported, not rerun, not changed.

## Follow-up (20 Nov, coordinator's task): D 251.88 flag-on with `--od_start_F 0`

Worktree `~/Source/choptuik-large-d-1054` checked out at 4204c9f9 (`feat/exact-recip-1043`; `git rev-parse HEAD` in `exits_1054.txt`, lines "1054b"), only `hp/anm_run.py`, `hp/arclength.py`, `hp/exact_recip_check.py` and the note changed since the 5f488e2b build, so venv-i1054 stands.
`run1054b.sh` (unit `i1054b`): `resolve251_r1b` (the flag-on polish of the D 251.88 state with `--od_start_F 0 --log_proj 1`, otherwise the flags of `resolve251_r1`), then `check251b.py` (the coordinator's pass rule: no "attempt stopped", "octo-double Newton: K steps, max|F| X" with X <= 1e-50, "base polish saved as" after it), then `delta251b` against `resolve251_r0`'s base.
`check251b.py` controls: the flag-off log prints PASS, the stopped flag-on log (`resolve251_r1.log`) prints FAIL.

### Result (18:10 UTC, 20 Nov): the pass rule fails, no value

`resolve251_r1b`: exit 0, 1462 s, unit `i1054b` (17:43:35 to 18:07:57 UTC, journal memory peak 295 MB, no memory alert), HEAD 4204c9f94d030aef508131c41a4573cd9b9de64e. `check251b.txt`: FAIL (no "attempt stopped": ok; "octo-double Newton: 1 steps, max|F| 2.0e-05": FAIL against 1e-50; no "base polish saved as": FAIL);
its controls hold (the flag-off log passes, the stopped `resolve251_r1.log` fails). The log's "projection failed (n)" lines n = 1 to 12 are in `resolve251_r1b.log` and in the PR comment. "base polish not adopted (max|F| 2.0e-05 -> 2.0e-05)": no base is saved, so `delta251b.log` ends in a FileNotFoundError (exit 1).

## Follow-up (20 Nov, coordinator's task): the flag-on pairs at D 246.44 and D 249.47

Worktree at 4204c9f9 (no fetch, no rebuild), venv-i1054, unit `i1054c` (`run1054c.sh`, a braced block ending in `exit`): for `I966-dh370/ks_chain3b/leg01_D243.8361_ks293/anm_pin3_D246.4399.npz` and `leg02_D247.2801_ks293/anm_pin3_D249.4664.npz` (taken from origin/main by `git archive`:
blobs 7ced8b8d and 7b642543) the flag-off and flag-on polish (`resolve<D>_r0`, `resolve<D>_r1`, the D 251.88 flags with `--log_proj 1`), `exact_recip_check.py delta` (`delta<D>.json`), then `check251b.py` on each of the four logs (`check_<D>_r<R>.txt`, the coordinator's convergence rule)
and `fit_change.py` (`fit_change.txt`: the three changes against D and their rows' quoted errors, the least-squares line of log10|change| in D evaluated at 251.88, marked as an extrapolation; `fit_change_selftest*.txt`: its controls).

### Result (19:18 UTC, 20 Nov): both flag-on polishes stop at their start

Unit `i1054c` ran 19:02:37 to 19:15:44 UTC (13 min, 1 h 59 min CPU, journal memory peak 256 MB, no memory alert), HEAD 4204c9f94d030aef508131c41a4573cd9b9de64e. Flag off converges at once at both D (1 Newton step, max|F| 7.6e-83 at D 246.44 and 1.8e-82 at D 249.47, 56 s and 60 s, bases saved).
Flag on, default start bound (1e-6): "projection failed (1): point max|F| 3.29e-06" (D 246.44) and "9.02e-06" (D 249.47), then "the start's projection failed, attempt stopped" (333 s and 336 s), no base, so `delta246.4399.log` and `delta249.4664.log` end in a FileNotFoundError (exit 1) and `fit_change.txt`
has one point ("need at least two points"). By the coordinator's reading (b) the number is the change at the last D where both converged, D 241.96: +3.290002e-13 (`delta241.json`).

## Follow-up (20 Nov, coordinator's task): the two jobs of notes/EXACT_RECIP.md 3.6

Worktree `~/Source/choptuik-large-d-1059` at main 8179068d (the note's own commit; 394c9f2d is its ancestor), venv-i1054's python (the only dh610 build with `Solver.set_exact_recip`, built at 5f488e2b; main's `hp/src` differs from that build's only by `plan_auto`, the #1056 pins and test modules, listed in `summary_1054.txt`). One unit `i1054d` (`run1054de.sh`):
`run1054d.sh` job (1), `--od_start_F 0` at D 246.44 and 249.47 against the flag-off bases of the 3.5 batch (`resolve<D>_r1b`, `delta<D>b`), then `run1054e.sh` job (2), the default-bound pair at D 242.8630, 243.8361 (leg 0, ks 291), 244.7177 and 245.5586 (`resolve<D>_r0`, `_r1`, `delta<D>`).
`classify.py` reads each log by the note's rule (converged, stopped at start, not converged; `--selftest` and `--selftest --mutate` are its controls), `table1054.py` builds the tables (`table_job1.md`, `table_job2.md`), `fit_change.py` the line through the converged changes (`fit_change_job1.txt`).

## Job 2 first try (20 Nov, 21:27 UTC): no input states

`run1054de.sh` chained into job 2 at 21:26:59 UTC and every run exited at once (`FileNotFoundError`): the four input states were not in the live raw clone and `run1054e.sh` does not extract them. Not a result; the logs are in `job2_try1_nostates/`. The four states were then extracted with `git archive origin/main I966-dh370/ks_chain3b/<S>.npz` (blobs ff8926fa, a3af7539, 56209d07, e8772fd6) and job 2 was run again with `run1054e.sh` as it is, unit `i1054e`.

## Job 1 result (20 Nov, 21:28 UTC): no value at D 246.44 or 249.47

`--od_start_F 0` with the flag on does not converge at either D: the projection fails at the start (u0 rung, quad-double u0 and ladder all NOT converged), the strong chord's first step is refused (theta inf), and no trial step is accepted. D 246.4399: pinned max|F| 3.29e-06, first step |dz| 6.48e-05, 13 "projection failed" lines, polish not adopted (3.3e-06 -> 3.3e-06), 2157 s. D 249.4664: 9.02e-06, |dz| 1.19e-03, 12 lines, 9.0e-06 -> 9.0e-06, 1714 s. Flag-off polishes of the same states converge in 1 step (7.6e-83, 1.8e-82). No change value and no extrapolation (`fit_change_job1.txt`: one point). Files: `resolve246.4399_r1b*`, `resolve249.4664_r1b*`, `table_job1.md`, `fit_change_job1.txt`, `summary_1054.txt`, `exits_1054.txt`. Posted on #1043 (comment 7051048042).

## Job 2 result (20 Nov, 21:54 UTC): every flag-on polish stops at its start under the default bound

Unit `i1054e`, 21:28:56 to 21:54:01 UTC, same worktree/venv as job 1. All four flag-off polishes converge (1 step; max|F| 2.4e-84, 1.1e-83, 2.4e-84, 3.4e-67). All four flag-on polishes stop at the start ("the start's projection failed, attempt stopped"; no Newton line), with pinned max|F| 1.00e-06 (D 242.8630), 1.38e-06 (243.8361), 1.85e-06 (244.7177), 2.45e-06 (245.5586), each above the 1e-6 start bound. No `delta` file (no flag-on base). Basin edge by the fixed rule: last D whose flag-on polish converges is 241.96 (the 3.5 batch), first where it stops is 242.86. Files: `table_job2.md`, `resolve24[2-5].*_r[01]*`, `delta24[2-5]*.log`, `summary_1054.txt`, `exits_1054.txt`, `memlog_1054e.log`.

## Job 3 (20 Nov, coordinator's task after job 2): the unbounded flag-on polish at D 242.8630 only

`run1054f.sh`: `anm_run.py` from `hp/` of the worktree `~/Source/choptuik-large-d-1059` (main 8179068d) with venv-i1054's python, 3.6's flags, `--exact_recip 1 --od_start_F 0`, on `I966-dh370/ks_chain3b/leg00_D237.7132_ks291/anm_pin3_D242.8630.npz` (blob ff8926fa), output `resolve242.8630_r1b`; then `exact_recip_check.py delta` against job 2's flag-off base `resolve242.8630_r0/base_pin3_D242.8630.npz`. Read by 3.5's rule (`classify.py`): converged means "octo-double Newton: K steps, max|F| X" with X <= 1e-50 and "base polish saved as" after it. Converged: the change, its share of 3.4e-11 (the quoted error of the row at D 242.7053), and the two-point line of log10|change| in D through D 241.96 (+3.29e-13) and D 242.86, evaluated at 251.88 against 4.7e-7, marked as having no spread (`fit_change_job3.txt`). Not converged: the steps and last max|F|, the first step's |dz| and the "projection failed (n)" lines. Starts after the #1058 build and its four checks end (unit `i1054f`).

## Job 3 result (20 Nov, 23:08 UTC): the unbounded flag-on polish at D 242.8630 does not converge

Unit `i1054f`, 22:34:21 to 23:07:43 UTC (`resolve242.8630_r1b`, 2002 s), `run1054f.sh`. Not converged by 3.5's rule: pinned start max|F| 1.00e-06, the projection at the start fails (u0 rung 1 iteration |R| 2.58e+21 -> 2.58e+21, quad-double u0 8 iterations 5.19e+14 -> 4.04e+11, ladder failed after 8 rungs), the strong chord's first step is refused (theta inf), the trial points blow up (7.74e+114, nan, then falling to 9.39e+76), "on 0: |F| 1.00e-06, |dz| 4.05e-06: no trial step accepted, stopping", 13 "projection failed" lines, "octo-double Newton: 1 steps, max|F| 1.0e-06, not converged", "base polish not adopted (max|F| 1.0e-06 -> 1.0e-06)". No flag-on base, so `delta242.8630b.log` exits 1 and there is no change value; `fit_change_job3.txt` has the one point D 241.96 and exits 1 ("need at least two points for the line"). Controls: job 2's flag-off log of the same D converges (1 step, 2.4e-84); `classify.py --selftest` exit 0 and `--selftest --mutate` exit 1 (`classify_selftest_job3.txt`, `classify_selftest_mutate_job3.txt`). Files: `resolve242.8630_r1b*`, `delta242.8630b.log`, `table_job3.md`, `fit_change_job3.txt`, `memlog_1054f.log`.

## Job 4 (20 Nov, coordinator's task after job 3): the two D 241.96 bases continued two fixed steps of 0.25, flag off and on

`run1054g.sh`: `anm_run.py` from `hp/` of the worktree `~/Source/choptuik-large-d-1043g` (main 796f4bac; hp differs from the jobs 1-3 worktree 8179068d only in Python: the off-by-default Broyden corrector, `octo_corrector.py`, `anm_run.py`, `arclength.py` and two check scripts) with venv-i1054's python, crawlJ's flags (notes/EXACT_RECIP.md 3.3) plus `--a0 0.25 --h_max 0.25 --a_grow 1 --steps 2 --D_max 300`, `--exact_recip 0` on `resolve241_r0/base_pin3_D241.9602.npz` and `--exact_recip 1` on `resolve241_r1/...`, outputs `cont241_r0`, `cont241_r1` (no `--allow_unraw`: `require_raw` checks only the output path). Reading (a): `refusal.py` polls each log every 30 s (an attempt is refused when its max|F| is above its tol and the line has no "stall accepted", or "stopped: no convergence") and stops that run by its exact pid at its first refusal; the other run still goes so that both logs exist. Reading (b): `exact_recip_check.py delta` on the two runs' states at each common D (`delta_cont<D>.json`), its share of the nearest quoted error and its ratio to +3.290002e-13 (`table1054g.py` -> `table_job4.md`). Reading (c): the first polish line of each log is printed. Controls: `refusal.py --selftest` (exit 0, five planted/real lines) and `--selftest --mutate` (exit 1). Unit `i1054g`.

## Job 4 result (21 Nov, 00:19 UTC): flag off takes both steps, flag on refuses its first

Unit `i1054g`, 23:13:16 UTC (20 Nov) to 00:17:21 UTC, 1 h 04 min wall, 9 h 47 min CPU, journal memory peak 3 GB, no line in `memlog_1054g.log` beyond its header. `refusal.py --selftest` exit 0, `--selftest --mutate` exit 1.

| run | exit | wall | step 0 (base polish) | attempt 1, D 242.2102 | attempt 2, D 242.4602 |
|---|---|---|---|---|---|
| flag off (`cont241_r0.log`) | 0 | 961 s | first polish line: octo-double 1 step, max\|F\| 2.0e-65, converged | 3 steps, 8.6e-73, converged, accepted | 3 steps, 2.8e-72, converged, accepted |
| flag on (`cont241_r1.log`) | 143 (stopped by me at its first refusal, exact pid) | 2884 s | first polish line: octo-double 5 steps, max\|F\| 1.6e-24, not converged; "base polish not adopted (max\|F\| 6.8e-51 -> 1.6e-24): the stored state is the base" | 3 steps, 2.1e-24, not converged, REFUSED (last line: "no trial step accepted, stopping") | not run |

(a) Both runs did not accept two steps at the same D: only the flag-off run did. (b) No D has a state from both runs, so no Delta(on) - Delta(off) beyond +3.290002e-13 at 241.96 and no share (`delta_cont*.json` not made, "no flag-on state"). Printed on the attempt lines, to 12 digits: flag off D 242.2102 Delta 1.686261688522 (state 1.686261688522407147), flag on 1.686261688523 from the unconverged iterate, which is not a reading. (c) The flag-on base's first polish does not converge: from the stored 6.8e-51 every trial of its first Newton step raises max|F| (lam 1: 1.45e-21, then 4x lower per halving to 5.66e-24 at lam 0.0625, accepted at lam 0.03125 giving 1.41e-24; raw |dz_t| 2.6e-26 against the linear |dz| 1.73e-28), and it ends at 1.6e-24 after 5 steps. The flag-off base's first polish is 1 step, 2.0e-65. The attempt's corrector shows the same: max|F| 2.1e-24, raw |dz_t| / |dz| 196 at lam 1 in step 0, 249 in step 2.

Reading of the attempt line, corrected (a discrepancy in what I first wrote, not in the code): with `--corrector od` the attempt is accepted iff the octo-double Newton converged (`accepted = conv`, anm_run.py `correct()`). The figure printed after "steps ->" is the double-double |F| of the first two parts of the eight-part state (8.8e+05, 1.04e+06, 1.23e+06 here, flag on and off alike), and the label "stall accepted" is printed whenever the attempt is accepted and that figure is above tol. So the flag-off attempts are converged (8.6e-73, 2.8e-72, both at or below tol_od 1e-60), not stall-accepted. My first `table_job4.md` called them "stall accepted"; it is kept as `table_job4_first_mislabeled.md`. `table1054g.py` now reads the octo-double line before each attempt line (control: `controls_job4_reading.txt`, a "converged" changed to "not converged" flips the flag-off reading, 8.6e-73 changed to 8.6e-50 reads "says converged, max|F| above tol_od"). `refusal.py` read accepted from the same label or Fc at or below tol; in this od path every Fc is 1e+05 to 1e+06 and the label is the only signal, so its two readings agree with `accepted` here.

## Job 5 (21 Nov, coordinator's task after job 4): the flag-on polish of job 4's two flag-off states, D 242.2102 and 242.4602

`run1054h.sh`: from `hp/` of `~/Source/choptuik-large-d-1043g` (main 796f4bac, the worktree that made the states), venv-i1054, job 2's F (notes/EXACT_RECIP.md 3.5's flags: `--N 31 --qd_it 40 --od_accept natural --od_strong 4 --reseed_start pred --reseed_qd_bar 1e-21 --steps 0 --save_base 1 --log_proj 1`, default `--od_start_F` bound 1e-6). Inputs `cont241_r0/anm_pin3_D242.2102.npz` and `.../D242.4602.npz` (job 4's flag-off states, sha256 prefixes in `summary_1054.txt`). Per D: `resolve<D>_r0` (flag off, the control: the job 4 state re-polished, cap 3600 s), `resolve<D>_r1` (flag on, cap 7200 s), read by `classify.py` (3.5's rule: converged iff max|F| <= 1e-50 and "base polish saved as"), `exact_recip_check.py delta` of job 4's state against the flag-on base (`delta_job5_<D>.json`, the reading asked for) and of the flag-off re-polish against it (`delta<D>.json`). First `check_delta_control.py` (A vs A must be 0, A vs B must equal the difference of anm_run.py's own two "Delta of the saved state" sums in `cont241_r0.log` to 1e-30; its `--mutate` moves the log's value by 1e-20 and must exit 1: dry run exit 0 and 1). `table1054h.py` builds `table_job5.md` (planted test `controls_job5_table.txt`: a delta 10 times larger reads ratio 10, a stopped-at-start log reads no change). Expectation fixed before the run: the pinned start max|F| of a flag-off state under the flag on grows 1.396 times per unit D (job 2: 1.00e-6, 1.38e-6, 1.85e-6, 2.45e-6 at D 242.8630 to 245.5586), which extrapolates to 8.0e-7 at D 242.2102 and 8.7e-7 at D 242.4602, under the 1e-6 bound, so both should start; whether the Newton then converges is not predicted.

## Job 5 result (21 Nov, 00:56 UTC): both flag-on polishes converge, change +3.443409e-13 at D 242.2102 and +2.798345e-13 at D 242.4602

Unit `i1054h`, 00:23:56 to 00:55:19 UTC (31 min wall, 4 h 43 min CPU, journal memory peak 225 MB, no line in `memlog_1054h.log` beyond its header). `delta_control_job5.txt` exit 0 and `delta_control_job5_mutate.txt` exit 1 (before the polishes), `classify.py --selftest` PASS and `--mutate` exit 1 (after). By 3.5's rule (`classify.py`, `table_job5.md`):

| D | flag off, re-polish of job 4's state | flag on (default 1e-6 bound) | change vs job 4's state | nearest row, quoted error | share | change / 3.290002e-13 |
|---|---|---|---|---|---|---|
| 242.2102 | converged, 1 step, 8.6e-73, 63 s | converged, 5 steps, max\|F\| 4.5e-93, 876 s | +3.443409e-13 | D 241.96, 3.8e-11 | 9.06e-03 | 1.05 |
| 242.4602 | converged, 1 step, 2.8e-72, 68 s | converged, 5 steps, max\|F\| 2.2e-92, 874 s | +2.798345e-13 | D 242.7053, 3.4e-11 | 8.23e-03 | 0.851 |

The change against the flag-off re-polish is the same to the printed digits (the re-polish moved nothing). The first Newton step's own dDelta in the logs, +3.44e-13 and +2.80e-13, agrees with the delta tool's +3.44341e-13 and +2.79834e-13, and the later steps move Delta by 3e-25 or less. No flag-on log has a "projection failed" line: both started under the 1e-6 bound, as expected (the log prints a start max|F| only when the projection fails, so the extrapolated 8.0e-7 and 8.7e-7 are not tested beyond "below 1e-6"). Both flag-on polishes used the strong chord (`--od_strong 4`: "strong chord (4 weak directions), 7 steps after the full first step; theta 6.9e-12 and 9.1e-12 (bound 0.750): accepted") then 4 plain steps.

Discrepancy in the design of job 4, reported not fixed: job 4's F (the coordinator's) has the chain's Newton flags (`--qd_it 12`, none of `--od_accept natural --od_strong 4 --reseed_start pred --reseed_qd_bar 1e-21`), as did the D 241.96 polish that made the flag-on base (`resolve241_r1.log`, 12 steps, stalled at 6.8e-51; no "strong chord" line), and job 4's flag-on base polish and attempt used no strong chord; job 5's F is 3.5's (`--qd_it 40` and those four), whose flag-on polishes converge at 242.2102 and 242.4602 in 5 steps. The two differ in the input state (a converged flag-on base and a prediction from it, against a converged flag-off state) and in these flags, so job 5 does not say which one made job 4 fail.

## Job 6 (21 Nov, coordinator's task after job 5): job 4 again with 3.5's Newton flags, 4 steps of 0.25

`run1054i.sh`: `anm_run.py` from `hp/` of `~/Source/choptuik-large-d-1043g` (main 796f4bac), venv-i1054, from `resolve241_r0` and `resolve241_r1` (`base_pin3_D241.9602.npz`), `--exact_recip 0` then `1`, F = job 4's with 3.5's Newton flags and `--N 31 --qd_it 40 --lam_stall 0.04` (job 2's values), `--od_accept natural --od_strong 4 --reseed_start pred --reseed_qd_bar 1e-21`, `--a0 0.25 --h_max 0.25 --a_grow 1 --steps 4 --D_max 300`; outputs `job6_r0`, `job6_r1` (states at D 242.2102, 242.4602, 242.7102, 242.9602), logs `job6_r<R>.log`. Reading (b): the runs go one after the other (10 threads each, as job 4), `refusal.py` is polled every 30 s on the running log and kills the running pid at its first refused attempt; if the flag-off run refuses, the flag-on run is not started (both stop). The flag-on base polish's first line is read first (reading (c)); the run goes on to its first attempt as in job 4. Afterwards `exact_recip_check.py delta` of the two states at each common D (`delta_job6_<D>.json`), and consistency checks (`xcheck_job6.py`, bound fixed before the run: two converged solves of the same equations at the same D agree in Delta to 1e-30): job 4's flag-off state against job 6's, job 5's flag-on polish against job 6's, both at D 242.2102 and 242.4602, and the control, job 6's flag-off state against job 5's flag-on polish, which must exceed 1e-30 (the flag's own change, about 3e-13). Planted test of the check: `controls_job6_xcheck.txt` (a 4e-20 gap fails, `--mutate` exits 1). `table1054i.py` builds `table_job6.md`.
