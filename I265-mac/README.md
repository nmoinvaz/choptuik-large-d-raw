# I265-mac: the series gate after the solve in modecount_common.setup, its check, mutations and an end-to-end setup

Machine: mac (Apple M5, 10 cores, macOS 27, shared and loaded by other sessions).
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/265
Code: branch wip/i265 of the code repository, commit 27a258c (from main 1f805b5). Files hp/modecount_common.py
(`series_gate`, `prepare`, the gate after the solve, `DATA`) and hp/modecount_probe.py (`--gatecheck`, `--data`).
Versions: Python 3.14.7 (/Users/nathan/venv-314), hpkernel 0.1.0 from that venv, hp/modecount_cx from the main
checkout's build (PYTHONPATH /Users/nathan/Source/choptuik-large-d/hp/modecount_cx/build). Nothing was rebuilt.

Every run is from the worktree root, one process at a time, 1 thread, `nice -n 10 caffeinate -i`, through a wrapper
that writes the command, the code commit, the exit code and the wall time into each log (first and last lines).

Inputs from this repository were extracted with `git archive origin/main <paths> | tar -x` into a scratch directory
laid out as this repository (the `--raw` of the commands below), at 12b4cb66. They are not copied here:
I170-macm3/hp_data_after/modecount_state_D45.0507_M48_kf21.npz (#170's solution) and the 9 raw states of #141's
list (I141-mac/inputs/SOURCES.txt). The other 13 of the 22 are in the code repository's hp/data.

## Files

- logs/gatecheck.log, gatecheck.json: `hp/modecount_probe.py --gatecheck --raw=RAW`, exit 0 (2/2).
- logs/gatecheck_mutate_nogate_after.log: the same with `--mutate=nogate_after`, exit 1 (check 1 fails).
- logs/gatecheck_mutate_tight.log: the same with `--mutate=tight`, exit 1 (check 2 fails).
- logs/selftest.log: `hp/modecount_probe.py --selftest` (#141's checks), exit 0 (5/5).
- logs/setup_D45_kf21.log, setup_D45_kf21.json, states/: the end-to-end setup (below).
- logs/compare_I170.log: that solution against #170's (a scratch script that loads both npz files).

## Results

| run | exit | what it shows |
|---|---|---|
| `--gatecheck` | 0 | (1) D 45, M 48, kf 21: the start passes (centre 7.4e-74, horizon 1.3e-27), and setup refuses #170's solution at the gate after the solve (centre 2.4e-8, ratio 0.967 at x = 0.3). (2) The gate passes #141's 22 states, worst 4.8e-16 (D 30, M 48 without the cut), every tail as in I141-mac/probe/gate_states.log |
| `--gatecheck --mutate=nogate_after` | 1 | setup accepts the D 45 kf 21 solution (\|F\| 8.2e-17), so check 1 fails |
| `--gatecheck --mutate=tight` (gate 1e-16) | 1 | both D 30 M 48 no-cut states are refused, so check 2 fails |
| `--selftest` | 0 | #141's 5 checks unchanged |
| end to end, below | 1 | setup refuses the solution of a real solve |

In check 1 the solve is planted. Newton returns #170's solution, whose layout (M 48, nodes 0.3 ... 0.7, kt 36, kc 420,
ks 100) the check confirms equals the start's. The end-to-end run solves for real:

    hp/modecount_probe.py hp/data/states/up7_D45.0507.npz --M=48 --kf=21 --setup --fmax=1e-15 --data=<this folder>/states --setup_json=setup_D45_kf21.json

Newton left \|F\| at 3.2e-9 and Levenberg-Marquardt brought it to 8.2e-17. setup saved the state (states/), then
refused it, centre 2.4e-8 against the gate's 1e-15. The run took 1570 s and exited 1, the probe's exit when a setup
raises. The state reproduces #170's: the same layout, \|F\| 8.1688e-17 against 8.1688e-17, Δ within 2.1e-18, and the
largest component difference 1.7e-12.

setup saves a re-converged state before its gates on \|F\| and on the series, as it did before for \|F\|. A rerun loads
the saved state and refuses it at the start gate without solving.
