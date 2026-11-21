# I1025-win/p4_highD: hybrid roots at D 17.5 and 17.75 on winb's own k_c 63 states (winb)

Written before either row runs (2026-11-21 03:38 UTC). Row 4 of P4 (`I1025-win/p4`, D 16.25 k_c 63) still runs; these rows start after it.

## Order

The coordinator (hc, 2026-11-21 about 03:32 UTC), after P4's three clean passes: hybrid roots past D 17 on winb's own k_c 63 states, one row at a time, by `p4_hybrid.py` with the P4 rules (system check against the record, one sign change, the edge rule, noise robust, signtest at lambda -/+ 0.02). Row A: D 17.5, `out/sol_l1kc63Fw1025_D17.5000.npy`, record in `out/l1kc63Fw1025.jsonl`. Row B: D 17.75, `out/sol_l1kc63W1025_D17.750000.npy`, record = its line in `leap_kc63.log`. Each guess and window is written here before its run, taken from the signtested k_c 63 rows' trend (2.0265465 at D 17). xfkappa takes D 18 and 18.5 on the Mac, so those are not run here. A post on #1025 after each row, with cpu and memory.

## Inputs (raw origin/main, taken by `git show`, checked with `git hash-object --no-filters`; `prep_p4hi_inputs_1025.log`)

