# I814-mac: lam_gauge.csv rebuilt at raw 5d1c629a with the old naming kept, and the fit's top end scanned

Machine: the coordinator's Mac (Apple M5), agent xfkappa. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/814.
Code: wip/xf-814 e25ae01c and 50fd9424, on main d423507a. One process at nice 10.

## Runs

- `table.log`: `python3 hp/lam_gauge.py table <raw at 5d1c629a> --out=...`, the rebuild, `lam_gauge.csv` here.
  `table_rerun_e25ae01c.log` is the same command on the committed code, whose output is byte for byte the CSV here and
  the one committed in e25ae01c.
- `compare.py`, `compare.log`: bars 1 and 2, the stored table (main d423507a) against the rebuild, with main's
  `delta_all.csv`. `compare_control.log`: the tables swapped, which must fail (it does, exit 1).
- `check_full.log`: `check_numbers.py --full --selftest` on e25ae01c. `check_control.log`: the same checks without
  `--full` on the stored table, which must fail (15 of `lam_gauge_table`'s 36 items fail, exit 1).
- `spreads.py`: the same-D groups by kind, in both tables.
- `fit/`: `lam_gauge_fit.py fit` on the stored table (`fit_stored.log`) and on the rebuild (`fit_capped.log`), and
  `fit --dmax=D` for D from 244.64 to 260.
- `past_top.py`, `past_top.log`: λ_g of the 97 backbone states past D 244.64 minus the capped reference fit
  (c₀ = 1, 1/n, degree 14, D ≥ 20).

## Bars (fixed on the issue before the run)

| bar | result | verdict |
|---|---|---|
| 1. every state main's delta_all.csv names is in the table with its err | 1175 of 1175, 0 with another err pair; `lam_gauge_errs` 2 of 2 | PASS |
| 2. every stored state in the rebuild, λ_g, Δ, μ unchanged to the bit | 1510 of 1510, 0 changed (D and D_str too) | PASS |
| 3. `lam_gauge_table` passes, only 10.3's table numbers updated | 36 of 36 on the rebuild, 21 of 36 on the stored table | PASS |
| 4. any 10.4 or 10.5 number that moves is listed | none moves: `full_lam_gauge` 24 of 24; the capped fit's log equals the stored table's but for two range ends in the 11th digit and one more superseded line (crawlB3 at 225.13, 6.2e-14 off) | PASS |

## The rebuild

| | stored (raw 6913f312) | rebuild (raw 5d1c629a) |
|---|---|---|
| rows | 1510 | 1621 |
| backbone D | 1274 | 1371 |
| frontier D | 244.6366 | 259.7436 |
| λ_g at the frontier | 0.9711585000283656 | 0.9728509437334254 |
| n(1 − λ_g) at the frontier | 6.998004 | 6.9974954 |

New rows, 111: I603 chain_nsr 63, chain 26, chain_ns 5, I461 crawlB3 10 (D 216.13 to 225.13, which delta_all.csv names
in place of crawlG's), T84-mac 4 (re-solves of pin 7 at D 72.0, 72.4, 73.1, 73.27). Role changes: 20 backbone to alt
(crawlG at 216.13 to 224.13, T73 at 70.65 to 70.95, T75 at 72.0 to 73.27), 7 alt to backbone (T75 at 70.65 to 70.95).

Same-D spreads, over states, not bounds:

| group | D | largest spread |
|---|---|---|
| chain, #603 against I461 | 14 | 3.83e-13 at 237.13 |
| chain, I461 crawlB3 against crawlG | 9 | 6.05e-20 at 223.13 |
| pinned, 5 against 7, and T75 against T84-mac at 73.27 | 161 | 1.58e-14 at 67.75 |
| dd, M differs | 11 | 3.2e-8 at D 4 |
| dd, same M | 1 | 1.46e-31 at D 4.25 |

## μ and n(1 − λ_g) along the backbone

| | D | value |
|---|---|---|
| μ, local minimum | 38.020417 | 0.1291016242 |
| μ, maximum past D 50 | 256.01305 | 0.1303100340 |
| n(1 − λ_g), maximum | 258.60047 | 7.0321072 |
| first D past 50 with μ below the D 38 minimum | 259.05048 | 0.1290540399 |
| μ at the frontier | 259.74360 | 0.1274355406 |

## The fit's top end (`fit --dmax=D`, a diagnostic outside the selection)

| D_max | points | c₁ (c₀ = 1) | c₂ | c₃ | largest residual |
|---|---|---|---|---|---|
| 244.64 | 200 | −7.4165644374 ± 4.4e-6 | 107.508630 ± 0.0069 | −1529.97 ± 4.9 | −7.5e-13 at 244.64 |
| 246 | 201 | −7.4165644418 ± 7.7e-6 | 107.508644 ± 0.012 | −1529.97 ± 8.6 | −1.5e-12 at 245.64 |
| 248 | 202 | −7.4165644299 ± 2.9e-6 | 107.508627 ± 0.0045 | −1529.97 ± 3.2 | −1.5e-12 at 245.64 |
| 250 | 204 | −7.4165648653 ± 2.7e-4 | 107.508996 ± 0.42 | −1530.1 ± 300 | −1.2e-10 at 249.87 |
| 252 | 205 | −7.4165684515 ± 0.003 | 107.51194 ± 4.7 | −1531 ± 3400 | −1.1e-9 at 251.30 |
| 254 | 207 | −7.41645478 ± 0.12 | 107.43 ± 190 | −1504 ± 1.4e5 | 5.1e-8 at 253.64 |
| 256 | 208 | −7.41635823 ± 0.26 | 107.38 ± 420 | −1481 ± 3.0e5 | 8.3e-8 at 254.80 |
| 258 | 210 | −7.4265267 ± 29 | 116.1 ± 4.6e4 | −3347 ± 3.4e7 | −1.4e-5 at 257.20 |
| 260 | 212 | −7.4412665 ± 70 | 126.9 ± 1.1e5 | −5393 ± 8.2e7 | −4.1e-5 at 258.25 |

± is the half-width of the kept fits' range, a spread over fit choices, not a bound. The fit is stable to D 248 and
stops agreeing from D 250 on.

λ_g of the chain minus the capped reference fit (`past_top.log`): −1.1e-12 at 245.14, past 1e-11 from 248.02, 1e-10
from 249.87, 1e-9 from 251.30, 1e-7 from 254.21, 1e-6 from 256.01, 1e-5 from 256.95; −4.7e-5 at 258.71 and +9.2e-5 at
259.74. It changes sign five times (near 246.6, 249.2, 252.1, 255.2 and 259.27).

## Discrepancies

- notes/MODE_COUNT.md 10.3's spread table counts 11 double-double D ("M or layout differs"); both builds have 12 (the
  12th is D 4.25, two M = 48 states, 1.5e-31). Reported in the note, not changed.
- #765's sentence in 10.3 said delta_all.csv names #603's states in place of #461's from D 216.13. It names #461's
  crawlB3 states in place of crawlG's from 216.13 to 225.13, and #603's from 226.13. Corrected in the rewritten 10.3.
