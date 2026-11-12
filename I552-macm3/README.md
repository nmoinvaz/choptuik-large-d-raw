# I552-macm3: det M's pivots under one ulp of dh at kf 29 and kf 22 (D 61.03, M 48)

Machine: macm3 (Apple M3, 24 GB RAM). Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/552 (raised by macm3 in #498; the commands are the coordinator's message of 2026-11-12 05:30 UTC).

Build: a git worktree of main at ecca9c53 (~/Source/choptuik-large-d-b80), `hp/modecount_build.sh` run there at 06:00 UTC (cargo fetch --locked first for multidouble 4.1.0, which the offline build needs; finished in 2 min 26 s, exit 0; build.log is in I517-macm3/). Kernel of these runs: the new modecount_cx (compiled from hp/src at ecca9c53, multidouble 4.1.0) with the Python hpkernel of venv-macm3-314 built 2026-11-09 02:44 local (older than the hp/src changes of 2026-11-11; the coordinator's message of 05:35 UTC: go ahead, the bit check against #473's cached determinants decides, rebuild hp after #552 and M 80). The bit check (I517-macm3/bitcheck_473.py, log bitcheck_473.log) must pass first.
States copied from the main checkout's hp/data into the worktree's hp/data (so the runs read the matrices of #498 and #506, not remade ones): modecount_state_D61.0264_M48_kf29.npz sha256 bfe7150859d4b92c..., modecount_state_D61.0264_M48_kf22.npz sha256 7dd8e81469dbf2f7... (the one in I472-macm3/state_sha256.txt).

Commands, from the worktree's hp/ (one thread each, nice 10, caffeinate -is): run 1: python3 modecount_pivots.py data/seeds/local/up23_D61.0264.npz 3.1023 -0.0068 --M=48 --kf=29 --fmax=1e-15 --json=<raw>/I552-macm3/kf29.json > <raw>/I552-macm3/kf29.log 2>&1; run 2: python3 modecount_pivots.py data/seeds/local/up23_D61.0264.npz 2.0510 0 --M=48 --kf=22 --fmax=1e-15 --json=<raw>/I552-macm3/kf22.json > <raw>/I552-macm3/kf22.log 2>&1 (a point of #506's R 0.0075 circle at kf 22). Each runs the planted control first (it must print "pass" twice), then 6 determinants; exit 1 means a check failed, stop and report.

Written before the run (the issue's). Determinism control: shift 0 factored twice gives bit-identical pivots. Planted control: a matrix with a known number of rounding-level directions shows that number of moving pivots through the same code. Verdict: "localized" if at most 5% of the pivots carry 90% of the shift, all of them below 1e3 u ||M||; "global" if the shift is spread over more than half the pivots; otherwise reported with the numbers. Two sizes of perturbation: part hi (one ulp of the high part, as I506, I520, I498 did, relative 2^-53) and part lo (one unit in the last place of the double-double value, relative 2^-106).

## Results

(2026-11-12 06:25 UTC, macm3) Run 1 (kf 29, lambda 3.1023 -0.0068i): exit 0 at 06:18:56 UTC, 6 min 6 s; run 2 (kf 22, lambda 2.0510): exit 0 at 06:24:58 UTC, 6 min 2 s (started 06:12:50 UTC). In both: the planted controls pass twice (r 3: moved 3, want 3, localized; r 0: moved 0, none), consistency with mode_det passes (bit for bit), determinism passes (shift 0 twice, bit-identical pivots). The bit check of the rebuilt module (I517-macm3/bitcheck_473.log) passed first: 4 of 4 cached M 64 determinants of #473 identical, the control differs.
n = 1152 pivots in both. kf 29: plain ln|det| -132.681283, arg +1.881273, pmin 3.668e-16, pmax 7.484e+06, ||M||_F 1.549e+10. kf 22: plain ln|det| 355.302013, arg +3.6e-11 (the point is on the real axis), pmin 8.447e-14, pmax 7.491e+06, ||M||_F 1.546e+10.

| state | part, shift | change of ln\|det M\| | pivots moved by more than 1e-3 in ln | pivots carrying 90% | all below 1e3 u \|\|M\|\| | rows differ at | verdict |
|---|---|---|---|---|---|---|---|
| kf 29 | hi +1 | +266.935 | 47 of 1152 | 22 | yes (1.7e-3) | 39 | localized |
| kf 29 | hi -1 | +266.764 | 48 | 22 | yes | 40 | localized |
| kf 29 | lo +1 | -0.187 | 8 | 2 | no (1.9e-19) | 1 | between |
| kf 29 | lo -1 | -0.191 | 8 | 4 | no | 0 | between |
| kf 22 | hi +1 | +109.349 | 48 | 18 | yes (1.7e-3) | 39 | localized |
| kf 22 | hi -1 | +106.104 | 48 | 16 | yes | 39 | localized |
| kf 22 | lo +1 | -0.000 | 0 | 7 | no (1.9e-19) | 0 | none |
| kf 22 | lo -1 | -0.000 | 0 | 8 | no | 0 | none |

The top ten pivots of each part are in the logs and the JSON (only the ten largest are stored). Under hi they are all among the last 20 pivots (k 1132 to 1150 at kf 29; k 1138 to 1144 at kf 22 for the first five), each growing by e^8 to e^13. The JSON does not store the indices of the other carriers of the 90%.
