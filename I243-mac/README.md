# I243-mac: the earlier mode counts re-checked for hidden turns, with the alias rule of #242 and a second-scale check

Machine: mac (Apple M5, 10 cores, macOS 27, shared with #208's two CAPD processes), venv-314 (Python 3.14, hpkernel and
multidouble NEON, python-flint 0.9.0, modecount_cx cp314 build of 2026-11-08 16:26 from the main checkout). Issue:
https://github.com/nmoinvaz/choptuik-large-d/issues/243. Code: branch wip/i242 of the main repository (the #242 rule,
hp/modecount_wind.py 01f6c59). Inputs read from the raw-data repository by git archive into a scratch directory (nothing
pulled here): 6d8007f for every folder, 9ef605c for I241-macm3. All runs single-threaded under nice 10 and caffeinate -i,
at most two count processes at a time.

## Method

1. Scans, no determinants (scan.log, from scan_all.py): I230-mac/alias_scan.py, unchanged (copied as
   alias_scan_I230.py), and scan_rule.py (the #242 rule's first-pass flags, corners included) on the definitive record
   of every count (records/, listed with their sources in records/manifest.txt). Control first: #212's kf 23 record.
2. Re-evaluation (reeval.py, run_batch.py): each count's cache is copied into NAME/data/ and hp/modecount_wind.py
   reruns with the #242 rule and the record's own geometry (aLL, aL, a1, a2, aR, Im2, h0 and lam passed explicitly).
   It re-samples the flagged intervals (and whatever the rule's cascade reaches) to steps <= pi/4 with the repeated
   verification of steps > pi/8, and adds only the determinants it needs. NAME/cache_lines.txt has the line counts
   before and after and a check that the old lines are unchanged. The saved resampled states of the original runs
   (hp_data_after/ of each folder) were copied into the worktree's hp/data so that setup loaded them, not re-converged.
3. Second-scale check (offset_check.py, for the counts of 0 behind the README's statements): every interval gets one
   new sample at its golden-section point, and the two pieces must each be at most pi/4 and add up to the interval's
   step. It shares the determinant code, g's factors and the samples with the count, not the alias rule.
   planted_offset.py tests it on the synthetic det M of hp/modecount_planted.py, counted with the old rule.

Circles (#178, #190, I68): circle_scan.py applies the same rule to each circle's samples (from its cache, with the
record's beta; the points and winding must match the record), cyclically, no determinants; circles/circle_scan.log.

## Results

No count changes except the control. Every box of every count re-evaluated with the #242 rule is unchanged, with 0
verification mismatches in any pass and every step at most 0.392 rad. The one correction is #212's kf 23, already found
by #230: U +8 to +11, full +24 to +30.

**Control** (I212_D61.0264_M48_kf23): both scans flag T's two intervals Re 1.157 to 0.300. The re-evaluation adds 147
determinants, and T's phase change goes from +97.209 to +116.058 rad (#230's t_check.py: +116.058). U is +11, full
+30, and B1b, B1c, B1 are unchanged (+6, +2, +8).

| count (record) | scan flags (#242 rule / alias_scan) | new determinants | wind(g) B0 U0 B1a B1b B1c B1 U full | box |
|---|---|---|---|---|
| D 61.03 M 48 kf 23 (#212) | 33 / 2 | 147 | 0 0 0 +6 +2 +8 **+11 +30** (was +8 +24) | U, full corrected |
| D 61.03 M 48 kf 21 (#159, re-evaluated in #212) | 9 / 1 | 21 | 0 0 0 +4 +2 +6 +9 +24 | unchanged |
| D 45.05 M 48 kf 23 (#211) | 0 / 0 | 0 | all 0 | unchanged |
| D 45.05 M 48 kf 21 (#170) | 9 / 1 | 15 | 0 0 +1 0 0 +1 +1 +3 | unchanged |
| D 30.07 M 32 (main) | 0 / 0 | 0 | all 0 | unchanged |
| D 30.07 M 48 (main) | 10 / 5 | 28 | 0 0 0 0 +2 +2 0 +2 | unchanged |
| D 30.07 M 48 kf 13 (main) | 0 / 0 | 2 (repeated verification, which postdates the count) | all 0 | unchanged |
| D 45.05 M 32 (main) | 0 / 0 | 0 | all 0 | unchanged |
| D 61.03 M 32, and its Im 3.5 and Re 12 counts (main) | 0 / 0 | 0 | all 0 | unchanged |
| D 16.76 M 32, D 8.25 M 32 (main) | 0 / 0 | 0 | all 0 | unchanged |
| D 50.01 (#232) | 0 / 0 | 0 | all 0 | unchanged |
| D 52.04 (#237) | 2 / 0 | 4 | all 0 | unchanged |
| D 53.79 (#237) | 0 / 0 | 0 | all 0 | unchanged |
| D 53.79 fixed left column (#241) | 0 / 0 | 0 | all 0 | unchanged |
| D 54.04 (#240) | 20 / 5 | 33 | +2 +2 0 0 0 0 0 0 | unchanged |
| D 54.04 fixed left column (#241) | 17 / 4 | 32 | +2 +1 0 0 0 0 0 0 | unchanged |
| D 55.04 (#232) | 18 / 1 | 30 | +2 +1 0 0 0 0 +1 +2 | unchanged |
| D 55.04 fixed left column (#241) | 10 / 2 | 17 | 0 +1 +2 0 0 +2 +1 +4 | unchanged |
| D 55.04 M 32 (#237) | 0 / 0 | 0 | all 0 | unchanged |
| D 8.25, D 16.76 M 32 (#69, runs A and B), D 45.05 M 48 kf 13 (#70), D 4 M 48 (#70 job 3) | 0 / 0 | scan only | all 0 | unchanged |

The re-evaluations of counts with 0 flags added no determinant, as the scan predicts. A scan flag is a first-pass
flag: the cascade after it is the re-evaluation's.

**Second-scale check** of the counts of 0 behind the README's statements (offset_check.py, one new determinant per
interval). No interval is flagged in any of the six, and the largest piece is 0.26 rad against the tol of 0.785:

| count | intervals (new determinants) | flagged | largest piece | largest sum error | boxes |
|---|---|---|---|---|---|
| D 45.05 M 48 kf 23 (#211) | 68 | 0 | 0.259 rad | 2.0e-14 | unchanged |
| D 30.07 M 32 | 83 | 0 | 0.229 rad | 2.2e-14 | unchanged |
| D 45.05 M 32 | 91 | 0 | 0.245 rad | 1.3e-14 | unchanged |
| D 61.03 M 32 | 93 | 0 | 0.250 rad | 1.3e-14 | unchanged |
| D 53.79 M 48 kf 23 (#237, the onset bracket's lower end) | 71 | 0 | 0.240 rad | 2.5e-14 | unchanged |
| D 30.07 M 48 kf 13 (the cut test) | 67 | 0 | 0.244 rad | 1.3e-14 | unchanged |

Its planted test (planted_offset.log): on counts made with the old rule of the synthetic det M it flags and corrects
every miscounted row (7) and every miscounted random configuration (11). It misses the close pairs between two
samples, which a phase-only check does not see; the #242 rule's ln|g| scale catches those. Its control
(planted_offset_control_interp.log, --mutate=interp: no new sample) fails all 7 rows. A first control, the midpoint
instead of the golden point (planted_offset_control_phi0.5.log), did not fail: the old rule's samples on T hold one
turn per interval there, an odd number, which a midpoint catches too. It was replaced, as the script's docstring says.

**Circles** (#178 kf 13 to 21 and its locate rounds, #190 kf 21 to 27, I68's October and fresh D 30 M 48 circles and
the kf 13 one): all 25 have 0 flagged arcs, with points and windings matching their records. The two R 0.03 locate
circles of #178 come closest to the threshold pi/2 = 1.5708: 1.57 at 1.20 (winding 0) and 1.46 at 1.14 (winding +1,
the zero 0.03 or less from the circle's centre). Every other circle is at most 0.77.

**Test-field counts** (hp/data/modecount_test_results.jsonl on main, notes/GHOST_ADMIXTURE.md; outside the issue's list,
scanned only, records_test/scan_test.log): the M 32 ones (D 8.25 and its two planted runs, 16.76, 30.07, 45.05,
67.01) have 0 flags. The two D 4 M 48 ones are flagged: 26 of 138 intervals (alias_scan 1) and, with the planted zero,
38 of 186 (alias_scan 7). They were not re-evaluated here (a recommended task on the issue).

## Determinants and runs

329 new determinants in the re-evaluations, 473 in the second-scale checks, and 1 at a
stored sample point (offset_check's first lookup tolerance, 1e-12, missed the cache keys by 1e-11; kept as
I211_D45.0507_M48_kf23/data/offset_evals_v1_lookup_bug.jsonl, it reproduces macm3's value to 2.9e-11 in ln|det M| and
2.6e-9 rad in arg). Exits are in exits.txt and batch*.log. batch3.log is the first launch of the offset checks,
stopped by me after that point (exit 143); batch3b.log is the relaunch with the tolerance 1e-9. offset_run1.* are the
checks' first runs, offset.* their reruns from the cache that added the margins (no new determinant).
