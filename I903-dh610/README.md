# I903-dh610: the fixed-order chain at horizon order 140 from D 225.13 toward the fold, on dh610

Machine dh610 (Fedora 45, i7-12700, 20 threads), issue https://github.com/nmoinvaz/choptuik-large-d/issues/903.
Command: the coordinator's of 2026-11-16 15:20 UTC (`--ks 140 --keep_plan 1`, 10 threads, nice 10, `--D_max 262`), launcher
`run903.sh`, log `chain.log`, exits in `exits_903.txt`, output `chain_k140/`. State: `I903-mac/ladder/k140_from130/
base_pin3_D225.1312.npz` of the raw repository's origin/main (read from a scratch directory, beside the live clone).
Code: Python and `hp/data` from a worktree of origin/main at 1f3cda09; hpkernel from #911's build (0cf9b94a, venv
`choptuik-large-d-911`), by the coordinator's option (1) on #903: that build's existing paths passed #911's bit-identity
checks against the stored references, and `hp/src` differs from main's only by #914's order-by-order code (662 lines, 1
line of the Taylor recursion rewritten), which `anm_run.py` does not call at `--jet_by_order 0`.
