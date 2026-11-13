# I597-mac: modecount_cx on hp's engine, its checks against the old crate, and the smoothness test old against new

Machine: the Mac (Apple M5, macOS 27, 32 GB), Python 3.14 of venv-314 (`/Users/nathan/venv-314`), hpkernel of main
3c35f0c built in the session scratchpad (`i599/site2`, low-memory recipe). Issue:
https://github.com/nmoinvaz/choptuik-large-d/issues/597 (a subagent of the coordinator).

Builds (both `-C target-cpu=native`, unstripped, LTO off and 16 codegen units, the low-memory recipe of AGENTS.md):
- **new**: `hp/modecount_cx` of branch `wip/i597-subagent` (commit c76bf20 and on): `CSolver.mode_matrix`, `mode_det`
  and `mode_pivots` from multishoot's `Shooting::mode_matrix` on `Ctx::shooting()` at `Rate::new(lr, li)`;
- **old**: `hp/modecount_cx` of main 3c35f0c (its own copy of the complex linearisation, frozen rows with the
  double-double projector).

`env597.sh` sets the paths (`new` and `old` run Python with the build on PYTHONPATH, nice 10). Every run is from `hp/` of
the worktree. States: #609's (I609-macm3 `states/`, sha256 in its `state_sha256.txt`: M 40 beeebb84, M 48 5bea0e2c,
M 64 92f49438, M 80 130f87eb), I252-mac's D 61 M 64 kf 23 (179d0bd6), and `hp/data/states/up6_D30.0688.npz` (95443740)
and `up7_D40.0201.npz` of the repository. The resampled states are given by path, so setup loads them as they are.

## Contents
- `run597_smooth.sh`, `smooth/`: `modecount_smooth.py --joint` on both builds (8 cases), and `--mutate=lo` (control);
  `table597.py` makes `table597.md` (old against new, with #609/#612's macm3 counts), `--same` exits 1 unless each
  case's two logs are byte for byte equal, `--mutate` is its control (must exit 1).
- `run597_check.sh`, `check/`: `modecount_check.py` (2 threads) at the no-cut state D 30 M 32 and the kfreeze state
  D 40 M 32 kf 13 on both builds, `--mutate=dmat` (control, must exit 1), and the bit check against #473's cache
  (`check/modecount_D30.0688_M64_evals_I473.jsonl`, a copy of `I473-macm3/data/modecount_D30.0688_M64_evals.jsonl`)
  at D 30 M 64 on both builds, with its control.
- `run597_kf.sh`, `mm597.py`, `kf/`: the mode matrix and det dumped on both builds at the kfreeze states D 40 M 32 kf 13
  and D 61 M 64 kf 23 and compared entry by entry (`compare_*.log`): where the frozen rows differ, and how much; the
  no-cut D 30 M 32 comparison is the control (0 entries must differ).
- `smooth_k597.py`, `smooth_k/`: modecount_smooth.py's statistic at steps of k ulps.
- `exits.txt`: every run's exit code and time (UTC).

The matrix dumps of `mm597.py dump` (38 to 151 MB each, 0.8 GB in all) are not in this folder. They are remade by
`run597_kf.sh`, and the comparisons of them are logged in `kf/`.

## Results (2026-11-13)
- **Smoothness** (`table597.md`): in all eight cases the old and new logs are byte for byte equal, and each count equals
  #609's or #612's macm3 count: D 30 λ_phys M 32 1, M 40 830, M 48 3921, M 64 57, M 80 20,539; D 61 M 64 kf 23 s3
  55,821; D 30 position 1 M 64 4979, M 80 46,073. The M 32 control log is byte for byte macm3's #612 log.
  `--mutate=lo` fires: 11,520 of 17,054 changed entries non-linear.
- **modecount_check.py**: no cut (D 30 M 32), both builds pass; check 2 finds 0 of 589,824 entries differing from
  hpkernel's in a bit, and its control (one ulp above 1.7) finds 81,920. Kfreeze (D 40 M 32 kf 13): the new build
  passes (0); the old build fails check 2 with 1,854 entries, at most 2.0e-26 against max abs(M) 1.1e6, which is the
  projector's difference. `--mutate=dmat` at M 32: check 2 fails (81,920 entries), exit 1.
- **Bit check against #473's cache** (D 30 M 64, 8 cached λ, 7 complex): the new build equals all four floats at all 8;
  the control (Re λ one ulp up) changes 2 of 4. The old build's run was stopped by hand (exit 143) at machine load 60
  to 90 from other sessions, as old = new is shown bit for bit elsewhere.
- **Frozen rows, old against new** (`kf/compare_*.log`): at D 40 kf 13 and D 61 M 64 kf 23 every differing entry is in
  the horizon block's p rows, at most 1.9e-32 and 3.2e-32 of max abs(M). The det is bit for bit at 3 of 4 λ at D 40, and
  moves by 2.0e-7 in ln abs(det) and 1.2e-6 rad in arg at D 61 s3. No cut: 0 entries differ.
- **Fat LTO against the low-memory recipe** (`hp/modecount_build.sh`, `kf/compare_fat_*.log`): 0 entries differ, dets
  bit for bit, at D 30 M 32 and D 40 kf 13.
- **modecount_test_check.py** (the test field, `test_field.rs`): both builds PASS with the same log.
- **k-ulp smoothness** (`smooth_k/`): the non-linear share falls with the step (D 30 M 80: 3.34% at 1 ulp, 0.011% at
  4096), and the median abs(d_2k − 2 d_k)/abs(d_k) falls as 1/k. So the entries carry an error of fixed size, the
  double-double evaluation's noise floor.
