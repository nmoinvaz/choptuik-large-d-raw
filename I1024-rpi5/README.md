# I1024-rpi5: the P2 review checks p2c_disc.py, p2c_h8.py, p2c_b5.py rerun on aarch64 (Raspberry Pi 5, Linux)

Machine rpi5 (Raspberry Pi 5, Cortex-A76 x 4, 8 GB, aarch64, Linux 6.17, Python 3.13.7), runner, under the claude-me2 account.
Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1024 (#992, #1017, #1019 reproduced), assigned by message 2026-11-19.
Code: worktree `~/Source/choptuik-large-d-964` detached at origin/main 065b50dc, `solver/proof/review_p2c/`. Venv `~/Source/venv-choptuik`:
python-flint 0.9.0, FLINT 3.6.0 (`flint.__FLINT_RELEASE__` 30600), mpmath 1.3.0, numpy 2.5.4. nice 10, one run at a time.
The Mac's runs (I992-mac, I1017-mac, I1019-mac) were Apple M5, macOS, Python 3.14 (`/Users/nathan/venv-314`), python-flint 0.9.0, FLINT 3.6.0 (I992's README), mpmath for p2c_h8 and p2c_b5.

## Written down before the runs

Commands, from `solver/proof/review_p2c/` (the issue's list; `run1024.sh` is the driver, with each run's expected exit code):

| run | command | expected exit |
|---|---|---|
| disc_checkeq | `p2c_disc.py --checkeq` | 0 |
| disc_checkint | `p2c_disc.py --checkint` | 0 |
| disc_ray | `p2c_disc.py --discs=ray --out=$R` | 0 |
| disc_all_infl2 | `p2c_disc.py --discs=all --infl=2 --tag=all_infl2 --out=$R` | 0 |
| disc_K1_toolarge | `p2c_disc.py --discs=11:0 --radius=16 --out=$R` (control) | 1 |
| disc_K2_sign | `p2c_disc.py --discs=ray --mutate=sign --out=$R` (control) | 1 |
| h8_centre | `p2c_h8.py --centre` | 0 |
| h8_d0_0 | `p2c_h8.py --d0=0 --out=$R` | 0 |
| h8_d0_1e7 | `p2c_h8.py --d0=1e7 --out=$R` | 0 |
| h8_centre_mut_A | `p2c_h8.py --centre --mutate=A` (control) | 1 |
| h8_d0_0_mut_sign | `p2c_h8.py --d0=0 --mutate=sign` (control) | 1 |
| b5_model | `p2c_b5.py --model` | 0 |
| b5_phiz | `p2c_b5.py --phiz` | 0 |
| b5_residual | `p2c_b5.py --residual` | 0 |
| b5_sector_box | `p2c_b5.py --sector --box` (nr 8, na 24 as the issue lists it) | 0 |
| b5_phiz_mut_G0 | `p2c_b5.py --phiz --mutate=G0` (control) | 1 |
| b5_residual_mut_offphi | `p2c_b5.py --residual --mutate=offphi` (control) | 1 |

Added by me, because the issue's bare `--sector --box` uses the script's defaults (8 x 24 cells) while the Mac's I1019 log used 3073 cells: `b5_sector_box_nr32_na64`, `p2c_b5.py --sector --box --nr=32 --na=64 --out=$R` (notes/P2_remaining.md 6's command, expected exit 0, about 2 min on the Mac), the one to compare with I1019's `sector_box.log`.

Acceptance (the issue's): every run's exit code as listed, and the printed numbers (Lambda, M, delta, the sector constants) equal the Mac's logs to their printed digits. A difference in the last printed digit is reported, not a failure (arb radii can move with the build).
Comparison method (`compare1024.py`): each of my logs against the Mac's log of the same run, line by line with the timings ("[x s]", "(N s)") masked; a different line is listed with both texts. `--checkeq` prints only to the console on the Mac (not in I992-mac), so its reading is the exit code and the printed line.
Not decided here: nothing; a number that differs is listed and the coordinator judges it.

## Results (2026-11-19, 12:29 to 13:14 UTC, 45 min wall in all; `logs/driver.log`, `logs/exits.txt`)

**Every run exited as listed: 18 of 18** (the 17 of the issue and my extra), the six controls with exit 1 as required (`disc_K1_toolarge`, `disc_K2_sign`, `h8_centre_mut_A`, `h8_d0_0_mut_sign`, `b5_phiz_mut_G0`, `b5_residual_mut_offphi`).
Wall seconds: disc_checkeq 1, disc_checkint 62, disc_ray 19, disc_K1 1, disc_K2 19, h8_centre 118, h8_centre_mut_A 119, h8_d0_0 162, h8_d0_1e7 163, h8_d0_0_mut_sign 163, b5_model 0, b5_phiz 0, b5_residual 61, b5_phiz_mut_G0 0, b5_residual_mut_offphi 60, b5_sector_box (8 x 24, 289 cells) 186, b5_sector_box_nr32_na64 (3073 cells) 545, disc_all_infl2 1010.

**The printed numbers equal the Mac's: every one of the 15 logs with a Mac counterpart has 0 differing lines** (`logs/compare.log`, timings and the output path masked). Headline values, as printed here and there: disc ray 12 of 12 certified, all (inflation 2) 178 of 178, largest Lambda 0.541; K1 0 of 1; K2 0 of 12; (H8) delta = (5.58564e-12, 79.0419, 3.23126, 6.4634) against delta_ref (1, 200, 10, 20), (P2) PASS at d0 = 0 and d0 = 1e7; B5 sector box at 3073 cells: R_C 3.34546, T_F 3.93443, R_Phi 49.5804, the Mac's `sector_box.log` line for line. The bare `--sector --box` (289 cells) has no Mac log: R_C 3.37694, R_Phi 63.5616, Perron-weighted norm 0.94962, every super-solution certified, (P2) PASS (it is a coarser grid, so its constants are larger than the 3073-cell ones, as expected).
`--checkeq` prints only to the console on the Mac (nothing in I992-mac), so its reading here is the line and the exit code: worst relative difference 3.45e-58 at 10 random points, PASS.
`p2c_h8.py --d0=0 --mutate=sign` and the plain `--sector --box` have no Mac log either (I1017 ran `--centre --mutate=sign` and `--mutate=hS`); here only their exit codes are compared.

**The records differ in the last digits for 8 of the 178 discs (`logs/compare.log` lists every differing leaf at its end):** `p2c_disc_all_infl2.jsonl` against the Mac's, 37 numeric leaves, none in `ok` or any string. Discs (7, 8) to (7, 12) and (9, 9) to (9, 11), all with a reconstructed input box (k >= 1): Mmax and M0max by 2e-14 to 5e-13 relative, Lambda by 1e-12 to 5e-11, F0 and bmax (the cleared defect's scale, 1e-87 to 1e-52) by 5e-10 to 1.7e-8. The 12 stored-input ray discs, the K1 and K2 records, the h8 box JSONs and the b5 JSON are identical to the last stored digit. The differences are below every printed digit, and they are in the quantities that depend on the reconstructed boxes (the script's own non-rigorous integration from the row-start midpoint), so a build-dependent last digit there is the likely cause; I did not trace it further. The acceptance rule treats a last-digit difference as a report, not a failure.
`compare1024.py` controls (`logs/compare_mutate.log`): `--mutate` changes one printed Lambda digit of the rpi5 disc_ray log (reported as 1 differing line) and one float of `p2c_disc_ray.jsonl` by 1e-12 relative (reported, `/Lam`), so the comparison can fail.
