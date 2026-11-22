# I1070-macm3: γ at D 3.15 at M 128 (pilot) and M 160, hp/lowD_gamma.py

Machine macm3 (the M3 Mac, 8 CPUs, 24 GB, runner macm3b), issue https://github.com/nmoinvaz/choptuik-large-d/issues/1070
(the coordinator's hc of 2026-11-21). The question: the first growth rate γ = 1/λ below D 3.5, at D 3.15, at M 128 and M 160.
Our γ stops at D 3.5 (#628: 0.3223855827556097 at M 128); Ecker, Ecker, Grumiller and Jechtl (arXiv:2602.10185, §5.3) find γ → 0
faster than Δ as D → 3. README first: written before any run starts.

## Setup

- Code: worktree `~/Source/choptuik-large-d-1070`, detached at origin/main 6c4d845d (`hp/lowD_gamma.py` is unchanged since
  8179068d; no change to `hp/src`, `hp/Cargo.toml`, `hp/Cargo.lock`, `hp/pyproject.toml` or `hp/build.sh` between 8179068d and
  6c4d845d).
- Build: venv `venv-macm3-1058b` (hp built at 8179068d; hpkernel `.so` sha1 6d8213c28d71, isa neon; its installed
  `hpkernel/__init__.py` and `driver.py` are byte-identical to main's `hp/python/hpkernel/` files). Python 3.14. Each run's
  `exits_1070.txt` line carries the code commit, the interpreter, `hpkernel.__file__` and the multidouble package path.
- Inputs: raw `I927-mac/inputs/lowDhm_x0.000625-0.9_D3.1500_M128.npz` (blob df2ab378105434a07bad081e0ce4a973ff6b97cc, 168254 bytes)
  and `..._M160.npz` (blob 2515013d1ed23e09e5ca7d4aee82ac5781f72d12, 209326 bytes). Both blobs are the same at origin/main
  (028483847, fetched 2026-11-21) and in the `raw-749p` clone the runs read them from (`git hash-object` of the files on disk).
  States: D 3.15, kt 36, kc 100, ks 250, 17 nodes (0.000625 … 0.9), M 128 and M 160.
- Run: `run_1070.sh M128|M160 [LAM0]`, 6 threads, `caffeinate -is nice -n 10`, a 6 h cap (21600 s) by exact pid through
  `capped_run.py` (SIGTERM at the cap, SIGKILL 60 s later). `watch_1070.py MODE` logs the process's rss and cpu, the free memory
  and disk every 60 s (`res_MODE.log`, `res_summary_MODE.txt`); it is alert-only (hc at free disk < 3 GiB or free memory < 8%) and
  kills nothing.

## Command, against the issue's

The issue's pilot command (`issue_cmd.txt`, verbatim) and mine (`my_cmd_M128.txt`, from `DRY=1 run_1070.sh M128`), one token per
line, `diff issue mine` (`cmd_diff_M128.txt`):

```
1c1
< python3
---
> /Users/nathan/Source/venv-macm3-1058b/bin/python
4,5c4,5
< <raw>/I1070-macm3/lowD_gamma_D3.15_M128.jsonl
< <raw>/I927-mac/inputs/lowDhm_x0.000625-0.9_D3.1500_M128.npz
---
> /Users/nathan/Source/choptuik-large-d-raw-903/I1070-macm3/lowD_gamma_D3.15_M128.jsonl
> /Users/nathan/Source/choptuik-large-d-raw-749p/I927-mac/inputs/lowDhm_x0.000625-0.9_D3.1500_M128.npz
```

Only the interpreter (the venv's python for `python3`) and the two `<raw>` prefixes differ (output: the live folder
`~/Source/choptuik-large-d-raw-903/I1070-macm3`; input: `~/Source/choptuik-large-d-raw-749p/I927-mac/inputs`). Flags are the
issue's: `--threads=6 --polish=2 --xtol=1e-11`, no `--lam0` (the script's `lam_guess(D)`). The wrapper `caffeinate -is nice -n 10
capped_run.py 21600` is added around it. `check_cmd_1070.py M128` checks the run's command against the issue's token by token
(`--selftest`: 11 planted cases, 9 of them broken: threads, polish, xtol, a `--lam0` on M 128, the wrong state, a missing or
non-numeric `--lam0` on M 160, `python3`, a dropped `-u`; all fire). The M 160 run's command has the same differences plus
`--lam0=<λ of the M 128 run>`, as the issue says; its diff goes in the M 160 section below when it starts.

## Acceptance (the issue's)

- Each run ends with exactly one sign change in its bracket (`n_signchanges` 1) and F after the polish below 1e-27. If not,
  report and stop.
- γ(160) − γ(128) is the M error at D 3.15: a resolution change, not a bound.
- γ(3.15) against γ(3.5) = 0.32238558 and against Ecker et al.'s values near 3.15 if their data have one
  (`hp/lowD_ecker.py <clone>`, read only).
- Run 2 (M 160, `--lam0` the M 128 λ) only if the pilot ends with one sign change in its bracket.
- Report for the pilot: the determinants, the bracket's sign changes, F after the polish, λ, γ and the wall time, and the cpu and
  memory. Stop rules: a failed check or a bug stops the work and is reported; no workaround without the coordinator.

## Runs

### M 128 pilot: no sign change (stop)

`run_1070.sh M128`, started 2026-11-21 21:23:13 UTC, exit 0 at 22:14:35 UTC (capped_run wall 3082 s, own 3070.0 s, cap 21600 s not
reached), child pid 95148. Files: `run_M128.log`, `lowD_gamma_D3.15_M128.jsonl`, `table_M128.md` (from `table_1070.py`),
`res_M128.log`, `res_summary_M128.txt`, `res_stats_M128.txt`, `exits_1070.txt`.

Acceptance: F after the polish 1.103e-28 (below 1e-27: met). Sign changes in the bracket: 0 (needs exactly one): **not met**. The
script's four-width search (±1e-4, ±1e-3, ±1e-2, ±4e-2 round the guess λ 3.713742) found sign -1 at all 9 points, so λ and γ are
null. Per the issue: report and stop; the M 160 run was not started, and nothing was changed or restarted.

M128: D 3.15, M 128, F after the polish 1.103e-28, guess lam 3.713742062 (gamma guess 0.269270), sign changes 0, determinants 9, lam None, gamma None, own seconds 3070.0

polish lines:
- newton 0: |F| 6.69e-26 |dz| 2.10e-22 lam 1 dDelta +1.49e-31 Delta 2.961319687827138 piv 2.2e-04..9.3e+00  t 141.2s
- newton 1: |F| 1.29e-28 |dz| 9.18e-27 lam 1 dDelta -7.57e-31 Delta 2.961319687827138 piv 2.2e-04..9.3e+00  t 294.6s

| lam | sign | ln\|det\| | pivots | s |
|---|---|---|---|---|
| 3.673742062090 | -1 | 2230.826596 | 2.65e-04..2.90e+02 | 337.1 |
| 3.703742062090 | -1 | 2254.866799 | 2.65e-04..3.16e+02 | 308.7 |
| 3.712742062090 | -1 | 2262.078488 | 2.64e-04..3.24e+02 | 296.9 |
| 3.713642062090 | -1 | 2262.799647 | 2.68e-04..3.25e+02 | 252.8 |
| 3.713742062090 | -1 | 2262.879776 | 2.68e-04..3.25e+02 | 299.9 |
| 3.713842062090 | -1 | 2262.959904 | 2.68e-04..3.25e+02 | 282.8 |
| 3.714742062090 | -1 | 2263.681061 | 2.68e-04..3.26e+02 | 306.1 |
| 3.723742062090 | -1 | 2270.892530 | 2.67e-04..3.35e+02 | 322.2 |
| 3.753742062090 | -1 | 2294.929397 | 2.67e-04..3.65e+02 | 368.1 |

bracket scanned: lam 3.673742 .. 3.753742, gamma 0.266401 .. 0.272202; signs [-1]
d ln|det| / d lam between neighbouring points: min 801.2, max 801.3 (ln|det| rises with lam at every pair: True)
seconds per determinant: mean 308.3, min 252.8, max 368.1; sum 2775 of the run's 3070 s
lam_guess(3.5) = 3.092124 against 1/gamma(3.5) = 3.101876 (#628's M 128 gamma 0.3223855827556097): the guess misses by -0.009751 at D 3.5

Resources, from `res_M128.log`: polls 51 (60 s each), rss GB min 0.19 max 3.36 mean 1.89; cpu% (ps, 100 = one core) min 593.2 mean 598.9 max 600.0; load1 mean 6.33 max 9.62; free memory min 85%; free disk min 22.8 GiB

Machine after the pilot (22:15 UTC): cpu 86.6% idle, free memory 85%, free disk 23 GiB.

## Rerun r2: the M 128 command with `--lam0 4.3977` (the coordinator's order, 2026-11-21 22:19 UTC)

Cause of the pilot's stop: the guess (`lam_guess(3.15)`, a quadratic extrapolation from D 3.64 to 3.70) gave λ 3.7137, γ 0.2693. The coordinator's
comment on #1070 (7070090021): Ecker, Ecker, Grumiller and Jechtl's GammaList (their `complete_data/GammaList.dat`, read as data) has
γ 0.2225464 at D 3.14 and 0.2486066 at D 3.2; interpolated to D 3.15 through three or four of their points γ 0.227280 to 0.227411, so
λ 4.3973 to 4.3999 (an interpolation spread, not a bound). The order: the issue's M 128 command with `--lam0 4.3977`, otherwise
unchanged, cap 6 h; the script's brackets widen to ±0.04, which covers λ 4.358 to 4.438. Readings as before: exactly one sign change
in the bracket and F after the polish below 1e-27; then γ(3.15) at M 128 is compared with their interpolated 0.2274. If there is still
no sign change in the bracket, stop and report. M 160 follows only after a pass.

Command, the issue's (`issue_cmd.txt`) against mine (`my_cmd_M128_r2.txt`, from `TAG=_r2 DRY=1 run_1070.sh M128 4.3977`), one token per
line, `diff issue mine` (`cmd_diff_M128_r2.txt`):

```
1c1
< python3
---
> /Users/nathan/Source/venv-macm3-1058b/bin/python
4,5c4,5
< <raw>/I1070-macm3/lowD_gamma_D3.15_M128.jsonl
< <raw>/I927-mac/inputs/lowDhm_x0.000625-0.9_D3.1500_M128.npz
---
> /Users/nathan/Source/choptuik-large-d-raw-903/I1070-macm3/lowD_gamma_D3.15_M128_r2.jsonl
> /Users/nathan/Source/choptuik-large-d-raw-749p/I927-mac/inputs/lowDhm_x0.000625-0.9_D3.1500_M128.npz
8a9
> --lam0=4.3977
```

The differences: the interpreter, the two `<raw>` prefixes, the output name `..._M128_r2.jsonl` (a new file, so that the pilot's record and this run's
do not mix; `run_1070.sh` takes a `TAG` env for it and the log is `run_M128_r2.log`), and the added `--lam0=4.3977` (the order). Flags
otherwise the issue's: `--threads=6 --polish=2 --xtol=1e-11`. The wrapper is as before (`caffeinate -is nice -n 10 capped_run.py 21600`).
`run_1070.sh` and `check_cmd_1070.py` changed for this: `TAG`, and the checker's M 128 case now allows exactly the `--lam0` given on its
command line (`check_cmd_1070.py M128 4.3977`: pass; `--selftest`: 15 cases, 12 broken, all fire, among them a different `--lam0`, a
missing one, and `--polish=3` with it).

### Rerun r2 result: one sign change, a root (pass)

`TAG=_r2 run_1070.sh M128 4.3977`, started 2026-11-21 22:19:33 UTC, exit 0 at 23:41:37 UTC (capped_run wall 4924 s, own 4917.6 s, cap not
reached), child pid 99867. Files: `run_M128_r2.log`, `lowD_gamma_D3.15_M128_r2.jsonl`, `table_M128_r2.md`, `res_M128_r2.log`,
`res_summary_M128_r2.txt`, `res_stats_M128_r2.txt`, `exits_1070.txt`.

| criterion (the issue's) | result | met |
|---|---|---|
| F after the polish below 1e-27 | 1.103e-28 (the polish: 6.69e-26 -> 1.29e-28 in 2 Newton steps, 752.0 s) | yes |
| exactly one sign change in the bracket | `n_signchanges` 1: in the script's first grid (lam0 ± 1e-4: 4.3976 -, 4.3977 -, 4.3978 +) | yes |

λ = 4.397784106690153, γ = 1/λ = 0.22738724224291604 (`n_det` 7; brentq `xtol` 1e-11 on λ, so γ is good to about 3e-13: the last two points
4.397784106685 (-1) and 4.397784106690 (+1) bracket the root). The search stopped at its first width with a sign change, so the window
beyond ±1e-4 was not scanned for further roots (the bracket holds one).

The determinants near the root behave as a simple zero: the local slope of ln|det| against ln|λ - λ*| is 0.898, 0.952, 1.005, 1.000 over
|λ - λ*| from 1.8e-4 to 1.4e-8 (`table_M128_r2.md`).

Readings:
- γ(3.15) at M 128 = 0.2273872422, against the coordinator's interpolation of the Vienna group's GammaList, γ 0.22728 to 0.227411 (comment 7070090021; an interpolation spread, not a bound): inside it, 2.38e-05 below its upper end and 1.07e-04 above its lower end.
- The guess 4.3977 missed the root by 8.411e-05 in λ.
- γ(3.15)/γ(3.5) = 0.70533, with γ(3.5) = 0.3223855827556097 (#628, M 128).
- γ(160) − γ(128), the M error at D 3.15 (a resolution change, not a bound): from the M 160 run below.

Resources, from `res_M128_r2.log`: polls 82 (60 s each), rss GB min 0.18 max 2.43 mean 1.64; cpu% (ps, 100 = one core) min 99.1 mean 498.1 max 558.9; load1 mean 18.71 max 39.10; free memory min 78%; free disk min 22.1 GiB. The pilot's, for comparison: polls 51 (60 s each), rss GB min 0.19 max 3.36 mean 1.89; cpu% (ps, 100 = one core) min 593.2 mean 598.9 max 600.0; load1 mean 6.33 max 9.62; free memory min 85%; free disk min 22.8 GiB. Each determinant took 594.8 s (min 532.7, max 613.0), against 308.3 s in the pilot; the
polish 752.0 s against 294.6 s. The cpu of the process was lower (mean 498% against 599%) and the machine's load1 higher (mean 18.71,
max 39.10, against 6.33 and 9.62). I do not know what else ran; the process list at the end showed nothing heavy.

## M 160 run (after the pass; the issue's step 2, the coordinator's order "M 160 follows only after a pass", 2026-11-21 23:43 UTC)

`run_1070.sh M160 4.397784106690153` (`lam0_M160.txt`: the r2 run's λ, as in `lowD_gamma_D3.15_M128_r2.jsonl`), the M 160 state
(blob 2515013d1ed23e09e5ca7d4aee82ac5781f72d12), the same worktree (main 6c4d845d) and `venv-macm3-1058b`, 6 threads, `nice -n 10`, 6 h
cap by exact pid. The issue's command (`issue_cmd.txt`, the M 128 pilot's) against mine (`my_cmd_M160.txt`), one token per line,
`diff issue mine` (`cmd_diff_M160.txt`):

```
1c1
< python3
---
> /Users/nathan/Source/venv-macm3-1058b/bin/python
4,5c4,5
< <raw>/I1070-macm3/lowD_gamma_D3.15_M128.jsonl
< <raw>/I927-mac/inputs/lowDhm_x0.000625-0.9_D3.1500_M128.npz
---
> /Users/nathan/Source/choptuik-large-d-raw-903/I1070-macm3/lowD_gamma_D3.15_M160.jsonl
> /Users/nathan/Source/choptuik-large-d-raw-749p/I927-mac/inputs/lowDhm_x0.000625-0.9_D3.1500_M160.npz
8a9
> --lam0=4.397784106690153
```

The differences: the interpreter, the two `<raw>` prefixes, M 128 -> M 160 in the output and state names (the issue's step 2 runs "the
same with the M 160 state"), and the added `--lam0=4.397784106690153` (the issue's step 2: `--lam0` set to the M 128 λ). Flags otherwise the
issue's. `check_cmd_1070.py M160 4.397784106690153`: pass. The window: the script's brackets widen to ±0.04 round that λ; the same
acceptance (one sign change, F below 1e-27); stop and report otherwise. The cost: a determinant at M 160 is about (11521/9217)^3 = 1.95 times an M 128
one (an estimate from the LU's cube law, not a measurement), so about 600 s at the pilot's speed and 1160 s at r2's.

### M 160 run: refused at its first Newton step (stop), and `mode_det` refuses M 160 too

`run_1070.sh M160 4.397784106690153` started 2026-11-21 23:44:28 UTC (child pid 3205) and exited 1 after 10 s (`exits_1070.txt`, `run_M160.log`);
no record was written (`lowD_gamma_D3.15_M160.jsonl` does not exist). The log:

```
capped_run: child pid 3205, cap 21600 s
Traceback (most recent call last):
  File "/Users/nathan/Source/choptuik-large-d-1070/hp/lowD_gamma.py", line 95, in <module>
    main()
    ~~~~^^
  File "/Users/nathan/Source/choptuik-large-d-1070/hp/lowD_gamma.py", line 81, in main
    zh, zl, _ = newton_solve(s, zh, zl, tol=1e-29, it_max=int(opts["polish"]), verbose=True)
                ~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/nathan/Source/venv-macm3-1058b/lib/python3.14/site-packages/hpkernel/driver.py", line 304, in newton_solve
    dh, dl, Fh, Fl, pmin, pmax, info = newton_step(s, zh, zl, cur, mixed, gmres)
                                       ~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/nathan/Source/venv-macm3-1058b/lib/python3.14/site-packages/hpkernel/driver.py", line 212, in newton_step
    dh, dl, Fh, Fl, pmin, pmax = s.newton(zh, zl)
                                 ~~~~~~~~^^^^^^^^
ValueError: newton: the dense n x n path is limited to M <= 128 (memory); at M = 160 use newton_mixed (block storage)
capped_run: exit 1 wall 10 s cap_hit False
```

Cause: the kernel's dense n x n paths (`newton`, `jacobian`, `mode_matrix`, `mode_det`, `lu_factor`, `lm_steps`) stop at M = 128 (`DENSE_M_MAX`, `hp/src/python.rs`),
and above it only `newton_mixed` in block storage runs. `notes/HIGH_M.md` ("Not supported in block storage"): "the mode matrix (γ). Above M = 128
the dense paths (... `mode_matrix`, `mode_det`, ...) refuse ... So the exact double-double Jacobian, the Levenberg–Marquardt fallback and γ stop at
M = 128." So the `--polish=2` Newton step fails first, but dropping `--polish` would not help: `Solver.mode_det` begins with `dense_ok`. Probe (`probe_mode_det_M160.py`,
output `probe_mode_det_M160.txt`, 2026-11-21 23:45 UTC, 2 threads, 1.3 s, no output file): `ValueError mode_det: the dense n x n path is limited to M <= 128 (memory); at M = 160 use newton_mixed (block storage) (1.3 s)`.

The issue's step 2 cannot run with `hp/lowD_gamma.py` on this kernel, at any `--polish`. Stop; no workaround tried and none started (a block-storage determinant or a
different M pair needs the coordinator's word). The only D 3.15 states in raw `I927-mac/inputs/` are M 128 and M 160. So γ(160) − γ(128) at D 3.15 is not available.

## D 3.425 pair, no lift: M 96 then M 128 from T39's stored states (the coordinator's order, 2026-11-21 23:48 UTC)

The order (hc, 2026-11-21 after the PASS of r2; #1070's comment 7071100314 lists the first values): resolution pairs at D 3.45 (dh170) and D 3.425 (macm3b), both
from T39's stored M 96 and M 128 states, so no lift is needed. `hp/lowD_gamma.py` on each, `--threads=6 --polish=2 --xtol=1e-11 --lam0=3.23409`
(the Vienna group's γ 0.3092057 interpolated at D 3.425; 1/0.3092057 = 3.234093032566993), `nice -n 10`, cap 3 h each (10800 s, by exact pid), M 96 first,
then M 128 with `--lam0` set to M 96's λ. Readings as in the issue: each run ends with exactly one sign change in its bracket and F after the polish below
1e-27 (if not, report and stop); report γ(128) − γ(96), a resolution change and not a bound, and both against 0.3092057.

- Inputs: raw `T39-win/hp/data/lowD_states/lowDvh41_D3.4250_M96.npz` (blob 6b371fff7f184e647d29b4ad8c9d1e7885df0566, 87310 bytes) and `..._M128.npz`
  (blob a2c3c011391d2d36421716199941f0442924bcf9, 115986 bytes); both blobs are the same at origin/main (920cf2cf0, fetched 2026-11-21) and in the `raw-749p` clone the
  runs read them from. States: D 3.425, kt 36, kc 100, ks 250, 13 nodes (0.005 … 0.8), 5377 (M 96) and 7169 (M 128) unknowns.
- Code and build as for the D 3.15 runs: worktree `choptuik-large-d-1070` at origin/main 6c4d845d (still origin/main at this start; no change to `hp/lowD_gamma.py`, `hp/src`,
  `hp/python`, `Cargo.toml` or `pyproject.toml` since), `venv-macm3-1058b`.
- Scripts: `run_1070_D3425.sh M96|M128 LAM0` (output `lowD_gamma_D3.425_<M>.jsonl`, log `run_D3.425_<M>.log`), `check_cmd_1070_D3425.py M96|M128 LAM0` against the issue's pilot command
  (`--selftest`: 13 cases, 11 broken: threads, polish, xtol, the wrong M, the wrong D, a missing or extra or different `--lam0`, `python3`, a dropped `-u`; all fire),
  `table_1070.py LABEL LOGFILE JSONL` (the determinant table), `watch_1070.py D3.425_M96` (resources, alert-only).

### M 96 command, against the issue's

The issue's pilot command (`issue_cmd.txt`) and mine (`my_cmd_D3425_M96.txt`, from `DRY=1 run_1070_D3425.sh M96 3.23409`), one token per line, `diff issue mine` (`cmd_diff_D3425_M96.txt`):

```
1c1
< python3
---
> /Users/nathan/Source/venv-macm3-1058b/bin/python
4,5c4,5
< <raw>/I1070-macm3/lowD_gamma_D3.15_M128.jsonl
< <raw>/I927-mac/inputs/lowDhm_x0.000625-0.9_D3.1500_M128.npz
---
> /Users/nathan/Source/choptuik-large-d-raw-903/I1070-macm3/lowD_gamma_D3.425_M96.jsonl
> /Users/nathan/Source/choptuik-large-d-raw-749p/T39-win/hp/data/lowD_states/lowDvh41_D3.4250_M96.npz
8a9
> --lam0=3.23409
```

The differences: the interpreter, the output name, the state (D 3.425 M 96 from T39 for the issue's D 3.15 M 128 input) and the added `--lam0=3.23409` (the order). Flags
otherwise the issue's. `check_cmd_1070_D3425.py M96 3.23409`: pass. The M 128 command's diff goes in a section below when it starts.

### D 3.425 M 96: one sign change, a root (pass)

`run_1070_D3425.sh M96 3.23409`, started 2026-11-21 23:49:09 UTC, exit 0 at 2026-11-22 00:05:50 UTC (capped_run wall 1001 s, own 994.1 s, cap 10800 s not reached), child pid 6992.
Files: `run_D3.425_M96.log`, `lowD_gamma_D3.425_M96.jsonl`, `table_D3.425_M96.md`, `res_D3.425_M96.log`, `res_stats_D3.425_M96.txt`, `exits_1070.txt`.

| criterion (the issue's) | result | met |
|---|---|---|
| F after the polish below 1e-27 | 3.094e-30 (the polish: Newton step 0 found the state converged, \|F\| 3.09e-30, last \|dz\| 5.3e-26, so no step was taken) | yes |
| exactly one sign change in the bracket | `n_signchanges` 1 (grid lam0 ± 1e-4: 3.23399 -, 3.23409 -, 3.23419 +) | yes |

λ = 3.2341077237548475, γ = 1/λ = 0.3092042954088694 (`n_det` 7, 130.8 s per determinant; brentq `xtol` 1e-11 on λ, so γ is good to about 1e-12). Against the Vienna value 0.3092057: γ(96) − 0.3092057 = -1.405e-06 (relative -4.54e-06).
The guess 3.23409 missed the root by 1.772e-05 in λ. Near the root the local slope of ln|det| against ln|λ − λ*| is 0.708, 1.034, 0.997 (|λ − λ*| 1.2e-4 to 7.5e-7).
Resources: polls 17 (60 s each), rss GB min 0.16 max 1.46 mean 0.86; cpu% (ps, 100 = one core) min 449.2 mean 537.6 max 554.3; load1 mean 9.15 max 15.54; free memory min 79%; free disk min 20.0 GiB.

### M 128 command (`--lam0` = M 96's λ, as ordered; 2026-11-22 00:06 UTC)

`run_1070_D3425.sh M128 3.2341077237548475` (`lam0_D3425_M128.txt`: the M 96 run's λ from `lowD_gamma_D3.425_M96.jsonl`), the T39 M 128 state, cap 3 h (10800 s) by exact pid. The issue's command against mine
(`my_cmd_D3425_M128.txt`), one token per line, `diff issue mine` (`cmd_diff_D3425_M128.txt`):

```
1c1
< python3
---
> /Users/nathan/Source/venv-macm3-1058b/bin/python
4,5c4,5
< <raw>/I1070-macm3/lowD_gamma_D3.15_M128.jsonl
< <raw>/I927-mac/inputs/lowDhm_x0.000625-0.9_D3.1500_M128.npz
---
> /Users/nathan/Source/choptuik-large-d-raw-903/I1070-macm3/lowD_gamma_D3.425_M128.jsonl
> /Users/nathan/Source/choptuik-large-d-raw-749p/T39-win/hp/data/lowD_states/lowDvh41_D3.4250_M128.npz
8a9
> --lam0=3.2341077237548475
```

The differences: the interpreter, the output name, the state, and the added `--lam0=3.2341077237548475`. Flags otherwise the issue's. `check_cmd_1070_D3425.py M128 3.2341077237548475`: pass.
