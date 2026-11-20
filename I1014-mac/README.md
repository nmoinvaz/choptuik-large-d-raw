# I1014-mac: the coordinator's singularity fit of Delta(D)'s Taylor series at D 3.0475, at M 256, 320 and 384

Machine: Nathan's MacBook Air (M5), coordinator session t5, 2026-11-20 18:53 UTC. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1014

hp/series_singularity.py at main d9cf0253, /Users/nathan/venv-314/bin/python, on the series files of raw
I997-win2/series_D30475/series_D3.0475_M256_N20.npz, I1014-dh170/series_D3.0475_M320_N12.npz and
I1014-dh170/series_D3.0475_M384p_N12.npz (taken by git show of origin/main).

- planted.log: `series_singularity.py --planted`, exit 0 (P1-P3 PASS; P4 is a limit and not counted).
- mutate.log: `--planted --mutate`, exit 0 (the mutated check fails, as it must).
- real.log: the three series at window 3..6, and M 384 at 3..7 and 4..8.
