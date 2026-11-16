# I848-macm3: #812's kf 47 mode count (D 61.03, M 48) on a second radial layout

Machine macm3 (M3 Mac, 6 threads), issue https://github.com/nmoinvaz/choptuik-large-d/issues/848.

Scripts (written by the coordinator): `common.sh`, `job.sh`, `run_848.sh` (stages 1, 2, 3). They use the same worktree,
build and venv as #812 (choptuik-large-d-749 at bd7df22f, venv-macm3-314). Stage 1 is the control circle, stage 2 the noise
test (`modecount_qdet.py` draws), stage 3 the seven circles of #812's kf 47 count.

- `kf47ct/`: the first stage 1 run, `--centre_tol=1e-30`. No node was added (the resampled start's centre tail is 8.1e-89,
  under 1e-30), its saved state has #812's 5 nodes and header, and the control printed centre 7.1e-26 as on #812, so the
  layout did not change and the run was stopped (STOP line in `exits_848.txt`).
- `kf47_ct1e-100/<circle>/`: `--centre_tol=1e-100`, which adds the node 0.15 (6 nodes against #812's 5). Each circle's
  `run.log` and `data/*_evals.jsonl`. Circles: control, c_2.85_p0.25, c_2.85_m0.25, c_3.35_p0.25, c_3.35_m0.25, triple,
  lens, lensc.
- `state/modecount_state_D61.0264_M48_kf47_ct1e-100.npz`: the saved state that stages 1 to 3 loaded (md5 ae499cdda35d09a449d877e18baa007b). It belongs in
  `hp/data/` of that worktree, where `prepare()` finds it by name.
- `qdet_draws/`: the noise test, `run.log` and `qdet.json`.
- `exits_848.txt`: start and exit lines of every run, `run_848_*.out`: the stage drivers' output.
