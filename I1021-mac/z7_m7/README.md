# I1021-mac/z7_m7: box 7's zero at M = 7 by #1027's protocol and rule, xi1 0.2 only, on the Mac

Machine: the Mac (Apple M5), helper session xfchecks. Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1021, the
coordinator's hc message of 20 Nov 2026 (about 06:50 UTC): box 7's sign -1 M = 3 zero by the route dh610 runs for box 16
(I1021-dh610/z16_m7 at raw 5b72af8c), at xi1 0.2 only, with the known zero's controls at 0.2; #1027's rule unchanged.

Code: `hier_nb.py` of choptuik-large-d at fc7dee4d (worktree `choptuik-large-d-1021nb`, detached, clean), as dh610's.
Venv `/Users/nathan/venv-i1021nb` (new, uv): python 3.14.7, requirements.txt's pins (numpy 2.5.4, scipy 1.18.1, mpmath 1.3.0, ...), numba
0.68.1, llvmlite 0.50.0 (dh610: python 3.14.10, numba 0.68.1). No venv on the Mac had numba. NUMBA_CACHE_DIR is in the
session's scratchpad. `INNER_NB_RTOL=1e-13` at M = 7, as in #1027 (walk1027.py sets it).

Files:
- `dh610_5b72af8c/`: dh610's driver as fetched by `git show 5b72af8c:I1021-dh610/z16_m7/<file>` (`SHA256SUMS`).
- `walk1026.py`, `walk1027.py`, `eval1027.py`, `z16_args.py`: dh610's copies, unchanged (byte for byte).
  `eval1026.py`: I1026-dh610's at raw 245cdef1, unchanged, for the M = 5 control's reading.
- `eval_z7.py`: dh610's `eval_z16.py` with box 7's M = 3 zero (A 3.2454793232694903, w/w_inf 0.34585226845559425,
  located at xi1 0.17, `loc/z7_6da7da7b/`), the stored control's path (`inputs/walk_control_xi0.15.json`,
  I1027-dh610/walks at 245cdef1), xi1 0.2 only, no walk from an input point (box 7 has none: with no M = 5 zero the
  verdict is UNDECIDED), the M = 5 control's reading added, and the selftest's synthetic walks centered on box 7's
  zero instead of box 16's (`eval_z7.diff`).
- `common_z7.sh`, `run_z7.sh`: dh610's `common_z16.sh`, `run_z16.sh` with the Mac's paths, xi1 0.2 only, 1 process
  per solve (dh610: 2) and each walk's cap twice dh610's, the M = 5 control (`walk1026.py control5` from the known
  zero's M = 3 place with its M = 3 harmonics, #1026's control, which must reach the stored M = 5 zero within 1e-5),
  and the compiled backend's checks of `inner_nb_checks.sh` (fc7dee4d), with their logs here instead of the worktree.
- `inputs/z7_start.txt`: box 7's M = 3 zero and its M = 3 harmonics (B3, C3), from `m5/z7_start.txt`.

Readings (fixed before the run; #1027's, `eval1027.py` through `eval_z7.py`): CONVERGES: |F_7/F_5| <= 0.2 at the
first solve (at the M = 5 zero Z5) and the M = 7 walk converges with s57 = |Z7 - Z5| smaller than s35 = |Z5 - Z3|.
DOES NOT: |F_7/F_5| >= 0.3, or no M = 7 zero near it. UNDECIDED otherwise, or when no M = 5 zero is found. The M = 7
control was validated only at 0.15 (#1027), so its result at 0.2 is reported, not a gate.

A first start (06:51:54 UTC) failed at import, every step at once: the venv had numpy, scipy and numba only, and
inner_np.py imports mpmath (`start0_no_mpmath/`). With requirements.txt's pins installed the driver was started again at
06:53:11 UTC; the evaluator's and the compiled backend's checks then give their expected exits (`exits_z7.txt`).

The gate (the coordinator, 20 Nov about 06:56 UTC, before any M = 7 solve of box 7 had ended): an M = 7 result at xi1
0.2 counts only if #1027's M = 7 control converges at 0.2 in the same run; otherwise it is reported as no verdict at
M = 7, with the control's residual. `eval_z7.py` applies it (`gated`, `ctrl_res`): with the control failing, the z7 line
reads NO VERDICT, followed by what the ratios and shifts alone give and the control's last residuals. The selftest checks
the gate (`logs/eval_gate_selftest.log`, exit 0), and `--mutate=nogate` drops it and must fail
(`logs/eval_gate_selftestmutate=nogate.log`, exit 1). The run's final `eval_z7.py` call reads the gated file.

xi1 0.2 (06:53-07:06 UTC; `exits_z7.txt`, `eval_z7.txt`, `logs/`, `walks/`; driver `run_z7_v181e77d6.sh`, the
evaluator as gated below): #1026's M = 5 control PASSES, zero (2.718579192, 0.999228404), 2.9e-9 and 5e-11 from the
stored one (7 solves, 86 s). #1027's M = 7 control FAILS: its start solve at the known zero's M = 5 zero stays at
|r_3| 5.6e-3 after the three repeats (|r_5| 1.4e-6, |r_7| 2.7e-10, |r_1| 57.6, |F_7/F_5| 0.0573; dh610's box 16 run
at 0.2: 2.4e-2). Box 7's M = 5 walk fails at its start solve (|r_3| 6.3e4, |r_5| 1.8e2; `hier_nb.py` prints start
residuals 0 for r_1 and r_3, the radii LazyHier has not integrated yet), so the M = 7 walk did not run. Reading: NO
VERDICT at M = 7 at 0.2, by the gate (the M = 7 control's residual above).

xi1 0.15 (`xi015/`, `run_z7.sh 0.15`, from 07:07 UTC): the coordinator's order (about 07:00 UTC) after both controls
failed at 0.2 in dh610's box 16 run. The control was validated at 0.15 in #1027. The same route at 0.15, with #1026's M = 5
and #1027's M = 7 controls as gates (`eval_z7.py --xi 0.15` gates on both at every radius; at 0.2 the M = 5 control
passed, so its reading is the same). `run_z7.sh` now takes the radius; the 0.2 run read `run_z7_v181e77d6.sh`.

xi1 0.15 result (07:07-07:23 UTC, `xi015/`): the evaluator's and backend's checks give their expected exits again.
#1026's M = 5 control FAILS: its walk stops at "no step reduced |r_1| with a converged solve (five halvings)" after 15
solves (every |r_3| <= 6.6e-8), best |r_1| 2.1e-2 against the criterion's 1e-2, at (2.718582533, 0.999229421), 3.3e-6 in
A and 1.0e-6 in w/w_inf from the stored zero. dh610's control at 0.15 failed the same way (|r_1| 1.4e-2), and the
coordinator keeps it a fail. On the coordinator's word the driver was stopped by hand at 07:20:26 UTC, before box 7's
walks. #1027's M = 7 control was already running and finished at 07:23 (4 solves): PASS, zero (2.719239, 1.000026),
(-1.4e-6, +6.1e-7) from #1027's, |F_7/F_5| 0.0573 at the M = 5 zero (stored 0.0574). Reading (`xi015/eval_z7.txt`,
`eval_z7.py --xi 0.15` by hand after the stop): NO VERDICT at M = 7 at 0.15, by the M = 5 control's gate. The no-verdict
line now gives each failed control's own residuals. The first 0.15 reading named the M = 7 control's residuals instead,
and was fixed before it was used. `logs/eval_z7_rerun.log` is the 0.2 reading with that text, with the same verdict.
