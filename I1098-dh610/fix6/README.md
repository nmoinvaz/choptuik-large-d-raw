# I1098-dh610/fix6: full solves on the fastmul6 kernel (site_y) on dh610 (#1098)

Machine: dh610 (Fedora 45, i7-12700). Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1098

Settings: HP_EXACT_RECIP=1, HP_EXACT_DMAT=1, HP_HORIZON_RELAXED=1, release_ls with qq, od, tol 1e-48, Python 478e9d86
(`../fix/after_y.sh`, `../fix/run_m48_2000_6.sh`).

- `D2000_base6/`: I1088-dh610/rls2000d's full M 32 kfree-13 state (Moebius a 8, ks 2618), re-solved on fastmul6 with 6
  threads. It was released at outer 2 (qd check 1.0e-60). Delta 1.649074313745289325642428789601977779893: **-8.469e-22**
  against the old record, the double-double 1/k and d/dtheta together. The outer steps took 1555 s and 1709 s.
- `D2000_M48_6/` (running): the same state resampled to M 48 (I1098-mm5/m48_2000/h13_M48.npz), h13 then the tail
  h15..h31.
