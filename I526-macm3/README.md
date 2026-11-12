# I526-macm3: which f64 inputs move the kf 27 zero? One ulp in ph and in a plan boundary, at kf 27 and kf 22 (R 0.0075, D 61.03, M 48)

Machine: macm3 (Apple M3, 24 GB RAM), venv-macm3-314 (Python 3.14.3, python-flint 0.9.0, FLINT 3.6.0, hpkernel cp314 neon, modecount_cx with B = 5), main checkout at de63a118. Prepared 2026-11-12 01:04 UTC. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/526.

ulp_circle.py is #520's wrapper (I520-macm3/ulp_circle.py) with two more branches, as the coordinator approved: `ph I SHIFT` (entry I of the phase weights, a vector of 48) and `seg S K SHIFT` (interior boundary K of segment S of the plan, 4 segments of 4 to 6 boundaries; show_structure/ has the printout); the dh branch is kept. The hook is the same: modecount_cx.CSolver is replaced by a function that passes a copy with the one input changed by SHIFT ulps (np.nextafter, repeated), and hp/modecount_circle.py runs unchanged. Unit-checked on synthetic inputs: ph shift +1 changes only ph[10], by 1 ulp; seg shift +1 changes only seg[1][1]; shift 0 changes nothing; -2 moves a boundary two ulps down. Chosen inputs (arbitrary, stated before the runs): ph[10] = 0.7170... and seg[1][1] = 0.4389384307685937, one ulp up each.
Runs (run_526.sh, one after the other, 1 thread, nice 10, caffeinate -is, an empty cache each), circle 2.043532530673195,0,0.0075, --M=48 --n0=20 --fmax=1e-15: c_seg0 (kf 27, seg shift 0, a control of the wrapper: must reproduce #500's zero 2.043531512269278 - 7.605770534479667e-7i bit for bit), k27_ph, k27_seg, k22_ph, k22_seg, c_ph0 (kf 27, ph shift 0, the second control). Reference: kf 27 plain 2.0435315123 - 7.6e-7i (miss 1.27e-6); kf 22 plain 2.0435325298 + 3.4e-9i (miss 3.6e-9); dh one ulp: kf 27 +1.3e-5 to +4.5e-3.

Written before the run (the issue's). For each input, the zero's shift at both cuts. The input is "a lever" if one ulp moves the kf 27 zero by 1e-6 or more while the kf 22 zero moves by less than 1e-8. Otherwise the plain miss is not explained by these inputs.

## Results


(2026-11-12 05:17 UTC) k27_ph: the zero 2.043531512269278 - 7.605770534479667e-7i is equal to c_seg0's in both floats, the 30 matched determinants are bit for bit those of shift 0 (ln|det| offset 0.0, same pmin). The coordinator's message of 05:16 UTC: the ph weights enter only the phase condition's row of the Jacobian (hp/src/model.rs 779, 1120, 1281; read at de63a118) and mode_matrix_c drops that row and the Delta column (hp/modecount_cx/src/lib.rs 16 and 520), so ph is not an input of det M: not a lever, and no control run is possible. k22_ph was dropped on his instruction: its empty folder was moved away before its turn, so exits.txt has "k22_ph exit 1" (the redirection of its log failed; nothing ran). The segment family (k27_seg, k22_seg) and c_ph0 stay.
(2026-11-12 06:30 UTC, macm3) All runs finished (exits.txt): c_seg0 04:23:04 UTC, k27_ph 04:53:23, k27_seg 05:21:48, k22_ph dropped (exit 1, nothing ran), k22_seg 05:47:42, c_ph0 06:13:28 UTC (started 03:54:06 UTC). Kernel: modecount_cx of 2026-11-06 (B = 5) and the Python hpkernel of 2026-11-09, main checkout at de63a118. Baselines: kf 27 plain = c_seg0 = c_ph0 (the zero 2.043531512269278 -7.605770534479667e-7i, equal to #500's in both floats: both controls pass); kf 22 plain = I506-macm3/kf22_plain (2.0435325297652147 +3.43415048002782e-9i).
| run | perturbation | zero shift | ln\|det M\| offset at the matched points | pmin relative change |
|---|---|---|---|---|
| c_seg0 | seg[1][1] shift 0 (control) | 0.0 | 0.0 (30 points) | 0.0 |
| c_ph0 | ph[10] shift 0 (control) | 0.0 | 0.0 (30) | 0.0 |
| k27_ph | ph[10] +1 ulp, kf 27 | 0.0 | 0.0 (30) | 0.0 |
| k27_seg | seg[1][1] +1 ulp, kf 27 | 6.7e-12 (Re -3.4e-14, Im -6.7e-12) | -8.6e-9 to +9.1e-9 (30) | -5.5e-8 to +6.0e-8 |
| k22_ph | dropped | | | |
| k22_seg | seg[1][1] +1 ulp, kf 22 | 1.0e-12 (Re +2.4e-13, Im +9.9e-13) | -5.7e-9 to +5.6e-9 (30) | -6.5e-9 to +6.3e-9 |
All circles: winding +1, 28 points, 0 mismatches. The coordinator (message of 05:16 UTC): ph enters only the phase condition's row of the Jacobian (hp/src/model.rs 779, 1120, 1281, read at de63a118), which mode_matrix_c drops (hp/modecount_cx/src/lib.rs 16 and 520), so ph is not an input of det M: no lever, no control possible; k22_ph was dropped by moving its empty folder away. Lever criterion (kf 27 zero moves by 1e-6 or more while kf 22 moves by less than 1e-8): ph[10]: kf 27 shift 0.0, not a lever; seg[1][1]: kf 27 shift 6.7e-12, not a lever. The plain miss of the kf 27 control (1.27e-6) is not explained by one ulp of ph or of that plan boundary.
