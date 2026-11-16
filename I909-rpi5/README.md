# I909-rpi5: the sigma-model's least |F| at fixed Delta at D 10.5, eta 0.3, from both branch ends (Raspberry Pi 5)

Machine rpi5 (Raspberry Pi 5 Model B, aarch64 Linux, 4 cores, 8 GB), issue
https://github.com/nmoinvaz/choptuik-large-d/issues/909 (`solver/matter/sigdss_band.py profile`, depends on #907).
`run909.sh` has the issue's three commands as written, with `$PY`, `nice -n 10` and `2>&1` added, and the exit statuses
recorded: sweep A from `I907-winb/walk3_up_10.5.npy` (Delta 1.125743), Delta 1.120 up to 1.142; sweep B from
`I897-winb/walk2_hi_10.5.npy` (Delta 1.137324), the same twelve values descending, both at once with
`OPENBLAS_NUM_THREADS=2` (the coordinator's instruction), then the control `--mutate dfree` (required exit 1).
Worktree `~/Source/choptuik-large-d-909` (wip/i909-rpi5 at origin/main eb562150, which has 42a3e4b0 as an ancestor, never
committed). Outputs: `sweepA.log`, `sweepB.log`, `profile.jsonl`, `profileB.jsonl`, `control_dfree.log`, `exits_909.txt`
(each command's exit status against the required one and its wall time), `env.txt`.

Started 2026-11-16 06:26:47 UTC, `909 done` 06:40:35 UTC (13 min 48 s; the issue estimated about 30 min on winb, and the
Mac took 7 s per Jacobian, here it was about 16 s with both sweeps running). numpy 2.5.4, scipy 1.18.1, python 3.13.7,
aarch64 glibc 2.42 (`env.txt`), worktree commit eb562150, never committed (`git status` clean).

## Result

By the frozen rule the reading is **branch decides**: the two sweeps' least |F| differ by more than a factor 3 at 6 of
the 12 points (half), so Delta alone does not fix the residual, and with this solver at kc 15 the question of one or two
solutions is not answerable from this run. Sweep A (from the ascending branch end) stays between 1.01e-8 and 1.32e-8 at
every Delta, with no dip. Sweep B (from the descending branch end) falls from 1.02e-8 at Delta 1.120 to 1.29e-9 at 1.136 and
1.34e-9 at 1.138, and rises again to 3.19e-9 at 1.142.

| acceptance (frozen in #909) | verdict |
|---|---|
| both sweeps exit 0, Delta held at every point | yes: `exits_909.txt` sweepA 0, sweepB 0; `held` true at all 12 points of each |
| the control `--mutate dfree` exits 1 | yes: exit 1, `Delta held False` (Delta moved to 1.127044637 against the target 1.128) |
| Delta decides: the two sweeps agree within a factor 2 at every Delta | **no**: the ratio is above 2 at 7 of 12 points (1.130 to 1.142), at most 2 at 1.120 to 1.128 (1.29 to 1.97) |
| a Delta whose \|F\| is below half of both neighbours' in both sweeps | none (the rule applies only if Delta decides; sweep A has no such Delta, sweep B's least, 1.285e-9 at 1.136, is 0.96 of its neighbour 1.136 to 1.138) |
| branch decides: the sweeps differ by more than a factor 3 at half the points or more | **yes**: 6 of 12 (1.132 3.25, 1.134 4.89, 1.136 8.00, 1.138 7.93, 1.140 5.12, 1.142 3.65) |

The line is met by exactly half of the points, and the points nearest to the factor 3 are 1.132 (3.25) and 1.142 (3.65)
on one side and 1.130 (2.43) on the other, so one point more or less at the factor 3 would change which of the two
readings the rule gives.

### The points (`read909.py`, output `readings_909.txt`)

| Delta | A least \|F\| | A Jac | B least \|F\| | B Jac | ratio larger/smaller | A smallest sv | B smallest sv |
|---|---|---|---|---|---|---|---|
| 1.120 | 1.3249e-08 | 5 | 1.0237e-08 | 4 | 1.294 | 9.60e-10 | 1.60e-10 |
| 1.122 | 1.2457e-08 | 4 | 9.0226e-09 | 4 | 1.381 | 4.03e-10 | 1.34e-10 |
| 1.124 | 1.1753e-08 | 4 | 7.8136e-09 | 4 | 1.504 | 5.91e-10 | 1.02e-10 |
| 1.126 | 1.1153e-08 | 4 | 6.6138e-09 | 3 | 1.686 | 7.85e-10 | 6.34e-11 |
| 1.128 | 1.0676e-08 | 4 | 5.4266e-09 | 4 | 1.967 | 7.88e-10 | 2.17e-11 |
| 1.130 | 1.0338e-08 | 4 | 4.2575e-09 | 4 | 2.428 | 7.02e-10 | 1.78e-11 |
| 1.132 | 1.0154e-08 | 4 | 3.1227e-09 | 4 | 3.252 | 6.26e-10 | 3.94e-11 |
| 1.134 | 1.0134e-08 | 4 | 2.0713e-09 | 4 | 4.893 | 5.69e-10 | 4.35e-11 |
| 1.136 | 1.0279e-08 | 4 | 1.2851e-09 | 4 | 7.999 | 5.35e-10 | 5.71e-11 |
| 1.138 | 1.0585e-08 | 4 | 1.3357e-09 | 4 | 7.925 | 5.29e-10 | 7.83e-11 |
| 1.140 | 1.1037e-08 | 4 | 2.1543e-09 | 4 | 5.123 | 5.56e-10 | 9.62e-11 |
| 1.142 | 1.1623e-08 | 4 | 3.1857e-09 | 4 | 3.648 | 6.09e-10 | 3.65e-10 |

Delta held at every point of both sweeps: True
ratios above 2: 7 of 12 (Delta decides needs 0); above 3: 6 of 12 (branch decides needs 6 or more)
sweep A: least |F| 1.0134e-08 at Delta 1.134; below half of both neighbours: none
sweep B: least |F| 1.2851e-09 at Delta 1.136; below half of both neighbours: none
reading by the frozen rule: branch decides

`A smallest sv` and `B smallest sv` are the smallest singular value of J without its Delta column (the three smallest
and the largest are in the logs). Sweep A's are 4.0e-10 to 9.6e-10 (the Mac's, per the issue, near 6e-10), sweep B's are
1.8e-11 to 3.7e-10, smallest at Delta 1.128 to 1.134.

### Notes

- Every point ended by the 1% rule (3 Jacobians in a row that each lower |F| by less than 1%) after 3 to 5 Jacobians, none
  at the cap of 30, so the least |F| is where that rule stopped, not a floor shown to be reached. A: 5, then 4 at every
  other point; B: 4, except 3 at Delta 1.126.
- The walls of sweeps A and B in `exits_909.txt` are both 782 s because the script waits for A first. B's own last point
  was at 759 s (`sweepB.log`), A's at 782 s.
- The logs carry `RuntimeWarning` lines (overflow, invalid value) from `sigdss_solver.py` lines 241 to 248 (24 in each
  sweep, 15 in the control). The same warnings are in the winb logs `I907-winb/walk3_up_10.5.log` and
  `I897-winb/walk2_hi_10.5.log`, so they are not particular to this machine; the run's exit statuses and held checks
  are unaffected.
- `run909.sh` is mine (the issue gave commands, not a script): the three commands as the issue has them, with `$PY`,
  `nice -n 10`, `2>&1`, the exit recording and the environment variable added.

### Discrepancies

None against the issue's text. This run is on the Pi, the issue's estimate and the Mac's 7 s per Jacobian are for other
machines; no comparison with a winb or Mac profile was made, since none is stored (the issue's own Mac note is the
singular values near 6e-10, which sweep A's range 4.0e-10 to 9.6e-10 contains).

### Recommended tasks

- **Run the profile to a floor.** Rerun both sweeps with the stop rule `--settle 10` and `--maxjac 120` (the 1% rule
  stopped every point after 3 to 5 Jacobians) at Delta 1.126, 1.130, 1.134, 1.136, 1.138 and 1.142, and print each
  |F| per Jacobian. Acceptance: each point either reaches a |F| change below 1% in 10 Jacobians in a row or the cap of 120,
  and the ratio of the two sweeps' final |F| at each point is reported with the factor 2 and 3 lines of #909; the readings
  by the rule are given again. Depends on #909.
