# I270-mac: D 61.03 M 48 kf 23 on a layout with an inner node at 0.15, and circles at #230's four extra zeros

Machine: mac (Apple M5, 10 cores, macOS 27, shared and loaded by other sessions).
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/270
Code: branch wip/i265 of the code repository, commit 406fefd (#265's 27a258c, then `--centre_tol`). Files
hp/modecount_common.py, hp/modecount_probe.py (`--tolcheck`), hp/modecount_wind.py, hp/modecount_circle.py.
Versions: Python 3.14.7 (/Users/nathan/venv-314), hpkernel 0.1.0 from that venv, hp/modecount_cx from the main
checkout's build (PYTHONPATH /Users/nathan/Source/choptuik-large-d/hp/modecount_cx/build). Nothing was rebuilt.

Every run is from the worktree root, one process at a time, 1 thread, `nice -n 10 caffeinate -i`, through a wrapper
that writes the command, the code commit, the exit code and the wall time into each log (first and last lines).

The reading rule was fixed before the runs, in the issue's "started" comment:
- If the λ_phys control is not +1, or a circle is not resolved, there is no reading.
- If all four circles wind 0, the extras belong to the old layout (first node 0.3).
- If they wind as on #230's layout (+1, +1, +1, +2), they persist, so they do not belong to the layout.
- Anything else is mixed and is reported circle by circle.

## Files

- logs/probe_tails.log: the no-solve probe of the resampled start with `--centre_tol=1e-300` (centre truncation
  1.4e-92 at x = 0.3, 3.0e-219 at 0.15, which sets the check's and the build's T = 1e-150).
- logs/tolcheck.log, tolcheck.json: `hp/modecount_probe.py --tolcheck`, exit 0 (2/2).
- logs/tolcheck_mutate_nocentretol.log: the same with `--mutate=nocentretol`, exit 1 (check 1 fails).
- logs/gatecheck_at_406fefd.log, selftest_at_406fefd.log: #265's check (2/2) and #141's self-test (5/5) at this
  commit.
- logs/circle_*.log: the circle runs (setup's output first), circles/: their determinants
  (modecount_<tag>_evals.jsonl), logs and records (modecount_circles.jsonl), states/: the fitted state.

## Results

The work was stopped early at the coordinator's word (no subagents, to save tokens), so it ends after the control
circle. The four circles at #230's positions were not run to the end, and there is no reading.

The state (states/modecount_state_D61.0264_M48_kf23_ct1e-150.npz) was built by setup inside the control run
(logs/circle_control.log):

    hp/modecount_circle.py hp/data/seeds/local/up23_D61.0264.npz 2.043532530673195,0,0.2 --M=48 --kf=23 --centre_tol=1e-150 --fmax=1e-15 --n0=20 --data=<this folder>/circles --tag=D61.0264_M48_kf23_inner015

| D 61.03, M 48, kf 23 | nodes | ks | \|F\| | centre series | horizon series |
|---|---|---|---|---|---|
| this state | 0.15, 0.3 ... 0.7 | 127 | 1.3e-19 | 3.6e-234 (ratio 0.281 at 0.15) | 6.1e-38 (ratio 0.473 at 0.3) |

The start had \|F\| 1.3e-6, in the horizon block. Newton did not lower it (numpy printed an overflow warning in the
driver's norm), and Levenberg-Marquardt converged. Setup took about 7.5 min.

| circle (R 0.2, n0 20, tol pi/4, alias rule) | winding | points | max step | mismatches | resolved | zero inside (estimate) |
|---|---|---|---|---|---|---|
| lambda_phys 2.043532530673195 (control) | +1 | 28 + 2 | 0.376 | 0 | yes | 2.0435325241 + 1.2e-7 i (6.7e-7) |
| 1.3065 + 1.4158i | stopped | 24 determinants cached | | | | |
| 2.0073 + 0.9727i, 2.5584 + 0.5825i, 3.0196 (real axis) | not run | | | | | |

logs/circle_four.log is the stopped run (exit 143, from SIGTERM, after 1542 s). Its 24 determinants are in
circles/modecount_D61.0264_M48_kf23_inner015_evals.jsonl, which a rerun with the same --tag and --data reuses. The
state must first be copied into the code repository's hp/data, or rebuilt (setup looks for
modecount_state_D61.0264_M48_kf23_ct1e-150.npz there).
