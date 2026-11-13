# I632-macm3: the test-field rate mu at M 64, D 5 and 6 (mu's resolution error)

Machine: macm3 (Apple M3, 24 GB RAM), venv-macm3-314 (Python 3.14.3, python-flint 0.9.0, hpkernel cp314 neon of 2026-11-09), worktree ~/Source/choptuik-large-d-b596 at main b5d69cc2 (the build of #621; main is now at 3c35f0cd, a multidouble bump, not pulled), modecount_cx built from 742bb879's source. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/632 (macm3's #621 recommendation; the coordinator's message of 2026-11-13 02:52 UTC). Started 02:53 UTC.

Commands (run_632.sh), from the root of the worktree, nice 10, caffeinate -is: (1) python3 -u hp/scan_hp.py <raw>/I632-macm3/scan_to5.jsonl hp/data/lowD_states/lowDn_D4.0000_M64.npz 5.0 --dD 0.5 --maxdD 0.5 --kc 80 --ks 200 --threads 6 --tag m64 --attempts <raw>/I632-macm3/scan_to5_attempts.jsonl (saves m64_D5.0000.npz; the last step lands on D_END); (2) the same from m64_D5.0000.npz to 6.0 (scan_to6, m64_D6.0000.npz); (3) python3 -u hp/modecount_test_axis.py STATE --lo=-1.5 --hi=-0.02 --s=0 --threads=3 --out=<raw>/I632-macm3/axis_TAG.jsonl on m64_D5.0000 and m64_D6.0000, two at a time. The issue lets step 2 run beside the D 5 axis run (6 + 3 threads); here step 2 runs before the axis runs and the two axis runs together (3 + 3), to stay at 6 threads.

Written before the run (the issue's). Each scan saves its state and each axis run finds one real zero on the line; table mu(48) (I621-macm3: D 5 -0.4430361582, D 6 -0.5052240827) and mu(64) at D 5 and 6 and their difference, which is the resolution error of mu; name whether mu(5) moves toward -0.448 (Mittal, Gundlach and Martel) or away from it. About 1.5 h.

## Results (05:37 UTC; exits.txt: scan_to5 exit 0 04:05:27, scan_to6 exit 0 04:43:55, axis_D6 exit 0 05:16:31, axis_D5 exit 0 05:18:01, axis_D5_narrow exit 0 05:37:21 UTC)

| D | μ at M 48 (#621) | μ at M 64 | M 64 − M 48 | source of the M 64 value |
|---|---|---|---|---|
| 5 | -0.4430361582119 | -0.4430361582136 | -1.63e-12 | `axis_D5_narrow.jsonl` (window −0.47 to −0.43, h 0.004; the wide run `axis_D5.jsonl` ended off the line) |
| 6 | -0.5052240827037 | -0.5052240827037 | +6.99e-15 | `axis_D6.jsonl` (−1.5 to −0.02, h 0.02) |

D5 toward -0.448: M48 +4.964e-03, M64 +4.964e-03 from -0.448

The wide D 5 run (axis_D5.jsonl, -1.5 to -0.02) has the same phase jump of pi between -0.46 and -0.44 as M 48 but its secant refinement from -0.45 ended at -0.5576387280 -0.0061464079i, off the line; the coordinator's go (2026-11-13 05:19 UTC) for the narrow window (run_632_narrow.txt) gave the zero above. The scans: 10 attempts, 7 converged, 3 failed (D 4 to 4.5, 4 to 4.25, 4.125 to 4.28125) for D 4 to 5, 72 min; D 5 to 6 in 38 min.
