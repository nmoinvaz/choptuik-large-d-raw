# I202-win2: sigma at omega/omega_inf 1.10 with K 33, J 1000 on win2, against macm3's T153 file

Machine: win2 (Windows 11 desktop, Intel Core Ultra 7 265K, 20 threads, 96 GB, BIOS 3.40, microcode 0x122).
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/202.

The command of T153-macm3/w1.10.cmd with `--procs 3` (macm3 ran `--procs 2`) on Python 3.14.10 (`venv-t177`) from
`solver/inner_amp/` of `D:\choptuik-large-d`, Normal priority:
`amp_flint_par.py 1.10 33 1000 960 --procs 3 --fit phys --mf 6:12 --out <this folder>/sigF_w1.10_K33_J1000.json`.
`compare_202.py` compares it with `../T153-macm3/sigF_w1.10_K33_J1000.json` after dropping the timing keys and `procs`, and
names the first differing sigma string (`--selftest`: a changed digit is found at its index, a changed `procs` is ignored).
