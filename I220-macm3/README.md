# I220-macm3: win2's lemma 6a(5) enclosure at p-hat cross-loaded on macm3 (the converse of #196's cross-load)

Machine: macm3 (Apple M3), venv-macm3-314 (versions.txt: Python 3.14.3, python-flint 0.9.0, FLINT 3.6.0), main d28566c0. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/220.
win2's B: I196-win2/B_M5_sub1e-18_phat.json (Python 3.14.10 on win2, rho_6a 0.2081 on its own B; macm3's B loaded on win2 gave 0.2121). Box file: I103-macm3/A_M2_6a_M5_sub1e-18.json, --x = its "p" (centre_passed.txt).

`run_i220.sh` (from solver/proof/, 1 thread, nice 10, caffeinate -is): lemma6_jump_M.py --M=5 --box=<box> --x=$PHAT --rp=0.08 --k=20 --load-B=<win2's B> --json=lemma6a_loadB_win2_phat.json,
then, as controls with the same B, --mutate=partial and --mutate=coords (the controls of #184 and #196: partial must stop with a non-square G_slow, coords must give rho_6a above 1), and review_39/b_float.py on
win2's B (flow at p-hat within 0.01 of rad(B), as #184's check; --mutate=w must exceed 1). The controls are my addition to the issue's list so that the cross-load can fail.

Written before the run. Pass: rho_6a < 1 with win2's B (the issue's criterion, #111's rule: each machine's enclosure gives the same conclusion on the other). Controls as in #184/#196: partial exit 0 (G_slow 13 x 17), coords exit 2 with
rho_6a > 1, b_float.py exit 0 and its p-hat flow within 0.01 of rad(B), --mutate=w exit 0. The two rho_6a balls (macm3's own 0.2121 and win2's own 0.2081, and this cross-load) are expected to differ in the last digits
(radii depend on the integration path, #104, #110, #111's rule compares conclusions, not hashes); the rho_6a of this run is compared with win2's own B's on win2.

Results (macm3, 2026-11-09 06:29 UTC, 16 s in all, awake = wall: no sleep event since 2026-11-08 13:11 PST). Every step's exit is in exits.txt.
  win2's B loaded on macm3 at p-hat: exit 0, rho_6a = [0.2081327461 +/- 2.72e-11] < 1 (lemma6a_loadB_win2_phat.json, ok true), |H| <= 6.39e+01, |G_slow^-1| <= 5.16e+00, max radius of B 3.21e-05 (win2's), lemma S contraction
  0.7247, Lambda 0.4233. The centre passed (centre_passed.txt) equals the box file's "p" (diff). The log prints no centre line (as in #184).
  Against the other balls: win2's own B on win2 gave [0.2081327454 +/- 8.77e-12] (I196-win2), so the two balls of the same B are disjoint by 6.4e-10 (their difference 7e-10, radii 2.7e-11 and 8.8e-12): the stored radii are rounded to a
  30-bit mag on reload and the radii depend on the integration path (#104, #110, #111); the conclusion rho_6a < 1 is the same on both machines. macm3's own B on macm3 [0.2120798569 +/- 1.46e-11] and on win2
  [0.2120798570 +/- 2.97e-11] overlap.
  Controls with win2's B: partial exit 0 (G_slow 13 x 17, "MUTATION partial: failure expected"); coords exit 2, rho_6a 3.200 (not below 1); b_float.py exit 0, the flow at p-hat within 4.64e-08 of rad(B) (below 0.01; the flow from x-hat
  at 0.184), and --mutate=w exit 0 (232 of rad(B) from both flows, must exceed 1).
