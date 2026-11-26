# I1098-mm5/m48_2000fix: D 2000 at M 48, harmonics 13-25, exact 1/k (#1098)

Machine: macmini-m5-pro (Apple M5 Pro, 18 cores, 48 GB, macOS 27.2.1), runner `choptuik-mm5-i1088-me2`.
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1098

The D 2000 M 48 test of `../m48_2000/` again on fastmul5 (f350aa62, lane-precision reciprocals, `HP_EXACT_RECIP=1`), ordered by coordinator t5; 9 threads (the other 9 are for the jump agent's D 300 horizon checks).
`../m48_2000/` ran on fastmul4, i.e. the double-double 1/k system, and was stopped after h17 (its README has the table).

## The bar (relayed by the coordinator; recorded here 2026-11-26 13:40 UTC, before the run)

The h13 step's shift M 32 -> 48, then h15-h25 at M 48 falling or not. The old-kernel run (the dd-1/k system) gave h13 **+6.82191e-24**, h15 **-1.86895e-17**, h17 **-6.5853e-19** (D 1000's M 48 numbers:
h17 shift +1.38661e-19, h19 +1.2092e-19, h21 -3.4847e-21, h23 -1.5134e-21). Reported: each harmonic's change as it releases, beside the old-kernel ones. Stop rules: an exception, or an outer step 3x the first one's time;
an inner solve that stalls as at M 64 is reported at its second failed trial.

## Inputs and code

- `input/release_ls_h13_D2000.0000.npz`: git blob b26c20a9b984b19177ab91dc5b8a4a22cd8ce33f (verified) from `I1088-dh610/rls2000d/`: D 2000, M 32, ks 2618, kc 250, kfreeze 13, Moebius horizon (hmob 8);
  Delta 1.649074313745289325643275661277062778332.
- `tools/resample_m.py`: blob 4de5c3174ad1bad3a5a311f909db9d3ecec64b5b from `I1098-mac-a/` (hp/ on PYTHONPATH next to the site folder).
- Kernel and code: `~/Source/choptuik-fastmul5/hp` (f350aa62), `HP_EXACT_RECIP=1 HP_HORIZON_RELAXED=1 PYTHONPATH=~/Source/fastmul5-site`; the log's first two lines are `hpkernel.__file__` (must be under fastmul5-site) and the HP_EXACT_RECIP value.
- Steps, nice 10, detached, `timeout 6h` on the release, 9 threads, OPENBLAS_NUM_THREADS=1:

      PYTHONPATH=~/Source/fastmul5-site:~/Source/choptuik-fastmul5/hp python tools/resample_m.py input/release_ls_h13_D2000.0000.npz h13_M48.npz 48
      python -u form_s.py release_ls h13_M48.npz <this folder> --harm 13,15,17,19,21,23,25 --kmax 31 \
        --jac_by 13:qq,15:qq,17:qq,19:qq,21:qq,23:qq,25:qq --res od --tol 1e-48 --tol_h 1e-44 --threads 9 --outer 6 --commit f350aa62 > rls.log

Delta's change per harmonic is computed by `diff_delta.py` on the log's digits (mpmath), never by hand.

## M32_base (queued 2026-11-26 13:51 UTC, after `../horizon300/` ends; coordinator's order (b))

To separate D 2000's dd-1/k error from this run's M shift: the M 32 base state itself re-solved on fastmul5, same input (`input/release_ls_h13_D2000.0000.npz`, blob b26c20a9), into `M32_base/`:
`HP_EXACT_RECIP=1 HP_HORIZON_RELAXED=1 PYTHONPATH=~/Source/fastmul5-site OPENBLAS_NUM_THREADS=1 nice -n 10 timeout 3h python -u form_s.py release_ls input/release_ls_h13_D2000.0000.npz M32_base --harm 13 --kmax 13 --jac_by 13:qq --res od --tol 1e-48 --tol_h 1e-44 --threads 9 --outer 8 --commit f350aa62`.
**Bar:** its "h13's change" is D 2000's dd-1/k error at M 32. The true M 32 -> 48 shift is this run's h13 change minus it. Expect 30-80 min. Stop rules: an exception, the floor stop, or an outer step 3x the first one's time.

## Stopped (2026-11-26 14:26:57 UTC) on fastmul5, with h13 released and h15 outer 0 done; M32_base dropped

Stopped by hand, with SIGTERM to the `timeout` pid 31213 (python 31214; `queue.txt`: release_ls exit=143), on the coordinator's order. Reason (the jump agent's finding): the dd-stored d/dtheta matrices move Delta by about
-1.2e-24 at D 1000 (-2.2e-32 at D 300), growing roughly as D^15, so at D 2000 the term is likely near 1e-20, and D 2000 measurements on fastmul5 would mostly measure that term. A fastmul6 build
(a remainder per matrix entry) comes next. The queued **M32_base** run (`m32base_queue.txt`: queue script pid 31638, waiting for horizon300's driver) was dropped by SIGTERM to its pid at 14:26:5x UTC and never started
(no `M32_base/` folder). What this run measured (fastmul5, exact 1/k, M 48, harmonics from the M 32 h13 state of blob b26c20a9; script from the log digits):

| harmonic | outer steps | change in Delta | old kernel (m48_2000, dd 1/k) |
|---|---|---|---|
| h13 (shift M 32 -> 48) | outer 0 -8.9203e-24 (866.0 s), outer 1 -8.0288e-22 (748.1 s), outer 2 released (224 s) | **-8.11798e-22** | +6.82191e-24 |
| h15 (outer 0 only) | outer 0 -1.6398e-17 (905.8 s: target |F| 2.17e-44 -> 5.00e-53, harmonic-15 step 1.51e-10); outer 1 started 14:26:32, not finished | -1.63984e-17 so far (not released) | -1.86895e-17 (released) |

Last lines of `rls.log`:

    h15 outer 0: target |F| 2.17e-44 -> 5.00e-53, harmonic-15 step 1.51e-10 (full step's dDelta -1.64e-17), lam 1, Delta 1.649074313745289309244922315146592930935 (905.8 s)
    h15 outer 1 (qq Jacobian) starts 14:26:32 UTC, predicted end 14:41 UTC (906 s, the last qq outer step)

The h13 value (-8.118e-22) is therefore mostly the dd-stored d/dtheta matrices' term plus the M shift, not separated; no h17-h25 values exist for this kernel at D 2000.
