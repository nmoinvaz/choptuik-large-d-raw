# I884-mac: truth_system reads a re-stepped state in its source's system

Machine: mac (Apple M5), agent xfchecks. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/884

Code: wip/xf-884 (6118a8be, on main 1dee59e4): `octo_corrector.truth_system` takes a re-stepped state's held values
from its source (`meta["restep"]["source"]`, followed to a state that is not re-stepped), with `held_src="state"` as
the old behaviour; `pinned_o` takes them from `held_z`. `truth_restep.py` passes `--held_src` and adds `residuals`.
On main 3c35f0c's hpkernel, one process at nice 10, 3 kernel threads, OPENBLAS_NUM_THREADS=1 (`run.sh`). Runs in
`queue.sh` order, after I875-mac's queue.

In progress.

## Criteria (posted on the issue before the runs)

| # | criterion | fails when |
| --- | --- | --- |
| C1 | `check` of `I874-mac/anm_pin3_D240.1244_u2.npz` (held from the source): its step and max\|F\| before it equal #852's step 3 as doubles (`--match I852-mac/steps_D240.json --match_k 3`), the bounds of #874 pass, and the held offset against the source's system differs by 0 | the step differs, or the offsets differ |
| C2 | the control, `--held_src state` (the old behaviour): the match FAILS, with the step 1.5635832413406279e-99 of #874 | it matches |
| C3 | `residuals`: the four #837 truths (D 240.1244, 245.6366, 250.1676, 252.6135) read through `truth_system` give the pinned max\|F\| that #840 recorded (`I840-mac/ss_D*.json`, the unperturbed run) as doubles | any differs |
| C4 | the control, `residuals --held float` (#837's float-held values): FAILS | it passes |
