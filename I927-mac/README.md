# I927-mac: the low-D Taylor continuation in D, its predictions on fixed plans and the M 128 pilot

Machine: mac (Apple M5, shared; one process, 4 threads, nice 10). Issue https://github.com/nmoinvaz/choptuik-large-d/issues/927.
Code: branch `wip/sa-927` of choptuik-large-d (`hp/lowD_fixed_plan.py`, `hp/anm_lowd_pilot.py`), design in
notes/LOW_D_ANM.md there. Python: `/Users/nathan/venv-314` (hpkernel built 2026-11-08, `residual_jet` at every M).

## 1. The series at D 3.175, M 128 (`series_D3.175_M128.log`)

`measure_series.py` (a scratch script, kept here): the stored lowD_highM.py state
`hp/data/lowD_states/lowDhm_x0.000625-0.9_D3.1750_M128.npz` of the code repository (618-step plan), its f64 LU
(`newton_mixed`, 257 s) and `anm_lowd.coefficients` order by order. Stopped by hand after z_7 (the partial sums it
would have printed at the end were not needed). Max-norm ratios |z_(k-1)|/|z_k| for k = 2..7: 0.129, 0.185, 0.170,
0.220, 0.087, 0.019. GMRES converged at every order in 3-4 products; jets 37-60 s and solves 12-20 s per order.

## 2. Predictions on fixed plans at M 384 (`fixed_plan/`)

`hp/lowD_fixed_plan.py` with T135's stored series (`I798-win/probe/coeffs.npz`: z_0..z_3 at T105-win2's M 384 `p1`
state at D 3.04375, on that state's stored 8319-step plan), no Jacobian. Criteria, fixed before the run:

1. Reproduction: at D 3.04335 the partial sum of order 3 lies 3.18e-6 (max) and 1.65e-10 (Delta) from I343-win2's
   converged M 384 state (computed on the Mac before the run); the run must print the same to three digits.
