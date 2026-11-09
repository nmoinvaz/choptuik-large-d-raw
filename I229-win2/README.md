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

## Results

The run ended with exit 0 at k 33 on 2026-11-09 07:01:18 UTC, 11 034 s after its 03:57:24 start (2 processes; products 1643.7 s,
fit setup 28.7 s, fits 9355.1 s), beside #213 (three K 45 nodes, 12 processes) and the #204 watchers. `exits.txt`,
`w1.10_procs2.log`, `sigF_w1.10_K33_J1000_procs2.json`.

`compare_229.log` (exit 0; `compare_229_selftest.log` ok, it checks all three verdicts and a planted digit):

- against win2's `--procs 3` file (`../I202-win2`): first differing entry `/f/33_3[0]`, win2 procs 2 -6.60733747128514e-27 against
  procs 3 -6.607337464172256e-27;
- against macm3's `--procs 2` file (`../T153-macm3`): bit for bit equal (timing keys and `procs` dropped), all `sigma_str`,
  `sigma_err`, `f` and `fit_info` entries.

Verdict: the difference follows the process count. With 2 processes win2 reproduces macm3's file bit for bit, on a different CPU
(Intel Core Ultra 7 265K against Apple M3), OS (Windows against macOS) and, as far as recorded, FLINT build; with 3 processes it
differs from both at sigma_16 (1.5e-19 relative), at three `f` entries and in `fit_info` err and resid from order 21 on
(`../I202-win2/analyze_202.log`, part 1).

A mechanism the code allows, not tested here: `AmpPar._products` deals the tasks of an order to the workers in turn
(`tasks[i::nw]`) and adds their partial sums per group (`_add_rows`), so the order of summation, and with it the rounding of the
960-bit midpoints, depends on the number of workers; the late-order fits amplify that. The process count at 1 and 4 was not run.
