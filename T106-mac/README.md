# T106-mac: the low-D Taylor coefficients' link-by-link check at M 48 (D 4), before its M 320 run on win2

Machine: the Mac (Apple M5), coordinator session, one thread, 2026-11-04 UTC. Script `hp/jet_lowd_check.py` of
branch `feat/jet-all-sizes` (e8e7b6f) of the code repository, with the hpkernel of `/Users/nathan/Source/venv-anm`
(main's kernel, whose jet lanes include M 48). Comms: the cloud entries to win2 of 2026-11-04 after 12:40 UTC.

- `m48_states/`: four converged states at M 48 on one plan (192 Taylor steps): D 4.0 (hp/data/lowD_states/
  lowD_D4.0000_M48.npz with its plan from `Solver.plan(z, 1e-32, 0.05)`), and D 3.995, 3.9975 and 4.0025 by
  mixed-precision Newton from it (|F| 1.9e-30 to 5.2e-30). `make_states.py.txt` is the script that made them.
- `jet_lowd_check_m48.log`: the check, exit 1 with one failed link, GMRES at step_tol 1e-26 (changes 1, 6.9e-8,
  6.4e-16, 3.1e-24, then NaN); at 1e-20 it converges in 4 products to the stored states' tangent (8.6e-7).
- `jet_lowd_check_m48_mutate.log`: the control (`--mutate --no_gmres`), links b, c, c_cut and d fail as they must.
- `jet_lowd_check_m48.jsonl`: both runs' records.
