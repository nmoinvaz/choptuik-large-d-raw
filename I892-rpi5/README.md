# I892-rpi5: sigdss at eta = 0.3, does the smoothness prior hold Delta at D 9 to 11 (Raspberry Pi 5)

Machine rpi5 (Raspberry Pi 5 Model B, aarch64 Linux, 4 cores, 8 GB, Ubuntu), issue
https://github.com/nmoinvaz/choptuik-large-d/issues/892 (follows #846 and #859, matter/SIGMA_DSS.md 11). Script (the
coordinator's, md5 7ab78065, unedited): `run892.sh`, run from `solver/matter/` of the worktree
`~/Source/choptuik-large-d-892` (wip/i892-rpi5 at origin/main 5311991e, never committed), numpy only, one process
at nice 10, `OPENBLAS_NUM_THREADS=2`, the five walks two at a time.

Order: `sigdss_band.py width` at the six march states (D 8.0 without a prior is the control; D 9.0, 10.0, 10.5 from
`data/sigdss_m03up.npz`, D 10.5 and 11.0 from `data/sigdss_m03hi.npz`), the 20-Jacobian control walk from D 8.0,
then the five walks without the prior (up to 150 Jacobians each), then `width` at each walk's end.
Exits and wall times: `exits_892.txt`; versions: `env.txt`; each command's stdout and stderr: `<name>.log`;
JSON records: `width.jsonl`, `walk.jsonl`, `walk_*.jsonl`, `width_end.jsonl`; the walks' end states: `walk_*.npy`.

## Result

Started 2026-11-16 01:45 UTC, finished 03:07 UTC (1 h 22 min; the estimate was about 3 h, a Jacobian took 9 to 12 s).
18 commands, 17 exit 0 and `width_hi_11.0` exits 1 (the two g disagree, below). `env.txt`: numpy 2.5.4, scipy 1.18.1,
python 3.13.7, worktree commit 5311991e (never changed, `git status` clean at the end). `read892.py RAW` makes
`readings.txt` from the jsonl records.

### Control (D 8.0, no prior)

The 20-Jacobian walk settled after 1 Jacobian (Delta moved 6.2e-10 in one step, below `--dtol 1e-9`). Delta moved
6.2e-10 against W = 6.64e-8: within its width, so the readings went on. (The walk did not run 20 Jacobians: its own
stopping rule ended it, as it does when one step is below dtol.)

### Widths at the six march states

W = g |F| with g the SVD one, as the tool prints it. "Newton" is Newton's Delta step.

| state | Delta | \|F\| (no prior) | g (SVD) | W | Newton | g pair |
|---|---|---|---|---|---|
| m03up D 8.0 (control) | 1.171732918 | 6.7e-13 | 9.964e4 | 6.64e-8 | -2.6e-10 | agree (1.8e-12) |
| m03up D 9.0 | 1.164945055 | 3.4e-12 | 4.896e5 | 1.68e-6 | +5.1e-8 | agree (9.9e-11) |
| m03up D 10.0 | 1.154559202 | 3.2e-9 | 1.579e6 | 5.04e-3 | -2.80e-3 | agree (8.4e-9) |
| m03up D 10.5 | 1.112502242 | 8.4e-7 | 7.274e6 | 6.13 | +2.87e-2 | agree (4.1e-7) |
| m03hi D 10.5 | 1.139109365 | 2.6e-9 | 2.423e6 | 6.28e-3 | -1.19e-3 | agree (7.9e-11) |
| m03hi D 11.0 | 1.117461404 | 1.2e-8 | 3.9313e7 | 4.60e-1 | -1.319e-1 | **disagree (1.7e-5)** |

The coordinator's Mac values (D 8.0, 10.0, 11.0) match to the digits given, except Newton's step at D 8.0 (Pi -2.6e-10,
Mac -3.4e-9; |F| 6.7e-13 and the smallest singular value 1.7e-8 put it at roundoff).

The acceptance line "width's two g agree in every run" fails at m03hi D 11.0: g = 3.931301e7 (SVD) against 3.931234e7
(solve), relative 1.7e-5 against the 1e-6 bar. The cause is the conditioning, not the code: the smallest singular
value is 3.6e-12 against s_max 98 (condition about 3e13), where a double-precision SVD and LU differ at about that level.
W is unaffected at the 1e-5 level, and W above uses the SVD g. The bar and the script are unchanged (the coordinator's
instruction). The other five agree to 4.1e-7 or better, and so do the six widths at the walks' ends (the worst, at
m03hi D 11.0's end, 4.2e-7).

### Readings

