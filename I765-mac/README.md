# I765-mac: formula_cut.json reproduced from a stated commit, and lam_gauge.csv's err columns refreshed

Machine: the coordinator's Mac (Apple M5), agent xfkappa, one process at nice 10.
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/765
Code: `hp/formula_cut_fit.py` (with `--data-commit`, `--verify`), `hp/lam_gauge.py` (with `errs`), `check_numbers.py`
(`lam_gauge_errs`) of choptuik-large-d, branch wip/xf-765 (e9ed1ad1, 9dc6acf3) on main 3fb35dc7. python-flint 0.9.0.

| file | what |
|---|---|
| `formula_cut_verify.log` | `formula_cut_fit.py --data-commit 437b82a5 --verify` (PASS, byte for byte, exit 0) and its control at main 3fb35dc7 (FAIL, exit 1) |
| `lam_gauge_table_rebuild.log`, `lam_gauge_full_rebuild_at_6913f312.csv` | the full `lam_gauge.py table` rebuild on raw 6913f312 with main's delta_all.csv: not adopted (below) |
| `lam_gauge_errs.log` | `lam_gauge.py errs`: 761 rows' err columns set from delta_all.csv |

## formula_cut.json

Run from the 437b82a5 tree (its formula_cut_fit.py, dd_fits_mp.py and tables), the fit reproduces the stored file
byte for byte; neither script has changed since, only the tables (7eac2956, 71786d69, ff8a20d2, 5474fc41). The file now
records `data_commit: 437b82a5` and otherwise equals the old one. A refit on main 3fb35dc7's tables would give 1232
points (quoted 1214), max |r|/sigma 3.66 (quoted 3.47), Delta_inf 1.6438937452497 (quoted 1.643893745, unchanged at
the quoted digits) and Delta(3) 1.91891729393 (6.2e-5 below the stored 1.91897918858, not quoted), so it was not made.

## lam_gauge.csv

The bar posted before the run (against the stored file only Delta_err, Delta_err_kind may differ) failed for a full
`table` rebuild on the file's own raw commit 6913f312 with main's delta_all.csv: 1486 rows against 1510, 38 #461 chain
states (D 216.13 to 242.57) gone and 14 #603 states added, `named` changed on 43 common rows, `role` on 18,
`n_same_D` and `spread_same_D` on 31; lambda_g, Delta and mu identical on the 1472 common rows. The cause is that
delta_all.csv now names #603's states in place of #461's from D 216.13 and pin 7's in place of pin 5's from D 70.65.
With that file check_numbers' lam_gauge_table fails (the superseded #461 rows that MODE_COUNT.md 10.4 quotes are gone),
so it was not adopted. `lam_gauge.py errs` instead sets the two err columns on the 1064 rows whose state delta_all.csv
names, every other column kept: 761 changed, all of them empty before, and delta_all.csv has an err for every named
row. The new check_numbers item `lam_gauge_errs` gave 761 and 761 on the old file and 0 and 0 after. check_numbers
--full --selftest: 1855 of 1855, selftest 1855 of 1855.
