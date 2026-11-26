# I1098-dh610/tail300: D 300's kfree-31 tail with the old arithmetic switched back on (#1098)

Machine: dh610 (Fedora 45, i7-12700). Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1098

The runs are on the fastmul6 kernel (site_y) with Python 478e9d86, from the old u state: I1088-dh610/rls300's h13,
which is I1098-mac-a/budget300_src/D300_full_base.npz (ks 306, M 32). Settings: release_ls --harm 15..31 --kmax 31,
qq, od, tol 1e-48, --ddelta 1e-25, 2 threads (`../fix/tail300_toggle.sh`).

| run | 1/k, d/dtheta | h15's harmonic step | h15's change |
|---|---|---|---|
| `rd0/` | double-double, double-double (the old kernel's) | 9.70e-10 | -4.81e-17, released at outer 1 |
| `d0/` | lane precision, double-double | outer 0 3.37e-12 (the base re-converging), outer 1 1.71e-9 | |
| fastmul6 from D300_mob6 (I1098-mm5/ladder/D300, and `../chord_test/`) | lane precision, with the remainders | 1.71e-9 | -7.15e-17 |

- rd0 reproduces the old kfree300 run's h15 (-4.8083e-17, I1098-mm5/kfree300). The old tail's departure from fastmul6's
  -7.15e-17 comes from the double-double 1/k. Its residual of about 8e-31 moves the h15 coefficient by 7e-10.
- d0's h15 step at outer 1 matches fastmul6's.
- rd0 was stopped after h15 (16:42 UTC), since it had done its job. d0 continues.