2. Control: `--mutate drop2` must move the Delta difference of orders 2 and 3 at 3.04335 to about +8.8e-6 (the size of
   z_2's term, Delta_2 h^2 = -55.18 x 1.6e-7).
3. The question, at D 3.04315 (where #343's leg 2 found its Lagrange predictor's |F| NaN at M 320 and the fallback from
   the last state stalled): the residuals of the partial sums of orders 1 and 3 and of the Lagrange predictor through
   I343's three M 384 states, each on the base's plan (T105's, 8319 steps) and on the stored plan of I343's converged
   state at 3.04335 (8090 steps, the plan the leg would reuse there; lowD_highM.py itself re-plans that state at 1e-32).
   Reading: a finite |F| of order 3 where the Lagrange predictor's is not finite means that the series gives a start
   where the leg had none (a start, not a solve). Order 3 not finite on both plans means the series meets the same
   obstacle.

Results. 1: `fixed_plan/agree.log` prints 3.18e-06 and +1.65e-10 for order 3 at 3.04335: PASS. 2:
`fixed_plan/agree_drop2.log` prints +8.86e-06 and +8.83e-06 for orders 2 and 3 there: the control fires. 3
(`fixed_plan/d304315.log`, 23:30-00:03 UTC, 5-7 min per residual under a load of 30-50):

| D 3.04315 (h -0.0006) | base's plan (8319 steps) | 3.04335 state's plan (8090 steps) |
|---|---|---|
| order 3 | nan | nan |
| order 1 | nan | nan |
| Lagrange through 3.04375, 3.04355, 3.04335 | nan | nan |

The series meets the same obstacle as the Lagrange predictor (#343 at M 320), on both plans.

Probe 2 (`run_probe2.sh`), written after probe 1's first line (order 3 at 3.04315: |F| nan on both plans), as its
controls. (a) `onset`: the order-3 sum at 3.04335, 3.04325 and (for the segments) 3.04315 on the base's plan; at
3.04335, where the leg converged,
it must be finite, or the fixed-plan evaluation itself is broken and probe 1 is not read. (b) `last_state`: at 3.04315
on the 3.04335 state's plan, the series' base state (order 0) and I343's converged 3.04335 state rounded to f64
(lowD_highM.py's "last state" start, which #343 found finite, 2.7e-2, at M 320); the latter must be finite here too,
or the evaluation at 3.04315 is broken. The probe now also records which row blocks (segments in x) are not finite.

## 3. The pilot at M 128 (#927 part 2; `ref/`, `pilot/`)

Fixed before the runs. Base: lowD_highM.py's converged state `lowDhm_x0.000625-0.9_D3.1500_M128.npz` (17 nodes
0.000625..0.9, kc 100, ks 250, |F| 4.9e-29; `hp/data/lowD_states/` of the code repository, a copy in `inputs/`).

- References (`ref/`): `hp/lowD_highM.py --start_w <D3.1500_M128> --start_n <D3.1500_M160> --Ms 128,160 --dD 0.001
  --D_end 3.1476 --diff_max 1 --tag lowD927 --threads 4`, so lowD_highM.py itself solves D 3.149 and 3.148 at M 128 and
  160 (`--diff_max 1` keeps it from moving up to M 192, which is not the pilot's business). Each run under about 30 min,
  continued with `--resume`.
- Step 1: `hp/anm_lowd_pilot.py --state <D3.1500_M128> --target 3.149 --ref <ref's 3.149 M 128> --N 6`. Step 2: from
  step 1's corrected state to 3.148 against the ref's 3.148 M 128 state, N 6.
- Pass, per step: (A) |Delta(prediction) - Delta(ref)| <= 1e-12 and (B) the corrector converged (|F| < 1e-26) and
  |Delta(corrected) - Delta(ref)| <= 1e-12. Expected: the series' radius at D 3.15 about 0.1-0.15 (the ratios of
  section 1), so h/R <= 0.01 and the order-6 truncation in Delta about 4.4e-3 x 0.01^6 = 4e-15.
- Controls, from step 1's base, each must exit 1 with the check failed: `--mutate drop2` (z_2 left out: (A) fails by
  about |Delta_2| h^2), `--mutate kappa` (the jets with kappa's n frozen: a wrong dDelta/dD, (A) fails), `--mutate dshift
  --stop_on_fail 0` (the step to D + 1e-9: (A) and (B) fail by about dDelta/dD x 1e-9 = 4e-9).

**Amendment, 2026-11-17 01:00 UTC, before any pilot or reference run.** The Mac's load rose to 100-137 (others' work),
and an M 128 Jacobian took 257 s at a load of 22, so the M 128/160 references and pilot would take many hours. The
pilot runs first at the smallest M where lowD_highM.py has a stored pair at low D: `lowDv_D3.7000_M48.npz` and
`_M64.npz` (13 nodes 0.005..0.8, kc 100, ks 250; `inputs/`). References in `ref48/` (`run_ref.sh`, default `PAIR=48`:
`--Ms 48,64 --dD 0.005 --D_end 3.6876`, so lowD_highM.py solves D 3.695 and 3.69), pilot in `pilot48/` (`run_pilot.sh
step1|controls|step2`), N 6, steps of 0.005. Criteria (A), (B) and the three controls as above, unchanged. Expected:
the radius about D - 3 = 0.7, so h/R about 0.007 and the order-6 truncation far below 1e-12. Near Delta's maximum
(D 3.7557) dDelta/dD is only about 0.06 at 3.7, so dshift moves Delta by about 6e-11, still 60 times the bound; drop2
moves it by about |Delta_2| h^2 = 0.5 x 2.5e-5. The M 128 design above
stays as written (`PAIR=128`), for a quieter machine.

References (`ref48/leg.log`): lowD_highM.py solved D 3.695 at M 48 (two passes, |F| 3.5e-31 on its 63-step pass-2
plan, Delta 3.4648947264004986) and M 64 (Delta 3.4648937501254804; M 48 -> 64: -9.76e-7), then stopped on its own
--hours 0.5 rule before 3.69. For step 2 a second lowD_highM.py run starts from that converged 3.695 pair to 3.69
(`run_step2.sh`, `ref48b/`), written before it ran; step 2 is then checked against its M 48 state.

Step 1 (`pilot48/step1.log`, 01:41-01:46 UTC): PASS. Plan 63 steps, base |F| 3.7e-30, ratios |z_(k-1)|/|z_k| 0.46,
0.54, 0.56, 0.75, 0.84, every order's GMRES converged in 4 products.

| n | max \|P_n - ref\| | Delta(P_n) - Delta(ref) |
|---|---|---|
| 0 | 2.60e-1 | +3.07e-4 |
| 1 | 2.79e-3 | +1.46e-5 |
| 2 | 2.61e-5 | +9.23e-8 |
| 3 | 2.31e-7 | +4.89e-10 |
| 4 | 1.54e-9 | +2.56e-12 |
| 5 | 9.14e-12 | +1.46e-14 |
| 6 | 1.03e-13 | +8.74e-17 |

(A) 8.74e-17 <= 1e-12. The prediction's |F| on the fixed plan is 1.10e-13 (the base state's there 3.67e-3). The
corrector converged in 3 calls with full steps to |F| 1.44e-30; (B) |Delta - Delta(ref)| = 3.06e-30 <= 1e-12.

Controls (`pilot48/drop2.log`, `kappa.log`, `dshift.log`; `pilot48/exits.txt`), each exit 1 as required:

| control | Delta(P_6) - Delta(ref) | (A) | corrector | (B) |
|---|---|---|---|---|
| drop2 (z_2 left out) | +1.45e-5 | FAIL | not run | |
| kappa (kappa's n frozen in the jets) | -2.31e-2 | FAIL | not run | |
| dshift (the step to D + 1e-9) | +6.43e-11 | FAIL | converged, \|F\| 1.37e-30 | FAIL, +6.43e-11 |

Under kappa the ratios |z_(k-1)|/|z_k| become 0.21, 0.067, 0.26, 0.086, 0.0083 (the plain run's are 0.46-0.84), and
z_1's max norm 80.7 where the plain one is 51.5.

Second reference (`ref48b/leg.log`): lowD_highM.py from the converged 3.695 pair solved D 3.69 at M 48 (|F| 1.3e-30 on
its 63-step pass-2 plan, Delta 3.464558395113743) and M 64 (M 48 -> 64: -1.03e-6), then reached its grid's end.

Step 2 (`pilot48/step2.log`, from step 1's corrected state at 3.695 to 3.69, 02:21-02:27 UTC): PASS. Plan 64 steps,
ratios 0.47, 0.53, 0.57, 0.75, 0.83; partial sums n = 0..6 at Delta(P_n) - Delta(ref) +3.36e-4, +1.49e-5, +9.43e-8,
+5.02e-10, +2.65e-12, +1.53e-14, +9.03e-17 (max |P_n - ref| 2.66e-1 down to 1.10e-13). (A) 9.03e-17; prediction |F|
1.16e-13 on the fixed plan (the base state's 3.72e-3); the corrector converged in 3 calls with full steps to 4.1e-30;
(B) 3.51e-30.

## 4. Recommended tasks (for the coordinator)

1. **Low-D: the Taylor series as a start in lowD_highM.py.** What: notes/LOW_D_ANM.md section 5 (branch `wip/sa-927`):
   `lowD_dd.solve_point` returns its Solver (its LU is already at the converged state); `lowD_highM.py --predictor anm
   --anm_N 3` adds the start ("anm", the order-N sum) for M_w, evaluated on the last M_w solve's plan, and records the
   series' ratios and a_max; controls `--anm_mutate freeze|drop2`. Why: where starts are finite the series is 7000 times
   closer than the Lagrange predictor (D 3.04335, M 384), and in the M 48 pilot Newton converged from it in 3 full steps;
   about 2x fewer M_w Newton calls estimated. Acceptance: T107 A's M 48 smoke test (D 4 -> 3.99, 3.98) reaches both
   targets from the anm start; with `freeze` the anm start's |F| equals the last state's to 1e-12 relative; with
   `drop2` it is at least 10 times the plain anm start's; one M 320 point above D 3.0434 takes fewer M_w Newton calls
   than its Lagrange-start record. Depends on: #927, and #926 (below D 3.0433 it only helps with a projection).
   Estimate: a day of Python (coordinator), one M 320 point on a runner.
2. **The M 128 pilot at D 3.15 on a quieter machine** (optional). What: `PAIR=128 HOURS=1 bash run_ref.sh`, then
   `PAIR=128 bash run_pilot.sh step1` and `controls`, from this folder. Why: the pilot ran at M 48, D 3.7 under load;
   M 128 at 3.15 is nearer the low-D trouble (radius about 0.15, pollution from order 6). Acceptance: (A) and (B) at most
   1e-12 at step 1, each control exit 1. Depends on: #927. Estimate: 2 h on a quiet Mac.

Input for #926 (no new task): on fixed plans the predicted states fail from D 3.04325 on (order-3 sum from 3.04375,
h -0.0005), in the segment x 0.01 -> 0.02; at 3.04335 the same sum is finite (|F| 1.33e-6); the series' base state is
finite at 3.04315 (8.1e-2) where the nearer predictions are not.
