# I1054-dh610: PR #1054's exact 1/k (`--exact_recip`, #1043): the flag off against the main build, and the re-solves at D 73, 241.96 and 251.88, on dh610

Machine dh610 (Fedora 45, i7-12700, 20 threads, 62 GB). Pull request https://github.com/nmoinvaz/choptuik-large-d/pull/1054 (branch `feat/exact-recip-1043`, head 5f488e2b when this was written, based on main 6f401e0b),
the coordinator's order of 20 Nov 2026 (about 11:40 UTC), queued after #1052's A/B (unit `i1052`): the runner commands of `notes/EXACT_RECIP.md` section 3, in order.

Builds: the new one is a worktree `~/Source/choptuik-large-d-1054` at the PR head with a new venv `~/Source/venv-i1054` and `hp/build.sh` (`PIP_NO_CACHE_DIR=1 python -m pip uninstall -y multidouble` first, as the note says); the
comparison build ("main") is `~/Source/venv-i1050`, the #1050 build at 1c02b15b. Between 1c02b15b and main 6f401e0b (the PR's merge base) `hp/src`, `hp/python`, `hp/Cargo.toml`, `hp/Cargo.lock`, `hp/pyproject.toml` and `hp/build.sh` are
identical (checked: empty `git diff --stat`), so venv-i1050 is main's build for this comparison. The PR changes `hp/src/{model,python,series_split,split_tests,qd_residual,lib}.rs`, `hp/modecount_cx/src/lib.rs`, `hp/python/hpkernel/driver.py`,
`hp/anm_run.py`, `hp/arclength.py`, `hp/reseed.py` and adds `hp/exact_recip_check.py`, `hp/src/recip_tests.rs` and the note.

Steps (cheapest first within the coordinator's order; each under timeout, 3 times its estimate, on its exact pid; nice 10):
0. venv and worktree; 1. `hp/build.sh` (est. 31 min, 24 GB; cap 93 min);
(1) bit identity with the flag off: `highm_check.py` ref, scaled, jets and `jets --mutate=kappa` (the #1034 step 5 commands) on the new build, compared row by row with `../I1050-dh610/step5_*.log` (the venv-i1050 build; `compare1050.py` copy, with its control);
and `exact_recip_check.py bits $RAW/I461-win2/crawlJ/anm_pin3_D242.3642.npz --threads 10`: `--save=$OUT/bits242_main.json` with venv-i1050's python, then `--compare` with venv-i1054 (expect 0 of 6 differ), and `--compare ... --mutate=on` (control, exit 1) (est. 5 min each);
(2) the re-solves, `anm_run.py` with `--steps 0 --save_base 1 --exact_recip 0` and `1`: D 73 (`T81/conv_pin5_D73.0000_D73.000000.npz`, est. 5-15 min a run), D 241.96 (`I603-win2/chain/anm_pin3_D241.9602.npz`, 5-20 min), D 251.88
(`I966-dh370/ks_chain3b/leg06_D251.2845_ks293/anm_pin3_D251.8782.npz`, 1-3 h); (3) `exact_recip_check.py delta` on each pair. Pass criterion of the D 73 control, fixed before the runs (#1043): |Delta(exact) - Delta(recip_int)| < 1e-25.
The Mac's D 73 pair gave +1.74e-25 (a miss) and its D 241.96 pair about +3.3e-13 (note section 3.3); a polish that is not adopted is reported, not rerun with `--base_adopt 1`.

Inputs not in the live raw clone (`I603-win2/.../anm_pin3_D241.9602.npz`, `I966-dh370/.../anm_pin3_D251.8782.npz`) were taken from origin/main by `git archive`. `exits_1054.txt` and `summary_1054.txt` hold the exits and walls.

## Files

| file | what |
|---|---|
| `common1054.sh`, `run1054.sh`, `compare1050.py` | paths, the driver, the row-by-row comparator (a copy of I1050-dh610's) |
| `resolve73_r{0,1}/`, `resolve241_r{0,1}/`, `resolve251_r{0,1}/` (+ `.log`) | the re-solves with `--exact_recip 0` and `1`; each folder holds the saved `base_pin<k>_D<D>.npz` |
| `delta73.json`, `delta241.json` (`delta*_early.log`) | `exact_recip_check.py delta` on the D 73 and D 241.96 pairs, run by hand at 15:05 UTC while the D 251.88 pair ran (the driver reruns them after that pair, same inputs); D 73: Delta(on) - Delta(off) = +1.743109e-25 (a miss against 1e-25), D 241.96: +3.290002e-13 |
| `delta251.log` | `exact_recip_check.py delta` at D 251.88 failed (exit 1, FileNotFoundError): the flag-on polish saved no base, see below |
| `delta73.log`, `delta241.log`, `delta*.json` | the driver's own runs of the deltas, after the D 251.88 pair; the same values as the by-hand runs (`*_early.log`) |

## Results (16:20 UTC, 20 Nov)

| D | flag off (`--exact_recip 0`) | flag on (`1`) | Delta(on) - Delta(off) |
|---|---|---|---|
| 73.0 (T81) | exit 0, 121 s, 3 Newton steps, max\|F\| 2.6e-34 to 2.3e-83 | exit 0, 125 s, 4.4e-30 to 2.0e-73 | +1.743109e-25, a miss against the 1e-25 bound |
| 241.96 (I603) | exit 0, 70 s, converged at once (2.0e-65) | exit 0, 2948 s, stalled at max\|F\| 6.8e-51 after 12 steps, base saved | +3.290002e-13 |
| 251.88 (I966-dh370 leg 6) | exit 0, 3857 s, 7 steps, 4.55e-35 to 7.2e-82, base saved | exit 0, 320 s: "the start's projection failed, attempt stopped", no step, no base | none |

D 251.88, flag on: the log says `elim projections {'u0': 0, 'u0q': 0, 'ladder': 0, 'failed': 1, 'skipped': 0}: the start's projection failed, attempt stopped`. From `hp/octo_corrector.py` (`ElimO.project`) that error is raised only when the start's
pinned quad-double max|F| is above `--elim_switch` (1e-15) and above `start_F` (1e-6), so with the flag on the stored state's residual is above 1e-6 (flag off: 4.55e-35, its start was skipped by the switch). The log does not print that value (a reading of the code, not tested).
There is no "base polish not adopted" line and no "base polish saved" line: in `anm_run.py` the stopped attempt leaves no `od_F` and no `z8`, so the adoption branch saves nothing and prints nothing. Reported, not rerun, not changed.
