# I229-win2: K 33 J 1000 at omega/omega_inf 1.10 with --procs 2 on win2, against win2's --procs 3 file and macm3's

Machine: win2 (Windows 11 desktop, Intel Core Ultra 7 265K, 20 threads, 96 GB, BIOS 3.40, microcode 0x122).
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/229 (recommended by win2 in #202's summary).

Question: do win2's `--procs 3` file (`../I202-win2/sigF_w1.10_K33_J1000.json`) and macm3's `--procs 2` file
(`../T153-macm3/sigF_w1.10_K33_J1000.json`) differ at sigma_16 (1.5e-19) because of the process count?

Command, from `solver/inner_amp/` of `D:\choptuik-large-d`, Python 3.14.10 (`venv-t177`), Normal priority, no affinity:
`amp_flint_par.py 1.10 33 1000 960 --procs 2 --fit phys --mf 6:12 --out <this folder>/sigF_w1.10_K33_J1000_procs2.json`
(`run_i229.sh`, log `w1.10_procs2.log`, exit in `exits.txt`).

`compare_229.py` compares the new file with both others after dropping the timing keys and `procs` (`../I140-win2/compare.py`'s
rule), names the first differing entry and sigma string against each, and prints the verdict: equal to the #202 file (the process
count does not matter on win2), equal to macm3's and not to #202's (the difference follows the process count), or equal to
neither. `--selftest` plants each of the three cases.
