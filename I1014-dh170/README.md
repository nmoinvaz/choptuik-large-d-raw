# I1014-dh170: Δ's Taylor series at D 3.0475 at a second M (M 320), to test the D* 2.994 reading (#997)

Machine dh170 (Fedora 45, i7-7700, 4 cores / 8 threads, AVX2, 31 GB). Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1014 (coordinator's hc, 2026-11-19 about 08:25 UTC).

## Setup

- Worktree `~/Source/choptuik-large-d-1014` at origin/main 23844822; Python and hpkernel of `~/Source/choptuik-large-d-935/.venv` (4.8.2 build, **read only, nothing built**: #949's lanes import it). Both scripts, `hp/lowD_dd.py` and
  `hp/anm_lowd.py`, import against it (checked). 6 threads, nice 10. Beside it run #996's last 180-digit job (one core) and #949's idle near_null lanes.
- Inputs, the committed bytes of raw origin/main (`raw_commit.txt`), extracted into `~/scratch1014/raw`: T82-win's state `T82-win/states/lowDhm_x0.000157-0.975_D3.0475_M256.npz` (D 3.0475, M 256, 21 nodes, kt 36, kc 100, ks 250 in its meta)
  and dh610's M 256 series `I997-win2/series_D30475/series_D3.0475_M256_N20.npz`. Output goes to this folder of the live raw clone (`raw_out.py` requires a task folder of a raw checkout);
  `lowD_dd.py` writes its state to the worktree's `hp/data/lowD_states/` (the script's own place), copied here to `states/` right after.

## Runs and pass criteria, written before the first run

| # | run | pass |
|---|---|---|
| 1 | `lowD_dd.py m320.jsonl --start <M 256 state> --Ms 320 --nodes <the 21 nodes of its meta> --kt 36 --kcs 100 --ks 250 --jac f64 --tol 1e-29 --threads 6 --tag lowD1014` | converged = max\|F\| below 1e-27 (the issue's); Δ(320) − Δ(256) reported. A solve that does not reach the script's 1e-24 acceptance is saved as `*_fail.npz` and stops the task |
| 2 | `anm_lowd.py RAW series --state <the M 320 state> --N 12 --checks "" --target 3.0474 --threads 6 --save_series series_D3.0475_M320_N12.npz` | the series file is written (the saving comes before the target stage); the control (dimension frozen) fires, `ratio < 1e-10`; the target stage, if it runs more than 30 min after the series is saved, is stopped by exact pid |
| 3 | Δ_k at M 320 against M 256 (`I997-win2/series_D30475`) per order k = 0..12 | the relative difference per order reported; the coordinator reruns `hp/series_singularity.py` on the orders that agree to 1e-3 relative: orders 3 to 6 agreeing keeps the D 3.0475 reading at two M, otherwise it is withdrawn (not my call) |

Not done here, so not claimed: whether D* 2.994 stands (the coordinator's rerun of `series_singularity.py`).
