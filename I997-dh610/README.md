# I997-dh610: D 3.15 at M 256 from I927-mac's M 160 state, and Delta's Taylor series there (discovery candidate 6, step (a) at a second M)

Machine: dh610 (Fedora desktop, Linux 7.3, i7-12700, 20 threads, 62 GB). Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/997 (the coordinator's order of 2026-11-19 01:37 UTC, the last comment of #997 at the time).

Build: hp's Python from origin/main 459180e6 (worktree `~/Source/choptuik-large-d-997`, which adds `anm_lowd.py --save_series`) with #967's `.venv` kernel (origin/main d96a09a1; hp/src,
Cargo.* and build.sh are identical between the two commits). 12 threads, nice 10.
Input: `I927-mac/inputs/lowDhm_x0.000625-0.9_D3.1500_M160.npz` (raw origin/main 50c48773, blob 2515013d1ed2, sha1 874baa28f31e; extracted into `~/scratch997/raw`).
Its meta: D 3.15, M 160, 17 nodes 0.000625 ... 0.9, kt 36, kc 100, ks 250.

| file | what |
|---|---|
| `run997_m256.sh`, `common997.sh` | step 1, the solve at M 256 |
| `m256.jsonl`, `m256.log` | step 1's record and log (lowD_dd.py, the direct M 160 to M 256 lift) |
| `lowD997_D3.1500_M256.npz` | step 1's converged state (copied from `hp/data/lowD_states/` of the worktree, sha1 4407e801cb08) |
| `run997_series.sh`, `series/run.log`, `series_D3.15_M256_N20.npz` | step 2, the Taylor series at M 256 |
| `compare997.py`, `compare997.txt` | Delta_k of the saved series at M 256, M 160 and M 128 per order, with the partial sums at h = -0.01 (M 160 and M 128 files are win2b's `I997-win2/series/series_D3.15_M160_N20.npz` and `series_M128/series_D3.15_M128_N20.npz`, raw origin/main 012d465c) |

Step 2's anm_lowd process (pid 649398) wrote the series at 02:54 UTC and was still in its target-D 3.14 stage at 06:40 UTC (no "target" record in `series/anm_lowd.jsonl`).
