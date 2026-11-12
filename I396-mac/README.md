# I396-mac: hp's computed plans at D 30.0688, M 32, 48 and 64, on the Mac, for the cross-OS diff

Machine: the M5 Mac (coordinator), macOS 27, the hpkernel of /Users/nathan/venv-314 (built 2026-11-09; #523 left the planner unchanged). Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/396

- `plan_mac_M{32,48,64}.json`, `.log`: `hp/plan_print.py data/states/up6_D30.0688.npz --M=N --kf=none --threads=4` at choptuik-large-d 179afc4 (solved: |F| 6.9e-26, 9.0e-18 by Levenberg-Marquardt, 1.7e-26). Every run exits 0.
- `unsolved_a445b4d/`: the same at a445b4d, whose resampled M 48 and 64 states were not solved (|F| 1.6e-11). They are kept only as the matching pair of win's `I396-win/held_a445b4d/`.

Diff: `python3 hp/plan_diff.py I396-mac/plan_mac_M48.json I396-win/plan_win_M48.json` (choptuik-large-d fc697f3) and likewise for M 64 and M 32.
