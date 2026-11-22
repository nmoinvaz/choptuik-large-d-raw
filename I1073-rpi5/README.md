# I1073-rpi5: Ecker et al.'s Delta and gamma below D 3.6 per Fourier resolution, beside ours (reference values for #1072)

Machine: rpi5 (aarch64, one process, nice 10). Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1073
Started: 2026-11-22 21:06 UTC. Code: main c80b0e30 (worktree `choptuik-large-d-1073`); `hp/lowD_ecker.py` is unchanged since 17ae55bf.

Their repository (data only, none of its code is run): `git clone --depth 1 https://github.com/EckerChristian/CriticalSpacetimeCrystal ~/Source/ecc`,
commit `f002d0af1680abb967e694a121cb2a8de2984b5d` (2026-04-23, "added PRL cover plot").

## Runs

1. `cd hp && nice -n 10 python3 lowD_ecker.py ~/Source/ecc --dmax=4.0 > I1073-rpi5/ecker_tables.txt`
2. `cd hp && nice -n 10 python3 lowD_ecker.py ~/Source/ecc --fields > I1073-rpi5/ecker_fields.txt`
3. `report1073.py` reads `ecker_tables.txt`, `hp/data/delta_all.csv` and the stored values of notes/LOW_D.md 5 and prints the tables of
   the issue (their Delta and gamma at every D <= 3.6 per resolution with the change between resolutions; their gamma beside ours at
   D 3.0444, 3.0475, 3.15, 3.425, 3.475, 3.5; their Delta near D 3.04375 and 3.0475 beside ours; Delta/(2 gamma) against D).

## Acceptance (written before the runs)

At D = 3.7, their Delta and gamma at the highest resolution agree with ours as LOW_D.md 5 records them within 1e-7:
ours Delta 3.4652004835 and gamma 0.3486501896 (double-double, M = 80). If either differs by more than 1e-7, the files were read wrong:
stop and report. `report1073.py --mutate=shift` moves ours by 1e-6 and must fail (exit 1).

## Found before the runs (from `ls`, reported, not fixed)

`complete_data/FortranData` has 128 (233 dirs), 256 (93) and 512 (212) mode directories and no 1024. `gam.out` exists only at 512
(126 dirs). So `lowD_ecker.py`'s 1024 column and its "1024-512" change are empty, and "highest resolution" in FortranData is 512 (not 1024).
Their 1024-mode data are in `CppData/data_lowD_1024_{1..4}.json`, which `lowD_ecker.py` does not read; they are read in a separate step below
if the structure is plain JSON of numbers.

## Result (run 2026-11-22 21:0x to 21:15 UTC; exits in exits.txt, inputs' sha256 in sha256.txt)

**Acceptance at D 3.7: PASS.** Their 512-mode value (the highest resolution in FortranData) against ours (M 80, dd; LOW_D.md 5's values,
read from `hp/data/delta_dd_lowD.csv`):

| | theirs | ours | theirs - ours | bar |
|---|---|---|---|---|
| Delta | 3.465200504469 | 3.465200483544 | +2.09e-8 | 1e-7 |
| gamma | 0.3486502642 | 0.3486501896 | +7.46e-8 | 1e-7 |

The control `report1073.py --mutate=shift` (ours + 1e-6) fails both and exits 1.

