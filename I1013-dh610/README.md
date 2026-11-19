# I1013-dh610: M = 3 winding counts of the selection multiplier (#995)

Machine: dh610 (Fedora desktop, Linux 7.3, i7-12700, 20 threads, 62 GB). Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1013 (#995's runner step, discovery candidate 3).

Code: worktree `~/Source/cl-995` at fc7dee4d (branch wip/excited-zeros, `solver/inner_stokes/argcount.py`), Python 3.14.10 with numpy 2.5.4, scipy 1.18.1 and mpmath 1.3.0 from the main checkout's `.venv`
(`~/Source/choptuik-large-d/.venv`). 8 workers (`--procs=8`), nice 10, beside #1003's K 49 run (5 procs) and #1009's timings. The commands are xfchecks' (#1013's body).

## Readings, fixed before the runs (xfchecks, #1013)

- **Pilot** (the known M = 3 zero, a stop gate): one zero of sign +1, located at (2.72648, 1.01560) to 1e-4 at xi1 0.2 and again at 0.17, with no unresolved cells. Otherwise stop and report.
- **Control:** step 2 finds the known M = 3 zero at the pilot's place.
- **Persistence:** an M = 1 zero persists when an M = 3 zero of the same sign lies within the known zero's shift, |dA| <= 0.2 and |dw/w_inf| <= 0.25 (the known zero shifts by +0.184 and +0.239). Each M = 3 zero serves one M = 1 zero, the nearest.
- **Report:** each step's count line and zero lines, with the unresolved cells and their causes.

## Steps

1. selftest (must exit 0) and its `--mutate=norecount` (must exit 1);
2. pilot, `--M=3 --A=2.5,3.0 --wf=0.8,1.2 --nA=2 --nwf=4`, tag `pilot_known`, 2 h cap, then `gate1013.py` checks the reading above (it has a control that must fail);
3. the M = 1 candidates' box, `--A=1.9,3.9 --wf=0.2,1.1 --nA=8 --nwf=9`, tag `M3_cand`, 12 h cap;
4. its unresolved cells recounted at xi1 0.25 (seeded by the 0.2 points), tag `M3_cand_r0.25`, 6 h cap;
5. those recounted at xi1 0.17, tag `M3_cand_r0.17`, 6 h cap.

| file | what |
|---|---|
| `run1013.sh`, `gate1013.py`, `common1013.sh` | the driver, the pilot's gate, the paths |
| `logs/` | each step's log (selftest*.log, m3_pilot.log, m3_cand.log, m3_cand_r0.25.log, m3_cand_r0.17.log) |
| `m3/` | the points caches (`points_M3_r*.jsonl`), `count_<tag>.json` and `leaves_<tag>.jsonl` of each count |
| `exits_1013.txt`, `memlog_1013.log` | exits and the alert-only memory log |

Outcome so far: the selftest and its norecount mutation pass and fail as required; the pilot (912 s, 309 points) finds the known zero, but `gate1013.py` fails it on 4 unresolved cells (3 corner points of
no value on the box's high-wf rim, see the issue), so `run1013.sh` stopped at the gate by design (exits_1013.txt) and the candidates' box and the recount rungs have not run. `logs/gate_pilot_control.log` is the
gate's control run after the fact (--mutate=shift: located A moved by 2e-4), which fails on both the shift and the unresolved cells.

## Later orders

- (b), the coordinator's order after the pilot's gate: the pilot's 4 unresolved cells are recounted at xi1 0.25 and, if cells remain, at 0.17 (`run1013b.sh`, tags `pilot_r0.25`, `pilot_r0.17`, `eval1013.py` reads the counts; its control, the pilot's own count alone, fails with 4 unresolved cells). If they resolve (a zero they add is reported with its sign), the driver goes on to steps 3 to 5 above; if a rim cell stays unresolved at every radius it stops there (wf 1.11-1.21, outside step 3's box wf 0.2-1.1) and reports.
- Step 6 (`run1013c.sh`, after step 5 ended normally): xfchecks' second M = 3 box for the upper chain of M = 1 zeros, `--A=3.6,5.1 --wf=0.5,1.3 --nA=6 --nwf=8` (tag `M3_upper`, 12 h cap), then its two recount rungs (xi1 0.25 and 0.17, tags `M3_upper_r0.25`, `M3_upper_r0.17`, 6 h caps).
