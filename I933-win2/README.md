# I933-win2: the sonic valley's closing at M 384

Machine: win2 (runner win2b), 1 thread. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/933 (recommended by #926).

Code: worktree `D:\choptuik-i932` at origin/main 65ec482f, `hp/sonic_valley.py` (Python only, the installed hpkernel of #343's venv).
All four M 384 states carry a stored plan (`meta.segs`, 20 segments), so every `gap` runs with `--plan stored`.

`run933.sh` chains the coordinator's four commands (hc, 2026-11-17 ~03:45 UTC) and logs each exit in `exits_933.txt`:

1. `gap` of the M 384 states at D 3.0450 (T82-win), 3.04375 (T105-win2), 3.04355 and 3.04335 (I343-win2) into `gap_M384.jsonl`.
2. `gap --mutate dshift` of the 3.04335 state into `gap_dshift.jsonl`, the control, which must exit 1.
3. `tangency --M 384 --last 3` on `gap_M384.jsonl`.
4. `tangency --M 384 --last 3 --mutate slope`, the control, which must exit 1.
