# I247-win2: the fixed-order sum at K 33, J 1000, omega/omega_inf 1.10 with 2 and 3 workers

Machine: win2 (Windows 11 desktop, Intel Core Ultra 7 265K, 20 threads, 96 GB, BIOS 3.40, microcode 0x122).
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/247 (recommended by win2 in #236's summary).

Command, from `solver/inner_amp/` of `D:\choptuik-large-d`, Python 3.14.10 (`venv-t177`), Normal priority, no affinity, the two at once:
`python -u <raw>/I236-win2/amp_flint_par_fixsum.py 1.10 33 1000 960 --procs N --fit phys --mf 6:12 --out <this folder>/sigF_w1.10_K33_J1000_fixsum_procsN.json`
for N = 2 and 3 (`run_i247.sh`; logs `fixsum_procsN.log`, exits in `exits.txt`). `amp_flint_par_fixsum.py` imports the module of main
and adds each order's products per group in task order, whatever the worker count (#236). `compare_247.py` compares the two with each
other and with the original-code K 33 files of #202 (3 workers), #229 and T153 (2 workers), after dropping the timing keys and
`procs`, and names the first differing key (`--selftest`).

## Results (2026-11-09 19:12 UTC)

Both runs ended with exit 0 (`exits.txt`): `--procs` 3 after 10 532 s (18:25:40 UTC), `--procs` 2 after 13 284 s (19:11:32), started 15:30:08, beside
#228 and #256 (the original code took 8455 s and 11 034 s). `compare_247.py` (`compare_247.log`, exit 0; its selftest ok):

- The two fixed-order runs are bit for bit equal (`sigma_str`, `sigma_err`, `f`, `fit_info`, every other key; timing keys and `procs` dropped).
- Against the original-code files (#202 with 3 workers, #229 and T153 with 2 workers) each differs in the same places: `sigma_str` only at
  sigma_16 (sigma_0 to sigma_15 are equal to all 20 digits), `sigma_err[16]`, three `f` entries (33_3, 33_5, 33_7), and `fit_info` err and
  resid from order 21 (57 of 153 families against #202, 56 against #229 and T153).
- sigma_16 of K 33 at 1.10: fixed order (2 and 3 workers) 3.3878621466602032799e-13 - 2.0036709659677382527e-13 i; original with 3 workers
  3.3878621466602032849e-13 - 2.0036709659677382538e-13 i; original with 2 workers 3.3878621466602032852e-13 - 2.0036709659677382543e-13 i.
  Relative differences: fixed order against 3 workers 1.3e-18, against 2 workers 1.41e-18, the two originals 1.48e-19.
