# I787-mac: hp/update_delta.py with the weak pivot err, track C's series rows and the prediction screen

Machine: the Mac (Apple M5, the coordinator's machine), one process at nice 10, venv-314. Issues: #787, #804 and #806
of https://github.com/nmoinvaz/choptuik-large-d. Code: branch `wip/i787` at 44126bd1 (4c16220c the code, 44126bd1 the
rebuilt tables and checks). Raw data: this repository at 8f7b2dcf (origin/main at the run).

## Commands (from hp/, RAW a clone of this repository at 8f7b2dcf)

    python3 update_delta.py RAW                                    > update_delta.log   (exit 0)
    python3 track_c.py real                                        > trackc_real_main.log (on main's table, before)
    python3 track_c.py real                                        > trackc_real_rebuilt.log (on the rebuilt table)
    python3 export_delta_all.py RAW --verify [--mutate=series|weak_pivot]   > verify*.log
    python3 export_delta_all.py RAW --lam_screen [--mutate=lam|lam_pred]    > lam_screen*.log

`export_pass1.log`, `trackc_csv.log` and `export_pass2.log` are the steps that `update_delta.py` now runs (4 and 4b),
run one by one first.

## Results

| check | result |
|---|---|
| update_delta.py | every step ok, every control fails by its check. chain, projector and one_sided are skipped: no rows of those kinds, as on main |
| delta_all.csv | 2339 → 2450 rows: 95 new chain_fit rows from 246.26 to 259.74, 16 series rows from 250 to 400, 22 rows changed, none gone |
| the 22 changed rows | chain_fit below 245.64, now with fits differences that #608's newer comparison states measure ("fits d10 interp", for example), in place of "fits extrapolated" |
| weak pivot coverage (#806) | 95 of 95 rows past 245.64 within their err of the series, largest ratio 0.811 at 259.05 |
| --mutate=weak_pivot (K halved) | fails at 13 rows: 252.61 (by 0.4%, the calibration state at exactly half K), 255.05, and 11 from 258.44 to 259.16 |
| --mutate=series | fails at D 250 |
| --lam_screen (#787) | 286 of 286 backbone states, 87 past 250.46 by the prediction check |
| --mutate=lam, --mutate=lam_pred | fail: 1e-10 at 240.12 (polynomial), 1e-10 at 255.05 (prediction) |
| track C on the rebuilt table | Δ(250) 1.684955205950 ± 8.03e-11, Δ(300) 1.678171015415 ± 1.24e-10, Δ(400) 1.669658064111 ± 2.33e-10 |

**Held back.** The chain's newest state, D 259.7510, has no stored pivot yet (win2's run has not stepped from it), so it
has no row until it has one.
