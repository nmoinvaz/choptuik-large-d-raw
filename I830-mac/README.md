# I830-mac: Newton's Delta-step spread under 1e-65 horizon perturbations against D (240 to 252.6)

Machine: the Apple M5 Mac (`mac`), agent mac752. Issue https://github.com/nmoinvaz/choptuik-large-d/issues/830.

Code: branch `wip/i830` at 01c5df20 (`hp/step_spread.py`, on main 365d1bca), worktree
/Users/nathan/Source/choptuik-large-d-830. Build: main 3c35f0c's hpkernel (i599/site2), as #823 and #827. 3 threads,
nice 10, one job at a time (queue.sh).

Inputs: #603's states `I603-win2/chain/anm_pin3_D{240.1244,245.6366,250.1676}.npz`; D 252.6135 is #827's run
(`I827-mac/spread.json`, raw 504238d3); #805's p_min from `I805-mac/table.json` at raw fe89a58a, copied here as
`table805.json`.

## Plan and criteria (written by 2026-11-15 07:49 UTC, before the runs)

At each D, step_spread as #827: the plain pinned Newton step unperturbed, then again (`--repeat 1`), with m_h and a_h
perturbed by 1e-65 relative over seeds 1-4, and with the centre and each node (and Delta) perturbed alone (seed 1).

- **Checks at each D** (exit 1 on failure): the unperturbed step taken again has the same eight parts of its Delta
  part and the same smallest pivot; the centre's and every node's Delta step equal the unperturbed one as a double.
  The repeat check's control, `--mutate repeat` (the second step's centre perturbed by 1e-65), runs first at D 240
  and must fail. D 252.6 has #827's check against the recorded step (exact) instead of the repeat.
- **The spread** at each D is the largest |dDelta(seed) - dDelta(unperturbed)| over the four seeds, exact from the
  steps' eight parts (the seeds' standard deviation is reported beside it). It was fixed before the runs.
- **The fit** (`step_spread.py sum`): the slope of log(spread) against D over the four D by least squares, compared
  with #805's 1.44, and with the slope of log(2.2e-37/p_min) at the same four D (1.29 from the table).
- **The ratio** spread / (2.2e-37/p_min) at each D, with p_min from #805's table, in #808's bands: within a factor 3
  (1/3 <= ratio <= 3), below 1e-2, or between.
- The rules' self-test passes, and `--mutate=bar` and `--mutate=band` fail: selftest*.log, run before the queue
  (exit 0, 1, 1).

The ratios the plan expects to compare against: 2.2e-37/p_min is 3.0e-14 at 240.1244, 5.0e-11 at 245.6366, 2.1e-8 at
250.1676 and 3.0e-7 at 252.6135. #827's spread at 252.6135 is 4.18e-8, a ratio of 0.138 (between).

Estimate: the control 2 steps, then 13 steps per D at 3-4 min, about 2.4 h in all.
