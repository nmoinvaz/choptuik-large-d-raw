# I674-mac: the planted check of the strong-row chord after the octo-double corrector's first step

Machine: the coordinator's Mac (Apple M5, macOS). Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/674

Command, from `hp/` of main at 58628d94, with the i599/site2 build of main 3c35f0c (exact freeze projector), 3 threads,
nice 10:

    python3 -u octo_corrector.py planted RAW T138-win2/chain_o/anm_pin3_D200.0000.npz --qd 0 --accept natural --strong 4 --threads 3 --out I674-mac/planted_strong

PASS: 7 steps to pinned max|F| 2.90e-64, Delta 1.695088752463841744241523971202762929111, the natural-only run's
(I644-mac) to all 40 printed digits. The chord was refused at this start (theta 1.282 against 0.750, |F| stalling at
1.59e-24 after 5 chord steps), and the first step's trials then ran as without it. The start is moved by 1e-12 in
every direction, so the chord's premise (an error along the weak directions) does not hold there; the check tests the
code path and its fallback.
