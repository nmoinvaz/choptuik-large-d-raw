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

Control: the issue's `--rp=0.079` is refused by `lemma6_jump_M.py` after 1 s (`ValueError: Z beyond the real reach of D`,
`lemma6_sector_M.py` line 95; log `l6a_control_rp0.079_refused.log`), because Z = xi_a^2 = 0.004489 is fixed and rp = 0.08
just reaches it. The control runs with `--rp=0.081` instead (`run_i140_control.sh`, started 07:30:51 UTC), which the
coordinator approved on 2026-11-08. Probes of `--rp=0.081` (accepted) and `--rp=0.0795` (refused) are not kept.

Results (exits.txt: all seven processes exit 0; the lemma copies take 565-573 s, the control 553 s, the amplitude copies
607-611 s):
- `compare.txt`: the three lemma 6a copies hash identically in the rho_6a JSON and in the stored B, and both equal
  I104-win2's. The three amplitude copies hash identically. The rp = 0.081 control's JSON hashes differently (only the
  radius of Lambda differs, [0.4233267068 +/- 6.76e-12] against +/- 6.92e-12; rho_6a is the same ball), so the comparison
  can fail. The control's B is identical to the copies' B, as it must be, because B is computed from the box alone;
  macm3's B (I103-macm3) differs from the copies', and that is B's own control.
- `compare_first_run.txt` is the output of the first run of `compare.py`, which exited 2 because it also demanded that
  the control's B differ. That demand was wrong (rp does not enter B); the script was changed to use macm3's B for B's
  control and rerun on the same files. The hashes did not change.
- No crash and no traceback in any copy; no Application Error event in the Windows log since 07:00:18 UTC.
