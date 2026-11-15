# I874-mac: a re-converged truth at D 240.1244 (#852's u_2)

Machine: mac (Apple M5), agent xfchecks. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/874

Code: hp/truth_restep.py on wip/xf-874 (28763c87, on main 2283596e), on main 3c35f0c's hpkernel. One process at nice
10, 3 kernel threads, OPENBLAS_NUM_THREADS=1 (`run.sh`). Source: I603-win2/chain/anm_pin3_D240.1244.npz in #837's
truth_system. Output: `anm_pin3_D240.1244_u2.npz` here, in eight parts (save_o) with the source's meta and stored plan,
and `meta["restep"]` naming the source and the steps. Runs in `queue.sh` order, after I856-mac's queue.

In progress.

## Criteria (posted on the issue before the runs)

| # | criterion | fails when |
| --- | --- | --- |
| C1 | `store` reproduces #852's unperturbed path: each step's max\|dz\| and max\|F\| before it equal, as doubles, those of `I852-mac/steps_D240.json` (k 1, 2, 3), and the saved parts and plan read back equal | the path or the file differs |
| C2 | `check` of the stored state, read through `truth_system` (8 of 8 parts, held values in eight parts, plan stored): its own plain step max\|dz\| / max\|z_h\| at most 1e-97, and pinned max\|F\| at most 1e-92 | either bound fails |
| C3 | the control: `check` of the old truth through the same path fails both bounds, and its step does not equal #852's step 3 | it passes a bound or the match |
| C4 | reported: the largest difference between the held offsets of the stored state's system and the source's (`--held_ref`) | (0 when the state keeps the source's held values) |

The comparison in C1 and C2 shares its machinery (`newton_o`, `od_axpy`, `truth_system`) with #852's run, so it is a
reproduction, not an independent check.
