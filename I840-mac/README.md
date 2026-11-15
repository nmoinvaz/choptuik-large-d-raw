# I840-mac: step_spread in #837's truth_system at D 240.1, 245.6, 250.2 and 252.6

Machine: mac (Apple M5), agent xfchecks. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/840

Code: hp/step_spread.py at main 0cfff3c4 (worktree wip/xf-840), unchanged, on main 3c35f0c's hpkernel. One process
at nice 10, 3 kernel threads, OPENBLAS_NUM_THREADS=1 (`run.sh`). States: I603-win2/chain/anm_pin3_D*.npz, read in eight
parts with held values in eight parts and the stored plan (#837's truth_system, printed by each run).

In progress. Runs in `queue.sh` order, then `queue2.sh`.

| file | what |
| --- | --- |
| `ss_D240.log`, `.json` | D 240.1244: unperturbed, repeat, horizon seeds 1-4 at 1e-65, controls (centre, nodes 0-4, Delta), `--ref` from I837-mac/step_D240_dz0.npz |
| `ss_D245`, `ss_D250` | the same at D 245.6366 and 250.1676 (no `--ref`: no stored step) |
| `ss_D252` | the same at D 252.6135, `--ref` from I837-mac/ss_D252.log |
| `ss_D240_repeatctl` | the repeat check's control (`--mutate repeat`), must FAIL |
| `selftest*` | the verdict's and the bands' rules; `--mutate=bar` and `--mutate=band` must fail |
| `pw_D240_r66`, `r67` | diagnostic: seed 1 at rel 1e-66 and 1e-67, the same signs, for the power of the response in rel |

## The power diagnostic (registered before it ran)

At D 240.1244 the four seeds' dDelta are all positive (+2.40e-38 .. +2.67e-38, sd 1.1e-39). A response linear in the
random-sign perturbation would change sign between seeds, and a quadratic one would not. Reading, with
p = log10(dDelta(rel) / dDelta(rel / 10)) at 1e-65 -> 1e-66 and 1e-66 -> 1e-67 (seed 1, identical signs):

- both p in [1.8, 2.2]: quadratic, Newton's second-order error from a point off the root, which a second step removes;
- both p in [0.8, 1.2]: linear, the step's response to the input's uncertainty;
- otherwise neither.

The `--ref` check in each run must pass (the unperturbed step reproduced as a double).
