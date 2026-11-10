# I371-macm3: #97 (a) rerun with main's verbose line (max derivative radius), lemma 6a at M = 5, sub-box 1e-14

Machine: macm3 (Apple M3, 24 GB RAM), venv-macm3-314 (Python 3.14.3, python-flint 0.9.0, FLINT 3.6.0). Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/371.

Code. The checkout cannot be pulled (SSH to GitHub is refused here), so the run uses a copy of the checkout's solver/proof/*.py (main checkout at bfe5fd54) in the scratchpad, with validated_int.py replaced by main's version at
bfa7c40e99c3d21c6c0e93ee4465386a59e0738a (fetched with the contents API; git blob 12af9df954f5167baefa5d1773b19775b75a6eac, the only file of solver/proof that differs between bfe5fd54 and main dd4c70f). `diff` against the checkout's
validated_int.py shows only the verbose line (430 to 440). Paths are absolute, since the copy sits outside the checkout. Input: I36-macm3/A_M2_6a_M5_sub1e-14.json (the file of #97 (a); #97 ran under venv-macm3, Python 3.13.3, python-flint 0.9.0).

Command (run.sh, caffeinate -is, nice 10, one thread): the issue's, with absolute paths:
python3 -u lemma6_jump_M.py --M=5 --box=<raw>/I36-macm3/A_M2_6a_M5_sub1e-14.json --rp=0.08 --k=20 --verbose --save-B=<raw>/I371-macm3/B_M5_sub1e-14_verbose.json --json=<raw>/I371-macm3/lemma6a_M5_sub1e-14_verbose.json

Written before the run (the issue's). Acceptance: every verbose line carries "max derivative radius" (31 lines, the last at t 1.000000), and the last value equals the final line's "max radius of B" (3.35e-01 in #97). Report the 31 radii as a table
(#97's open question: where B widens along xi). A mismatch is reported, not fixed.

## Results

Result: exit 2 (G_slow: invertibility not proved; lemma 6a NOT established, as in #97 and #36), 15:25:24 to 15:37:57 UTC (752 s of integration), awake, beside 5 other single-thread jobs. 31 verbose lines, all with "max derivative radius", the last at t 1.000000
(3.35e-01) and the final line "max radius of B 3.35e-01". No --save-B or --json file was written (the run stops at exit 2 before them). The table of the 31 radii is in the closing comment of the issue.
The coordinator accepted this run as the task's (15:33 UTC) after checking blob 12af9df against bfa7c40.
