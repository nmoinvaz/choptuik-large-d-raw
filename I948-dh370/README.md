# I948-dh370: a ks ladder of base polishes at D 232.0 (up 240 to 320 converged, down 230 and 235 capped) and near_null reads, order 240 is converged for the Δ mode

Machine dh370 (Fedora 45, i7-8700, 12 threads). Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/948

Worktree `~/Source/choptuik-large-d-935` at main 808b1fac with its `.venv` (hpkernel, multidouble crate 4.8.2), the build of #941. Runs 2026-11-17 22:17 to
2026-11-18 04:04 UTC, nice 10, as systemd user units (`i948u` up, `i948d` and `i948f` down, `i948s` near_null scheduler, `i948c` cap watcher).

## What ran

Base polishes at D 232.0, each rung from the base before it: `anm_run.py R OUT --state <previous base> --ks K --keep_plan 0 --steps 0 --save_base 1`
with the flags of `I903-win2/run_ks_chain.sh` (`--threads` changed, `--D_max 400` added). A rung's directory holds only
`base_pin3_D232.0000.npz`. The first rung's state is `I903-win2/ks_chain/leg07_D222.0000_ks240/anm_pin3_D232.0000.npz`.
Then `near_null.py R <base> --k=6 --its=16 --json=...` on every converged base (2 or 4 threads).

