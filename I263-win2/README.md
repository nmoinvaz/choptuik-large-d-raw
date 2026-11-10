# I263-win2: main's count-independent amp_flint_par.py at K 33, J 1000, omega/omega_inf 1.10 with 2 and 3 workers

Machine: win2 (Windows 11 desktop, Intel Core Ultra 7 265K, 20 threads, 96 GB, BIOS 3.40, microcode 0x122).
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/263 (recommended by win2 in #247's summary).

Command, from `solver/inner_amp/` of a fresh worktree `D:\choptuik-i263` (detached at f57c976, main, which contains #246's 64914d8),
separate from the pinned checkout `D:\choptuik-large-d` (188853c, for #228 and #256), Python 3.14.10 (`venv-t177`, python-flint 0.9.0 / FLINT
3.6.0), Normal priority, no affinity, the two at once (`run_i263.sh`; logs `main_procsN.log`, exits in `exits.txt`):
`amp_flint_par.py 1.10 33 1000 960 --procs N --fit phys --mf 6:12 --out <this folder>/sigF_w1.10_K33_J1000_main_procsN.json` for N = 2 and 3.
`compare_263.py` compares the two runs with each other, their sigma_16 with the three earlier values (original code with 3 workers #202 and
2 workers #229/T153, per-task order #247) against the 1.4e-18 spread, and lists the wall times (`--selftest`).

## Results (2026-11-10 01:50 UTC)

Both runs ended with exit 0 (`exits.txt`): `--procs` 3 after 8816 s (21:42:06 UTC, started 19:15:09 beside #228 and #256), `--procs` 2 stopped by hand at 20:43:57 (order 25 of 33, memory, `main_procs2_stopped_at_k25.log`) and rerun alone from 22:43:13 to
01:48:18 beside #228 and #268, 11 105 s. `compare_263.py` (`compare_263.log`, exit 0; its selftest ok):

- the two runs of main's code are bit for bit equal (timing keys and `procs` dropped);
- sigma_16 of both is 3.3878621466602032849e-13 - 2.0036709659677382538e-13 i, identical to all 20 digits to the original code's 3-worker value
  (#202), 1.48e-19 from the 2-worker value (#229/T153) and 1.3e-18 from the per-task order (#247): within the 1.41e-18 spread;
- main's file is not bit for bit equal to any earlier K 33 file: `sigma_err[16]` differs, `f` in 2 of 136 entries (against #202) or 3 of 136, `fit_info`
  err/resid in 52 to 58 of 153 families;
- wall times (the `seconds` of the JSONs): main 3 workers 8814 s against 8454 s for the original (#202), main 2 workers 11 104 s against 11 033 s (#229),
  the per-task order of #247 10 531 s and 13 283 s; the load beside each run differed.
