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

## Stage 1 stopped at call 4; the 1e-27 bar replaced by the floor reading (2026-11-19 19:46 UTC)

Coordinator's hc (2026-11-19, after my report): stop call 5 by exact pid and run stage 2 from the call-4 checkpoint. The state is at the residual's evaluation floor (measured max|F| 1.420e-27), so call 5 cannot pass 1e-27, and Δ's own Newton correction there (dΔ +1.44e-29 at call 4, |dz| 8.41e-22) is about twenty orders below Δ(320) − Δ(256) = -1.9479e-9, which stage 2 compares at 1e-3 relative. The 1e-27 bar of criterion 1 is replaced by this floor reading, as on #945. Criterion 1 is therefore not met as written and is accepted as the floor reading by the coordinator's decision.

- Call 5 was stopped at 2026-11-19 19:46 UTC by exact pid 574646 (its wrapper 574645 and `run1014.sh` ended with it: `stage 1 exit 143 wall 40495 s`, `exits_1014.txt`). No call-5 state exists; the live checkpoint was the call-4 one (cmp-equal to `states/lowD1014_D3.0475_M320_ckpt_after_call4.npz`).
- The M 320 state for stage 2 is `states/lowD1014_D3.0475_M320.npz`, a copy of that checkpoint (cmp-equal). It was not written by a converged `lowD_dd.py` run, so its meta has no `converged` record. `m320.jsonl` has no final record either.
- `stage2_1014.sh` is `run1014.sh`'s stage 2 lines unchanged (the command, the series saved before the target stage, the 30-minute rule by exact pid), started by hand.

## Stage 2 and the Δ_k comparison (2026-11-20 00:5x UTC)

Stage 2 ran from the call-4 checkpoint (`stage2_1014.sh`, started 2026-11-19 19:46:18 UTC): base |F| 1.42e-27 (anm_lowd's own residual, equal to `resid1014.py`'s 1.420e-27), pivots 5.0e-05 to 4.5e+01, base 9294 s, orders 1 to 12 at about 9 to 16 min each (z_1 to z_12 converged, 3 to 4 products), **series saved 2026-11-20 00:48:41 UTC** (`series_D3.0475_M320_N12.npz`, `exits_1014.txt`). The control (dimension frozen) fires: |[F]_1| 0.00e+00, a ratio of 0.0 to the real one (criterion: below 1e-10). The target stage (D 3.0474, h -1e-4) printed `|F| of the prediction 6.69e-08 on its own plan (4713 steps)` and went on; the 30-minute rule from the save is in `stage2_1014.sh` (stop by exact pid at 01:18:41 UTC), see `exits_1014.txt` for what it did.

`compare1014.py` (output `compare1014.log`): Δ_k = delta_hi + delta_lo (math.fsum) of the M 320 series and of dh610's M 256 series (first 13 orders), relative difference (D320 − D256)/|D256|. Control, written first: M 256 against itself reads 0 at every order, and a copy with order 5 scaled by 1 + 1e-4 reads 1.000e-04 at order 5 and 0 elsewhere (pass); `--mutate` scales order 5 of the M 320 series by 1 + 1e-4 and the real table changes at order 5 only, by +1.000e-04 (pass).

| k | Δ_k (M 320) | Δ_k (M 256) | rel. diff | Δ_k/Δ_k−1 (320) | (256) |
|---|---|---|---|---|---|
| 0 | 2.4660121465594229 | 2.4660121485072883 | −7.9e-10 | | |
| 1 | 7.68772945961 | 7.68772905089 | +5.3e-08 | +3.117 | +3.117 |
| 2 | −49.7609136392 | −49.7608661147 | −9.6e-07 | −6.473 | −6.473 |
| 3 | 440.846130796 | 440.842450357 | +8.3e-06 | −8.859 | −8.859 |
| 4 | −4991.04327229 | −4990.83627145 | −4.1e-05 | −11.32 | −11.32 |
| 5 | 64108.6182181 | 64101.8583028 | +1.06e-04 | −12.84 | −12.84 |
| 6 | −881999.402027 | −878678.506999 | −3.8e-03 | −13.76 | −13.71 |
| 7 | 1.26268e+07 | 1.37571e+08 | −0.91 | −14.32 | −156.6 |
| 8 | −9.75505e+08 | −1.33606e+13 | +1.000 | −77.3 | −9.7e+04 |
| 9 | 4.45784e+13 | −1.13306e+18 | +1.000 | −4.6e+04 | +8.5e+04 |
| 10 | 1.00499e+19 | 9.27586e+22 | −1.000 | +2.3e+05 | −8.2e+04 |
| 11 | −4.12102e+23 | 6.60535e+27 | −1.000 | −4.1e+04 | +7.1e+04 |
| 12 | −8.40592e+28 | −4.44932e+32 | +1.000 | +2.0e+05 | −6.7e+04 |

