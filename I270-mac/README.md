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

RESULTS
