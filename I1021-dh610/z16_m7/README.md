# I1021-dh610/z16_m7: box 16's zero at M = 7, by #1027's protocol and rule

Machine dh610 (Fedora 45, i7-12700). Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1021, a #1021 step on the
coordinator's hc message of 20 Nov 2026 (about 04:20 UTC): box 16's M = 3 zero (sign -1) at M = 7, by #1027's protocol
and rule exactly (my #1027 scripts), at xi1 0.25 and 0.2, with the known zero's M = 7 control of #1027 at the same xi1.
Run after K 49's close, 2 processes at nice 10, beside #1031 and #1034 (the build keeps the memory).

Code: `hier_nb.py` of `~/Source/cl-995` (fc7dee4d, clean), venv `~/Source/venv-i1026` (numba 0.68.1, python 3.14.10),
`INNER_NB_RTOL=1e-13` for M = 7 as in #1027, 2 processes per solve.
Inputs: `inputs/z16_m7_inputs.json`, `I1021-mac/m5/z16_m7_inputs.json` of the raw repository at 69ab0429 (xfchecks, fetched
with `git show origin/main:<path>`, sha256 begins 3ba7268d68e19a98): the M = 3 zero's place (A, w/w_inf) = (3.553346605,
0.413172285) (its located value at xi1 0.18: 3.553346604669, 0.413172284516), xi1 0.25, x = B3, C3, B5, C5 = 0.843294116,
0.003092743, 0.24539945, 0.010876743 from the M = 5 fixed-(A, w) solve there (|r_3| 2.3e-7, |F_5/F_3| 0.2913).
Scripts are copies of #1026's and #1027's (`walk1026.py` from I1026-dh610, `walk1027.py` and `eval1027.py` from
I1027-dh610), unchanged; `eval_z16.py` is new.

## Route

#1027's rule compares the M 5 -> 7 shift with the M 3 -> 5 one, so the M = 5 zero of box 16 is needed, and the input gives
a fixed-(A, w) M = 5 solve at the M = 3 zero, not an M = 5 zero. Per radius (0.25, then 0.2):

1. `walk1026.py z16m5` (#1026's outer Newton over fixed-(A, w) M = 5 solves) from the M = 3 zero with B3, C3: the M = 5
   zero Z5 and the M 3 -> 5 shift s35 = |Z5 - Z3|.
2. `walk1027.py z16` (the M = 7 walk) from Z5 with the M = 5 solve's harmonics, F_7 = 0: |F_7/F_5| and |F_5/F_3| at the
   first solve (at Z5), the M = 7 zero Z7 and the shift s57 = |Z7 - Z5|.
3. `walk1027.py z16in` from the input's own point (3.553346605, 0.413172285) with its x, F_7 = 0: the first solve there
   and the M = 7 zero it reaches (information, the coordinator's inputs as given).

The control (`walk1027.py control`, the known zero from its M = 5 zero (2.718579189, 0.999228403) with F_7 = 0) at the
same two radii. #1027 validated it only at xi1 0.15 (|F7/F5| 0.0573, zero (2.719236, 1.000024)); its M = 5 start fails at
0.25 in #1026 (|r_3| 8.3e3), so a control failure here is a result, not a stop.

## Readings (fixed before the runs: #1027's, `eval1027.py` / `eval_z16.py`)

CONVERGES: |F_7/F_5| <= 0.2 at the first solve (at Z5) and the M = 7 walk converges to a zero with s57 < s35. DOES NOT:
|F_7/F_5| >= 0.3, or no M = 7 zero near it (the start or a Jacobian solve fails, or no step lowers |r_1|). UNDECIDED
otherwise (the ratio between 0.2 and 0.3, an iteration cap, or the shift not smaller). Walk convergence is #1027's: the
Newton step from the best point under 3e-4 in A and in w/w_inf.

## Files

| file | content |
|---|---|
| `inputs/z16_m7_inputs.json` | the coordinator's inputs, as fetched |
| `walk1026.py`, `walk1027.py`, `eval1027.py` | the #1026 / #1027 scripts, unchanged |
| `eval_z16.py`, `z16_args.py`, `common_z16.sh`, `run_z16.sh` | the evaluator (selftest, `--break`, `--mutate=shift`), the argument helper and the driver (`exits_z16.txt`, `logs/`, `walks/`, `eval_z16.txt` when it runs) |

## Driver change, 20 Nov 06:22 UTC

The coordinator's rule (hc, 06:17 UTC): a result at xi1 0.25 counts only if this run's own 0.25 control converges; if it fails, only the 0.2 results count. The 0.25 control failed at its start (`walks/walk_control_xi0.25.json`: |r_3| 4.2e1 after the first attempt and three perturbed repeats, 1201 s). `walk_z16m5_xi0.25.json` also stopped at its start (|r_3| 1.7e3): `walk1026.py` starts an M = 5 solve from B3, C3 only (B5, C5 from hier's default), not from the input's four harmonics that xfchecks's solve converged from, so that failure is not a verdict on box 16's M = 5 at 0.25. `run_z16.sh` was stopped by pid (06:22 UTC, while `z16in_xi0.25` was 12 s into its first solve) and `run_z16b.sh` (radii 0.2 only, unit `i1021-z16b`, 06:22:48 UTC) runs the rest. The files of the stopped part stay in `walks/` and `logs/` and `exits_z16.txt` (0.25 results do not count).

## Result, 20 Nov 07:02 UTC (`eval_z16.txt`; the driver's own evaluation before the gate edit is `eval_z16_driver_run.txt`)

No verdict at M = 7 at either radius: #1027's M = 7 control did not converge at 0.25 (start solve |r_3| 4.2e1) or at 0.2 (|r_3| 2.4e-2, |r_5| 9.5e-7, |r_7| 1.0e-9), and the coordinator's rule (hc, 06:3x UTC) makes the control the gate at both radii. Box 16 at 0.2: M = 5 start solve |r_3| 1.7e-4 (no M = 5 zero), M = 7 from the input's point |F7/F5| 0.3140, |F5/F3| 0.3089 at the first solve and |r_3| 1.2e-4, |r_5| 4.8e-6, |r_7| 2.1e-6 at best (no M = 7 zero). The post on #1021 has the table. Evaluator controls: `logs/eval_selftest.log`, `logs/eval_selftest_break.log` (exit 1), `logs/eval_mutate_shift.log` (exit 1), `logs/eval_mutate_ratio.log`.