Reading (mine, not a verdict): orders 0 to 5 agree to 1.1e-4 or better, the relative difference growing about ×10 to ×50 per order; order 6 differs by 3.8e-3, above the 1e-3 of criterion 3, so **orders 3 to 6 do not all agree to 1e-3** (order 6 is 3.8 times over). Orders 7 and up are not the same series at the two M. The ratio Δ_k/Δ_k−1 follows one smooth sequence (3.12, 6.47, 8.86, 11.3, 12.8, 13.7) at both M, continues at M 320 to −14.32 at k = 7 and breaks at k = 8 (−77); at M 256 it breaks at k = 7 (−157). The full-vector radii |z_k−1|/|z_k| fall to 1e-5 from order 5 (printed by the control line in `stage2.log`). Whether D* 2.994 stands is the coordinator's rerun of `hp/series_singularity.py`.

Discrepancy still open from stage 1 (reported, not fixed): the M 320 state's max|F| is 1.42e-27 (the residual's floor), above criterion 1's 1e-27; the coordinator replaced the bar by the floor reading (above).

## T82-win's stored states against mine, found 2026-11-20 about 01:00 UTC (before the M 384 run)

Measured with `resid1014.py` (one state per call, cwd outside the folder so `resid1014.json` is not overwritten; `resid_T82_M320_M384.log`, `resid_T82_M320.json`, `resid_T82_M384.json`), each state at its own stored step plan; the planted +1e-20 control reads 1.000e-20 on both (the check can fail).

| state | step plan | max\|F\| | Δ (hi, lo) |
|---|---|---|---|
| mine, after call 4 (`states/lowD1014_D3.0475_M320.npz`) | 4388 steps | 1.420e-27 | 2.466012146559423, −7.12758549185511e-17 |
| T82-win `lowDhm_..._D3.0475_M320.npz` | 1619 steps | **9.557e-29** | 2.466012146559423, −7.12758549186122e-17 |
| T82-win `..._M256.npz` (plan only) | 1557 steps | not measured | |
| T82-win `..._M384.npz` | 1623 steps | 1.369e-28 | 2.466012146521712, +3.14906e-17 |

- Δ of T82-win's M 320 state and of mine agree to 6.1e-29 although the plans differ (1619 against 4388 steps) and the residuals differ (9.6e-29 against 1.4e-27). The vectors differ by at most 2.6e-14 (index 302 of 28161, max|z| 634). This supports the floor-reading decision (Δ's Newton correction is far below the M-to-M differences), and is independent of the floor argument.
- Discrepancy (reported, not explained): the "evaluation floor" 1.42e-27 is the reading at my 4388-step plan only. T82-win's M 320 state reads 9.6e-29 on its 1619-step plan with the same evaluator, 15 times lower. The floor depends on the state or plan; I did not test which (evaluating one state on the other's plan mixes in the two plans' discretization, so it is no clean test).
- Plan confound for the M-to-M comparisons: the M 256 series (dh610) starts from T82-win's M 256 state (1557 steps) and the M 384 series from T82-win's M 384 state (1623 steps), but my M 320 series starts from my own state (4388 steps). T82-win's own M 320 state (1619 steps, 9.6e-29) was not used for a series. Δ_(384) − Δ_(320) = −3.8e-11 (from the stored states), against −1.95e-9 for 320 − 256.

## Stage 2's target stage stopped; stage 3 (M 384 series) started (2026-11-20 01:18 UTC)

