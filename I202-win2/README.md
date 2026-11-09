# I202-win2: sigma at omega/omega_inf 1.10 with K 33, J 1000 on win2, against macm3's T153 file

Machine: win2 (Windows 11 desktop, Intel Core Ultra 7 265K, 20 threads, 96 GB, BIOS 3.40, microcode 0x122).
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/202.

The command of T153-macm3/w1.10.cmd with `--procs 3` (macm3 ran `--procs 2`) on Python 3.14.10 (`venv-t177`) from
`solver/inner_amp/` of `D:\choptuik-large-d`, Normal priority:
`amp_flint_par.py 1.10 33 1000 960 --procs 3 --fit phys --mf 6:12 --out <this folder>/sigF_w1.10_K33_J1000.json`.
`compare_202.py` compares it with `../T153-macm3/sigF_w1.10_K33_J1000.json` after dropping the timing keys and `procs`, and
names the first differing sigma string (`--selftest`: a changed digit is found at its index, a changed `procs` is ignored).

## Results

The run ended with exit 0 at k 33 on 2026-11-09 03:51:36 UTC, 8455 s after its 01:30:41 start (3 processes; products 1233.9 s,
fit setup 21.0 s, fits 7192.5 s), while the machine also ran the 13-copy #204 loop, #195, #196, #213 and negative-mass jobs.
macm3's file took 12 597 s with 2 processes. `exits.txt`, `w1.10.log`, `sigF_w1.10_K33_J1000.json`.

Against `../T153-macm3/sigF_w1.10_K33_J1000.json` (`compare_202.log`, exit 1, not bit for bit; `compare_202_selftest.log` ok):

- `sigma_str` is equal for n = 0 to 15, all 20 digits. The first differing sigma string is sigma_16:
  win2 (3.3878621466602032849e-13, -2.0036709659677382538e-13), macm3 (...852e-13, ...543e-13), relative 1.5e-19.
- `sigma`, `sigma_rad`, `K`, `J`, `prec`, `phys_prec`, `mf`, `fit`, `fit_step`, `wf` are equal. `procs` differs (3, 2) and is
  dropped. `sigma_err[16]` differs by 4.3e-6 relative (1.32039523e-26 against 1.32038961e-26), the others are equal.
- `fit_info` (Mf, err, resid): Mf is equal in all 153 families, err and resid are equal for every order below 21 and differ from
  order 21 on (2 of 11 families at 21, 5 of 12 at 23, 4 of 13 at 25, 11 of 14 at 27, 8 of 15 at 29, 12 of 16 at 31, 14 of 17 at
  33). `f` differs in 3 of 136 entries, 33_3, 33_5 and 33_7, values near 1e-27 (about 1e-16 of S_1^(33)).
- The cause of the difference is not determined. The fits are `arb` approximate solves at 960 bits (`amp_flint_par.py` line 168
  and 444); macm3 is Apple M3 with python-flint 0.9.0, its FLINT version is not in T153's README, win2 is x86-64 AVX2 with
  python-flint 0.9.0 / FLINT 3.6.0 on Python 3.14.10.

`analyze_202.py` (`analyze_202.log`) recomputes #82's table with win2's file. Its control reproduces #82's posted values (nine
entries, n = 7, 9, 16 of the three rows). |dsigma_n|/|sigma_n| of #82's K 45, J 1500 node, from the 20 stored digits:

| n | 6 | 7 | 8 | 9 | 14 | 15 | 16 |
|---|---|---|---|---|---|---|---|
| 1.09 against T155-win2 K 33 | 0 | 6.7e-20 | 8.5e-20 | 3.2e-17 | 9.3e-17 | 2.5e-16 | 3.5e-16 |
| 1.11 against T155-win2 K 33 | 0 | 3.6e-19 | 9.9e-20 | 3.3e-18 | 1.3e-16 | 2.8e-16 | 4.4e-16 |
| 1.10 against T153-macm3 K 33 | 9.7e-21 | 1.2e-18 | 6.1e-20 | 9.4e-18 | 1.3e-16 | 4.0e-16 | 1.2e-15 |
| 1.10 against this folder's win2 K 33 | 9.7e-21 | 1.2e-18 | 6.1e-20 | 9.4e-18 | 1.3e-16 | 4.0e-16 | 1.2e-15 |

The 1.10 row with win2's K 33 file equals the row with macm3's to the digits shown (the files differ only at sigma_16, 1.5e-19).
It is above the larger of the 1.09 and 1.11 rows at n = 6 (9.7e-21 against 0), n = 7 (3.3 times), n = 15 (1.46 times) and
n = 16 (2.79 times), within it at n = 1 to 5 and 8 to 14. The second acceptance condition of #202 is not met.
