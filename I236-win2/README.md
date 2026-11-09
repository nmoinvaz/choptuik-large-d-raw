# I236-win2: how amp_flint_par.py's output depends on --procs (K 25, J 1000 at omega/omega_inf 1.10, 1, 2, 3 and 4 processes, two runs each)

Machine: win2 (Windows 11 desktop, Intel Core Ultra 7 265K, 20 threads, 96 GB, BIOS 3.40, microcode 0x122).
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/236 (recommended by win2 in #229's summary).

Command, from `solver/inner_amp/` of `D:\choptuik-large-d`, Python 3.14.10 (`venv-t177`), Normal priority, no affinity, beside #213:
`amp_flint_par.py 1.10 25 1000 960 --procs N --fit phys --mf 6:12 --out <this folder>/sigF_w1.10_K25_J1000_procsN_rR.json`
for N = 1, 2, 3, 4 and R = r1, r2 (`run_i236.sh`: the four N of r1 at once, then the four of r2; logs `procsN_rR.log`, exits in
`exits.txt`). `compare_236.py` compares every pair after dropping the timing keys and `procs`, names the first differing key
per section (sigma_str index, sigma_err index, f key, fit_info key), and groups the runs into bit-for-bit equal classes.
