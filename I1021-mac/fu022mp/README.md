# I1021-mac/fu022mp: the driver of #1076, fu021's guard-blocked points valued with the M = 3 inner solve in mpmath

Written on the Mac by the coordinator (hc t5), 2026-11-23, before the run. Issues:
https://github.com/nmoinvaz/choptuik-large-d/issues/1076 and https://github.com/nmoinvaz/choptuik-large-d/issues/1021.

## Why

fu021 (`../../I1021-rpi5/fu021`, 425ba356) leaves 17 unresolved leaves; 16 are blocked by the 10 sigma guard alone,
named by 7 points. At 5 of them sigma is the float64 rounding floor sig0 = 1e-15 |Y(xi1)| scale, which no integration
tolerance lowers. `value_mp.py` values a point with `inner_mp.py`, the same model in mpmath (34 and 42 digits).

## Code

choptuik-large-d branch `feat/inner-mp` at the commit in `CODE_COMMIT` (from `wip/argcount-m3-bounds` 6da7da7b, so
argcount.py is the record's): `solver/inner_stokes/inner_mp.py` and `value_mp.py`.

## Checks run on the Mac before the run (`mac_checks/`, the project venv: python 3.14, mpmath; nice 19)

| check | result |
|---|---|
| 1: at the 3 best-valued float64 points of fu021's cache, the mp R_1 within the float64 sigma, v within 1e-9 | PASS: dR 1.8e-6, 6.8e-7, 3.1e-6 against sigma 3.9e-6, 5.2e-6, 7.9e-6; dv about 2e-16; sigma_mp 1.7e-24, 2.6e-25, 1.5e-24 |
| 1, control `--mutate=conv` (drops [C S] from D's equation) | FAIL, exit 1, as it must (dR 5.7e10) |
| 2: R_1 at (34 digits, order 40, margin 12) against (42, 50, 14) within 1e-25 relative | PASS: 7.27e-28 |
| 2, control `--mutate=series` (8 terms of the start series) | FAIL, exit 1, as it must: 1.33e-6 relative (`check2_series8.log`). The earlier half-terms control was vacuous (it changes the start state by 3e-34, `check1_series.log`, `check2_series.log`) and is not counted |

## Command

From the raw clone's root, with a worktree of choptuik-large-d at `CODE_COMMIT` and a python with numpy, scipy and
mpmath:

    bash I1021-mac/fu022mp/run_fu022mp.sh <worktree> <python> "$PWD" <procs>

It refuses unless CODE is at CODE_COMMIT and clean, the output folder `I1021-<host>/fu022mp` does not exist, and
fu021's three inputs match `SHA256SUMS_fu021`. Preflight: `value_mp.py check1 --n=1` (exit 0) and with
`--mutate=conv` (exit 1). Then at most 2 passes: `select_points.py` (fu021's, unchanged) on the unresolved leaves,
`value_mp.py batch` on them (each row in `rows_passN.jsonl`, the valued ones appended to the cache, where argcount
reads the last record of a point), and the recount of the record's 11 cells with the record's arguments. A pass with no
new point, with no point valued, or a count with 0 unresolved leaves ends it. Last, `prefix_keys.py` fu021 -> fu022mp.

## Criteria (fixed before the run)

1. The preflight exits `0 1`.
2. A row is valued only when |R_1| >= 10 sigma_mp and max|Y| <= 100, sigma_mp = |R_1(34) - R_1(42)| + |J_1 J_3^-1| |r_3|
   (floor 1e-28 |R_1|); the recount applies argcount's own tests to the cache, unchanged.
3. `prefix_keys.py` fu021 -> fu022mp exits 0: fu021's cache is a prefix, and every later record of an old key is a
   valued `fu: "mp"` row.
4. The counts are on hold until xfchecks' sheet check of the new points passes (as fu021's criterion 5).
5. Accepted when the recount leaves 0 unresolved leaves, or each is named with its blocking point and cause
   (`../final/leftovers/leftovers.py` on fu022mp's cache and last leaves). The point whose continuation lost S_3's
   zero has no float64 F_3 to start from, so value_mp skips it (`skipped` row); it stays named by its cause.

## Cost

A point is two Newton solves (34 and 42 digits) of a few mp residuals each, 30 to 40 s per residual on the Mac: about
9 to 15 min a point. The recount's time depends on how far the 11 cells refine (fu021's pass 2 recount took 2.6 h on
rpi5's 4 workers).