| rung | from | threads | wall (s) | iterations | first step \|dz\| | final max\|F\| |
|---|---|---|---|---|---|---|
| up 240 (control) | the state | 6 | 2011 | 3 | 2.75e-25 (the plan's floor) | 7.78e-88 |
| up 250 | 240 rung | 6 | 3962 | 7 | 4.69e-17 | 3.29e-88 |
| up 260 | 250 | 6 | 3418 | 3 | 2.27e-19 | 4.11e-69 |
| up 270 | 260 | 6 | 5054 | 3 | 3.27e-20 | 8.74e-81 |
| up 280 | 270 | 6 | 1913 | 3 | 9.77e-22 | 1.48e-88 |
| up 300 (+20) | 280 | 6 | 2098 | 3 | 1.53e-23 | 6.89e-88 |
| up 320 (+20) | 300 | 6 | 1882 | 3 | 1.24e-24 | 2.29e-88 |
| down 230 (−10) | the state | 4 | 7263, capped | 1 | 1.40e-15 | not reached: last accepted state 6.39e-26 to 2.12e-11, lam 1/8; trials lam 1, 1/2, 1/4, 1/8 refused at 1.8e8, 4.7e7, 1.5e7, 6.8e6 |
| down 235 (−5) | the state | 4 | 7208, capped | 2 | 2.51e-16 | not reached: iteration 1 2.04e-14 to 2.56e-20, lam 1/4, \|dz\| 1.88e-16 to 1.41e-16; iteration 2's trial lam 1 refused at 5.8e6 |

The caps (the coordinator's amendment on #948): 2 h for a down rung, 3 h for an up rung, killed by `cap948.sh`, which polls every 30 s. The 230 rung's cap
fired at 7262 s (the first version's `sed` did not extract the rung's directory, so it was fixed after 7200 s), the 235 rung's at 7208 s. A capped −5 rung stops
the down ladder, so no −2 rung was run and the down ladder has no near_null reads. Wall times depend on the load (up 270 ran with the down ladder and two reads,
load 10, 5054 s; 280 to 320 ran at load 5 to 6, 1882 to 2098 s).

## Results (`analysis948.log`, `delta948_control.log`)

| ks | σ_Δ | σ_Δ(K)/σ_Δ(240) − 1 | σ_pair (geometric mean of the two members) | σ₂ | σ₅ | Δ(K) − Δ(240 rung) |
|---|---|---|---|---|---|---|
| 240 | 5.2769245118e-15 | 0 | 2.9442e-10 | 2.172e-14 | 2.40e-06 | 0 (floor 2.7544e-25) |
| 250 | 5.2769245047e-15 | −1.34e-9 | 2.9440e-10 | 2.172e-14 | 1.43e-06 | 4.685242e-17 |
| 260 | 5.2769245045e-15 | −1.39e-9 | 2.9440e-10 | 2.172e-14 | 3.54e-06 | 4.696103e-17 |
| 270 | 5.2769245045e-15 | −1.40e-9 | 2.9440e-10 | 2.172e-14 | 2.50e-06 | 4.692831e-17 |
| 280 | 5.2769245045e-15 | −1.40e-9 | 2.9440e-10 | 2.172e-14 | 2.74e-06 | 4.692733e-17 |
| 300 | 5.2769245045e-15 | −1.40e-9 | 2.9440e-10 | 2.172e-14 | 4.01e-06 | 4.692732e-17 |
| 320 | 5.2769245045e-15 | −1.40e-9 | 2.9440e-10 | 2.172e-14 | 2.28e-06 | 4.692732e-17 |

The Δ mode is vector 1 at every rung (Δ share 0.913), the harmonic-3 pair vectors 3 and 4 (members 2.918e-10 and 2.970e-10, convergence 5e-4 and 6e-4).
σ₅ is not converged in any read (relative change over the last iterations 0.05 to 1), so its wander is the read's, not the order's.
D 222.0 (no solves, `near_D222_ks*.json`): ks 160 σ_Δ 3.3501e-13, pair 2.3613e-12, σ₅ 1.67e-06; ks 230 σ_Δ 3.3528e-13, pair 2.8331e-10, σ₅ 1.34e-04
(Δ vector 1 both, shares 0.830 and 0.832). The ks 240 read at D 222 is missing: leg 7's base polish at D 222 is not stored, and no rung was ordered to make it.

Verdict by the issue's rule: σ_Δ at 280, 300 and 320 is within 1.4e-9 of the 240 rung's (rule: within 10%), so order 240 is converged for the Δ mode at D 232.

## Controls

| control | result |
|---|---|
| the 240 rung reproduces #941's σ_Δ 5.2769e-15 within 1% | 0.000%, pass |
| the 240 rung's Δ against the state's, the plan's floor at most 3e-25 | 2.7544e-25, pass (`delta948_control.log`, exit 0); `--mutate` adds 1e-20 and fails (`delta948_mutate.log`, exit 1) |
| `check948.py` (converged, max\|F\| ≤ 1e-60, ks as asked) | the 240 rung passes (`check948_pass.log`); `--mutate` reads max\|F\| as 1e-50 and fails (`check948_mutate.log`); asked ks 250 on the 240 rung fails (`check948_wrongK.log`) |
| `analyze948.py --selftest` (planted records with known answers) | exit 0 (`selftest948.log`); `--mutate` swaps the expected σ_Δ and σ_pair, exit 1 (`selftest948_mutate.log`) |
| near_null `--planted=1` passes and `--mutate=scale_block` fails on this build | not rerun here, the same build 808b1fac in `I941-dh370/` (`ctl_planted.log` exit 0, `ctl_planted_mut.log` exit 1, `--mutate=sigma` exit 1) |

## Files

- `run948.sh` (stages `up`, `down`, `near`), `run948_down2.sh` (the −5 and −2 fallback), `cap948.sh`, `caprep948.py`, `check948.py`, `near948.sh`, `delta948.py`, `analyze948.py`
- `exits_948.txt` (every start, exit and cap), `up_K*_from*.log/.check`, `down_K*_from*.log/.check/.capped`, `up_K*/` and `down_K*/` (`base_pin3_D232.0000.npz`)
- `near_up_K*_from*.json/.log/.started`, `near_D222_ks160.*`, `near_D222_ks230.*`, `near_early_up_K240_from240.*` (the 240 rung's first read at 2 threads, a copy, not used by `analyze948.py`)
- `analysis948.log`, `delta948_control.log`, `delta948_mutate.log`, `check948_*.log`, `selftest948*.log`