- Stage 2 (M 320 series from my lifted state): the target stage (D 3.0474, prediction |F| 6.69e-08 on its 4713-step plan) ran 30 min after the series was saved (00:48:41 UTC) and was stopped by exact pid 728678 (wrapper 728676) at 01:18:42 UTC, `stage 2 exit 143 wall 19944 s` (`exits_1014.txt`). It printed no Newton line before the stop. No target-stage state exists.
- Stage 3 (coordinator's order, issue comment 2026-11-20 00:52 UTC): `stage3_1014.sh` started 01:18:51 UTC from T82-win's stored M 384 state (plan 1623 steps, max|F| 1.369e-28 measured above): `anm_lowd.py RAW RAW/I1014-dh170/series384 --state .../T82-win/states/lowDhm_x0.000157-0.975_D3.0475_M384.npz --N 12 --checks "" --target 3.0474 --threads 6 --save_series series_D3.0475_M384_N12.npz` at nice 10, log `stage3.log`. Caps by exact pid: 30 min on the target stage after the series is saved, and 10 h of wall time for the whole run. Pids: script 781837, `/usr/bin/time` 783329, python 783331. Forecast about 8.5 to 9 h (base about 4.5 h, then 12 orders about 4 h; M 320 took 9294 s and 8849 s).
- Stage 4 (coordinator's order, hc about 01:05 UTC): `launch4_1014.sh` starts `stage4_1014.sh` (the same command from T82-win's own M 320 state, series `series_D3.0475_M320t82_N12.npz`, same caps) when stage 3's exit line is in `exits_1014.txt`.
- The comparison across M 256, M 320 (T82-win's state), M 384 and my lifted M 320 is `compare4_1014.py` (controls first, `--mutate`), run when the series exist.

## Stage 3 (M 384 from T82-win's stored state): not converging (2026-11-20 04:05 UTC)

Base done 03:13:27 UTC (6876 s, 1623 steps, max|F| 1.4e-28 = my `resid1014.py` 1.369e-28), smallest pivot **2.8e-10** (largest 5.1e+01), against 6.5e-05 for dh610's M 256 series (1557 steps) and 5.0e-05 for my M 320 (4388 steps). Orders 1 and 2 stopped at the 40-product cap (`converged False`): |z_1| 1.48e9, |z_2| 3.5e20, against 1.255e4 and 2.18e5 (M 256) and 1.253e4 and 2.30e5 (my M 320), which converged in 4 products. Each order takes about 19 min (178 s jets, 960 s solve), so the series file is expected about 07:00 UTC; the run goes on until the coordinator says otherwise (reported on #1014, comment 7030064560, and by hc). Not explained: whether the nearly singular block comes from M 384, from T82-win's 1623-step plan or from the state itself. In the two finished series' `anm_lowd.jsonl` the full vectors also leave the smooth growth (17 to 21 per order for z_1 to z_4, extrapolating to about 1.9e9 for |z_5|) at order 5: |z_5| is 5.59e9 (my M 320) and 6.75e11 (M 256), whose bearing on the order-6 difference is open.

## Stage 3 stopped, recorded as unconverged; stage 4 started (2026-11-20 04:05 UTC, coordinator's hc)

- **Stage 3 (M 384 series from T82-win's stored M 384 state): UNCONVERGED, stopped by exact pid on the coordinator's order.** Python 783331 and its `/usr/bin/time` wrapper 783329 were killed (TERM) at 04:05:46 UTC (`stage 3 exit 143 wall 10015 s`, `exits_1014.txt`; the hc arrived about 04:05, the line there that says "about 04:06" is a few seconds off). Run for 02 h 47 min, 6876 s of it the base. The data that make it unconverged: base smallest pivot **2.8e-10** (against 6.5e-05 for M 256 and 5.0e-05 for my M 320), z_1 and z_2 at the 40-product cap (`converged False`), |z_1| 1.48e9 against 1.25e4. No series file exists and **its Δ_k are not used**. The target stage was never reached.
- Coordinator's verdict on the z_5 question (hc): M 256's |z_5| of 6.8e11, 350 times off the smooth trend, means M 256's order 6 cannot be trusted, so the 3.8e-3 order-6 mismatch between M 256 and M 320 is not evidence either way, and the withdrawal of the D* 2.994 reading stands under the fixed rule.
- **Stage 4 (series from T82-win's own M 320 state, 1619-step plan, same flags): started 04:06:09 UTC** by `launch4_1014.sh` (script pid 782021, wrapper 810246, python 810248), 6 threads at nice 10, caps by exact pid (30 min on the target stage, 10 h for the run). Its base smallest pivot is to be posted as soon as it is printed: near 5e-5 means the 2.8e-10 pivot belongs to M 384, near 1e-10 means it belongs to T82-win's plan. It measures the plan's share against my lifted M 320 (4388 steps), as planned. The hp rebuild follows stage 4 (expected about 3 h earlier than before).

## Stage 4's base (2026-11-20 05:10 UTC; posted on #1014, comment 7031067584)

T82-win's own M 320 state (plan 1619 steps): base max|F| 9.6e-29 (equals `resid1014.py`'s 9.557e-29), smallest pivot **1.8e-11**, largest 45, base 3840 s. With T82-win's M 384 (2.8e-10, 1623 steps) it is far from my lifted M 320 (5.0e-05, 4388 steps) and from T82-win's M 256 (6.5e-05, 1557 steps). By the coordinator's rule (near 5e-5: the small pivot belongs to M 384; near 1e-10: to T82's plan) the small pivot belongs to T82-win's plan or state, not to M 384. Not only the plan size: M 256 on 1557 steps is fine. Not tested: plan, state or build. Stage 4's order 1 is the next thing to read (a 40-product cap there would make this series unusable like M 384's).

## Stage 4 stopped, recorded as unconverged (2026-11-20 05:26 UTC, the coordinator's rule of 05:12)

Stage 4 (series from T82-win's own M 320 state, 1619-step plan) printed `z_1: |z| 1.024e+08, |rhs| 1.20e+02, 40 products, converged False, 134 + 680 s` at 05:26 UTC (the base: |F| 9.6e-29, smallest pivot 1.8e-11, 3840 s). z_1 is at the 40-product cap, as M 384's was, so by the coordinator's rule I stopped it by exact pid (python 810248 and its wrapper 810246, TERM, `stage 4 exit 143 wall 4832 s`, 05:26:41 UTC, `exits_1014.txt`). No series file exists and its Δ_k are not used. |z_1| is 1.02e8 against 1.25e4 at dh610's M 256 and at my M 320. So T82-win's family cannot test the rule: only its M 256 converges, and its order 6 is untrusted.
`plan_resid1014.py` (`plan_resid1014.log`) measures how T82-win's states stand on the planner's own plan (tol_step 1e-32, hmax 0.05, the one my lifted M 320 uses) for the proposal of a lifted M 384 pair (cost and its first Newton start).

### `plan_resid1014.py` (2026-11-20 05:27 to 05:29 UTC, 3 threads, `plan_resid1014.log`), for the cost of a lifted M 384

| state | stored plan | planner's own plan (tol_step 1e-32, hmax 0.05) | my 4388-step plan |
|---|---|---|---|
| mine, M 320 after call 4 | 4388 steps, 1.420e-27 | **1820 steps, 1.420e-27** | (is its plan) |
| T82-win M 320 | 1619 steps, 9.557e-29 | 2392 steps, **2.425e-21** | 2.425e-21 |
| T82-win M 384 | 1623 steps, 1.369e-28 | 2638 steps, **2.252e-22** | |

Planted +1e-20 on my state reads 1.000e-20 (the check can fail). Controls as written before the runs: the stored-plan reading of my state reproduces 1.420e-27 (pass); the prediction that the planner would reproduce my 4388-step plan **failed**: on the converged state it gives 1820 steps. So my M 320 lift's 4388 steps came from planning on the unconverged lifted start vector, and a converged state needs 2.4 times fewer.
Readings: (1) my state's max|F| is 1.420e-27 on 1820 and on 4388 steps alike, so the 1.42e-27 is not a property of the plan; (2) T82-win's states are solutions of their coarse plans only: on a converged plan their residual is 2.4e-21 (M 320, on 2392 and on 4388 steps alike) and 2.3e-22 (M 384). That is the discrepancy with my earlier "floor depends on the plan" text, partly resolved: T82-win's 9.6e-29 is specific to its coarse plan, mine is the same on any plan; why mine is 1.42e-27 and not lower is still not explained.

## Steps C and B approved; rules fixed before the runs (coordinator's hc, 2026-11-20 about 05:31 UTC)

- **C** (started 05:33:07 UTC, `stage5_1014.sh`; script 823727, wrapper 823730, python 823732): the series (N 12, `--checks ""`, `--target 3.0474`, 6 threads, 30-minute rule on the target stage, 10 h cap) from my lifted M 320 state re-planned to the planner's converged plan, `states/lowD1014_D3.0475_M320_plan1820.npz` (`make_plan1820_1014.py`: 1820 steps, max|F| 1.420e-27 as on the 4388-step plan, vector byte-identical to `lowD1014_D3.0475_M320.npz` (sha256 1acce203...), meta keys kept; its mutation (last unknown scaled by 1 + 1e-9) raises |F| to 9.0e-9 and fails, as it must). It runs the whole series, not only the base, because B's rule compares the two M on converged plans. **C's question, fixed:** if the base smallest pivot on the 1820-step plan is near 5e-5, the 1e-11 pivot of T82-win's M 320 and M 384 comes from their coarse-plan states, not from the step count; near 1e-11 it is the step count's or the state's. Its output is `series_D3.0475_M320p_N12.npz`.
- **B** (after C ends): `lowD_dd.py` to M 384 from T82-win's M 384 state on the planner's plan, then its series; fail-able criteria as in the proposal (comment 7031379312): final max|F| at the floor (my `resid1014.py` with its planted control), base smallest pivot above 1e-6 and z_1 converging in at most 6 products with |z_1| near 1.25e4, else stopped like M 384. **Rule for B, fixed before the runs:** the D* 2.994 reading is reinstated only if my lifted M 320 and the lifted M 384, both on the planner's converged plans, agree on orders 3 to 6 to 1e-3 relative; `hp/series_singularity.py` then reads D* from M 384. Otherwise the withdrawal stands.
- No hp rebuild on dh170 (the 29.4 GB peak leaves no margin on 31 GB). These runs need no new kernel, but their `t_jac` fields are the old LU-fill copy (#1040): **quote wall times only.**
