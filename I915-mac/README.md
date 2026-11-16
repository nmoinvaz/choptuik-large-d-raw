# I915-mac: the sigma-model kernel at M = 24 and 48, at eta = 0.3, D 10.5 and at eta = 1, D 10.475

Machine: mac (Apple M5 Mac). Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/915. Code: main 8e5b034f
(worktree branch `wip/sa-915`), `matter/sigma_ms/run_eta.py --solver band`. The kernel module is the build of #652
(`I652-mac/README.md`), run with python 3.14 and `PYTHONPATH` at that build's site directory, one process with 2 threads
at nice 10. `run_i915.sh` ran the four points in turn, each behind `gate.sh` (the 1-minute load at each start is in
`out/gate.log`: 22.3 to 28.7, all below 31). Each run starts from #913's M = 32 state (`I913-mac/out/`,
`sm_hi_D10.5_polish_M32.npz` and `sm_ctrlB_D10.475_polish_M32.npz`), resampled in tau by `run_eta.py --from`, and a
converged run is followed by a run from its state with `--tol 1e-30`. Local paths are removed from the copies here.

## Result

| point | M | unknowns | max \|F\| at the resampled state | Newton steps | max \|F\| | Delta | minus Delta(32) |
|---|---|---|---|---|---|---|---|
| eta 0.3, D 10.5 | 24 | 2641 | 4.5e-12 | 2 | 1.54e-31 | 1.142980986472450205538266 | +1.03e-21 |
| | 32 (#913) | 3521 | | | 1.05e-31 | 1.142980986472450205537241 | |
| | 48 | 5281 | 2.2e-15 | 1, then 2 more | 1.42e-31 | 1.142980986472450205537212 | -2.9e-23 |
| eta 1, D 10.475 | 24 | 2641 | 2.9e-11 | 2 | 1.29e-31 | 1.020104800025154886837944 | -2.06e-19 |
| | 32 (#652's chain) | 3521 | | | 1.4e-31 | 1.020104800025154887044163 | |
| | 48 | 5281 | 1.7e-14 | 1, then 1 more | 1.41e-31 | 1.020104800025154887044211 | +4.8e-23 |

Delta(32) at eta 0.3 is #913's `hi` state. Against its other two M = 32 states, Delta(48) differs by -3.8e-23 (`up`)
and -1.4e-23 (`march`), and Delta(24) by +1.02e-21 and +1.04e-21. The three M = 32 states themselves spread over
2.3e-23, so Delta(48) - Delta(32) is at the level to which the band lets a converged double-double state fix Delta.
At eta 1, Delta(48) is 2.1e-23 from #913's control state.

Every step was Newton's own: the resampled states are within 3e-13 to 5e-11 of the solutions, so the band solver's
short-step path ran and no SVD was taken.

The resolution here is M, the number of tau points. The x direction was the same in every run: the 21 nodes, the
Taylor steps planned to 1e-32, and the series orders 36, 80, 80.

## Why M = 24 already gives 1e-21

The centre datum's harmonics at eta 0.3, M = 48 (odd k): 0.79 at k = 1, 6.1e-4 at 7, 1.1e-6 at 13, 2.5e-9 at 19,
6.1e-12 at 25, 1.5e-14 at 31, then 5e-16 and 4e-15 at 37 and 43, the level at which the band leaves q free. So q
loses a factor of about 400 per six harmonics, and the harmonics that M = 24 drops are of order 1e-11. They are the
band, whose singular values are 1e-10 and below, and their product is the 1e-21 seen.
