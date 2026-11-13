# I643-win: RT's weakest direction on the K = 7 roots and on an N_t = 48 state at D 50 (rt_sigma.py, rough starts)

Machine win (Surface Laptop 4, i7-1185G7, 32 GB), issue https://github.com/nmoinvaz/choptuik-large-d/issues/643 (the coordinator's message `1794552400733-0` on the `choptuik-large-d` channel; follows #423, raw `I423-win/` at 3d0a1b2c, and #163, raw `I163-mac/`). Worktree `choptuik-i423` (reused, main 5135cdeb, `solver/rt/rt_sigma.py` and `rt_run.py`), venv-t151 (Python 3.10, numpy 2.2.6, scipy 1.15.3, python-flint 0.9.0), `rt_launch.py` and `resource.py` of `I423-win/` (supply `multidouble._dd_dot`, `math.fma` and the Unix `resource` module; no repository file changes). Pure Python. BLAS threads: 2 for a matrix under 4 GiB, one above (AGENTS.md; #423 found multithreaded OpenBLAS crashes on 4 GiB matrices on this machine).

## Plan, written before the runs (the issue's acceptance)

1. **Checks first**, repeated for this task: `rt_sigma.py --planted` must exit 0 and `--planted --mutate=shift` must exit 1 (logs `planted.log`, `planted_mutate_shift.log`).
2. **The K = 7 states** (#163's roots with horizon rows, `horizon` 7 in their metadata, 32x121, D 50.007491, read in place from the raw repository's origin/main checkout): `I163-mac/acc/a_32x121_D50.0075_32x121.npz` (start a) and `b_32x121_D50.0075_32x121.npz` (start b). As the same-process controls without rows (`horizon` 0, same starts, same code, `--mutate=norows`): `a_32x121_mutnorows_D50.0075_32x121.npz` and `b_32x121_mutnorows_...`. Each is run with `rt_sigma.py --starts 3`, rough (the acceptance) and smooth (for #423's rules).
3. **The N_t = 48 state at D 50.** The raw repository has none (its 48-wide states are D 40.02 on 48x141, D 60.002 on 48x95 and D <= 30 on 48x101), so I make one the way #145 made its D 40 one: re-solve the stored D 50.007491 K = 0 root `I145-mac/fol/fol_32x121_D50.0075_32x121.npz` (the state #423 measured at 32x121) on 48x121 with `rt_run.py --start ... --grids 48x121 --solver mp --tol 1e-12 --max_products 250 --refresh_dz 1e-5 --patient --it_max 20 --full_below 1e-4 --newton_tol 1e-40 --horizon 0` (#163's `run_one.sh` options, 192 bits). A solve that does not converge to max|F| <= 1e-36 is reported and the N_t = 48 part stops there. Its Delta is compared with the 32x121 root's and with hp's double-double row (`hp/data/delta_all.csv`, err 2e-15). It is then run like the others. The matrix is 3.1 GiB (L about 20500), under 4 GiB.
4. **Classification, #423's rules, unchanged** (`I423-win/README.md`): per run the best bound over 3 starts; x's class from the best start's content relative to its largest field entry: *edge* if E >= 0.5 and E >= 3 C0, *centre in omega_4* if C4 >= 0.5 and C4 >= 3 E, else *mixed*; *seen by smooth* if the smooth bound is within 100 of the rough one. The D trend cannot be formed from a single D, so criterion 3 is carried over from #423's 32x121 K = 0 series (D 40 to 50: -0.57 decades per 10 in D, not horizon-like) and said to be carried over. Verdict per state: (H) = edge + seen only by rough + horizon-like (impossible with the carried trend, so (H) cannot come out here); (C) = centre in omega_4 + seen by smooth + not horizon-like; **neither** otherwise, with the parts named. The table also gives, for each state, the bound against #423's K = 0 value at the same grid (rough 1.404e-34 at 32x121, D 50.007) and against #163's (4.9e-34 with the rows, 1.2e-34 without), so the question the issue asks, whether the rows move where x sits, is answered by comparing the class and the bound of the K = 7 states with their K = 0 controls.
5. **Reproduction as a control**: the K = 0 state `a_32x121_mutnorows` was measured by #163 at 1.2e-34 (rough, best of 2); here it must come out within a factor 3.

## Summary

The planted check passes (exit 0) and its `--mutate=shift` control fails (exit 1). All ten `rt_sigma.py` runs finished with exit 0, and the N_t = 48 state at D 50 was made (a 48x121 re-solve that converged to max|F| 1.3e-55 after 11 Newton steps). By #423's rules:

| state | K | rough bound (best of 3) | smooth bound | smooth / rough | where x sits (rough start) | verdict |
|---|---|---|---|---|---|---|
| #163 start a, 32x121 | **7** | 4.882e-34 | 2.698e-33 | 5.5, **seen by smooth** | omega_4 near xi = 0 (C4 1.00, E 0.30, mu 0.14) | **(C)** |
| #163 start b, 32x121 | **7** | 6.112e-34 | 2.487e-33 | 4.1, **seen by smooth** | omega_4 near xi = 0 (C4 1.00, E 0.20, mu 0.05) | **(C)** |
| start a without rows (control), 32x121 | 0 | 1.184e-34 | 2.380e-19 | 2.0e15, not seen | mixed (C4 1.00 but E 0.40, mu 0.34) | neither |
| start b without rows (control), 32x121 | 0 | 7.817e-35 | 8.852e-20 | 1.1e15, not seen | mixed (C4 1.00 but E 0.60, mu 0.50) | neither |
| **N_t = 48**, 48x121, D 50.007 | 0 | 9.893e-35 | 1.606e-19 | 1.6e15, not seen | omega_4 near xi = 0 (C4 1.00, E 0.30, mu 0.10) | neither |

**Do the rows move where x sits? No.** In all eight runs of the four 32x121 states the largest content of x is in omega_4 near xi = 0 (C4 = 1.00), as in #423; what the rows change is smaller: the edge content falls (0.40 to 0.30 and 0.60 to 0.20) and the mu content falls (0.34 to 0.14 and 0.50 to 0.05), which moves the class from "mixed" to "centre in omega_4" by the rules' 3E threshold; the rough bound rises by a factor 4.1 and 7.8 (the rows remove part of the weak space, they do not remove the direction); and, **the one large effect, smooth starts now reach the direction**: the best smooth bound goes from 2.4e-19 and 8.9e-20 without rows to 2.7e-33 and 2.5e-33 with them, within a factor 6 of the rough bound instead of 10^15. The K = 7 verdict is therefore (C) on all three parts (centre in omega_4, seen by smooth, not horizon-like with the trend carried from #423), where #423's K = 0 states were "neither" because smooth starts did not see the direction. The N_t = 48 state is "neither", by the failure of smooth starts, with x in omega_4 near xi = 0 as at N_t = 32.

## What ran

Checks: `logs/planted.log` (`rt_sigma.py --planted`: best bound 1.41e-21 in [1e-22, 1e-20], exit 0) and `logs/planted_mutate_shift.log` (`--mutate=shift`: 1.42e-19, FAIL, exit 1).

`run_423.py` (copied from `I423-win/`; its log is `logs/run_423.log`), BelowNormal, 3 starts per run, `rt_sigma.py`'s defaults (192 bits, 250 products), worktree `choptuik-i423` at main 5135cdeb, venv-t151 through `rt_launch.py`:

| runs | BLAS threads | start (UTC) | end |
|---|---|---|---|
| K7_a, K0_a, K7_b, K0_b, smooth and rough (8 runs) | 2 | 07:13:20 | 08:57:31 (K7_b rough, 2570 s; K0 runs 881 to 916 s; K7 smooth 1558 to 2489 s, K7_a rough 2780 s) |
| NT48 smooth and rough | **1** (3.1 GiB matrix; the coordinator's rule after the OpenBLAS finding) | 08:55:39 | 09:23:57 (1693 s and 1698 s) |

The first K = 7 and K = 0 runs shared the machine with the OpenBLAS side-task tests of #423 (07:13 to about 07:38), which lengthened them.

**The N_t = 48 state** (`run_nt48.py`, `nt48/`, `logs/nt48_121.log`): `rt_run.py --solver mp` (192 bits) of `I145-mac/fol/fol_32x121_D50.0075_32x121.npz` on 48x121 at D 50.007491, #163's options, started 07:09:27 UTC, 6342 s, 2 BLAS threads (the f64 Jacobian is 3.1 GiB, below the 3.44 GiB where crashes appeared; peak resident memory 6.88 GB). It did not converge smoothly: max|F| wandered for ten steps between about 1e-30 and 1e-12 (2.0e-17, 2.5e-16, 1.3e-12, 3.2e-12, 2.1e-23, 2.8e-12, 1.2e-23, 2.7e-16, 1.6e-30, 4.8e-28), then step 10 reached 1.25e-55 and the run stopped converged (`ok` true in `nt48/nt48_121.jsonl`; state `nt48/nt48_121_D50.0075_48x121.npz`, 11 steps, max|F| stored in double-double 4.7e-31). Its Delta is 1.8416311331993655570, **2.90e-12 below hp's row** (1.8416311332022643, err 2e-15), the same miss as the 32x121 root it started from (-2.9e-12); rt_run.py's own check against 1e-12 therefore printed FAIL and exited 1, which is the quantity under study, not a failure of the solve.

## Results (`table_643.txt`)

| state | K | grid | kind | bound (best of 3) | starts' spread | worst residual | products | mu | E (edge) | C0 (centre) | C4 (w4 centre) | class |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| a_32x121_D50.0075_32x121.npz | 7 | 32x121 | rough | 4.882e-34 | 7.1 | 4.9e-15 | 250 | 0.14 | 0.30 | 1.00 | 1.00 | centre in w4 |
| a_32x121_D50.0075_32x121.npz | 7 | 32x121 | smooth | 2.698e-33 | 2.1 | 7.2e-17 | 175 | 0.16 | 0.30 | 1.00 | 1.00 | centre in w4 |
| a_32x121_mutnorows_D50.0075_32x121.npz | 0 | 32x121 | rough | 1.184e-34 | 2.2 | 9.6e-20 | 76 | 0.34 | 0.40 | 1.00 | 1.00 | mixed |
| a_32x121_mutnorows_D50.0075_32x121.npz | 0 | 32x121 | smooth | 2.380e-19 | 7.9 | 4.5e-31 | 76 | 0.33 | 0.40 | 1.00 | 1.00 | mixed |
| b_32x121_D50.0075_32x121.npz | 7 | 32x121 | rough | 6.112e-34 | 12.2 | 1.4e-15 | 228 | 0.05 | 0.20 | 1.00 | 1.00 | centre in w4 |
| b_32x121_D50.0075_32x121.npz | 7 | 32x121 | smooth | 2.487e-33 | 4.3 | 1.4e-17 | 139 | 0.06 | 0.20 | 1.00 | 1.00 | centre in w4 |
| b_32x121_mutnorows_D50.0075_32x121.npz | 0 | 32x121 | rough | 7.817e-35 | 4.3 | 2.5e-18 | 76 | 0.50 | 0.60 | 1.00 | 1.00 | mixed |
| b_32x121_mutnorows_D50.0075_32x121.npz | 0 | 32x121 | smooth | 8.852e-20 | 26.4 | 2.2e-32 | 76 | 0.51 | 0.60 | 1.00 | 1.00 | mixed |
| C:\Users\nathan\Source\choptuik-large-d-raw\I643-win\nt48\nt48_121_D50.0075_48x121.npz | 0 | 48x121 | rough | 9.893e-35 | 3.5 | 1.3e-18 | 85 | 0.10 | 0.30 | 1.00 | 1.00 | centre in w4 |
| C:\Users\nathan\Source\choptuik-large-d-raw\I643-win\nt48\nt48_121_D50.0075_48x121.npz | 0 | 48x121 | smooth | 1.606e-19 | 1.8 | 2.1e-34 | 85 | 0.02 | 0.30 | 1.00 | 1.00 | centre in w4 |

Per state (smooth against rough, class, verdict by #423's rules with the carried D trend):
  K7_a: rough 4.882e-34, smooth 2.698e-33, smooth/rough 5.53e+00 (seen by smooth); x centre in w4 (rough start; smooth start: centre in w4); trend (carried) not horizon-like -> (C)
  K0_a: rough 1.184e-34, smooth 2.380e-19, smooth/rough 2.01e+15 (not seen by smooth); x mixed (rough start; smooth start: mixed); trend (carried) not horizon-like -> neither
  K7_b: rough 6.112e-34, smooth 2.487e-33, smooth/rough 4.07e+00 (seen by smooth); x centre in w4 (rough start; smooth start: centre in w4); trend (carried) not horizon-like -> (C)
  K0_b: rough 7.817e-35, smooth 8.852e-20, smooth/rough 1.13e+15 (not seen by smooth); x mixed (rough start; smooth start: mixed); trend (carried) not horizon-like -> neither
  NT48: rough 9.893e-35, smooth 1.606e-19, smooth/rough 1.62e+15 (not seen by smooth); x centre in w4 (rough start; smooth start: centre in w4); trend (carried) not horizon-like -> neither

The rows against their same-start controls (rough bound, K = 7 / K = 0):
  start a: 4.882e-34 / 1.184e-34 = 4.12; class centre in w4 (mu 0.14) against mixed (mu 0.34)
  start b: 6.112e-34 / 7.817e-35 = 7.82; class centre in w4 (mu 0.05) against mixed (mu 0.50)

Reproduction of #163 (same code, another machine):
  K0_a rough 1.184e-34 against 1.2e-34: factor 0.99 -> within 3
  K7_a rough 4.882e-34 against 4.9e-34: factor 1.00 -> within 3

N_t = 48 (48x121) rough 9.893e-35 against #423's 32x121 K = 0 at D 50.007 (1.404e-34): factor 0.70

Columns as in #423: the bound is the best of 3 starts, E, C0, C4 the edge, centre and omega_4-centre content of that start's x relative to its largest field entry, mu is |mu| / max|x|. The solve residuals of the K = 7 rough starts are larger than the others (4.9e-15 and 1.4e-15 at the 250-product cap, against 1e-18 to 1e-20), so those bounds 1 / max|x| hold to a relative accuracy of that size; the K = 7 rough starts' spreads are 7.1 and 12.2 (some starts at or near the 250-product cap), against 2.2 to 4.3 for the controls.

## Controls

- **Planted check and its mutation**, above.
- **Reproduction of #163 on this machine:** the K = 0 start-a control gives 1.184e-34 against #163's 1.2e-34 (factor 0.99) and the K = 7 start a gives 4.882e-34 against 4.9e-34 (factor 1.00), inside the plan's factor 3. Same code on another machine and BLAS, not an independent method. #163 also found the smooth K = 7 bound 2.7e-33, which this run's 2.698e-33 reproduces.
- **N_t = 48 against the other 32x121 K = 0 states:** the rough bound 9.89e-35 is a factor 0.70 of #423's 1.404e-34 (the `fol` root) and 0.84 of the start-a control's 1.184e-34. At D 40.02 and N = 141 #423 found a factor 0.19 for the same change of N_t; here, at N = 121 and D 50, the change is smaller, and x stays in omega_4.
- **Not run:** a second implementation of the bound, an SVD of J, more starts than 3 for the K = 7 states (their rough starts range over a factor 7 to 12), K = 7 at other D, and the N_t = 48 state on another N.

## Discrepancies

None with #163 or #423. The N_t = 48 solve behaved differently from the 32-wide ones (a ten-step cycle before converging) and is reported as such; it is not evidence about the K = 7 question.

## Recommended tasks (for the coordinator)

1. **K = 7 at other D.** What: `rt_sigma.py` with rough and smooth starts on K = 7 roots at D 40.02 and 54.996 on 32x121 (`rt_run.py --horizon 7 --resample_mp` from #145's roots, as #163's `run_one.sh`; about 20 min each solve, 15 to 45 min each sigma run). Why: smooth starts reach the weak direction only with the rows, at D 50; whether that holds at D 40 and 55, and whether the bound follows the D trend of #423's K = 0 series (-0.57 and -1.48 decades per 10 in D), would complete the (C) verdict, which here rests on a trend carried over from K = 0. Acceptance: the bound, class and smooth/rough ratio per state, with the planted check and its control repeated. Depends on #643.
