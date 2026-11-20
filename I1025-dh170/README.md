# I1025-dh170: signtests of four ℓ = 1 lambda records at k_c 55 (D 15, 15.5, 16, 16.5), taken off win2b's batch

Machine: dh170 (Linux x86-64, 8 logical CPUs). Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1025. Task from the coordinator's hc, 2026-11-20 about 08:30 UTC.
Started 2026-11-20 08:31 UTC. Beside #1014 step B1 (6 threads) and the #949 lane (2 threads), so it slows both (the box has 8 CPUs, not 5 idle threads).

**What.** `signtest.py` (xfkappa's, from `origin/main:I1025-mac/signtest.py`, hash must start a2f53a90) on the four records of `l1kc55Fb1025.jsonl` (the Mac's k_c 55 batch): for each D the state `sol_l1kc55Fb1025_D<D>.npy` is tested at the record's λ minus and plus 0.02, the sign of det(QM) times sign det Q for the matrix itself and three random orthogonal Q.

**Pass criterion (the coordinator's, fixed before the runs).** A pass is `agree` true at both λ, with opposite signs at λ − 0.02 and λ + 0.02. The table on #1025 has D, pass or fail, the signs, and the count of singular values below 1e-12 sigma_max.

**Control, before the real runs.** `signtest.py planted` must print agree, agree, DISAGREE (the check can fail: the DISAGREE case has 40 singular values at 1e-19).

**Setup.** Worktree `~/Source/choptuik-large-d-1025st` detached at origin/wip/ell1-highD (head recorded in the log below), the -935 venv's python (4.8.2 build, numpy and scipy), run from `solver/matter`, 4 BLAS threads, nice 10, one D at a time, `timeout 7200` each. The inputs are taken by `git show` from the raw clone's `origin/main` (no pull) into a fresh folder outside the raw repo and each `git hash-object` is logged in `hashes.txt` (inputs are already in the raw repo's I1025-mac; they are not copied here). Output: `signtest.log`.

## Stopped at 2026-11-20 08:43 UTC (written 2026-11-20 08:43 UTC)

The coordinator's hc ("8 logical CPUs, all already used; stop the signtest chain now by exact pid so B1 gets its 6 threads back; post what finished, the rest moved to win2b"). `run_signtest.sh` (852113), its `timeout` (852115) and the python (852116) were stopped by exact pid at 08:43:05 UTC, 10 min 44 s into D 15, which had printed only its header line. **No D finished: no row to keep.** What ran: the planted control (agree, agree, DISAGREE, `planted.log`) and the first 10 min of D 15 (`signtest.log`). The four records (D 15, 15.5, 16, 16.5) are not tested here; win2b takes them. The worktree `~/Source/choptuik-large-d-1025st` (detached at d4f0f854, `git status` clean) was removed at 08:44 UTC by the coordinator's order (`git worktree remove`).