**What their data hold (differs from the issue's text; reported, nothing fixed):**

- `FortranData` has no 1024-mode directory at any D. `gam.out` exists only at 512 modes. So gamma has one resolution only, and
  `lowD_ecker.py`'s 1024 column and "1024-512" change are empty. Their 1024-mode Delta (Ntau 2048) are in `CppData/*.json`, at 58
  D from 3.046 to 3.096, with no gamma.
- Their gamma (GammaList, 512 modes) has D >= 3.1 only and a gap: nothing between 3.14 and 3.2 (no D 3.145 to 3.18 although their Delta
  there has 128/256/512). Nothing at or near D 3.0444 or 3.0475: the nearest is D 3.1 (0.2005723277).
- Their Delta (DeltaList) has D >= 3.046, so nothing at 3.04375 or 3.0444.
- 207 of the 269 entries of `critcoll_data.json` (D 3.101 to 5.5) are not C++ solves (IterNewton 0, mismatchNorm 1.0, PrecisionNewton
  0.1); their Delta equal the Fortran 512 values to 5e-13. They are not an independent check. The C++ solves are at D <= 3.1.

**Self-convergence of their Delta, D <= 3.6** (full table in report1073.txt): 128 -> 256 and 256 -> 512 alternate in sign and contract
slowly where it matters. 512 -> 1024 exists at three D only: 3.094 -9.9e-10, 3.095 +6.9e-11, 3.096 +1.1e-12.

| D | 256-128 | 512-256 | theirs(512) - ours | our error |
|---|---|---|---|---|
| 3.15 | -1.2e-4 | +1.0e-3 | -5.2e-11 | 9e-12 |
| 3.175 | -8.7e-5 | +4.6e-4 | -2.1e-10 | 3e-10 |
| 3.2 | -5.9e-5 | +2.2e-4 | +2.5e-6 | 2e-11 |
| 3.3 | -1.3e-5 | +1.8e-5 | +6.6e-8 | 2e-10 |
| 3.5 | -9.7e-7 | +4.9e-7 | +1.9e-9 | 6e-13 |
| 3.6 | -2.9e-7 | +1.1e-7 | +7.5e-9 | 2e-11 |

Their Delta agrees with ours to 3e-9 at every common D from 3.0475 to 3.175 (below 7e-10 except 3.075 at +2.9e-9; our errors up to
3.3e-10; 1024 modes below 3.097, 512 above). Between 3.175 and 3.2 the difference steps up to +2.5e-6, then falls to +1.4e-9 to 1.4e-8 at
3.35 to 3.6. Cause not known.

**Discrepancy with notes/LOW_D.md 5:** its estimate "good to about 5e-7 at 3.5, 2e-5 at 3.3 and 1e-3 at 3.15" takes their 256 -> 512
change as the error of the 512 value. Against ours the 512 value is better than that by 260x at 3.5, 300x at 3.3 and 7 orders at 3.15.

**Their gamma beside ours** (512 modes; off-grid values are interpolation spreads over the Lagrange choices that bracket D, not
bounds; in ln(D-3) the choices agree to 6e-8 at 3.425 and 3.475, where ours lies 3e-8 to 1.6e-7 outside the spread):

| D | theirs | ours | note |
|---|---|---|---|
| 3.0444 | no data (nearest D 3.1: 0.2005723) | | power-law extrapolation of their D 3.1 to 3.2 points: 0.1558 to 0.1560 (not data) |
| 3.0475 | no data | | extrapolation 0.1591 to 0.1592 (not data) |
| 3.15 | 0.2273877 to 0.2273965 (3 choices, in D and in ln(D-3); gap 3.14 to 3.2) | 0.2273872422 (M 128; M 96 -1.05e-6) | ours is 5e-7 below the lowest choice |
| 3.425 | 0.3092041 to 0.3092042 (ln(D-3)); 0.3092038 to 0.3092057 (D) | 0.3092042856 (M 128) | |
| 3.475 | 0.3182481 (ln(D-3)); 0.3182479 to 0.3182492 (D) | 0.3182480362 (M 128) | |
| 3.5 | 0.322385723 | 0.3223855828 (M 128) | +1.40e-7 |

At the common grid points theirs - ours: 3.35 +5.9e-7 (ours M 96), 3.45 -4.6e-8, 3.5 +1.4e-7, 3.6 +1.4e-7 (ours M 96), 3.7 +7.5e-8.

**Delta near D 3.04375 and 3.0475** (their DeltaList, 1024 modes; ours `hp/data/delta_all.csv`, dd): D 3.0475 theirs 2.466012147213, ours
2.466012146522, +6.9e-10 (our error 3.8e-11). D 3.04375 is 0.00225 below their lowest D (3.046): no data; a cubic extrapolation of their
first four points gives 2.436459532 against ours 2.436459113 (+4.2e-7; extrapolation, not data). Also theirs - ours at 3.05 +5.0e-10 and
3.075 +2.9e-9.

**Delta/(2 gamma) from their data** (DeltaList and GammaList): it rises monotonically as D falls. 0 of 48 adjacent grid pairs (D <= 4)
rise with D.

| D | 4.0 | 3.6 | 3.5 | 3.4 | 3.3 | 3.2 | 3.14 | 3.1 |
|---|---|---|---|---|---|---|---|---|
| Delta/(2 gamma) | 4.607 | 5.125 | 5.309 | 5.532 | 5.819 | 6.224 | 6.581 | 6.913 |

The local dln(gamma)/dln(Delta) between grid rows is 5.7 (3.6), 3.8 (3.5), 2.9 (3.4), 2.0 (3.2) and 1.86 to 1.94 (3.1 to 3.14): gamma falls
faster than Delta over their whole range. The slope falls as D falls (5.7 to 1.9) and stays above 1. Their gamma stops at D 3.1, so their data
alone say nothing about D 3.0444.

**Their fields** (`ecker_fields.txt`, three D): D 3.046 |F_1| 437.19, F_3/F_1 0.558, beta(9..31) 0.032 (antiperiodicity error 4e-2).

## Files

README.md (this), report1073.py (the tables; `--mutate=shift` control), report1073.txt (all tables, D <= 3.6 per resolution in full),
report1073_mutate_shift.txt, ecker_tables.txt and ecker_fields.txt (their outputs of `hp/lowD_ecker.py`), exits.txt, sha256.txt.
Run: `python3 -I report1073.py ECC ecker_tables.txt CODE RAW [--mutate=shift]` (CODE = main checkout, RAW = raw clone for the I1070 gamma records).
`lowD_ecker.py` needs numpy: the system python3 on the rpi5 has none, so the venv python ran it.
