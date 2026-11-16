# I910-rpi5: where the sigma-model's least |F| at fixed Delta is lowest, on a finer grid at D 10.5 (Raspberry Pi 5)

Machine rpi5 (Raspberry Pi 5 Model B, aarch64 Linux, 4 cores, 8 GB), issue
https://github.com/nmoinvaz/choptuik-large-d/issues/910 (`solver/matter/sigdss_band.py profile`, depends on #909, whose
raw folder is `I909-rpi5/`). `run910.sh` has the issue's two commands as written, with `$PY`, `nice -n 10` and `2>&1`
added, and the exit statuses recorded: fine A from `I907-winb/walk3_up_10.5.npy` (Delta 1.125743), Delta 1.130 up to
1.140 in steps of 0.001, and fine B from `I897-winb/walk2_hi_10.5.npy` (Delta 1.137324), the same eleven values
descending, both with `--maxjac 60 --settle 5`, at once with `OPENBLAS_NUM_THREADS=2` each. Worktree
`~/Source/choptuik-large-d-909` (wip/i909-rpi5 at origin/main eb562150, which has 42a3e4b0 as an ancestor, never
committed), reused as the coordinator said. Outputs: `fineA.log`, `fineB.log`, `fineA.jsonl`, `fineB.jsonl`,
`exits_910.txt`, `env.txt`.

Started 2026-11-16 06:44:32 UTC, `910 done` 07:02:10 UTC (17 min 38 s). numpy 2.5.4, scipy 1.18.1, python 3.13.7, aarch64
glibc 2.42 (`env.txt`), worktree commit eb562150, never committed (`git status` clean).

## Result

By the frozen rule the reading is **between 0.002 and 0.004, reported**: the parabola minima through each sweep's three
lowest points are at Delta 1.133391 (sweep A, from the ascending end) and 1.136895 (sweep B, from the descending end),
3.505e-3 apart. Both runs exit 0 with Delta held at all 11 points of each, no point reached the cap of 60 Jacobians
(3 to 7 used), and sweep B's minimum is the sharp one while sweep A's is flat.

