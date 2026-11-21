# I1025-win/scan_low: hybrid sign scans of lambda 1.00 to 1.55 on D 18.0625 and D 18, k_c 63: where the root that crossed 1.20 went (winb)

Written before the run, 2026-11-21 18:20 UTC by my clock (substituted from `date -u` when pushed).

## Order

The coordinator (hc and #1025 comment 7067116072, edited 18:16:03 UTC), after the dd check at 1.20 (comment 7067101365): the sign flip at lambda 1.20 between D 18 and D 18.0625 is confirmed in full double-double, equal to the hybrid at both, so an odd number of real roots crossed 1.20 there. The map at D 18.25 also has a root at 1.3885 (xfkappa's (ii)); whether it is the same root is open. **Next: where the root that crossed 1.20 went.** Hybrid sign scans, each on the state used for the dd check, with the same tool and robustness rule as (ii) at D 18.25: D 18.0625 over lambda 1.00 to 1.55 and D 18 over lambda 1.00 to 1.55. As in (ii) (`d18_hybsign.py`, e089207a, read by `d18f_read.py`, 5fb96dce): points at 0.05, then at 0.01 inside each bracket with a sign change. A change counts only if both of its grid points are noise-robust (1e-15 on blocks 0 to 11, two seeds). Its position is the four-estimator range, which is information, not a bound. The ln|det| minima are listed beside it. Two processes.

Correction (hc, about 18:2x UTC, replacing a first reading of the comment that asked for a 1e-4 bisection and a full 0.01 grid): do exactly as xfkappa's (ii). Per state the 12 points at 0.05 over 1.00 to 1.55, then the 0.01 points inside each bracket with a sign change, and stop there: no 1e-4 bisection and no remaining 0.01 points. Report the four-estimator range and the ln|det| minima, which also flag a pair of roots that the 0.05 grid could hide. Two processes are fine. Expected end about 5 h from the start. (My first plan, with the bisection and the full grid, was sent at 18:16 and crossed the correction; it is withdrawn.)

## Readings, copied from the comment, fixed now

- A robust change in (1.20, 1.30) at D 18.0625 and one in (1.00, 1.20) at D 18 mean the root **rose** through 1.20. Its rate is read from the two positions.
- A robust change in (1.20, 1.55) at D 18 and none in that range at D 18.0625 mean it **fell** through 1.20.
- Any other pattern is reported as found, with no reading.

The rate is then compared with the 1.3885 root at D 18.25: can one track join them at a rate between the two bases, or are they two roots? (Decision it informs: whether the fast root is a mode that rises from below toward #1025's band near 2, the inner target 1.997, or one that falls away.)

How I apply them (`read_scanlow_1025.py`, six planted cases as wanted: rose, fell, a root at 1.40 only at D 18.0625, two changes at D 18, a STOP-level repeat, and no change at both): the "robust change" and its position are those `d18f_read.py window` prints (the det-linear estimate and the four-estimator range [lo, hi]); "a robust change in (1.20, 1.30)" means the change's bracket lies inside that interval; the rate is (position at D 18.0625 minus position at D 18) / 0.0625, with the extremes of the two ranges beside it; the comparison with D 18.25's root prints the rates a track would need from D 18.0625 and from D 18 to 1.3885 (range [1.388522, 1.388581]) and leaves the comparison to the coordinator. A STOP-level message of the reader (a repeated point disagrees) is flagged and the pattern is then reported without a reading.

## The tool and the commands, quoted from xfkappa's (ii) (`I1025-mac/d18/lane_d18f.sh` at raw origin/main; the criteria are in `d18_criteria.log`, 16:17:22 UTC)

```
L=$($PY -c 'print(",".join(f"{1.20 + 0.05 * i:.2f}" for i in range(8)))')
hyb 3600 $REC $ST25 18.25 $L $LOW $Q/d1825_low.log                                   # d18_hybsign.py REC STATE D LAMS OUT
P=$($PY $Q/d18f_read.py refine 18.25 1.20 1.55 $REF,$Q/d1825_scan_1025.jsonl,$LOW)     # exit 4 if there is none or more than 4 brackets
hyb 3600 $REC $ST25 18.25 $P $LOWF $Q/d1825_lowfine.log
$PY $Q/d18f_read.py window 18.25 1.20 1.55 $REF,$Q/d1825_scan_1025.jsonl,$LOW,$LOWF
```

Mine, per state (`scanlow_driver_1025.py`): the same four steps with lambda 1.00 to 1.55 (12 points at 0.05, `1.00 + 0.05 * i` for i in 0 to 11) and no earlier scan file; `REF` (the check's file, `d18_refsign_1025.jsonl`) is in the refine and the window as in (ii). `window` is run twice: as in (ii) with REF (its 1.20 point repeats xfkappa's check; a repeat must agree, same sign and ln|det| to 1e-6), and without REF (my points only), because the repeat compares a value from the Mac with one from this laptop; if they differ by more than 1e-6 the first reading prints "STOP-level", and the second is then the reading on my points alone, stated as such. More than 4 brackets stops that state and is reported (as in (ii)); no bracket goes straight to the reading.

## Inputs (raw origin/main by `git show`, `git hash-object --no-filters`; `prep_scanlow_inputs_1025.log`)

| item | raw path | blob |
|---|---|---|
| scanner | `I1025-mac/d18/d18_hybsign.py` | e089207a61fbd98614716abd309571cbc4888db2 |
| readers | `I1025-mac/d18/d18f_read.py` (imports d185_scan_read.py, d18c_read.py, d18d_read.py) | 5fb96dceb427e965b830b42db5b8f30255f20532; 7c9d400f, 1383470f, 6b608903 |
| the check's file (REF) | `I1025-mac/d18/d18_refsign_1025.jsonl` | 3e2d8b4e8f72943983fab091730629464b04e854 |
| D 18.0625 state, record | `I1025-mac/d18/sol_l1kc63Wm1025_D18.062500.npy`; `l1kc63Wm1025.jsonl`, the leap's D 18.0625 line | f2307f0e8ffb4621b61f74450a920c652981d973; 08f4dbf367edba55814e5cf989ccd32a9a5dbe67 |
| D 18 state, record | `I1025-win/out/sol_l1kc63W1025_D18.000000.npy`; `l1kc63W1025.jsonl`, the D 18.0 line | 45e72c6a5c22ee3f0196f7b08f07fecfe3a07b21; c33039dfa38b495486fb3ef7da77077d43db775a |
| D 18.25 test data (xfkappa's (ii)) | `I1025-mac/d18/d1825_low_1025.jsonl`, `d1825_lowfine_1025.jsonl`, `d1825_scan_1025.jsonl` | b2ba7229, 35fde209, a66a2a4a |

Code: scans from worktree `choptuik-i1025-lowd` at 505d8399 (`P4_WT_MATTER`; the solver code xfkappa's lane pins), readers from `choptuik-i1025d` at 48c36355 (`ell_delta.py`, which his lane pins), PY `venv-md510`, BelowNormal, 4 BLAS and rayon threads per scan process. The system check of both states passed on 2026-11-21 (D 18: F 2.6298e-10 against 2.6303e-10, 2552 steps; D 18.0625: F 2.6781e-10 against 2.6754e-10, 2540 steps; `I1025-win/d18ref120`), and `d18_hybsign.py` checks it again at the start of every call.

## Tests of the tool here, before the run

`d18f_read.py selftest`: PASS (6 planted cases); `selftest --mutate=refine`: FAIL, as it must. On xfkappa's own D 18.25 data (the three files above plus the check's) it reproduces his (ii): `refine 18.25 1.20 1.55` gives 1.36,1.37,1.38,1.39; `window 18.25 1.20 1.55` gives one robust change in (1.38, 1.39), plus to minus, det-linear 1.388522, range [1.388522, 1.388581], no ln|det| minimum without a change, repeats 1.20 and 1.55 agree to 0.0e+00, float64 sign changes in (1.40, 1.45) and (1.50, 1.55) (`vtest/d1825_reader_control.log`).

## Run

`scanlow_driver_1025.py` (launcher `start_scanlow_1025.cmd`, BelowNormal): checks the pins, runs the two states in parallel, one process each, and applies the readings. Every child has a cap of 6 h (21600 s) and is killed at the cap by its exact pid (`taskkill /PID <pid> /T /F`; tested on dummy children, `scanlow_driver_selftest.log`). The coarse scan takes 12 points at about 850 to 980 s with two processes together (the D 18.125 scan averaged 800 s, the first point of a call 980 s), so about 3 h; the fine scan 4 points per bracket, about 1 h per bracket; the end about 5 h after the start, as the coordinator expects. Output: `scanlow_w.log`, `scan_*_coarse_1025.jsonl`, `scan_*_fine_1025.jsonl`, the filtered logs, `rows/refine_*.log`, `read_D18.0625.log`, `read_D18.log` (with the check file), `read_D18.0625_noref.log`, `read_D18_noref.log`, `read_scanlow_1025.log` (the readings), `rows/scanlow_samples.csv` (a sampler, `sample_driver3_1025.ps1`, every 60 s: each python's cpu seconds, working set, private bytes and their peaks, and the laptop's memory and load). No RESUME.

## Status

Not started (18:20 UTC).