Rules (the issue's): prior-held when the walk ends 1e-3 or more from the march's Delta, or does not settle while Delta
moves by more than 1e-3; prior-free when it ends within the march state's own W of the march's Delta and the end's own W
is at most 1e-4; otherwise undecided. "rate" is the change of Delta per Jacobian, the last one and the mean of the last 10.

| state | Delta (march) | W (march) | walk | Delta (end) | end minus march | \|F\| march to end | W (end) | rate | reading |
|---|---|---|---|---|---|---|---|---|---|
| m03up D 9.0 | 1.164945055 | 1.68e-6 | 1 Jacobian, settled | 1.164945055 | -2.2e-16 | 3.4e-12 to 3.4e-12 | 1.66e-6 | -2.2e-16 | **prior-free** |
| m03up D 10.0 | 1.154559202 | 5.04e-3 | 150, not settled | 1.153750697 | -8.09e-4 | 3.2e-9 to 2.34e-9 | 3.70e-3 | -4.52e-6, -4.57e-6 | **undecided** |
| m03up D 10.5 | 1.112502242 | 6.13 | 150, not settled | 1.115098687 | +2.60e-3 | 8.4e-7 to 2.06e-8 | 1.43e-1 | +1.93e-5, +1.95e-5 | **prior-held** |
| m03hi D 10.5 | 1.139109365 | 6.28e-3 | 111, stalled | 1.137696236 | -1.41e-3 | 2.6e-9 to 1.28e-9 | 3.09e-3 | 0 (stalled), -6.3e-6 | **prior-held** |
| m03hi D 11.0 | 1.117461404 | 4.60e-1 | 57, settled by the rule | 1.115934614 | -1.53e-3 | 1.17e-8 to 1.01e-8 | 7.02e-2 | +2.7e-10, -2.3e-5 | **prior-held** (g pair at the march state disagrees, 1.7e-5) |

Notes on each, so that the table is not read as more than it is:

- **m03up D 9.0.** The width alone decides it: W = 1.7e-6 at the march state, so Delta cannot move more than that at its
  own residual. The walk is one Jacobian, and Delta moved one ulp (|F| 3.44e-12 to 3.40e-12).
- **m03up D 10.0.** Delta fell 8.09e-4 in 150 Jacobians, 0.9e-4 under the 1e-3 line, at a rate that is falling
  (-6.3e-6 per Jacobian over the first 10, -4.6e-6 over the last 10, so about 28% in 150) and |F| falling 3.2e-9 to 2.3e-9.
  Newton's remaining step at the walk's end is -1.98e-3, and the first one at the march state was -2.80e-3, so the
  linear estimate of the total move is -2.8e-3, from the walk (-0.81e-3) plus the remainder (-1.98e-3). That is an
  estimate, not a measurement (W at the end is 3.7e-3), and it is why the reading is "undecided" and not "prior-free".
  The walk would need to go on to decide it.
- **m03up D 10.5.** The march state has |F| 8.4e-7 and W = 6.1 without the prior: it is nowhere near a residual zero
  of the system without the prior, so Delta is not fixed by it at all. The walk first moves Delta down for 22
  Jacobians (rate -3.2e-5 at jac 0, falling to -1.8e-6 at jac 20, then -1.7e-5), to a minimum 1.112241931 at jac 21
  (2.6e-4 below the march's Delta), then turns and goes up by +2.6e-5 per Jacobian, falling to +1.9e-5. It ends 2.6e-3
  above the march's Delta, still moving at +1.9e-5, at |F| 2.1e-8 (W 0.14, Newton +2.4e-2).
- **m03hi D 10.5.** The walk ended "stalled" at jac 110, after a step of -2.3e-9 and one of 0, with the rate before
  that at -7.7e-6 per Jacobian and falling, |F| 1.275e-9. It ends 1.41e-3 from the march's Delta, which is inside the
  march state's W (6.3e-3) and inside the end's own W (3.1e-3), so the move is held by the rule's 1e-3 line and not by
  an end that is pinned. Newton's step at the end is +2.9e-4.
- **m03hi D 11.0.** The walk "settled" at jac 56 because one LM step was +2.7e-10, below `--dtol`. The steps before it
  were -2.5e-5 to -4.3e-5 per Jacobian for 56 Jacobians, and the one at jac 47 was also tiny (-2.5e-7) without ending the
  walk. So Delta was still moving at about -2.3e-5 per Jacobian when it stopped, and the "settled" flag is the
  stopping rule's, not a settled Delta. It ends 1.53e-3 from the march's Delta (W at the end 7.0e-2, Newton +9.8e-3).
  m03hi D 10.5 stopped the same way (a step of -2.3e-9 then a stall).

### Files

`<name>.log` per command (18), `exits_892.txt`, `env.txt`, `run892.sh` (unedited, md5 7ab78065), the records
`width.jsonl`, `walk.jsonl`, `walk_*.jsonl`, `width_end.jsonl`, the walks' end states `walk_*.npy` (the start for a longer
walk), `readings.txt` and `read892.py`.
