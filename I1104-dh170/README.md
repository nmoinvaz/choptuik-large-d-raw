# I1104-dh170: #1104's second run: the kappa correction of the l = 1 root at a second D (k_c 127, D 23.125)

Machine dh170 (i7-7700, 4 physical cores, 31 GB; Linux). Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1104 (coordinator t5; t5's order is the comment of 27 Nov 19:34 UTC, 7226665371, and the hc after it, quoted at the end).
Written 2026-11-27 19:37 UTC by the clock, before any run (bars, reading rule, pins, commands, predictions first).

## Question
At D 23.0 the kappa 0.7 -> 0.5 re-solve moved the root of det M (the mode matrix of the l = 1 perturbation) by delta(23.0) = +0.04904 (R0 0.045967998 -> R1 0.09500769, #1101). The corrected zero needs the same at the D where lambda_1 crosses zero. At kappa 0.7 the k_c 127 root at D 23.125 is about -0.0419 (macm3's legs, #1025), so a correction near +0.05 at kappa 0.5 puts it near +0.007.
This run measures delta(23.125) = root(kappa 0.5) - root(kappa 0.7) at k_c 127, D 23.125, and compares it with delta(23.0).

## Bars (t5's, fixed before the run; each can fail)
1. **The re-solve** (macm3's k_c 127 D 23.125 state at kappa 0.5, `ell_refine.py`): |F| <= 5e-10 and steps 5855 +- 2% (5738 to 5972; 1.4 times the kappa 0.7 state's 4182). Otherwise the state is not used and the cause is looked for.
2. **The reading:** delta(23.125) = root(kappa 0.5) - root(kappa 0.7), both roots on the same scanner (Rust block 12, `d18_secant.py`), the kappa 0.7 root re-measured first at lambda -0.045 and -0.040 (the bracket of macm3's lane), against delta(23.0) = +0.04904.
   - **Equal within 10%** (delta(23.125) in 0.04414 .. 0.05394): the correction is D-independent near the zero, and then the kappa-corrected zero follows from one more D.
   - Anything else: reported as measured, with the ratio delta(23.125) / 0.04904.
3. Scans: kappa 0.5 state at lambda -0.020, -0.005, +0.010, +0.025 (4 processes), then the secant (`run`, tol 5e-5) on the change; if none, widen to -0.035 and +0.040 (t5). No further widening by me.

**Reading rule (mine, stated before the run):** a root is read only from a `d18_secant.py run` ending with status `tol`, both bracket ends robust (noise signs equal the hybrid sign, dln <= 0.1) with opposite hybrid signs, and inside the scan's pair. The ratio is read on the ranges of the final brackets [a, b] (kappa 0.5) and [c, d] (kappa 0.7): delta in [a - d, b - c]; the whole range of delta / 0.04904 inside 0.9 .. 1.1 reads as "equal within 10%", the whole range outside it as "not equal within 10%", anything else (a range that straddles 10%) as "between, reported as measured". `lam_lin` (the det-linear root inside the final bracket) is printed beside it. The estimator values are at the width of the final bracket, not rigorous enclosures. delta(23.0) = 0.09500769 - 0.045967998 = 0.049039692 is taken from t5's #1101 comments (R1 root by t5 on macm3; R0 root by dh370), as t5 quotes it.

## Resources (R2's secant keeps priority, t5)
R2's secant (#1101, unit `i1101r2w`, 1 thread, nice 10) runs on. The re-solve takes 3 threads at nice 10 (t5's order), so 4 threads are busy at nice 10 on the 4 physical cores. The two kappa 0.7 re-root scans and their secant (1 thread each) run at **nice 19**, so they use only what is left (6 threads on 4 cores at most; my rule: busy threads at nice 10 <= 4 physical cores, the rest at nice 19). The kappa 0.5 scans (4 processes) start only after the re-solve, when R2's secant may still run; they start at nice 10 only if the busy nice-10 threads then are <= 4 with them, else at nice 19. If R2's secant evaluation time rises above 1.5 times its time alone (about 2400 s per evaluation alone, 4600 s beside 5 busy threads), I throttle my runs and say so.

## Pins (by blob; the drivers refuse any other)
| what | where | blob |
|---|---|---|
| start state (kappa 0.7, k_c 127, D 23.125) | raw `I1025-macm3/kc127_leg/states/sol_l1kc127Lmacm3_D23.1250.npy`, copy in `in/` | e1dccb3c |
| its record (|F| 2.98e-10, 4182 steps, kappa 0.7, u0 0.04) | `l1kc127Lmacm3.jsonl`, copy in `in/` | 58d3b080 |
| regrid worktree | `~/Source/choptuik-large-d-1025k79` at 48c36355, `ell_refine.py` | 631e5801 |
| | `dss_ell.py` (and `ell_ddm.py`, `ell_dd.py`, `ddnp.py` equal to 505d8399) | 5d28c19e |
| scanner worktree | `~/Source/choptuik-large-d-1101k` at f56f91d2, `solver/matter/d18_secant.py` (no `--kappa_mm`: the plain scan) | 2f3ee874 |
| Rust block 12 | `ell_b12rs.py`, ellrs in `~/Source/ellrs-site-1102`, venv `~/Source/choptuik-large-d-1058b/.venv` | a1fff74f |
| re-solve driver `run_resolve1104.sh` (unit `i1104resolve`) | this folder | 8c5a1be8 |
| re-root driver `run_reroot1104.sh` (unit `i1104reroot`, nice 19) | this folder | 50425177 |
| reader `results_1104.py` (selftest exit 0; `--mutate=sign`, `bar`, `ref`, `last` exit 1; `selftests/selftest_results_1104*.txt`) | this folder | a1dd91ba |
| kappa 0.5 scan driver `run_scan1104.sh` (unit `i1104scan050`, launched by hand after the re-solve passes) | this folder | b8352614 |
| scan readers | `in/read_lower.py`, `in/d185_scan_read.py` (the #1101 copies) | 89309d3c, 7c9d400f |

## Commands
1. Re-solve (cwd `~/Source/choptuik-large-d-1025k79/solver/matter`, 3 threads, nice 10, cap 57600 s on the python pid; t5's command):
   `python -u ell_refine.py l1kc127Lmacm3 127 l1kc127k050dh170d23125 127 1 23.125 2.0992182200 --kappa 0.5 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma`
   (start state and record are copied into the worktree's `data/` first, blob-checked; the result is copied to this folder). `ell_refine.py` prints no progress, so the pilot is the process's life: the driver logs the python pid's RSS and CPU every 30 min.
2. Re-root of the kappa 0.7 source: `d18_secant.py scan in/l1kc127Lmacm3.jsonl in/sol_l1kc127Lmacm3_D23.1250.npy 23.125 L scan_070/scan_D23.125_p<i>.jsonl --b12=rust --b12_threads=1 --pin=e1dccb3c,58d3b080` at L = -0.045 and -0.040, then `run ... LO HI secant_070.jsonl --tol=5e-5 --maxev=20 --b12=rust --b12_threads=1 --ends=scan_070_all.jsonl --pin=...` on the robust change.
3. After the re-solve passes its bars: the same for the re-solved state at L = -0.020, -0.005, +0.010, +0.025 (`scan_050/`, `secant_050.jsonl`), widening to -0.035 and +0.040 if none. The scan must print the record system (|F| and steps equal to the record's) and `block 12 by ellrs`.
4. Reading: `results_1104.py` (planted selftest with mutations, written and pushed before the secants end).

## Predictions (mine, registered before the run; information, not pass rules)
| item | prediction |
|---|---|
| re-solve |F| <= 5e-10 | 90% |
| re-solve steps within 2% of 5855 | 90% (at D 23.0: R1's 5847 against R0's 4179, ratio 1.399) |
| re-solve wall (3 threads, nice 10, beside R2's secant and the re-root) | 3 to 10 h: 60%; over 16 h (the cap): 5% |
| the kappa 0.7 re-root has a robust change in (-0.045, -0.040) | 80% |
| root(kappa 0.7) within 2e-3 of macm3's -0.0419 | 75% |
| the kappa 0.5 scan has a robust change in the first four points (-0.020 .. +0.025) | 80% (no change, widening needed: 20%) |
| root(kappa 0.5) > 0 | 70% (t5's near +0.007) |
| delta(23.125) equal to 0.04904 within 10% | 45%; between 10% and 25% off: 35%; more than 25% off: 20% |
| scan wall per point (4 processes) | 4400 to 6200 s: 60% |
| each secant wall | 4 to 8 h: 60% |

## Status
- 2026-11-27 19:37 UTC: bars, reading rule, pins, commands and predictions written before any run. Not started.
- 2026-11-27 19:39 UTC: unit `i1104resolve` (`run_resolve1104.sh`, 8c5a1be8) started 19:37:51 UTC (pins ok, python pid 2322724, nice 10, 3 threads). Reader and re-root driver written; the re-root starts next.
- 2026-11-27 19:40 UTC: unit `i1104reroot` (`run_reroot1104.sh`, 50425177) started 19:39:37 UTC (selftests 0/1/1/1 and 0, mutations fail; nice 19, 1 thread per scan); at 19:39:59 both scans print the record system (|F| 2.9978e-10 against the record's 2.9775e-10, steps 4182 = 4182). `run_scan1104.sh` written for the kappa 0.5 state (pushed before use).
- 2026-11-27 20:22 UTC: kappa 0.7 re-root scans done (19:39:37 to 20:22:41 UTC, 2567 s and 2557 s per point at nice 19): hybrid sign + at -0.045 and - at -0.040, both noise-robust and robust (dln 5.05e-06, 1.05e-05); `read_lower.py`: one robust change (-0.045, -0.040), det-linear -0.041286 (macm3's -0.0419: +6.1e-4); `results_1104.py scan` exit 0; the secant started 20:22:41 UTC (`--ends`, nice 19). The re-solve is alive at 1800 s (RSS 0.60 GB, CPU 280%). R2's secant: 5 evaluations, bracket (0.114683, 0.123441).

## Order, verbatim

> t5 19:34 UTC: Test K's extension accepted, and the driver cleanup is fine. New task beside R2's secant: #1104's second run (my newest #1104 comment is the record; read #1104's body first). Re-solve macm3's k_c 127 D 23.125 state (raw I1025-macm3/kc127_leg/states/: sol_l1kc127Lmacm3_D23.1250.npy blob e1dccb3c, record l1kc127Lmacm3.jsonl blob 58d3b080) at kappa 0.5 in your 1025k79 worktree (48c36355): 'ell_refine.py l1kc127Lmacm3 127 l1kc127k050dh170d23125 127 1 23.125 2.0992182200 --kappa 0.5 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma', 3 threads, nice 10, cap 57600 s. Bars: |F| <= 5e-10, steps 5855 +- 2%. Meanwhile, re-root the kappa 0.7 source on the Rust block at lambda -0.045 and -0.040, plus the secant. After the re-solve: scan -0.020, -0.005, +0.010, +0.025 and the secant at tol 5e-5; widen to -0.035 and +0.040 if none. New raw folder I1104-dh170/, README with the bars first. R2's secant keeps priority.

