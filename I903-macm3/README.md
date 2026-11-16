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
