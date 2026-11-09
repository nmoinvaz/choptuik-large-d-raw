# I236-win2: how amp_flint_par.py's output depends on --procs (K 25, J 1000 at omega/omega_inf 1.10, 1, 2, 3 and 4 processes, two runs each)

Machine: win2 (Windows 11 desktop, Intel Core Ultra 7 265K, 20 threads, 96 GB, BIOS 3.40, microcode 0x122).
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/236 (recommended by win2 in #229's summary).

Command, from `solver/inner_amp/` of `D:\choptuik-large-d`, Python 3.14.10 (`venv-t177`), Normal priority, no affinity, beside #213:
`amp_flint_par.py 1.10 25 1000 960 --procs N --fit phys --mf 6:12 --out <this folder>/sigF_w1.10_K25_J1000_procsN_rR.json`
for N = 1, 2, 3, 4 and R = r1, r2 (`run_i236.sh`: the four N of r1 at once, then the four of r2; logs `procsN_rR.log`, exits in
`exits.txt`). `compare_236.py` compares every pair after dropping the timing keys and `procs`, names the first differing key
per section (sigma_str index, sigma_err index, f key, fit_info key), and groups the runs into bit-for-bit equal classes.

## Progress (2026-11-09 09:13 UTC)

Batch r1 done, exits and walls in `exits.txt` (`--procs` 4: 2719 s, 3: 3292 s, 2: 4369 s, 1: 7450 s). Every pair of counts differs
in `fit_info` only: Mf equal, err and resid differ in 11 of 91 families (21_19, 21_21, 23_15 to 23_23, 25_19 to 25_25), four
different triples in each; `sigma_str`, `sigma_err`, `f` and the other keys are equal. Equal counts (r1 against r2) come with batch r2.
`smoke/` holds a K 13 test of `amp_flint_par_fixsum.py` (original `--procs 1` and the variant at 1, 2, 3 all equal).
