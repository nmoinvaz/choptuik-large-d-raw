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

## Newton calls (stage 1), measured 2026-11-19 19:45 UTC

Each call line of `stage1.log` prints the residual at the start of its step. `resid1014.py` (this folder; `resid1014.log`, `resid1014.json`) evaluates max|F| of a saved checkpoint at its own step plan, as `lowD_dd.py` does.

| call | printed start \|F\| | \|dz\| | dΔ | seconds | measured max\|F\| of the checkpoint after it |
|---|---|---|---|---|---|
| 1 | 7.99e-05 | 2.89e-01 | -7.57e-10 | 9424 | |
| 2 | 6.23e-09 | 2.95e-06 | -1.19e-09 | 9693 | |
| 3 | 1.20e-16 | 2.81e-11 | -9.66e-19 | 10760 | 2.216e-27 (`states/..._ckpt_after_call3.npz`) |
| 4 | 2.22e-27 | 8.41e-22 | +1.44e-29 | 9469 | **1.420e-27** (`states/..._ckpt_after_call4.npz`) |

Controls, written before the run: the after-call-3 checkpoint must give call 4's printed 2.22e-27 within 1%: it gives 2.216e-27 (pass). A planted 1e-20 in one low part of each state must raise max|F| above 1e-26: both give 1.0e-20 (pass, the check can fail).

Discrepancy with criterion 1 (reported, not fixed): the state after call 4 has max|F| = 1.42e-27, above the issue's 1e-27. The last step was |dz| 8.4e-22, so a step error of the f64 Jacobian (about 1e-11 of |dz|) could not leave 1e-27; the residual sits at its double-double evaluation floor (the code's own comment puts it at 2 to 4e-28 at M 256). Δ changed by +1.44e-29 in the last step: Δ(320) − Δ(256) = -1.9479e-9 at both checkpoints (Fraction difference of hi+lo). My forecast on #1014 that call 4 would print |F| ~1e-32 and end stage 1 was wrong (it assumed quadratic convergence below 1e-16). Call 5 (a further step of about 2.6 h) is running; the script's own acceptance is 1e-24, which the state meets. Whether to stop at the call-4 state is the coordinator's decision.
