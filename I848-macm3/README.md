# I848-macm3: #812's kf 47 mode count (D 61.03, M 48) on a second radial layout

Machine macm3 (M3 Mac, 6 threads), issue https://github.com/nmoinvaz/choptuik-large-d/issues/848.

Scripts (written by the coordinator): `common.sh`, `job.sh`, `run_848.sh` (stages 1, 2, 3). They use the same worktree,
build and venv as #812 (choptuik-large-d-749 at bd7df22f, venv-macm3-314), with `--centre_tol=1e-30`, which adds inner
nodes to the layout (kf 47's centre tail is 7.1e-26 on #812's). The state is saved as
`modecount_state_D61.0264_M48_kf47_ct1e-30.npz` in that worktree's hp/data.

- `kf47ct/<circle>/`: each circle's log and data.
- `qdet_draws/`: the noise test on the new layout's state.
- `exits_848.txt`: start and exit lines.
