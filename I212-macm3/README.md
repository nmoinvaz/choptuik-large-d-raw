# I212-macm3: the D 61 M 48 count at kf 23, and the re-evaluation of #159's kf 21 count with --resolve=last

Machine: macm3 (Apple M3, 4 performance + 4 efficiency cores, 24 GB RAM, macOS 26.3.1), venv-macm3-314 (Python 3.14.3 from Homebrew, python-flint 0.9.0, FLINT 3.6.0, hpkernel cp314 neon, modecount_cx for 3.14),
main d72280ff (hp/modecount_wind.py has --resolve=last). Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/212. Runs in parallel with I211-macm3's count, one thread each.

Part 1, reeval159/ (no new determinant): #159's kf 21 count (I159-macm3, 707 determinants) re-evaluated from a copy of its cache (reeval159/data/, 707 lines) with the saved kf 21 state copied into hp/data for the run
(reeval159/state_*.npz is its byte-identical copy, moved back out afterwards), command (reeval.cmd): python3 hp/modecount_wind.py hp/data/seeds/local/up23_D61.0264.npz --M=48 --kf=21 --h0=0.6
--lam=2.043532530673195 --fmax=1e-15 --resolve=last --tag=D61.0264_M48_kf21 --data=<raw>/I212-macm3/reeval159/data. Written before the run: pass = the cache has the same 707 lines after (no new determinant, cache_lines_*.txt)
and the log prints both mismatch counts per edge; the question is whether the edge Im = y2, Re aR to aL, resolves under --resolve=last (its last pass has no mismatch). If it resolves, U and full of #159 become counts and the
log's wind(g) of those boxes is read; if it does not, they stay "not a count". The boxes that #159 resolved must print the same windings as #159 (B1b +4, B1c +2, B1 +6, others 0) since the points are the same:
a difference there is a failed control.

Part 2, count (count.cmd, caffeinate -is, nice 10): python3 hp/modecount_wind.py hp/data/seeds/local/up23_D61.0264.npz --M=48 --kf=23 --h0=0.6 --lam=2.043532530673195 --fmax=1e-15 --resolve=last
--tag=D61.0264_M48_kf23 --data=<raw>/I212-macm3/data > count.log. Written before the run: gate = setup |F| <= 1e-15 (hp/modecount_common.setup raises above --fmax: a stop, |F| reported, the saved state moved
out of hp/data). Reading rule: wind(g) in B1b and B1c is 0 at kf 23 means the D 61 extras of #159 belong to the cut at 21 (as at D 45, #190); nonzero means they persist at a cut past 21. An edge that does not resolve
(under --resolve=last) is "not a count" and its boxes are not read. Both mismatch counts per edge are reported (all passes and the last pass). No D 61 M 48 kf 23 state or cache exists in hp/data or --data at the start.

Part 1 result (macm3, 00:02 UTC, exit 0, seconds, awake): the cache has 707 lines before and after (cache_lines_before.txt, cache_lines_after.txt), the state setup loaded is byte-identical to I159's (|F| 1.3e-19).
  The edge Im = y2, Re aR to aL resolves under --resolve=last: 350 points, max step 0.388 rad, "verified 183 (mismatch 9, last pass 0) in 4 passes"; no UNRESOLVED line (reeval159/reeval.log).
  Windings: B0 0, U0 0, B1a 0, B1b +4, B1c +2, B1 +6 (the same as #159's, a control that held), U +9 (winding of det M 2, 7 poles inside), full +24 (winding of det M 12, 14 poles inside).
  Additivity: full 24 = B1 6 + U 9 + the mirror strip 9. Nine extra zeros per strip at D 61 kf 21 (D 45 kf 21, #170: one per strip).

Part 2 result (macm3, main d72280ff, venv-macm3-314 = Python 3.14.3, python-flint 0.9.0, FLINT 3.6.0; awake.log: awake = wall, 22209 s = 6 h 10 min, caffeinate -is; the first 1 h 45 min shared the machine with I211's count).
  count.log: exit 0 at 06:13:24 UTC. Setup |F| 1.3e-06 in the layout, 1.3e-06 after Newton, 1.3e-19 after Levenberg-Marquardt (below 1e-15; the saved state is in hp_data_after/, hp/data back to hp_data_before.txt).
  776 evaluations (772 distinct points, four corners twice, equal to 8.8e-06 rad), 28.1 s on average, pivot minima 2.0e-15 to 1.3e-10.
  All 14 edges resolve under both rules: mismatches 0 in any pass and 0 in the last pass, largest step 0.392 rad, at most 4 passes (the long edge Im = y2, Re aR to aL has 307 points, phase change of g +97.2).
  wind(g) is NOT 0: B1b +6, B1c +2, B1 +8, U +8, full +24 (B0, U0, B1a 0). Windings add: full 24 = B1 8 + U 8 + the mirror strip 8. kf 21 re-evaluated (#159): B1b +4, B1c +2, B1 +6, U +9, full +24.
  The real axis has only the two expected sign changes ((0.5, 1.0) and (2.0, 2.5)), as at kf 21, so the extras are off the axis (the boxes are symmetric about it: they come in conjugate pairs).
  Reading rule fixed before the run: nonzero wind(g) in B1b and B1c means the D 61 extras persist at a cut past 21. They do (B1b +6, B1c +2). The total in the full box is 24 at both cuts; 4 of the
  six B1 zeros of kf 21 are in B1b and two in B1c, now 6 and 2 in B1b, B1c with U and the mirror strip going from 9 to 8 each: two zeros moved from the strips (one per strip) into B1b between the two cuts.
  No cause is tested here.
