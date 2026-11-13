# I644-mac: the planted check of the octo-double corrector's natural monotonicity test against its default test

Machine: the coordinator's Mac (Apple M5, macOS). Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/644

Command, from `hp/` of main at b780bbd2 (the natural test with the ElimO displacement fix), with the i599/site2 build of
main 3c35f0c (exact freeze projector), 3 threads, nice 10:

    python3 -u octo_corrector.py planted RAW T138-win2/chain_o/anm_pin3_D200.0000.npz --qd 0 --accept natural --threads 3 --out I644-mac/planted_natural
    python3 -u octo_corrector.py planted RAW T138-win2/chain_o/anm_pin3_D200.0000.npz --qd 0 --accept own --threads 3 --out I644-mac/planted_own

The start is the D 200 chain state moved by 1e-12 relative (pinned max|F| 3.39e-12). Pass: max|F| below 1e-40 for
both, and the two Delta within 1e-30.

| rule | steps | final pinned max\|F\| | Delta |
|---|---|---|---|
| natural | 7 | 2.90e-64 | 1.695088752463841744241523971202762929111 |
| own | 6 | 6.52e-49 | 1.695088752463841744241523971202762929113 |

PASS: |Delta_natural - Delta_own| = 2e-39. The natural test refused the full first step (theta 1.28 against its bound
0.75) and took lam 1/2; the default test took full steps. `planted_*.json` hold the step records, with theta per trial
for the natural run; `planted_*.npz` the converged states (eight parts).
