# I625-macm3: the sign of the exact det M on a 65-point grid across the D 58 root, M 32 (control) and M 48

Machine: macm3 (Apple M3, 24 GB RAM), venv-macm3-314 (Python 3.14.3, python-flint 0.9.0, FLINT 3.6.0, hpkernel cp314 neon of 2026-11-09), worktree ~/Source/choptuik-large-d-b596 at main ef466c7, modecount_cx built from 742bb879's source. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/625 (macm3's #615 recommendation; the coordinator's message of 2026-11-12 23:27 UTC: after #624, with the M 32 grid centred on lambda(32)).

Command, from hp/ of the worktree, four processes per grid (run_625.sh): python3 -u modecount_qdet.py data/states/up12_D58.0060.npz RE,0 [RE,0 ...] --M=M --kf=13 --threads=1 --json=qdet_MM_pP.json, with the points of points_MM.txt dealt round robin (point i to process i mod 4); process 0 starts first and makes the M 48 state, the others start when its first line is out. Points: lambda = centre + k*1e-14 for k = -32 to 32 (rounded once to the nearest double from exact rational arithmetic, make_points.py), k = 0 twice (index 32 in process 0 and index 65 in process 1: the repeat). Centres (my choice of "lambda(48)" and "lambda(32)"): the mean of the five ball lambda(48) (2.045529761477787) and of the five ball lambda(32) (2.045529761477775) of b1 to b5 in I615-macm3; the band of +-3.2e-13 covers all five lambda(48) (-1.3e-13 to +1.7e-13 from the mean). The background state is modecount_common.setup's (resample to M 48 and polish to |F| <= 1e-20), not gamma_dd.py's M 48 state (which Newton-polishes to its floor); their roots can differ, which the M 32 control tests for M 32 only.

