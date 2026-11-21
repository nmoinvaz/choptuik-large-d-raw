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
