# I1025-win2b: #1025 lambda_1 at k_c 55, D 16.25 and 16.75, from the k_c 47 leap states

win2 (Windows desktop, 20 threads), https://github.com/nmoinvaz/choptuik-large-d/issues/1025. Task from the coordinator (hc 2026-11-20), commands from xfkappa.

- Code: worktree `D:/choptuik-i1025b`, detached at `origin/wip/ell1-highD` 5c9d001c, run from `solver/matter`. Python: venv-i962 (3.14.10, numpy 2.5.4, scipy 1.18.1, mpmath 1.3.0), 4 BLAS threads per solve (`OPENBLAS_NUM_THREADS=4 OMP_NUM_THREADS=4 MKL_NUM_THREADS=4`), BelowNormal, the two solves at once beside win2-build's build and #1003 K 49.
- Inputs, taken by `git show origin/main:I1025-mac/...` of choptuik-large-d-raw (no checkout), blob hashes checked: `sol_l1kc47F1025_D16.750000.npy` -> `data/sol_l1kc47Fx1025_D16.7500.npy` (6c4d8278), `sol_l1kc47F1025_D16.250000.npy` -> `data/sol_l1kc47Fx1025_D16.2500.npy` (4c169200), `I1025-mac/signtest.py` (a2f53a90).
- Commands (`ell_refine.py l1kc47Fx1025 47 TAG 55 1 D LAM0 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60`): D 16.75, TAG `l1kc55Fv1025`, lam0 2.0928; D 16.25, TAG `l1kc55Fu1025`, lam0 2.2009. Glue: `run1025.sh` (the ordered `timeout 43200` replaced by a 43200 s cap on each job's tree by its exact pid, so no orphaned python), `rootpid1025.ps1`, `mem1025.sh` (+ `mem1025.ps1`: free-memory log; below 4 GiB it stops the D 16.25 solve first and tells the coordinator).
- Record checks: `n_signchanges` 1 and lambda within 2% of its guess; then `signtest.py planted` (must print agree, agree, DISAGREE) and a signtest at lambda +- 0.02 on each record (agree true in both JSON lines, opposite signs).

Files: `out/` the two jsonl and two `sol_l1kc55F*_D*.npy`; `kc55_D16.75.log`, `kc55_D16.25.log`, `signtest.log`, `exits_1025.txt`, `mem_1025.log`, `signtest.py` (the Mac's, blob a2f53a90).