Written before the run (the issue's). Acceptance: the M 32 grid has exactly one sign change (else the task stops: run_625.sh's gate); the M 48 sign pattern and the width of the band that holds all its sign changes are tabled (signs625.py); the repeated point gives the same result bit for bit. Started 23:29 UTC (after #624's runs).

## Results (2026-11-13 00:14 UTC)

M 32 grid (control; exits.txt, 23:57:57 to 23:58:32 UTC, all exit 0): exactly one sign change, between k = 0 and k = +1 (signs_M32.md); the repeat of k = 0 is bit for bit equal; the gate wrote 'control passes'.
M 48 grid: all four processes exit 1 (00:04:44 to 00:13:37 UTC) in setup: RuntimeError: background not converged in this layout: |F| = 2.3e-15 > 1e-20 (M = 48); signs_M48.md says '0 of 66 points done'. The coordinator decides (options a, b, c of the comment on the issue); nothing was changed or rerun.

## Option (b) (the coordinator's message of 2026-11-13 00:18 UTC, main be8bfb1; commands on the issue)
The M 48 grid of modecount_qdet was refused (see above). run_625b.sh: python3 -u hp/gamma_dd.py <raw>/I625-macm3/scan48_pN.jsonl hp/data/states/up12_D58.0060.npz --threads=1 --polish=4 --M48 --kf48=13 --ball=320 --scan=2.0455297614777672,1e-14,K0,K1 --scan_only, (K0, K1) p0 (-32, -16), p1 (-16, 0), p2 (0, 16), p3 (16, 32), and the M 32 control --scan_at=base --scan=2.045529761477775,1e-14,-4,4 without --M48 --kf48=13. Started 00:19 UTC. The centre of the issue, 2.0455297614777672, is not the mean of #615's five ball lambda(48) as I computed it (2.0455297614777874, make_points.py, 2.0e-14 higher); the band of +-3.2e-13 covers all five either way, and the commands were run as written.
Written before the run (the issue's). Pass: the control has exactly one sign change, between k = 0 and +1; the three overlap points (k = -16, 0, +16) are bit for bit equal across processes; then the M 48 sign pattern over k = -32..32 and the width of the band that holds all its sign changes, with ln|det| beside each sign.

## Results of option (b) (2026-11-13 00:46 UTC; scan32 exit 0 00:23:57, scan48_p0..p3 exit 0 at 00:44:59 to 00:45:01 UTC; scan_results.md is scan625.py's output)

M 32 control (centre 2.045529761477775, k = -4..4): signs -----++++; sign changes 1 between k pairs [(0, 1)]
overlap k = -16: p0 and p1: lambda, sign, ln|det| bit for bit equal (-1, 730.0249180175585 against -1, 730.0249180175585)
overlap k = +0: p1 and p2: lambda, sign, ln|det| bit for bit equal (+1, 729.9466344736046 against +1, 729.9466344736046)
overlap k = +16: p2 and p3: lambda, sign, ln|det| bit for bit equal (+1, 729.6686386150601 against +1, 729.6686386150601)

| k | lambda | sign | ln abs det |
|---|---|---|---|
| -32 | 2.045529761477447 | -1 | 728.724729471 |
| -31 | 2.0455297614774572 | -1 | 729.072287425 |
| -30 | 2.045529761477467 | -1 | 729.855044057 |
| -29 | 2.0455297614774772 | -1 | 728.815322197 |
| -28 | 2.045529761477487 | +1 | 727.544176305 |
| -27 | 2.045529761477497 | -1 | 729.743965677 |
| -26 | 2.0455297614775074 | -1 | 728.642550752 |
| -25 | 2.045529761477517 | -1 | 728.423889399 |
| -24 | 2.0455297614775274 | -1 | 728.133010273 |
| -23 | 2.045529761477537 | -1 | 728.442011792 |
| -22 | 2.0455297614775474 | +1 | 729.114907512 |
| -21 | 2.045529761477557 | +1 | 728.786996982 |
| -20 | 2.0455297614775674 | +1 | 729.181379127 |
| -19 | 2.045529761477577 | +1 | 729.652436590 |
| -18 | 2.0455297614775874 | -1 | 729.064354198 |
| -17 | 2.045529761477597 | -1 | 729.137202945 |
| -16 | 2.0455297614776073 | -1 | 730.024918018 |
| -15 | 2.045529761477617 | -1 | 728.430474928 |
| -14 | 2.0455297614776273 | +1 | 726.807043256 |
| -13 | 2.045529761477637 | -1 | 729.407339102 |
| -12 | 2.0455297614776473 | -1 | 728.363153608 |
| -11 | 2.045529761477657 | -1 | 729.526848458 |
| -10 | 2.0455297614776673 | -1 | 729.350588014 |
| -9 | 2.045529761477677 | +1 | 729.189391039 |
| -8 | 2.0455297614776873 | +1 | 728.497746747 |
| -7 | 2.045529761477697 | -1 | 729.942270616 |
| -6 | 2.0455297614777073 | +1 | 728.871950548 |
| -5 | 2.045529761477717 | -1 | 729.100401346 |
| -4 | 2.0455297614777272 | +1 | 729.068301694 |
| -3 | 2.045529761477737 | +1 | 729.589574857 |
| -2 | 2.0455297614777472 | -1 | 728.247730855 |
| -1 | 2.045529761477757 | -1 | 729.163373361 |
| +0 | 2.045529761477767 | +1 | 729.946634474 |
| +1 | 2.0455297614777774 | +1 | 729.414297687 |
| +2 | 2.045529761477787 | -1 | 729.792445540 |
| +3 | 2.0455297614777974 | -1 | 729.595754949 |
| +4 | 2.045529761477807 | -1 | 730.241589851 |
| +5 | 2.0455297614778174 | +1 | 729.674328522 |
| +6 | 2.045529761477827 | +1 | 729.958042030 |
| +7 | 2.0455297614778374 | +1 | 729.524485914 |
| +8 | 2.045529761477847 | +1 | 729.838826385 |
| +9 | 2.0455297614778574 | +1 | 726.659432200 |
| +10 | 2.045529761477867 | +1 | 729.346455941 |
| +11 | 2.0455297614778774 | +1 | 730.199846639 |
| +12 | 2.045529761477887 | +1 | 729.781609263 |
| +13 | 2.0455297614778973 | +1 | 725.224319345 |
| +14 | 2.045529761477907 | +1 | 729.165749105 |
| +15 | 2.0455297614779173 | +1 | 728.693988350 |
| +16 | 2.045529761477927 | +1 | 729.668638615 |
| +17 | 2.0455297614779373 | +1 | 729.173412381 |
| +18 | 2.045529761477947 | -1 | 726.676203182 |
| +19 | 2.0455297614779573 | -1 | 729.195103816 |
| +20 | 2.045529761477967 | +1 | 729.673627993 |
| +21 | 2.0455297614779773 | -1 | 728.300058311 |
| +22 | 2.045529761477987 | +1 | 730.125690756 |
| +23 | 2.0455297614779973 | +1 | 728.427997117 |
| +24 | 2.045529761478007 | +1 | 729.677360374 |
| +25 | 2.0455297614780172 | +1 | 726.178472517 |
| +26 | 2.045529761478027 | +1 | 729.054474313 |
| +27 | 2.0455297614780372 | +1 | 728.875258792 |
| +28 | 2.0455297614780474 | +1 | 728.968699432 |
| +29 | 2.045529761478057 | +1 | 729.053086780 |
| +30 | 2.0455297614780674 | +1 | 729.362940666 |
| +31 | 2.045529761478077 | +1 | 729.145947155 |
| +32 | 2.0455297614780874 | +1 | 726.731085892 |

signs from k=-32: ----+-----++++----+----++-+-++--++---+++++++++++++--+-+++++++++++
sign changes 19 between k pairs [(-29, -28), (-28, -27), (-23, -22), (-19, -18), (-15, -14), (-14, -13), (-10, -9), (-8, -7), (-7, -6), (-6, -5), (-5, -4), (-3, -2), (-1, 0), (1, 2), (4, 5), (17, 18), (19, 20), (20, 21), (21, 22)]
band holding all sign changes: between k=-29..-28 and k=21..22: at most 5.10e-13 and at least 4.90e-13 wide
overlaps bit for bit equal

Reading: the M 32 control has one sign change (between k = 0 and +1, in this scan and in the modecount_qdet grid above). At M 48 the sign changes 19 times between neighbouring points in a band between k = -29/-28 and k = +21/+22 (4.9e-13 to 5.1e-13 wide, 52 of the 65 points, 24 of them - and 28 +), is - below it (k <= -30) and + above (k >= 23); ln|det| is 725.2 to 730.2 at every point (median 729.15). I615's five ball lambda(48) lie at k = -10.66 (b4), -8.44 (b3), -2.18 (b1), +12.26 (b2), +19.10 (b5), all inside the band; for b1 and b5 the neighbouring grid signs differ, for b2, b3 and b4 they agree (sub-grid flips, the spacing is 22 ulps).
