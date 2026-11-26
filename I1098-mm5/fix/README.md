# I1098-mm5/fix: the budget reruns on the reciprocal-fix kernel, fastmul5 (#1098)

Machine: macmini-m5-pro (Apple M5 Pro, 18 cores, 48 GB, macOS 27.2.1), runner `choptuik-mm5-i1088-me2`.
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1098

The jump agent's reruns of the budget (raw I1098-mac-a, `fix_reruns.sh`; its inputs at raw commit d7e2e14e) on a kernel with lane-precision reciprocals (fastmul5, f350aa62;
HP_EXACT_RECIP=1), ordered by coordinator t5. They start only after both `../fastmul5-build/` recip_check runs PASS (the queue script checks the exit codes and the PASS lines). Wave 1
runs together, 3 threads each; wave 2 starts when wave 1 ends. If the threads are short with m48_2000 and L50000 running, m48_2000 (on fastmul4, a dd-1/k measurement) is stopped
by exact pid when wave 1 starts, and the coordinator is told.

## Bars, written before the runs (2026-11-26 12:57 UTC; relayed by the coordinator)

| run (`<name>/`) | input (`inputs/<name>.npz`) | what its change measures; bar |
|---|---|---|
| D300_u_base | I1098-mac-a/budget300_src/D300_full_base.npz, blob 569779b213ca7334c01417ae53b7389863220cc9 | its change is the dd-1/k error of the u D 300 record; predicted about **-3.1e-18** |
| D300_u_steps2 | I1098-mac-a/budget300_src/D300_full_steps2.npz, blob fa5ac392d136ea3b82943d2c577dcc44272ec236 | against D300_u_base: the step term with the fix; **below 1e-23** (it was 5e-20) |
| D300_mob_base | I1098-dh610/budget300_src/D300_full_mob8,ks=600.npz, blob b8e2b0008c7cca3c1ad4102888eddb2499045341 | against D300_u_base: u against Moebius with the fix; **below 1e-23** |
| D1000_base | I1098-dh610/budget1000_src/D1000_full_base.npz, blob 19e37e7a05599041730c7659bdac983ae412fd8b | its change is the dd-1/k error of the D 1000 records |
| D1000_steps2 | I1098-dh610/budget1000_src/D1000_full_steps2.npz, blob 786fc4059321f124ffde5ad2cfa33e4af300be15 | against D1000_base: the step term at D 1000, which was **-7.6e-23** |
| D1000_M48 | I1098-dh610/budget1000_src/D1000_full13_M48.npz, blob 0077e2d304ca85026d3766359f3912ffe9a346c1 (M 48, kfreeze 13) | against D1000_base: M 32 -> 48 at kfree 13 with the fix |

Reported: each run's change from the log's "h13's change" line, and the three differences (steps2 - base at D 300 and at D 1000, mob - u base at D 300, and M48 - base at D 1000), against
their bars. All differences are computed by script from the logs' digits.

## Command (common settings)

Run in `~/Source/choptuik-fastmul5/hp` (f350aa62), `HP_EXACT_RECIP=1 HP_HORIZON_RELAXED=1 PYTHONPATH=~/Source/fastmul5-site OPENBLAS_NUM_THREADS=1`, nice 10, `timeout 4h` each, the log's first
line is `hpkernel.__file__` (must be under fastmul5-site), the inputs are the copies in `inputs/` (blobs above, verified with `git hash-object`):

    python -u form_s.py release_ls inputs/<NAME>.npz <NAME> --harm 13 --kmax 13 --jac_by 13:qq --res od --tol 1e-48 --tol_h 1e-44 --threads 3 --outer 8 --commit f350aa62 > <NAME>/rls.log

Wave 1 (about 30-60 min): D300_u_base, D300_u_steps2, D300_mob_base. Wave 2 (about 1-2 h): D1000_base, D1000_steps2, D1000_M48. D1000_M48 uses the same command; `fix_reruns.sh`'s header
mentions `--harm 13,15,...,23 --kmax 31` for M 48, but the order's common command (`--harm 13 --kmax 13`, "M 32 -> 48 at kfree 13") is followed.
