# I1025-win2/kc95_leap: a k_c 95 leap along D from winb's D 21.0 and dh170's D 21.125 states (the third resolution)

Machine: win2 (desktop-pc, Windows 11, 20 logical cores). Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1025. Written 2026-11-24 16:15 UTC, before any run of this folder (the dry run at 16:12 UTC ran only the pins and the seed checks).

## The order (the coordinator's hc, 2026-11-24 ~16:20 UTC, verbatim)

"no restart of tag g; let it end at its cap (19:19:49 UTC). ... FOR THE FREED THREADS, at tag g's end: a k_c 95 leap, the third resolution along D. Seeds: winb's accepted k_c 95 state at D 21.0 (raw I1025-win/kc95_d21, state d7a4844a, record 2e8fe124) and dh170's at D 21.125 (raw I1025-dh170/kc95_d21125); check both with kc95_syscheck_1025.py first (dh610's, controls must exit 1; the kc87 check must refuse them). Command: ell_leap.py l1kc95Lw1025k 1 95 <seed 21.0> 21.0 <seed 21.125> 21.125 21.75 0.0625 --tol 1e-12 --fmax 1e-8 --cmax 1e-2 --fold, 4 threads, the same guard (--seeds), 12 h cap, raw kc95_leap/ in your folder, README first. Dry run before the cap so it starts at once. Report each point with the usual row."

## Inputs (copies in `inputs/`, pinned by git blob; the driver refuses any other blob)

| item | raw source | blob |
|---|---|---|
| winb's k_c 95 state at D 21.0 (`sol_l1kc95winbg_D21.0000.npy`, 49848 bytes) | `I1025-win/kc95_d21/` | d7a4844a (the coordinator's) |
| its record `l1kc95winbg.jsonl` (one row: D 21.0, kc 95, \|F\| 4.5952560080e-10, F_start 1.469e-5, 3219 steps, psi-constraint 1.646e-3, Delta 1.118224805703, 8985 s) | same folder | 4d6ca87d (LF form); **2e8fe124 is the same row with CRLF line ends** (`regrid_accepted.txt` of winb's folder lists the CRLF form; checked: LF-to-CRLF conversion of the raw copy gives 2e8fe124 exactly) |
| dh170's k_c 95 state at D 21.125 (`sol_l1kc95dh170f_D21.1250.npy`) | `I1025-dh170/kc95_d21125/` | c9d37744 |
| its record `l1kc95dh170f.jsonl` (D 21.125, \|F\| 4.6199429159e-10, F_start 1.664e-5, 3206 steps, constraint 1.859e-3, Delta 1.121573196527, 5520 s) | same folder | 6df5a5ee |
| `kc95_syscheck_1025.py` (dh610's: the k_c 87 check with the k_c test changed to 95) | `I1025-dh170/kc95_d21125/in/` | d487e628 |
| `kc87_syscheck_1025.py` | same | 6df5d960 |

Code: the worktree `D:/choptuik-i1025k79` at 48c36355 (`dss_ell.py`, `ell_ddm.py`, `ell_dd.py`, `ddnp.py` equal 505d8399's; `ell_leap.py` 1eb873e4), python of `venv-md510`, the code of every leap and regrid here. Guard: `../kc71_leap/leap_guard.py` f1fe7c7c.

## The seed checks (dry run 16:12 UTC, `run_kc95.sh`, `DRY=1`)

`kc95_syscheck_1025.py` selftest exit 0; on winb's seed exit 0 (record |F| 4.5952560080e-10, state |F| 4.5961869028e-10, `freeze_from` 3219 steps = the record's), `--mutate=F` and `--mutate=steps` exit 1; on dh170's seed exit 0 (record |F| 4.6199429159e-10, state |F| 4.6222148090e-10, 3206 steps = the record's), both controls exit 1; `kc87_syscheck_1025.py` selftest exit 0 and exit 1 ("NOT ACCEPTED: the record is not k_c 87 at D 21 (kc 95, D 21.0)" and "at D 21.125") on both. The checks are repeated when the leap starts.

## The run

`run_kc95.sh` (headless, BelowNormal, started 16:1x UTC) waits for `../kc79_leap/all8.done` (the tag g leap's end at its cap, 19:19:49 UTC; any end of tag g frees its 4 threads), repeats the pins and the seed checks, copies the two seed records for the guard, starts the guard (`leap_guard.py --seeds`, the same rule; the seed records carry no n_null or cos_t_reg, so the n_null rule starts at the second point; table `leapk95_points.txt`, stop file `leapk95_STOP.txt`) and the alert-only samplers (`leapk95/`) through `launch_kc95_extras.ps1`, then:

```
ell_leap.py l1kc95Lw1025k 1 95 D:/choptuik-i935-raw/I1025-win2/kc95_leap/inputs/sol_l1kc95winbg_D21.0000.npy 21.0 D:/choptuik-i935-raw/I1025-win2/kc95_leap/inputs/sol_l1kc95dh170f_D21.1250.npy 21.125 21.75 0.0625 --tol 1e-12 --fmax 1e-8 --cmax 1e-2 --fold
```

in `D:/choptuik-i1025k79/solver/matter`, 4 BLAS threads, BelowNormal, cap 43200 s (12 h) by the exact root pid with the `ell_leap.py` command-line check; files `leapk95.log`, `exits_leapk95.txt`, `summary_leapk95.txt`, `leapk95.finished`, `allk95.done`; the record file `data/l1kc95Lw1025k.jsonl` and states `sol_l1kc95Lw1025k_D*.npy` are copied into `states/` by a copier. The seed pair is 0.125 apart and h is 0.0625, so the first predictor extrapolates over half the seed difference; the leap halves h to 0.03125 if a step fails. A k_c 95 point should cost more than the k_c 79 one (4500 s at 4 threads; dh170's k_c 95 regrid took 5520 s on 8 threads, winb's 8985 s on 4): the 12 h cap may end the leap before D 21.75; a restart follows only on an order.

Each point is reported with the usual row: Delta, dDelta/dD, the tracked weak mode and its ratio, the mode with the largest tangent cos and that cos, the third regular value (the mode the coordinator follows) with its fall run and distance to the cutoff, the fold signature ((i), (ii)), |J+dF/dn|, h, constraint, |F|, steps, n_null, the cutoff and the seconds; beside the k_c 79 value at the same D where there is one.

## Result

Not yet run.
