# I686-dh370: is the chain's singularity the discretization's or the solution's? The 24-order series with a plan made at the state (the dh370 run of #686)

Machine: dh370, Fedora Linux 45 Workstation, Intel Core i7-8700 (6 cores, 12 threads, AVX2 and FMA), 31 GB. Run at `nice -n 10`, 12 threads, `OPENBLAS_NUM_THREADS=1`, no memory guard.
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/686 (recommended by #634, after #685).
Code: choptuik-large-d main at aedb403b, worktree `choptuik-large-d-685` (as for #685), run in the venv of `choptuik-large-d-614` (the 3c35f0c build).
Inputs: #603's states `I603-win2/chain/anm_pin3_D252.2497.npz` and `anm_pin3_D252.6135.npz`, and the kept-plan series of the same bases from I685-dh370/repro/ (raw commit abed955c), which equal #603's records bit for bit (I685-dh370/repro_check685.log).

Command (the series of #685 with the plan made again at the state): `anm_run.py $RAW $R/newplan --state S --N 24 --tol_od 1e-60 <#603's flags> --keep_plan 0 --save_jet 2`, `--threads 12`.

## The decision rule, written before the new-plan series were read

Singularities are compared by track (D* = D0 + s, as grouped in I685-dh370/table685.txt: every stable Pade pole of Delta and every row's nearest stable pole, within 0.4 of the track's median).
For a base and a track present in the kept-plan series, spread = the largest |D* - the track's median D*| over its poles (Delta's Pade poles and the rows) in either series, and d = |median D* of the new-plan series - median D* of the kept-plan series|.
d <= spread: the singularity is the solution's. d > 3 spread: the discretization's. Otherwise undecided. A track absent from the new-plan series is reported as absent (it moved or left the range).
"Another M or layout": the octo-double kernel is M = 32 only, and no converged state exists on another layout at this D (#654's polish at 0.975 did not converge), so it is reported as not available unless one is found.

Clarification, added before the new-plan series were read: a track with fewer than 3 poles in the kept-plan series has no usable spread, so it is reported with d and called undecided. The comparison is made at each of the two bases separately.

## Result

The nearest singularity is the solution's: with the plan made again at the state, its D* equals the kept plan's to 1e-4 at both bases, inside the track's spread (0.010 and 0.094).

| base D0 | track D* (kept plan) | rows with this pole, kept / new | spread | d | verdict by the rule above |
|---|---|---|---|---|---|
| 252.2497 | 252.31 + 5.81i (nearest) | 25 / 25 | 0.010 | 1.0e-4 | the solution's |
| 252.2497 | 255.77 + 5.02i | 1 / 1 | none | 5e-4 | undecided (fewer than 3 poles) |
| 252.2497 | 259.87 + 3.46i | 1 / 1 | none | 1.9e-2 | undecided (fewer than 3 poles) |
| 252.6135 | 252.30 + 5.80i (nearest) | 25 / 25 | 0.094 | 1.0e-4 | the solution's |
| 252.6135 | 255.74 + 5.01i | 1 / 1 | none | 3e-4 | undecided (fewer than 3 poles) |
| 252.6135 | 259.97 + 3.25i | 1 / 1 | none | 6.3e-3 | undecided (fewer than 3 poles) |

Root test of Delta, kept against new plan: 6.5145 and 6.5066 at D 252.2497, 6.0317 and 6.0335 at D 252.6135. Rows with a stable pole: 24 of 24 in all four series.
The control `compare686.py --mutate=shift` (`compare686_mutate_shift.txt`) turns the nearest tracks into "the discretization's" (d = 0.5), and the kept series compared with itself gives d = 0 (`selftest_identity.txt`).

The coefficients of the series change much more than D* does (max|dz_k|/max|z_k|, `compare_series_D*.log`): at D 252.2497 1.8e-07 (k 1), 5.3e-04 (2), 2.4e-03 (3), 2.1e-03 (5), 4.8e-02 (7), 6.1e-02 (13), 6.1e-03 (24); at D 252.6135 3.9e-07, 1.4e-04, 9.7e-05, 7.1e-04, 2.2e-03, 5.6e-03, 4.4e-03.
`jet_singularity.py compare` control: the kept series against itself gives 0 at every order, and with `--mutate scale` 1.0e-06 at order 5 only (`compare_series_selftest_*.log`).

Caveat: with the new plan the state is a solution of the new equations only to pinned max|F| 3.3e-36 (D 252.2497) and 2.7e-36 (D 252.6135), and its base polish did not converge (to 1.5e-21 and 2.5e-20, one Newton step each, then no trial accepted), so it was not adopted and the series is the one at the stored state.
Runs: 4193 s and 4100 s (exit 0), against about 2330 s for the kept plan.
Another M or layout: not run. The octo-double kernel is M = 32 only, and no converged state exists on another layout at D 252 (I654-dh370's polish at 0.975 stopped at 3.8e-20).

## Files

| file | what |
|---|---|
| `run686.sh`, `exits_686.txt`, `newplan_D*.log`, `newplan/jet_pin3_D*.npz` | the two new-plan series (`--keep_plan 0`) |
| `stage_summary686.sh`, `summary686.log`, `jet_686.json` | `jet_singularity.py summary` on them (same staging as I685-dh370) |
| `compare686.py`, `compare686.txt`, `compare686_mutate_shift.txt`, `selftest_*.txt` | the comparison with the kept plan's (I685-dh370/jet_685.json), its control and self-test |
| `compare_series_*.log` | `jet_singularity.py compare` of the series, orders 1 to 24, and its controls |
