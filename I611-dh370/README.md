# I611-dh370: the D 54.996085 polishes of #611, by double-double continuation (scan_hp.py) then quad-double polish (scan_qd.py)

Machine: dh370, Fedora Linux 45 Workstation, Intel Core i7-8700 (6 cores, 12 threads, AVX2 and FMA), 31 GB.
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/611
Code: choptuik-large-d main at be8bfb18818352f18b1c9020d526dccbbabf687f, worktree `choptuik-large-d-611`; the kernel is the
build of I604-dh370/ (hp/src, hp/python, the Cargo files and the pyprojects are unchanged since e835d94).
Steps (from `hp/`, nice 10): 1. `scan_hp.py` back from `up10_D55.0351.npz` and forward from `up10_D54.0414.npz` to D 54.996085,
`--kfreeze 13`, 4 threads each. 2. Their Delta must agree to 1e-20. 3. `scan_qd.py` at D 54.996085 from the back state with
`--kfreeze 13` and `--kfreeze -1`, 3 threads each. 4. The cut's effect against win's interpolated -1.2096e-15 (I611-win/README.md).
