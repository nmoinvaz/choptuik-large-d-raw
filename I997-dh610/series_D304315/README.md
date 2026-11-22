# I997-dh610/series_D304315: Delta's Taylor series in D at D 3.04315, M 320, N 8, next to the sonic closing (#997)

Machine dh610 (Fedora 45, i7-12700, 20 threads, 62 GB). Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/997 (the coordinator's comment of 2026-11-22, id 7073219529, on dh610's free 10 threads beside #1067). Base: raw `I945-win2/leg/states/lowD343_D3.043150_M320.npz` (blob c23b9cb3, M 320, accepted at its residual floor 7.35e-21, #945). Run: `anm_lowd.py` from a worktree at origin/main ab0ddb8c (`~/Source/choptuik-large-d-997c`) with venv-i1058, 10 threads at nice 10. Pilot stop rule (the comment's): each order's time is reported; if order 2 is not done within 3 h, or an order's solve does not converge, stop and report; the target stage is stopped by exact pid past 30 min after the series file is saved. Readings (fixed by the coordinator): a ratio-test radius of 0.03 or more over the converged orders means the closing is not a singularity of Delta; 0.001 or less means it is; between, no reading; with `hp/series_singularity.py`'s plants first, a plant at 3.000 and one at 3.04312 at this base.

Written as the run goes.

## Before the launch (22 Nov): the command diff, the plants, the selftests

Command diffed against the coordinator's (`ref/commands_hc_997.txt`, verbatim from his comment) by `cmddiff997.py` (tokens after `anm_lowd.py`; `nice`, python and `-u` dropped; the empty `--checks` kept): `cmddiff_prelaunch.txt`:

```
cmddiff997: EMPTY
```

Selftests: `cmddiff997.py --selftest` (a same command, and five slips: `--N 9`, `--target 3.0432`, `--threads 6`, a wrong state, a dropped `--checks ''`, each must differ) PASS, `--break` exits 1; `run997c.py --selftest` (the z_k parser, the order-2 3 h rule, the not-converged rule) pass, `--mutate` exits 1. Plants (`read997c.py plants`, `plants_997c.txt`; criteria fixed before the data: at D0 3.04315, N 8, for every K from 4 to 8 the plant D* = 3.000 (true radius 0.04315) must read 'not a singularity' and D* = 3.04312 (true radius 3e-5) 'a singularity', by the ratio fit over orders 2..K): PASS (radius 0.0379 to 0.0421 and 2.99e-5 to 3.00e-5); `plants --mutate` (the not-a-singularity bar raised to 0.5) exits 1 as it must. The ratio fit and plants come from `hp/series_singularity.py` at ab0ddb8c.

## Pilot end (22 Nov, 05:58:34 UTC): stopped by the 3 h rule, no order and no base line

`run997c.py` sent TERM to the exact pid 1124569 at 05:58:34 UTC, 10801 s after the start (02:58:32): "order 2 not done within 3 h" (`exits_997c.txt`; exit -15). `anm_lowd.log` holds only its command line and `anm_lowd.jsonl` is empty, so the run printed no `base` line (written after the base state's f64 Jacobian and block LU) and no `z_k` line: the base stage had not ended in 3 h. CPU (`rss_997c.log`): about 130% for the first 15 min, then 670% rising to 955% (10 threads), RSS 475 MB rising to 817 MB, load 20 (this run and #1067's 10 threads each). The state's plan has 14358 steps (`meta['segs']`, 20 segments, L 28161), against 1063 steps for the M 256 run at D 3.15, whose base line took 261 s (`I997-dh610/series/run.log`), and 2348 to 5082 steps for the T82 M 320 states, whose base lines took 1645 s (2348 steps) and 1196 to 2493 s (5082 steps), so the step count alone does not give the time. This run ran on shared threads at nice 10 and took more than 3 h. The cause is not measured. Not relaunched: the rule says stop and report.
