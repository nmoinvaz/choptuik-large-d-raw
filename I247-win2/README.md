# I247-win2: the fixed-order sum at K 33, J 1000, omega/omega_inf 1.10 with 2 and 3 workers

Machine: win2 (Windows 11 desktop, Intel Core Ultra 7 265K, 20 threads, 96 GB, BIOS 3.40, microcode 0x122).
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/247 (recommended by win2 in #236's summary).

Command, from `solver/inner_amp/` of `D:\choptuik-large-d`, Python 3.14.10 (`venv-t177`), Normal priority, no affinity, the two at once:
`python -u <raw>/I236-win2/amp_flint_par_fixsum.py 1.10 33 1000 960 --procs N --fit phys --mf 6:12 --out <this folder>/sigF_w1.10_K33_J1000_fixsum_procsN.json`
for N = 2 and 3 (`run_i247.sh`; logs `fixsum_procsN.log`, exits in `exits.txt`). `amp_flint_par_fixsum.py` imports the module of main
and adds each order's products per group in task order, whatever the worker count (#236). `compare_247.py` compares the two with each
other and with the original-code K 33 files of #202 (3 workers), #229 and T153 (2 workers), after dropping the timing keys and
`procs`, and names the first differing key (`--selftest`).
