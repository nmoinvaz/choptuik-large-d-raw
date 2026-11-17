# I903-macm3: macm3's rebuild of hp at main 1f3cda09 and its bit-identity checks

Machine macm3 (M3 Mac, 24 GB, NEON), issue https://github.com/nmoinvaz/choptuik-large-d/issues/903. The coordinator's task on
2026-11-16 15:17 UTC: rebuild hp at origin/main into a new venv (`~/Source/venv-macm3-main`, Python 3.14.3, requirements.txt
pins) with `hp/build.sh` and nothing else running, note the peak memory and the time, then run AGENTS.md's new-machine
bit-identity checks (`highm_check.py ref`, `scaled`, `jets` and its `--mutate=kappa` control) against the stored references
T81/ref_main.json, T81/scaled_main.json and anm-mac/jets_inputs/jets_inputs.json.

The order-140 chain that this issue's comment first named for macm3 runs on dh610 instead.

Files: `run_build_903.sh` (the build driver, with the low-memory recipe `CARGO_PROFILE_RELEASE_LTO=false`,
`CARGO_PROFILE_RELEASE_CODEGEN_UNITS=16` of AGENTS.md), `mem_monitor.py` (samples the build tree's rss every 5 s into
`build_mem.csv`, would kill the tree above 15 GB of swap or under 5 GB of free disk), `build.log`, `build_times.txt`,
`run_checks_903.sh` and its logs `ref_compare.log`, `scaled_compare.log`, `jets_compare.log`, `jets_mutate_kappa.log`,
`checks_times.txt`. The references are in the raw repository at ee77cff7b: `T81/ref_main.json`, `T81/scaled_main.json`,
`anm-mac/jets_inputs/jets_inputs.json`.

## Order 135 (the coordinator's comment on #903 of 2026-11-16 16:01 UTC)

`run_903_k135.sh`: a fixed-order chain at horizon order 135 from q130's base (`I903-mac/q130/base_pin3_D225.1312.npz`,
copied in from the raw repository at its main for the run). First the rung (`rung135/`, `rung135.log`: `--ks 135
--keep_plan 0 --steps 0 --D_max 226 --save_base 1`), then, if its octo-double polish converges to max|F| <= 1e-60 with the
base saved, the chain (`chain_k135/`, `chain_k135.log`: `--ks 135 --keep_plan 1 --steps 400 --D_max 262`), with chain_nsr's
flags at 6 threads, nice 10 under caffeinate. Code: worktree at main 5897ee28 with the 1f3cda09 hpkernel of this folder's
build, which has no `Solver.series_o`, so the series are formed by the jets (the same bits, a notice in the log).
`exits_k135.txt` has the start and exit lines.

## Fold rule (the coordinator's stop rule, 2026-11-17)

The command is xfkappa's `hp/fold_est_903.py verdict`, from a worktree at main 66d6ebfd (`~/Source/choptuik-large-d-903f`),
run from its `hp/` with this venv (numpy 2.5.4, mpmath 1.3.0):

    python3 fold_est_903.py verdict <RAW>/I903-macm3/chain_k135 <RAW> --json=<RAW>/I903-macm3/fold_verdict.json

after each new jet with base D of at least 258.5. Exit 0 stops the chain, 1 means #603's control failed, 2 continues. The
pilot before any base is in range (`fold_pilot.log`, `fold_pilot.json`, `run_fold_pilot.sh`) gave exit 2 in 108 s, with
control 1 passing: max|D* - 259.9033| 2.48e-04 over 45 bases of #603's chain_nsr (bound 0.005). Each later run appends to
`fold_verdict_k135.log` and rewrites `fold_verdict.json`; the exits are in `exits_k135.txt`.
