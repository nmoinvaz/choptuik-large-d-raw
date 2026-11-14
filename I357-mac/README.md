# I357-mac: logs of the two-endpoint zero-law test of S1 (planted calibration; the data run was not made)

Machine: Apple M5 Mac (`mac`), xftheory, an hc agent of the coordinator.
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/357

From `solver/harmony/stokes/` of choptuik-large-d (branch wip/xf-theory), venv-314, nice 10, one process:
- `stokes_lines_k22.log`, `.json`: `stokes_lines.py planted --K=22` (exit 3, not decisive). The exact zero search is
  part of this run, about 15 CPU minutes.
- `stokes_lines_k30_40.log`, `.json`: `planted --K=30,40 --cache=...` (exit 3, not decisive at either K).
- `stokes_lines_explore.log`: `explore` (post hoc, the law's error from exact zeros).
- `stokes_lines_k40_d3.log`, `.json`: `planted --K=40 --d=3` (post hoc; the control fires at d = 3).
- `stokes_lines_exact_zeros.json`: the exact zeros of P1 and P2 in |x| < 30 (the cache).

The test was fixed in notes/STOKES_LINES.md §1–§4 (commit c85c93d3) before these runs; the results are its §5.
