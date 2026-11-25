# I1025-macm3/kc_d23_secant: secant refinement of lambda_1 at D 23.0 at k_c 87 and at k_c 95, to set beside the k_c 103 root 0.026505

Machine macm3 (Apple M3, 24 GB; runner macm3b, session me2). Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1025. Written 2026-11-25 23:52 UTC 2026-11-25, **before any run of this folder**.

## Order (coordinator t5, hc 25 Nov ~23:50 UTC), verbatim
"excellent: 0.026505, bracket 5e-6. After the D 23.0625 k_c 103 scan (and its secant refinement), refine with the same tool at D 23.0: k_c 87 (your part c2 state, bracket -0.040..-0.020) and k_c 95 (win2's accepted state raw I1025-win2/kc95_d23, blob 096f1cc0, record e3fff23f, bracket 0.000..0.020), tol 1e-5, pinned, one process each (they can run side by side). Register each inside its scan's estimator range. Then post on #1025 with the three-k_c table at D 23.0."

## Why
The k_c 103 root at D 23.0 is 0.02650535 (secant, `kc103_d23/secant/`) against the scan's det-linear 0.028275 and range [0.023982, 0.028275]. The scans' det-linear numbers at k_c 87 (-0.021546) and k_c 95 (+0.015921) are the upper ends of their estimator ranges, so the k_c steps (+0.0375, +0.0124 unrefined) are not yet comparable to the refined k_c 103 value. This folder refines the other two with the same tool. The k_c roots are not yet physical.

