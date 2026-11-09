# I228-win2: #82's K 45, J 1500 node at omega/omega_inf 1.10 rerun on win2's new firmware

Machine: win2 (Windows 11 desktop, Intel Core Ultra 7 265K, 20 threads, 96 GB, BIOS 3.40, microcode 0x122).
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/228 (recommended by win2 in #202's summary).

Command of #82 (`../I82-win2/run_i82_one.cmd`), from `solver/inner_amp/` of `D:\choptuik-large-d` (main checkout at 188853c,
`amp_flint_par.py` unchanged in code since #82's 700da3a, only docstring lines were added later), Normal priority, no affinity,
one thread per process:
`amp_flint_par.py 1.10 45 1500 1280 --procs 3 --fit phys --mf 6:12 --fit-step 1 --out <this folder>/sigF_w1.10_K45_J1500_p1280.json`
with the interpreter of #82, `venv-t126` (Python 3.12.8, python-flint 0.9.0 / FLINT 3.6.0, mpmath 1.3.0, numpy 2.5.4), so that
what changed against #82's run is the firmware (BIOS 3.40, microcode 0x122, ME 19.0.11.2289) and not the software (`run_i228.sh`,
`w1.10.log`, `exits.txt`). It starts when #213 has ended (its memory), the coordinator's order.

`compare_228.py` compares the new file with `../I82-win2/sigF_w1.10_K45_J1500_p1280.json` bit for bit (timing keys dropped,
`procs` kept, both 3), names the first differing entry and the first differing sigma string, and gives the difference of the
new file from win2's K 33 J 1000 value at 1.10 against #82's same-machine 1.09 and 1.11 rows (`--selftest`: a planted digit in
one sigma string is found at its index, a copy is equal).
