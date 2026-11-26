# I1098-mm5/m48_2000: D 2000 full state at M 48, harmonics 13-25 (#1098)

Machine: macmini-m5-pro (Apple M5 Pro, 18 cores, 48 GB, macOS 27.2.1), runner `choptuik-mm5-i1088-me2`.
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1098

The jump agent's M test at D 2000, ordered by coordinator t5 after `../m64_1000/` was stopped (its README records the D 1000 results: the M 48 -> 64 shift +7.01281e-22
after h23 outer 0, and h23 not released at M 64).

## The bar, written before the run (relayed by the coordinator; recorded here 2026-11-26 12:18 UTC)

The h13 step's shift (M 32 -> 48 with harmonics up to 13 free) compared with D 1000's +1.39e-19 at h17 and +2.3e-19 by h21 (M 48 minus M 32 after h21), then h15-h25 at M 48
falling as at D 1000 (h21 -3.5e-21, h23 -1.5e-21) or not. Reported: each harmonic's Delta change as it releases, and the h13 shift. Stop rules: an exception, or an outer step 3x the
first one's time. If an inner solve stalls as at M 64, report at its second failed trial instead of running all six.

## Inputs and code

- `input/release_ls_h13_D2000.0000.npz`: git blob b26c20a9b984b19177ab91dc5b8a4a22cd8ce33f, from `I1088-dh610/rls2000d/` of this repository (verified with `git hash-object`): D 2000, M 32, 5 nodes (last
  x_l 0.703559), ks 2618, kc 250, kfreeze 13, Moebius horizon (hmob 8), solved. Delta 1.649074313745289325643275661277062778332. Its record: od check 6.87e-49, Hamiltonian check a rows 3.4e-26, Track C 1.649074313886 +- 1.2e-9.
- `tools/resample_m.py`: git blob 4de5c3174ad1bad3a5a311f909db9d3ecec64b5b from `I1098-mac-a/` (as in m48_1000).
- Kernel and code: worktree `~/Source/choptuik-fastmul4` at a3888ffe (form_s.py: relaxed hook at line 71, qq acceptance fix at line 1296), kernel `~/Source/fastmul4-site`, `HP_HORIZON_RELAXED=1`;
  the log's first line is the loaded `hpkernel.__file__`, which must be under fastmul4-site.
- Steps, from `~/Source/choptuik-fastmul4/hp`, `~/venv-314`'s python, nice 10, detached, `timeout 6h` on the release, 9 threads:

      PYTHONPATH=~/Source/fastmul4-site:~/Source/choptuik-fastmul4/hp python tools/resample_m.py input/release_ls_h13_D2000.0000.npz h13_M48.npz 48
      HP_HORIZON_RELAXED=1 PYTHONPATH=~/Source/fastmul4-site python -u form_s.py release_ls h13_M48.npz <this folder> --harm 13,15,17,19,21,23,25 --kmax 31 \
        --jac_by 13:qq,15:qq,17:qq,19:qq,21:qq,23:qq,25:qq --res od --tol 1e-48 --tol_h 1e-44 --threads 9 --outer 6 --commit f50707a8 > rls.log

Delta's change per harmonic is computed by `diff_delta.py` on the log's digits (mpmath), never by hand.
