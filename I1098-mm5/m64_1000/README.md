# I1098-mm5/m64_1000: D 1000 harmonics 23-27 at M 64 from the M 48 state (#1098)

Machine: macmini-m5-pro (Apple M5 Pro, 18 cores, 48 GB, macOS 27.2.1), runner `choptuik-mm5-i1088-me2`.
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1098

The jump agent's M 64 test at D 1000, queued by coordinator t5 to start the moment `../m48_1000/` ends (after h23's release).

## The bar, written before the run (relayed by the coordinator; recorded here 2026-11-26 11:41 UTC)

M 48 suffices at D 1000 if the h23 step's shift (M 48 -> 64 with harmonics up to 23 free) is below about 1e-22 and h25 and h27 keep falling.
If the shift is about 1e-20 or more, M 64 is needed and M 80 must be tested next.

Reported: the h23 shift (M 48 -> 64) after it releases, then h25 and h27, beside M 48's h19 +1.2092e-19, h21 -3.4847e-21 and h23 -1.51343e-21 (outer 0;
the m48_1000 README has its final changes). Stop rules: an exception, a harmonic that ends at the outer floor stop without being released, an outer
step 3x past the first one's time, the 4 h timeout. Expect about 1-2 h.

## Inputs and code

- `input/release_ls_h23_D1000.0000.npz`: a copy of `../m48_1000/release_ls_h23_D1000.0000.npz` (the M 48 state after h23, harmonics up to 23 free), made by the queue
  script when m48_1000 ends; its git blob is in `queue.txt`.
- `tools/resample_m.py`: git blob 4de5c3174ad1bad3a5a311f909db9d3ecec64b5b from `I1098-mac-a/` (verified). Its hard-coded `sys.path.insert` path does not exist here,
  so hp/ goes on PYTHONPATH next to the site folder (the ordered command had only the site folder, which lacks `octo_corrector`).
- Kernel and code: worktree `~/Source/choptuik-fastmul4` at a3888ffe (= wip/large-d-form-s f50707a8 + the relaxed horizon), the release build of
  `../fastmul4-build/` in `~/Source/fastmul4-site` (its check PASSED, including the M 64 line). Its form_s.py has the relaxed hook (line 71) and the qq acceptance
  fix (line 1296). `HP_HORIZON_RELAXED=1`; the log's first line is the loaded `hpkernel.__file__`, which must be under fastmul4-site.
- Steps, from `~/Source/choptuik-fastmul4/hp`, `~/venv-314`'s python, nice 10, detached, `timeout 4h` on the release, 9 threads:

      PYTHONPATH=~/Source/fastmul4-site:~/Source/choptuik-fastmul4/hp python tools/resample_m.py input/release_ls_h23_D1000.0000.npz h23_M64.npz 64
      HP_HORIZON_RELAXED=1 PYTHONPATH=~/Source/fastmul4-site python -u form_s.py release_ls h23_M64.npz <this folder> --harm 23,25,27 --kmax 31 \
        --jac_by 23:qq,25:qq,27:qq --res od --tol 1e-48 --tol_h 1e-44 --threads 9 --outer 6 --commit f50707a8 > rls.log

Delta's change per harmonic is computed by `diff_delta.py` on the log's digits (mpmath), never by hand.

## Stopped (2026-11-26 12:17:45 UTC) with h23 not released at M 64

Stopped by hand, with SIGTERM to the `timeout` pid 24957 (python 24958), after 35 min 40 s, on the coordinator's order. Started 11:42:03 UTC by the queue
script (`queue.txt`: input blob 2f100cd0b5f271ea82227b7701ab75b78a786b46, resample exit 0, first log line `hpkernel /Users/nathan/Source/fastmul4-site/hpkernel/__init__.py
HP_HORIZON_RELAXED 1`).

- **The M 48 -> 64 shift at D 1000 is +7.01281e-22** (script on the log's digits: Delta after h23 outer 0, 1.654240854145891722526809527864182415828, minus the M 48
  h23 Delta 1.654240854145891722526108246523219277594), after h23 outer 0 (harmonic-23 step 8.76e-18, target |F| 1.38e-21 -> 6.31e-30, the inner solve at its floor in 2 steps at 6.31e-30,
  590.0 s). That lies between the bar's 1e-22 (M 48 suffices) and 1e-20 (M 80 next).
- **h23 is not released at M 64.** Outer 1 (harmonic-23 step 2.11e-14, target |F| 6.31e-30): the inner solve stalls near 1.2e-31 to 1.4e-31 whatever lam is
  (lam 1: 'NOT converged in 3 steps (|F| 1.17e-31)', 846 s; lam 0.5: 'NOT converged in 3 steps (|F| 1.39e-31)', 1483 s), unlike M 32's floor, which fell as lam^4. Each trial took about 640 s.
  h25 and h27 were not reached. The exit code of the killed run is not meaningful.
