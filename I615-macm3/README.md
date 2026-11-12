# I615-macm3: gamma's root resolution at D 58 and M 48 on the exact determinant (gamma_dd.py --ball=320), #458's D 58 runs repeated

Machine: macm3 (Apple M3, 24 GB RAM), venv-macm3-314 (Python 3.14.3, python-flint 0.9.0, FLINT 3.6.0, hpkernel cp314 neon of 2026-11-09), worktree ~/Source/choptuik-large-d-b596 at main ef466c7 (the issue asks for 742bb87 or later), modecount_cx built from 742bb879's source. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/615 (the coordinator's message of 2026-11-12 22:36 UTC).

Runs (common.sh run(), chainA.sh to chainD.sh, one thread per run, four at a time, nice 10, caffeinate -is): python3 -u hp/gamma_dd.py <raw>/gamma_up12_D58.0060_NAME.jsonl hp/data/states/up12_D58.0060.npz --threads=1 --polish=4 --M48 --kf48=13 --bracket=A,B --xtol=1e-16 --ball=320, the command of I458-macm3/common.sh with --ball=320 added. The state up12_D58.0060.npz has sha256 d5cc8be5de0ab765... in the worktrees b458, b596 and the main checkout alike (I458-macm3/README.md gave the hashes of the D 40 and D 58 states swapped; corrected there). Brackets as in #458: b1 2.0452297615,2.0456297615; b2 2.0454297615,2.0458297615; b3 2.0435297615,2.0460297615; b4 2.0454797615,2.0457297615; b5 2.0455197615,2.0455697615; b1r = b1 again; none 2.0456297615,2.0458297615 (no sign change). 7 runs. Started 2026-11-12 22:37 UTC.

Written before the run (the issue's). Controls: b1r equals b1 bit for bit (lambda(32) and lambda(48)), and none exits 1 with lam null. Table lambda(32) and lambda(48) per bracket and their spreads (max - min over b1 to b5) beside #458's double-double values (lambda(48) spread 2.554e-13, min 2.045529761477577, max 2.0455297614778325; lambda(32) spread 2.220e-15). Verdict: "the LU's noise" if the lambda(48) spread falls below 2.55e-14, otherwise both are reported. Also lambda(48) on the exact determinant against #458's double-double lambda(48) per bracket, the difference reported. A run that exits 1 for another reason (a floor check, a ball containing 0) is reported, not rerun.

## Results (2026-11-12 23:24 UTC; exits.txt: b4 23:04:13, b1 23:05:27, b2 23:05:44, none 23:06:42 (exit 1), b3 23:07:54, b1r 23:19:16, b5 23:23:38 UTC; the others exit 0; first four started 22:37 UTC)

| bracket | λ(32) ball | λ(32) LU (#458) | λ(48) ball | λ(48) LU (#458) | ball − LU at M 48 | dets M 32 / M 48 (ball) | run time M 32 + M 48 (s) | floor check |
|---|---|---|---|---|---|---|---|---|
| b1 | 2.045529761477775 | 2.0455297614777743 | 2.0455297614777455 | 2.0455297614776238 | +1.22e-13 | 6 / 13 | 1662 | ok |
| b2 | 2.045529761477775 | 2.045529761477775 | 2.04552976147789 | 2.045529761477577 | +3.13e-13 | 7 / 13 | 1679 | ok |
| b3 | 2.045529761477775 | 2.045529761477775 | 2.045529761477683 | 2.0455297614778325 | -1.50e-13 | 7 / 16 | 1810 | ok |
| b4 | 2.045529761477776 | 2.0455297614777765 | 2.0455297614776606 | 2.0455297614777126 | -5.20e-14 | 7 / 11 | 1588 | ok |
| b5 | 2.045529761477775 | 2.0455297614777748 | 2.045529761477958 | 2.045529761477681 | +2.77e-13 | 6 / 17 | 943 | ok |
| b1r | 2.045529761477775 | 2.0455297614777743 | 2.0455297614777455 | 2.0455297614776238 | +1.22e-13 | 6 / 13 | 829 | ok |

Spread over b1 to b5 of λ(32), ball: 8.882e-16 (min 2.045529761477775, max 2.045529761477776, 5 brackets)

Spread over b1 to b5 of λ(32), LU (#458): 2.220e-15 (min 2.0455297614777743, max 2.0455297614777765, 5 brackets)

Spread over b1 to b5 of λ(48), ball: 2.975e-13 (min 2.0455297614776606, max 2.045529761477958, 5 brackets)

Spread over b1 to b5 of λ(48), LU (#458): 2.554e-13 (min 2.045529761477577, max 2.0455297614778325, 5 brackets)

Control b1r vs b1: λ(32) bit for bit equal, λ(48) bit for bit equal

Verdict (the issue's): the spread of lambda(48) over b1 to b5 on the exact determinant is 2.975e-13, against 2.554e-13 for #458's double-double LU (ratio 1.16); it does not fall below 2.55e-14, so it is not "the LU's noise", and both are reported. The M 48 background state is the same as #458's in all six runs (F, Delta and the Newton step estimate equal bit for bit); only det M differs. Differences ball - LU at M 48: +1.217e-13, +3.126e-13, -1.497e-13, -5.196e-14, +2.771e-13 (mean +1.02e-13, largest 3.13e-13).
Controls: b1r equals b1 bit for bit (lambda(32) and lambda(48)); none exits 1 with lam null (2 determinants).
Near each M 48 root (iterates within 1e-9 of the final lambda(48), from the logs): b1 9 iterates, signs -+----+--, ln|det| 725.38 to 729.71; b2 10, +-++-+++-+, 725.96 to 734.75; b3 12, +-++--+--+-+, 727.26 to 733.87; b4 8, +-++-+--, 726.03 to 732.56; b5 13, --++-+-+-+-++, 725.59 to 730.00. The one iterate each between 1e-9 and 1e-6 has ln|det| 738.8 to 744.0.
