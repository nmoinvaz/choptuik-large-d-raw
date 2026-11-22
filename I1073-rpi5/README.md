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
