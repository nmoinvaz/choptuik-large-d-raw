# I675-dh610: #499's weak split at the REF start with the frame from the LU at z0, and the old frame as the control

Machine: dh610 (the former win3), Fedora Linux 45 Workstation (kernel 7.3.3), Intel Core i7-12700 (12 cores, 20
threads, AVX2 and FMA), 62 GB. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/675

Code: choptuik-large-d main at 0da740e1 in a detached worktree (`choptuik-i675`), with `hp/weak_corrector.py`'s
`--split_at`. The venv is the main checkout's (`.venv`, Python 3.14, hpkernel built from main a879ccc3, as #608). One user
unit `i675` runs the two commands one after the other, each with 2 threads at nice 10 under `systemd-inhibit`, with
`OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 PYTHONFAULTHANDLER=1`. The second does not start if the first exits non-zero.

The attempt is #461's `I461-win2/probeG03125b/dz0_pin3_D242.5459_a0.031250.npz` from the base
`I461-win2/probe03125/anm_pin3_D242.5146.npz` (read from the raw-data clone, not copied), `--mode=weak --k=4`.

| run | `--split_at` | frame of U and B | log, record |
|---|---|---|---|
| split_start | start | the LU at z0, before newton_od | split_start.log, split_start.json |
| split_after | after | the LU newton_od leaves at its last trial point (#499's, the control) | split_after.log, split_after.json |

Criteria (#675, each can fail), read from the line `weak residual / |B a| at z1 X, at z1 + dz Y`:

- split_after reproduces #499's line, X 0.517 and Y 0.384 (`I499-mac/wcorr_5146_a03125_weak_split.log`, line 16).
- split_start gives about 0.0044 at z1 and 0.0041 at z1 + dz, #528's figure in the start's frame, to 1e-2 of |B a|.

Stop conditions: an import error, a Traceback, or either check line missing. Each run took about 2.1 h on the Mac (#499).

| file | what |
|---|---|
| exits_675.txt | start and exit of each run |
