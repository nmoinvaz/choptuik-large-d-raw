# I841-dh370: a chain on a new plan from #808's converged re-planned state at D 251.8859, to the fold

Machine dh370 (Fedora 45, i7-8700, 12 threads), issue https://github.com/nmoinvaz/choptuik-large-d/issues/841.

`run841.sh` (written by the coordinator, md5 22e08cd3, run unedited by absolute path): `anm_run` from
`I808-dh370/s251.8859_plandrop/base_pin3_D251.8859.npz` (max|F| 2.1e-64 on its own 23-step plan, kept), #603's flags
(`--held_fit data/held_fit.json`) plus `--od_full_drop 1e-2` (#836), `--od_abort_theta 1e8 --od_abort_it 2` (#784), `--save_jet 1`
and `--D_max 259.95`, 12 threads at nice 10; worktree choptuik-large-d-841 at main 0cfff3c4, venv-i800.
`run841.sh pilot` (unit `i841p`): two steps, each must converge to max|F| <= 1e-60; then `run841.sh chain` to D_max 259.95.
Output: `chain.log`, `chain/` (states `anm_pin3_D*.npz`, series `jet_pin3_D*.npz`, predictions, `anm_run.jsonl`), `exits_841.txt`.
