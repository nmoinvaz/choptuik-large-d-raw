# I1025-win: the l = 1 DSS solution at k_c 63 from D 17 to 20, its growth rate, and the eigenvalues near it on the Mac's k_c 47 and 55 states (#1025, winb's lane)

Runner winb on the win laptop (Surface Laptop 4, i7-1185G7, 4 cores / 8 threads, 32 GB, Windows 11), agent claude-me2. Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1025 (xfkappa's #1025, lane handed over by the coordinator). Status: **running** (started 2026-11-20 00:14:05 UTC; this README is rewritten at each publish).

## Question

#1025 asks whether the l = 1 multiplet's growth rate at finite D heads to #994's 1.997 or to ELL.md's 2.09 to 2.31. Its comment of 2026-11-20 00:08 UTC found lambda_1 at k_c 47 under-resolved at D 17.5 by about 0.07 (k_c 55 gives 1.9522284 against 1.8831583), with the two k_c moves of opposite sign (-0.011 at D 17, +0.069 at D 17.5), so two k_c do not pin lambda_1 there, and k_c 55's psi-constraint (7.9e-4 at D 17, 1.3e-3 at D 17.5, about 1.8x per half unit of D) likely cannot reach D 20. This lane adds a third k_c at D 17 and 17.5, continues at k_c 63 from D 17.5 to 20, and scans the eigenvalues near lambda_1 on the Mac's stored states. Numerical evidence only; the reading belongs to the issue.

## Inputs and code

| item | value |
|---|---|
| code | worktree `C:\Users\nathan\Source\choptuik-i1025`, detached at `56b8f680` (branch `wip/ell1-highD`, `solver/matter/ell_win1025.sh` with `ell_refine.py`, `ell_leap.py`, `ell_eigs.py`, `dss_ell.py`). The worktree has `core.autocrlf=true`, so I re-checked out `ell_win1025.sh` alone with LF (`git -c core.autocrlf=false checkout -- solver/matter/ell_win1025.sh`; the blob is unchanged), since bash does not run it with CRLF |
| inputs (RAW) | the push worktree `choptuik-large-d-raw-754`, detached at origin/main `a1ccd3af` (the coordinator asked for `aa5f2d40` or later); the six input states of `I1025-mac/out` (`sol_l1kc55Fs1025_D17.0000`, `_D17.5000`, `sol_l1kc47Fr1025_D16.0000`, `_D16.5000`, `_D17.0000`, `_D17.5000`, `.npy`) equal the git blobs byte for byte (`cmp`) |
| interpreter | `venv-choptuik-314`: Python 3.14.10, numpy 2.5.4, scipy 1.18.1, mpmath 1.3.0 |
| run | `start_win1025.cmd` (detached, BelowNormal priority, which the issue did not ask for and I use on this machine as usual): `bash ell_win1025.sh` from `solver/matter` with `RAW`, `PY`, `LOGS` set. Four processes at 2 BLAS threads each (P1 k_c 63 starts, then the continuation; P2 lambda on the continuation's states; P3a and P3b the eigenvalue scans), every python under a 12 h `timeout` |
| nothing written in the raw repo while jobs run | outputs go to the code worktree's `solver/matter/data/` and `logs1025/`; the `publish` step copies them into this folder |

## Commands (as `ell_win1025.sh` runs them, from `solver/matter`)

```
ell_eigs.py planted ; ell_eigs.py planted --mutate=beyn                                             # checks.log
ell_refine.py l1kc55Fs1025 55 l1kc63Fw1025 63 1 17,17.5 2.025718689014619 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60       # P1, kc63_start.log
ell_leap.py l1kc63W1025 1 63 data/sol_l1kc63Fw1025_D17.0000.npy 17 data/sol_l1kc63Fw1025_D17.5000.npy 17.5 20 0.125 --tol 1e-12 --fmax 1e-8 --cmax 1e-2 --fold   # P1, leap_kc63.log
ell_refine.py l1kc63W1025 63 l1kc63Fw1025 63 1 18,18.5,19,19.5,20 1.9 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 7200   # P2, lam_kc63.log
ell_eigs.py <state> D kc lambda --r 0 --N 24 --p 12 --dlam 0 --no_polish_complex [--check] --out data/eigs_win1025_{a,b}.jsonl    # P3a, P3b, eigs_a.log, eigs_b.log
    a: kc 47 D 17.5 (--check), D 17, D 16;  b: kc 55 D 17.5 (--check), D 17, kc 47 D 16.5
```

## Checks, fixed before the runs (the coordinator's)

- `logs1025/checks.log` has `planted OK` with exit 0, then `--mutate=beyn` BAD with exit 1. I ran the two once by hand before the start (`pre/planted.log` 6 of 6 true eigenvalues found, exit 0 after 2 s; `pre/planted_beyn.log` 0 of 6 BAD, exit 1), since the script starts its jobs without waiting for them.
- The first job of `eigs_a.log` and of `eigs_b.log` has check (a) <= 1e-6 and (b) <= 1e-12 OK.
- Any failed check stops the lane and is reported.

## Files

| file | what |
|---|---|
| `README.md` | this file |
| `start_win1025.cmd` | the detached launcher |
| `pre/` | the two planted checks run by hand before the start |
| `checks.log` | `ell_eigs.py planted` (exit 0) and its mutation `--mutate=beyn` (exit 1), then the lane's end line |
| `kc63_start.log`, `out/l1kc63Fw1025.jsonl`, `out/sol_l1kc63Fw1025_D*.npy` | k_c 63 at D 17 and 17.5 from k_c 55, with lambda; then lambda at D 18 to 20 |
| `leap_kc63.log`, `out/l1kc63W1025.jsonl`, `out/sol_l1kc63W1025_D*.npy` | `ell_leap --fold` at k_c 63, D 17.5 to 20 |
| `lam_kc63.log` | lambda at k_c 63 on the continuation's half-integer states |
| `eigs_a.log`, `eigs_b.log`, `out/eigs_win1025_*.jsonl` | `ell_eigs`: the eigenvalues inside a circle around lambda_1 (Beyn), with the state checks |
| `main.log` | the script's own stdout and stderr |

## Result

Not yet. Filled at the first publish.
