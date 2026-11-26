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