| item | raw path | blob |
|---|---|---|
| p4_hybrid.py | `I1025-mac/p4_hybrid.py` | a402559b5d37661b49da50f07f877af21fd29b3a (the P4 rows' script) |
| signtest.py | `I1025-mac/signtest.py` | 179ea09681b0a75f7cefdff98984b48051b3f085 (with `around=` and the system check) |
| row A record | `I1025-win/out/l1kc63Fw1025.jsonl` | 7ee33d79eb195a4cbf19c71db799cb93ea92c8d5 |
| row A state | `I1025-win/out/sol_l1kc63Fw1025_D17.5000.npy` | d85f7b71c2c1750ca91d941320b9f2cdf57fe029 |
| row B line | `I1025-win/leap_kc63.log`, line 53 (equal to the D 17.75 line of `I1025-win/out/l1kc63W1025.jsonl`, blob c33039df) | 94ef7a72ed7ac963b42bb01e6b4fbd718c2f70fe |
| row B state | `I1025-win/out/sol_l1kc63W1025_D17.750000.npy` | de9fc3e55aa46bafd4ef62536861f94aed9e3035 |

Code worktree `C:/Users/nathan/Source/choptuik-i1025-lowd` at 505d839940456a3d04321d75cf66cc3b5bc831c4 (the P4 rows'), PY `C:/Users/nathan/Source/venv-md510` (Python 3.14.10, numpy 2.5.4, scipy 1.18.1, mpmath 1.3.0, multidouble 5.1.0 at 8c4360ac).

## The two rows, their records and the stubs

| row | D | k_c | record system (what the check compares) | float64 record lambda |
|---|---|---|---|---|
| A | 17.5 | 63 | F 2.2919997574734327e-10, 2649 steps, u0 0.04, Ks 30, kappa 0.7, rk 1 | 1.974481053107075 (n_eval 28): SUSPECT, its signtest failed (raw `I1025-win` 67a15ffb, comment 7033113186), not used |
| B | 17.75 | 63 | F 2.4283364241408305e-10, 2598 steps, u0 0.04, Ks 30, kappa 0.7 (a leap state: `leap_kc63.log` line 53) | none (the leap does not solve for lambda) |

`p4_hybrid.py` reads the guess from the record line's `lam_guess` and needs a `lam` in it. So each row runs on a stub record, made by `make_stubs_p4hi_1025.py` (`make_stubs_p4hi_1025.log`):

- Stub A, `stub_rowA_l1kc63Fw1025_D17.5_trendguess.jsonl`: the D 17.5 line of `l1kc63Fw1025.jsonl` unchanged, except `lam_guess` set to the trend guess below. The record's own `lam_guess` is D 17's lambda, 2.0265465 (kept as `lam_guess_record`). Its `lam` stays the float64 record, so the output's `minus_record` is the hybrid minus that suspect value.
- Stub B, `stub_rowB_l1kc63W1025_D17.75_leapline.jsonl`: `leap_kc63.log`'s D 17.75 line unchanged, plus `lam_guess` and a `lam` equal to the guess. The `lam` is a placeholder: the output's `lam_record` and `minus_record` for row B are the guess and the root minus the guess, not a record.

## Guess and window, fixed here before the runs

The guess is the quadratic through the three signtested k_c 63 rows at equal spacing, D 16.5 (2.1454677042524617, winb, signtest passed), D 16.75 (2.0834870037231608, win2b's signtest passed, winb's record) and D 17 (2.026546497375959, signtest passed), evaluated at the row's D and rounded to 4 decimals.

| row | D | trend value | guess |
|---|---|---|---|
| A | 17.5 | 1.9277860672 | **1.9278** |
| B | 17.75 | 1.8859661434 | **1.8860** |

The search is `ell_refine.lam_root`'s, unchanged in `p4_hybrid.py`: det sign at guess * (1 + w * (-1, 0, 1)) for w = 0.02, 0.06, 0.15, 0.35 in turn, stopping at the first w with a sign change, then `brentq` inside that interval (xtol 2e-8 * guess, rtol 1e-12). Windows:

| row | w 0.02 | w 0.06 | w 0.15 | w 0.35 |
|---|---|---|---|---|
| A, guess 1.9278 | [1.88924, 1.96636] | [1.81213, 2.04347] | [1.63863, 2.21697] | [1.25307, 2.60253] |
| B, guess 1.8860 | [1.84828, 1.92372] | [1.77284, 1.99916] | [1.60310, 2.16890] | [1.22590, 2.54610] |

Other readings of the trend, for scale: linear from the last two rows 1.9127 (A) and 1.8557 (B); linear least squares over the four signtested rows D 16.25 to 17 1.9129 and 1.8558; quadratic least squares over those four 1.8965 and 1.8274; the Mac's k_c 55 value at D 17.5, 1.9522. All of A's lie inside its w 0.02 window; B's lie inside its w 0.02 window except the quadratic least squares 1.8274, which lies in w 0.06. The float64 record 1.9745 of row A lies outside the w 0.02 window and inside w 0.06. The alternative, the record's own guess 2.0265465 for row A, would start at w 0.06 ([1.9049, 2.1481]) with a bracket of 0.12.

## Pass rules (fixed before the runs)

A row PASSES if all hold:

1. record system true: steps equal and |F| within 1% of the record's or 1e-13 (amendment 5), rebuilt by `p4_hybrid.py` from the stub's `F` and `steps`;
2. one sign change on the search grid, and one over all evaluations in lambda order;
3. every evaluation's sign unchanged under 1e-15 relative noise on blocks 0 to 11 (2 seeds);
4. final bracket at most 1e-7;
5. edge rule (`check_1025.py`'s, 2026-11-20): the root is at least 0.05 grid steps from both edges of the grid interval that holds it (the grid and step are those of the first w with a sign change, read from the row's own evaluations; the distances are printed, so another bar can be read off);
6. signtest at the hybrid lambda -/+ 0.02 (`signtest.py STATE D 63 around=<the row's hybrid jsonl>:D:0.02`, with the record's u0 0.04, Ks 30, kappa 0.7, rk 1): both lines agree (the sign from an LU of M equals the signs from LUs of three random orthogonal rotations of M) and the two signs are opposite; its system line must read same true.

A row failing any of these is reported, not read. The verdict is computed by `verdict_p4hi_1025.py` and logged in `rows/verdict_D<D>.log`. A timeout (21600 s per row) or crash is reported, and the other row still runs.

## Smoke test of the system check (2026-11-21 03:36 UTC, `signtest.py ... syscheck`, 13 s each, `smoke_syscheck_A.log`, `smoke_syscheck_B.log`)

| row | F rebuilt | F in the stub | steps rebuilt | steps in the stub | same |
|---|---|---|---|---|---|
| A | 2.2919997574734327e-10 | 2.2919997574734327e-10 | 2649 | 2649 | true |
| B | 2.4280912473748936e-10 | 2.4283364241408305e-10 (1.0e-4 relative) | 2598 | 2598 | true |

## Run

`p4hi_driver_1025.sh` (a thin driver, no solver code) waits for `p4_driver_w.sh done` in P4's `p4_w.log`, then runs row A and row B one at a time: `p4_hybrid.py` on the stub, then the signtest, then the verdict. Launcher `start_p4hi_1025.cmd` (BelowNormal, 4 BLAS and rayon threads, no `nice`, so no Idle priority). Output: `p4hi_w.log`, `ell_p4_hybrid_1025_w_highD.jsonl`, `rows/D<D>.log`, `rows/signtest_D<D>.log`, `rows/verdict_D<D>.log`.

Timing, estimated from P4's k_c 63 rows (678 to 913 s per evaluation at 4 threads; 12 to 16 evaluations): about 2.3 to 3.5 h per row, plus minutes for the signtest. No RESUME: if the laptop stops, the coordinator decides.

## Status

Not started. The Result section is written at the last push.