## Inputs (copies in `in/`, `kc87/`, `kc95/`; `in_blobs.txt` lists their blobs; each lane refuses any other blob)
| item | source | blob |
|---|---|---|
| k_c 87 state at D 23.0 (my part c2, **REDUCED QUALITY**: psi-constraint 1.0496e-2) | raw `I1025-macm3/kc87_leg2/c2/sol_l1kc87Lmacm3c2_D23.000000.npy` (commit efb772ac), pinned copy of the scan `kc87_leg_lambda/23.0/in/` | bb32ff05 |
| its record (2 rows: D 22.9375 and 23.0; the tool takes the row of D) | `l1kc87Lmacm3c2.jsonl` | 2dda16f7 |
| the k_c 87 scan (22 evaluations, -0.10 to 0.30; one change (-0.040, -0.020), '+ to -', det-linear -0.021546, range [-0.035344, -0.021546]) | `kc87_leg_lambda/23.0/scan/scan_D23.0_1025.jsonl`, `read_lower.txt` | ecdc637d, acff1e58 |
| k_c 95 state at D 23.0 (win2's accepted regrid of the state above; reduced-quality lineage, k_c 95 constraint 7.67e-3) | raw `I1025-win2/kc95_d23/sol_l1kc95win2d23_D23.0000.npy` | 096f1cc0 |
| its record (1 row) | `l1kc95win2d23.jsonl` | e3fff23f |
| win2's k_c 95 scan (19 values and a repeat; one change (0.000, 0.020), '+ to -', det-linear 0.015921, range [0.002668, 0.015921]) | raw `I1025-win2/kc95_d23/scan_D23.0_all.jsonl` (commit 3a4b4d557), `read_lower.txt` | 2b31cf9b, e661bac0 |
| `capped_run.py`, `summarize_point.py` (the leg lane's, numbers from the files) | | 11f0647b, a4da8dc4 |
Code: worktree `~/Source/choptuik-large-d-1025s` at 6010e37b (wip/ell1-speed; `d18_secant.py` a3d90cd5, `ell_fastm.py` 93f963f6, `ell_fastdd.py` 237ebfdd; `dss_ell.py`, `ell_ddm.py`, `ell_dd.py`, `ddnp.py` equal the scan worktree's 505d8399), `venv-macm3-1058b` (python 3.14.3, multidouble 5.1.0; t5 accepted it for `venv-1025dd`). The setup and controls of SPEED_ELL1.md ran once for these blobs (`kc103_d23/secant/checks/`: all selftests and controls as wanted); each lane repeats the `d18_secant.py` selftest and its three mutations (wanted exits 0 1 1 1).

## Commands (`secant2.sh kc87|kc95`, launched detached by `launch_1070.py` under `caffeinate -is`; stops go to t5 by hc), one process each, nice 10, cap 18000 s by `capped_run.py`
    d18_secant.py run in/<record> in/<state> 23.0 <LO> <HI> <case>/secant/secant.jsonl --tol=1e-5 --maxev=10 --pin=<state blob>,<record blob>
k_c 87: `-0.040 -0.020`, pin bb32ff05,2dda16f7. k_c 95: `0.000 0.020`, pin 096f1cc0,e3fff23f. No `--ends` (both ends evaluated), default fast float64 matrix and ell_ddm's block 12. Read by `summarize_point.py` from the files; the root is read by position: the final bracket and the det-linear root inside it; the scan's estimator range is a spread over interpolation choices, not an enclosure.

## Registered (mine, information; t5's is the first of each)
**Each root lies inside its scan's estimator range** (t5's register): k_c 87 in [-0.035344, -0.021546] 80%, k_c 95 in [0.002668, 0.015921] 80%. At k_c 103 the refined root sat 59% of the way from the lower end of the range to the det-linear end (0.026505 in [0.023982, 0.028275]); taking the same fraction (a weak analogy: SPEED_ELL1.md's k_c 55 case sat at 89%) gives k_c 87 about **-0.0272** and k_c 95 about **+0.0105**; k_c 87 within 0.004 of -0.0272 about 55%, k_c 95 within 0.004 of +0.0105 about 55%; each below its scan's det-linear 85%. Then the refined steps are +0.0377 (87 to 95) and +0.0160 (95 to 103): both positive 95%, the second smaller than the first 85%, their ratio between 0.3 and 0.6 about 65%.
**The runs.** Exit 0 (bracket at most 1e-5 within 10 evaluations) 80% each; both ends robust (dln at most 0.1) 85% each; evaluations including the ends 5 to 9 about 80% each; the ends' ln|det| differ from the scans' by at most 3e-3 about 85% (k_c 87, my own scan) and 75% (k_c 95: win2's scan was by the complex step on Windows); the float64 sign (fast matrix alone) differs from the hybrid sign at one or more evaluations 70% each (k_c 103: 3 of 7). Per evaluation (one process each beside the k_c 103 scan of D 23.0625): k_c 87 3 to 7 min and k_c 95 4 to 8 min about 70% each (k_c 103 took 5.3 to 9.1 min, mean 7.3); total wall 20 to 60 min (k_c 87) and 25 to 70 min (k_c 95) about 70% each. Peak RSS below 5 GiB 85% each. No memory alert 90%, no Traceback 95%.
**Starting.** t5 said "after the D 23.0625 k_c 103 scan (and its secant refinement)". The machine has free cores (the scan of D 23.0625 runs on 2 processes), t5 accepted the same overlap for the D 23.0 secant and the leg, and the two runs are deterministic one-process jobs that can be killed by exact pid: I start both as soon as the dry runs pass and tell t5 at once; a "wait" from t5 is obeyed by killing them.

## Status
- 2026-11-25 23:52 UTC: folder, README (registration), lane script and pins written; pushed first; dry runs next, then both lanes.
- 2026-11-25 23:53 UTC: both lanes started (`secant2.sh kc87` lane pid 34087, `secant2.sh kc95` lane pid 34204; one `d18_secant.py` process each, nice 10; dry runs 23:53:02 UTC passed: pins, `d18_secant.py` selftest 0 and its mutations 1 1 1). Both print "the record system" (k_c 87: |F| 3.4968757434e-10, 2864 steps; k_c 95: state |F| 3.3713160876e-10, record 3.3831738778e-10, 3127 steps). They run beside the scan of the k_c 103 leg's D 23.0625 (2 processes); t5's order says "after" that scan and its refinement: told t5 at once (hc 23:5x UTC).
- 2026-11-25 23:57 UTC: t5 (hc, quoted): "leave both refinements running beside the scan; fine." The lanes continue; nothing changed.
