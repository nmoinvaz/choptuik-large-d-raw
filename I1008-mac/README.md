# I1008-mac: the floor probe of #1008's arclength predictions, run by the coordinator on the Mac

Machine: Nathan's MacBook Air (M5, 10 cores), coordinator session t5. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1008

## floor1 (written 2026-11-20 15:24 UTC, before the run)

Question: where does the predicted max|F| floor of run2 (I1008-macm3, about 1e-36 at D 259.43-259.53 for every
arclength step a) come from? `anm_run.py --arclength 1 --arc_diag 2` (hp/arclength.py run_floor) at run2's arc step 7
state `I1008-macm3/run2/arc_002_D259.485823.npz`, not polished, with that base's series
`I1008-macm3/run2/arcjet_002_D259.485823.npz`, at a = 0, 1e-4, 1e-3 and 0.0138854375 (arc step 8's a): the predicted
max|F| before and after the re-seed, split into held rows and other rows. Flags: run2's (run_1008.sh F and ARC), with
--threads 4 --arc_diag 2. Kernel: a release-dev build of feat/exact-recip-1043 (hp at main a90d330e plus the off flag),
not macm3's, so bits may differ in the last places; the reading is about orders of magnitude.

Readings, fixed before the run:
1. Checks (each can fail; exit 1 if 1a or 1b fails):
   a. a = 0 before the re-seed is at the base's own level (<= 1e-60; arc step 7 converged at 1.94e-70).
   b. The control (w_1 times 1 + 1e-20 at a = 0.0138854375) raises max|F| before the re-seed by >= 100 times.
   c. At a = 0.0138854375 the max|F| after the re-seed is within a factor 3 of run2's logged 1.87e-36 (arc step 8's
      attempt). If not, the probe is not the run's prediction, and readings 2-4 are not made.
2. If max|F| after the re-seed is >= 1e-37 at a = 0 too, the re-seed itself puts the point at the floor.
3. If max|F| before the re-seed falls with a and is <= 1e-40 at a = 1e-4, while after the re-seed it stays near
   1e-36, the floor is the re-seed's.
4. If max|F| before the re-seed is near 1e-36 at every a > 0 but at the base's level at a = 0, the floor is in the
   prediction (the series' low orders, the held values off the base, or the move to double-double D). The held/other
   split says which rows.

## floor1 result, and floor2 (written 2026-11-20 15:40 UTC, before floor2 runs)

floor1 (floor1.log, floor1/arc_floor.json; a first try died on a TypeError in the probe's own report,
floor1_try1_typeerror.log): check 1b passed (the control raised max|F| to 2.9e16) and 1c passed (after the re-seed at
a = 0.0138854375: 1.87e-36, run2's logged value exactly). Check 1a FAILED: at a = 0 the held rows read 7.69e-38 (other
rows 1.94e-70). D is the same to 34 digits in the state, the series and the probe. Hypothesis: the held values are
taken relative to a run's first state, run2's was ab2/arc_001, and this probe's is arc step 7's state, so the held
rows carry the fit's offset between the two (run2's own base polish removed 4.37e-38 of the same kind at its start).
floor2 tests it: the same command with --floor_polish 1 (the base polished first), and the re-seed's octo-double rung
residuals logged. The hypothesis passes if the polished base reads <= 1e-60 in all rows and every after-re-seed max|F|
at a > 0 stays within a factor 3 of floor1's (7.78e-36, 1.06e-35, 1.87e-36); otherwise it fails and floor1's readings
are not made.

## floor2 result, and floor3 (written 2026-11-20 15:58 UTC, before floor3 runs)

floor2 (floor2.log): the polish took the base from 7.69e-38 to 1.17e-67 in 3 steps, and every after-re-seed max|F|
equals floor1's, so both written criteria hold. But the second holds trivially: the predictions are formed from the
series' own z_0, which the polish does not change, so floor2 did not test what it was meant to. The held-offset
hypothesis rests instead on the polish line and on floor1's 1.87e-36 equalling run2's logged value, where run2's base
has no such offset. New in floor2: the re-seed's octo-double rungs converge to 2e-71..7e-71 at every a. Rows: before
the re-seed the max is in rows 736-767 (the a_h horizon data's rows), linear in a; after it the max is in rows 96-98
and 126-127.

floor3: floor1's command, with the rows split three ways (held, the 2M rows at the horizon data's offsets 704-767,
the rest). Readings, fixed now:
1. Checks as floor1's 1b and 1c (control fires; 1.87e-36 after the re-seed at a = 0.0138854375 within a factor 3).
2. If the rest rows before the re-seed already read within a factor 3 of their after-re-seed value at each a > 0, the
   floor is in the prediction's non-horizon part, and the re-seed only uncovers it.
3. If the rest rows before the re-seed read <= 1e-38 at every a > 0 while after it they read >= 1e-36, the re-seed
   puts it there.
4. Anything else is reported as it is, with no reading.

## floor3 result, and floor4 (written 2026-11-20 16:08 UTC, before floor4 runs)

floor3 (floor3.log): checks 1b and 1c pass again (control 2.9e16; 1.87e-36 at a = 0.0138854375). Neither reading 2
nor 3 holds, so it is reported as it is. Before the re-seed every row group grows linearly in a (horizon 2.77e-31,
3.36e-30, 4.23e-29; rest 4.44e-32, 5.38e-31, 6.76e-30 at a = 1e-4, 1e-3, 0.0139). After it, the horizon rows read
3.1e-70, 3.7e-69, 4.7e-68, and the rest rows 7.78e-36, 1.06e-35, 1.87e-36, with no trend in a. They sit in rows 96-98
and 126-127, node 0's second block of M (offsets: node i at 2M + 4Mi, M = 32), and at a = 0 they read 1.94e-70.

Hypothesis: the residual's dependence on D is not smooth at about 1e-36 in those rows (a D-dependent coefficient
rounded below octo-double), so any prediction at D != D_base misses by it and no shorter step helps. floor4 tests it at
the base state, with z fixed: R(h) = F(z_0, D + h) - (D_h - D) F_D(z_0) for h = 1e-29 ... 1e-20 (D_h rounded to
double-double). Readings, fixed now:
1. Control: with F_D scaled by 1 + 1e-6, R must grow at the larger h (>= 10 times R at h = 1e-20), or the test is blind.
2. If the rest rows' R stays >= 1e-37 and within a factor 10 of one value from h = 1e-29 to 1e-24, while a smooth F
   predicts h^2 F_DD (far below 1e-37 there), the hypothesis holds: the floor is non-smooth D-dependence of the
   discrete system in those rows.
3. If R in the rest rows is <= 1e-38 at h <= 1e-24, the hypothesis fails.
4. Anything else is reported as it is.
