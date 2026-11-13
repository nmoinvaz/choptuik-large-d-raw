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
