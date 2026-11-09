# I263-win2: main's count-independent amp_flint_par.py at K 33, J 1000, omega/omega_inf 1.10 with 2 and 3 workers

Machine: win2 (Windows 11 desktop, Intel Core Ultra 7 265K, 20 threads, 96 GB, BIOS 3.40, microcode 0x122).
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/263 (recommended by win2 in #247's summary).

Command, from `solver/inner_amp/` of a fresh worktree `D:\choptuik-i263` (detached at f57c976, main, which contains #246's 64914d8),
separate from the pinned checkout `D:\choptuik-large-d` (188853c, for #228 and #256), Python 3.14.10 (`venv-t177`, python-flint 0.9.0 / FLINT
3.6.0), Normal priority, no affinity, the two at once (`run_i263.sh`; logs `main_procsN.log`, exits in `exits.txt`):
`amp_flint_par.py 1.10 33 1000 960 --procs N --fit phys --mf 6:12 --out <this folder>/sigF_w1.10_K33_J1000_main_procsN.json` for N = 2 and 3.
`compare_263.py` compares the two runs with each other, their sigma_16 with the three earlier values (original code with 3 workers #202 and
2 workers #229/T153, per-task order #247) against the 1.4e-18 spread, and lists the wall times (`--selftest`).
