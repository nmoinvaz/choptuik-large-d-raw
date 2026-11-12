# I589-mac: the freeze projector's rounding against the chain's Delta, D 215-240, on cadcaf1 (exact projector) and main's wheel

Machine mac (the shared Apple M5 Mac, 4 threads at nice 10, one job at a time), issue https://github.com/nmoinvaz/choptuik-large-d/issues/589 (subagent).
Code: `hp/plan_state.py` and `hp/held_homotopy.py` on branch `wip/i562-subagent` of the code repository (0153062), and main d020d58's `hp/near_null.py` (stored plan by default).
Kernels: main's wheel (venv-314) and #523's cadcaf1 checked wheel (freeze projector in octo-double), installed with `pip install --no-deps --target` into a scratch folder and put first on PYTHONPATH; every cadcaf1 log's first line prints `hpkernel.__file__`.

States, and the plan each is factored on (`plan_state.py`: anm_run.py plans once, at its run's first base; three of the states were saved without that plan, so it is made again there, `--base`, and the state saved with it as `sNNN.npz`):

| file | state | plan |
|---|---|---|
| `s215.npz` | I462-win/chain_d6/anm_pin3_D215.0000.npz | planned at I215-win/chain_d6/anm_pin3_D214.7500.npz (the run's first base, chain_d6.log line 9) |
| `s225.npz` | I461-win2/crawlB3/anm_pin3_D225.1312.npz | planned at I461-win2/crawlB2/anm_pin3_D215.1312.npz (crawlB3.log line 7) |
| `s235.npz` | I461-win2/crawlB5/anm_pin3_D235.1312.npz | planned at I461-win2/crawlB4/anm_pin3_D231.6312.npz (crawlB5.log line 8) |
| `s240.npz` | I461-win2/crawlJ/anm_pin3_D240.0258.npz (a copy) | its stored plan |

Files: `plan_main_*.log`, `plan_c2_*.log` (pinned max|F| by block on each kernel, `run_plans.sh`); `c2_probe_*` (held_homotopy.py's probe on cadcaf1: tangent = pinned step, Delta's linear response by rows, chord ladder, `run_c2.sh`); `c2_nn_*` (near_null.py on cadcaf1: sigma_1..4, pinned step, check). Exit codes in `exits.txt` (all 0). The D 242.3642 row is #562's, raw `I562-mac/c2_probe_07.*` (690c41a9).
