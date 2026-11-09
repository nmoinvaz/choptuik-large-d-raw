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

## Results (2026-11-09 13:18 UTC)

All twelve runs ended with exit 0 (`exits.txt`, `exits_fixsum.txt`). Walls, beside #213 (not a clean timing; the load differed between batches):

| `--procs` | r1 | r2 | fixed summation |
|---|---|---|---|
| 1 | 7450 s | 7387 s | 7459 s |
| 2 | 4369 s | 4319 s | 4894 s |
| 3 | 3292 s | 3235 s | 3939 s |
| 4 | 2719 s | 2672 s | 3407 s |

`compare_236.py` (`compare_236.log`, exit 0; `compare_236_selftest.log` ok, it plants a changed digit in one sigma string, one `f`
entry, one `fit_info` entry and one `sigma_err` entry, and a differing pair of equal counts that must give exit 1):

- Equal counts give equal bits: r1 against r2 is bit for bit equal for counts 1, 2, 3 and 4 (4 of 4 pairs), after dropping the
  timing keys and `procs`.
- Different counts: all six pairs of counts differ (24 run pairs), the same way each time. `sigma_str` (13 strings of 20
  digits), `sigma_err`, `f` (78 entries) and every other key are equal; `fit_info` (Mf, err, resid) has Mf equal in all 91
  families and err and resid different in 11 of them, the first at `21_19`, the others 21_21, 23_15, 23_17, 23_19, 23_21,
  23_23, 25_19, 25_21, 25_23, 25_25. In each of the 11 the four counts have four different triples. Largest relative
  difference between two runs: 1.29 in err, 0.095 in resid. So no two counts reproduce each other at K 25, J 1000.

Mechanism test (`amp_flint_par_fixsum.py`, one run per count, `compare_fixsum.log`): `_products` of the module in
`solver/inner_amp` (main, unchanged) is replaced so that every task of an order is a chunk of its own and the main adds the single
products per group in task order, the association of the serial path. The four runs (counts 1 to 4) are bit for bit equal to each
other (six pairs) and to the original `--procs 1` runs (r1 and r2), while the variant with 2, 3 or 4 workers differs from the
original run with the same count in the same 11 `fit_info` families. So the summation order of the workers' partial products
is the source of the dependence at K 25. `smoke/` holds the K 13 test (variant at 1, 2, 3 equal to the original at 1).
