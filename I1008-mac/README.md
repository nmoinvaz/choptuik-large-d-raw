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
