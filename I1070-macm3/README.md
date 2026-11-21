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

