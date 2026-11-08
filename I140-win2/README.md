# I140-win2: repeat-and-compare test of win2's arithmetic

Machine: win2 (Windows 11 Pro build 26300, ASRock Z890I Nova WiFi, BIOS 1.38 dated 2024-09-08, Intel Core Ultra 7 265K,
20 cores, AVX2, 2 x 48 GB DDR5 at 4800 MT/s). python-flint / FLINT: 0.9.0 FLINT 3.6.0 (venv choptuik-venv, Python 3.12.8,
mpmath 1.3.0). Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/140

Checkout: worktree `..\choptuik-i140` at origin/main d9fab0b (contains 58b048c). Launched detached by `run_i140.sh` at
Normal priority with `PYTHONFAULTHANDLER=1`, beside #82's twelve processes. Seven processes: three copies of lemma 6a(5)
on the 1e-18 sub-box (`l6a_copy<i>`, `B_copy<i>`), one control copy with `--rp=0.079` (`l6a_control`, `B_control`),
and three copies of `amp_flint_par.py 1.10 15 750 640 --procs 1` (`amp_copy<i>`). Each exit and wall time is in
`exits.txt`. `compare.py` hashes the outputs; `compare.txt` is its output.

Deviation from the issue's rule for timing keys, fixed before the run: `compare.py` drops `sec`, `timing`, any key
ending in `_s` or `time`, and also `seconds` and `order_times`, which the amplitude JSON uses for its timings and which
the issue's rule would have kept. It prints every key it drops.
