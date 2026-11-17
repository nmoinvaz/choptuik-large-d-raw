# I942-dh370: is hpkernel's pinned quad-double solve deterministic, arm (a) stopped at 15 runs

Machine dh370 (Fedora 45, i7-8700, 12 threads). Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/942

Code: worktree `~/Source/choptuik-large-d-935` at main 043834d9, its `.venv` (multidouble 4.8.2, multishoot 3.2.0, avx2). Each run is
`cd hp && python -u qd_window.py <run>.jsonl T84-mac/pin5_D71.0000.npz --mode pinned --threads 2 --states <dir>`, from `run942.sh a`
(unit `i942a`, nice 10, idle machine, started 14:01:24 UTC on 2026-11-17). `count942.py` counts the distinct results of an arm
(`python count942.py <this folder> a`); `qd_window_perturb.py` is the control's wrapper (qd_window.py unchanged); the control, arms (b)
and (c) were not run.

I stopped the unit at 14:10:26 UTC (`systemctl --user stop i942a`), on the coordinator's order after xfkappa found the cause of the Mac's
odd run: the Mac's site2 `hpkernel/__init__.py` was deleted at 07:02:31 UTC and later runs loaded an older kernel, so the odd run was a
kernel swap, not nondeterminism. `a/r16` was killed mid-run and has no result (its log says so).

## Results

| | runs | converged | steps | distinct (Delta parts, final \|F\|) | distinct saved-state bits |
|---|---|---|---|---|---|
| arm (a), `a/r01`..`r15`, idle | 15 | 15 | 3 | 1 | 1 |

All 15: Delta = 1.7849845180052943 + 9.389859e-17 - 5.816e-33 + 8.0e-50, final |F| 2.099e-53, 36 s and 112 MB per run. Its |F| and
third part equal the Mac's odd run's printed ones (2.10e-53, -5.816e-33), not the Mac's common result (1.43e-53, 3.600e-33); the Mac's
parts are printed to 7 digits, so a difference below about 1e-23 is not resolved here, and the builds differ (multidouble 4.8.2 here).
