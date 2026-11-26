# I1098-mm5/fix6/D1000_M48_tail6b: D 1000 M 48 harmonics 19-31 with the dDelta release test (#1098)

Machine: macmini-m5-pro (Apple M5 Pro, 18 cores, 48 GB, macOS 27.2.1), runner `choptuik-mm5-i1088-me2`.
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1098

The tail rerun after `../D1000_M48_tail6/` (stopped: its h19-h27 were released by the residual alone while the pending step still moved Delta by about +2.7e-22). Code: `~/Source/choptuik-fastmul6/hp` at dcd93f55
(Python only; its `release_ls` releases by the residual only when the pending step's |dDelta| <= `--ddelta`, default 1e-25), kernel `~/Source/fastmul6-site` (d368a0c0). Start state:
`../D1000_M48_tail6/release_ls_h17_D1000.0000.npz` (M 48, harmonics up to 17 free; blob 6a79f7dd862e9a4b8f7dc74cfbd9d49cb5a59964). Settings: HP_EXACT_RECIP=1, HP_EXACT_DMAT=1, HP_HORIZON_RELAXED=1, OPENBLAS_NUM_THREADS=1, nice 10, `timeout 12h`, 16 threads.

## Bars, written before the run (2026-11-26 15:40 UTC; relayed by the coordinator)

- h19 takes its step ("the step is taken"); the first moves Delta by about **+2.6e-22**, the pending dDelta seen in tail6.
- The next pending dDelta is **<= 1e-25**, so h19 is released "residual and dDelta".
- h21 and h23 then carry their own, smaller dDelta. Their changes are the true tail at D 1000.
- If a harmonic ends at a "Delta floor ... not released", report the floor value: it is the release's resolution at D 1000.

Reported: each harmonic's change, its released_by and any floor (by script from the log's digits).

## Command

    cd ~/Source/choptuik-fastmul6/hp
    HP_EXACT_RECIP=1 HP_EXACT_DMAT=1 HP_HORIZON_RELAXED=1 OPENBLAS_NUM_THREADS=1 PYTHONPATH=~/Source/fastmul6-site nice -n 10 timeout 12h python -u form_s.py release_ls \
      ../D1000_M48_tail6/release_ls_h17_D1000.0000.npz <this folder> --harm 19,21,23,25,27,29,31 --kmax 31 --jac_by 19:qq,21:qq,23:qq,25:qq,27:qq,29:qq,31:qq \
      --res od --tol 1e-48 --tol_h 1e-44 --ddelta 1e-25 --threads 16 --outer 8 --commit dcd93f55 > rls.log