| acceptance (frozen in #910) | verdict |
|---|---|
| both runs exit 0 with Delta held at every point | yes: `exits_910.txt` fineA 0, fineB 0; `held` true at all 11 points of each |
| each sweep's minimum location from a parabola through its three lowest points | A: Delta 1.132, 1.133, 1.134 (\|F\| 1.0183e-08, 1.0146e-08, 1.0150e-08), vertex **1.133391**, parabola minimum \|F\| 1.0143e-08; B: Delta 1.136, 1.137, 1.138 (1.2774e-09, 1.1688e-09, 1.3349e-09), vertex **1.136895**, parabola minimum \|F\| 1.1673e-09; both triples adjacent, curvature positive |
| location agrees (difference at most 0.002) | no: the difference is 0.003505 |
| location differs (difference more than 0.004) | no: 0.003505 is below 0.004 |
| between: reported, with the Jacobians per point and any point at the cap | difference 0.003505; Jacobians A 6 to 7, B 3 to 6 (jsonl `jac`, which counts a stalled Jacobian), none at the cap of 60 |

The mean of the two locations would be 1.135143 and half their difference 0.00175, but the rule gives no estimate in
this band, so none is claimed. Newton's estimates from the walks' ends, quoted in the issue, are 1.1378 and 1.13775;
sweep B's vertex is 0.0009 below them, sweep A's 0.0044 below.

### The points (`read910.py`, output `readings_910.txt`)

### sweep A

| Delta | least \|F\| | Jacobians | cap reached | Delta held | smallest sv |
|---|---|---|---|---|---|
| 1.130 | 1.0381e-08 | 7 | no | True | 8.63e-10 |
| 1.131 | 1.0262e-08 | 6 | no | True | 4.45e-10 |
| 1.132 | 1.0183e-08 | 6 | no | True | 4.18e-10 |
| 1.133 | 1.0146e-08 | 6 | no | True | 3.89e-10 |
| 1.134 | 1.0150e-08 | 6 | no | True | 3.62e-10 |
| 1.135 | 1.0196e-08 | 6 | no | True | 3.37e-10 |
| 1.136 | 1.0283e-08 | 6 | no | True | 3.19e-10 |
| 1.137 | 1.0412e-08 | 6 | no | True | 3.10e-10 |
| 1.138 | 1.0577e-08 | 6 | no | True | 3.12e-10 |
| 1.139 | 1.0781e-08 | 6 | no | True | 3.24e-10 |
| 1.140 | 1.1020e-08 | 6 | no | True | 3.44e-10 |

three lowest: Delta 1.132, 1.133, 1.134 (|F| 1.0183e-08, 1.0146e-08, 1.0150e-08), adjacent; parabola curvature positive; vertex Delta 1.133391, parabola minimum |F| 1.0143e-08

Delta held at every point: True; points at the cap: none; Jacobians 6 to 7

### sweep B

| Delta | least \|F\| | Jacobians | cap reached | Delta held | smallest sv |
|---|---|---|---|---|---|
| 1.130 | 4.2525e-09 | 4 | no | True | 3.89e-11 |
| 1.131 | 3.6792e-09 | 3 | no | True | 4.66e-11 |
| 1.132 | 3.1180e-09 | 4 | no | True | 5.92e-11 |
| 1.133 | 2.5745e-09 | 6 | no | True | 7.38e-11 |
| 1.134 | 2.0627e-09 | 6 | no | True | 8.84e-11 |
| 1.135 | 1.6099e-09 | 6 | no | True | 1.02e-10 |
| 1.136 | 1.2774e-09 | 6 | no | True | 1.14e-10 |
| 1.137 | 1.1688e-09 | 6 | no | True | 1.24e-10 |
| 1.138 | 1.3349e-09 | 5 | no | True | 1.33e-10 |
| 1.139 | 1.6958e-09 | 5 | no | True | 1.39e-10 |
| 1.140 | 2.1540e-09 | 5 | no | True | 3.09e-10 |

three lowest: Delta 1.136, 1.137, 1.138 (|F| 1.2774e-09, 1.1688e-09, 1.3349e-09), adjacent; parabola curvature positive; vertex Delta 1.136895, parabola minimum |F| 1.1673e-09

Delta held at every point: True; points at the cap: none; Jacobians 3 to 6

locations: A 1.133391, B 1.136895, difference 0.003505
reading by the frozen rule: between 0.002 and 0.004, reported

### Notes

- The vertex of sweep A rests on a flat minimum. Its three lowest |F| differ by 0.36% (second difference 0.4% of |F|),
  and the points from 1.131 to 1.136 are within 1.4% of the lowest. The vertex's sensitivity to a change of each of the
  three |F| (my arithmetic, not part of the rule, not an error bar; the vertex moves by up to 0.012 when a corner's
  curvature nears zero):

  | each of the three \|F\| changed by up to | vertex range, A | vertex range, B |
  |---|---|---|
  | 0.05% | 1.133217 to 1.133757 | 1.136893 to 1.136898 |
  | 0.1% | 1.133100 to 1.145223 | 1.136890 to 1.136901 |
  | 0.5% | 1.132760 to 1.133468 (3 of 8 corners have no minimum) | 1.136866 to 1.136922 |

  The last Jacobians of each point lowered |F| by 0.01% to 0.13% (A: 0.01% to 0.03%, B: up to 0.13% at 1.138 and
  0.10% at 1.140), so the least |F| of each point is stable at that level, not shown to be a floor.
- Each point ended by the settle rule (5 Jacobians in a row each lowering |F| by less than 1%), not by the cap.
- The walls of the two sweeps in `exits_910.txt` are both 1058 s because the script waits for A first; sweep B's own last
  point was at 933 s (`fineB.log`) and sweep A's at 1058 s (`fineA.log`).
- `run910.sh` is mine (the issue gave commands): the issue's two commands as written, with `$PY`, `nice -n 10`, `2>&1`,
  the exit recording and `OPENBLAS_NUM_THREADS=2` added. The logs carry the same `RuntimeWarning` lines
  (overflow, invalid value) as in #909.

### Discrepancies

None against the issue's text.

### Recommended tasks

- **A finer grid and a sharper condition near the minimum of sweep A.** Rerun sweep A on Delta 1.1320 to 1.1350 in steps of
  0.0005 with `--settle 10`, and report the parabola through the three lowest. Acceptance: the vertex is reported with
  its move under a 0.1% change of each of the three |F|, and the two locations (A and B from #910) are compared with the
  0.002 and 0.004 lines. Depends on #910.
