# I851-dh370: the horizon response's power in rel at D 245.6366, 250.1676 and 252.6135

Machine dh370 (Fedora 45, i7-8700, 12 threads). Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/851

`run851.sh` (unit `i851`, 14:13:03 to 14:40:14 UTC on 2026-11-17, nice 10): worktree `~/Source/choptuik-large-d-935` at main 043834d9, its 4.8.2
`.venv`. `step_spread.py --selftest` (exit 0) and `--selftest --mutate=bar` (exit 1, must fail) first; then the three states
`I603-win2/chain/anm_pin3_D{245.6366,250.1676,252.6135}.npz` at once, 3 threads each, `--rel 1e-70,1e-75,1e-80 --seeds 1 --controls 0
--repeat 0 --threads 3`; then `step_spread.py power` on the three outputs with `--quad 1.8,2.2 --lin 0.9,1.1` (`power.log`, `power.json`).
`--ref` is #840's recorded unperturbed step 5.2645963792835124e-82 at D 252.6135 only (I840-mac/ss_D252.log, where #840 passed it); the issue's
"`--ref` at 252.6" is that D, and a step of 252.6 would fail by design. No `--ref` at the other two D, where no step was recorded.
`coef851.py` (`python coef851.py .`, log `coef851.log`) tabulates c = |dev| / rel^2 and the pivot ratio from the stored JSONs.

## Results

Each run took 1494 s (D 245.6366), 1631 s (D 250.1676) and 1551 s (D 252.6135) at 3 threads, 154 MB. Exits 0, `step_spread: PASS` for all
three (`exits_851.txt`).

| D | rel | smallest pivot | pivot / unperturbed - 1 | dev = dDelta(seed) - dDelta(unperturbed) | p from the next larger rel |
|---|---|---|---|---|---|
| 245.6366 | unperturbed | 4.374269e-27 | | dDelta +3.3839e-53, max\|F\| 5.0e-66 | |
| | 1e-70 | 4.374260e-27 | -1.9e-6 | -9.2441e-44 | |
| | 1e-75 | 4.374269e-27 | -1.9e-11 | -9.2441e-54 | 2.0000 |
| | 1e-80 | 4.374269e-27 | -3.3e-16 | -9.2447e-64 | 2.0000 |
| 250.1676 | unperturbed | 1.068665e-29 | | dDelta +7.6531e-49, max\|F\| 3.05e-61 | |
| | 1e-70 | 1.066682e-29 | -1.9e-3 | -8.7926e-41 | |
| | 1e-75 | 1.068665e-29 | -1.9e-8 | -8.7280e-51 | 2.0006 |
| | 1e-80 | 1.068665e-29 | -1.9e-13 | +1.8029e-61 | none (sign change) |
| 252.6135 | unperturbed | 7.286891e-31 | | dDelta +5.2646e-82, max\|F\| 5.6e-92 | |
| | 1e-70 | 9.065005e-31 | +2.4e-1 | -1.2678e-38 | |
| | 1e-75 | 7.286907e-31 | +2.2e-6 | -1.0537e-48 | 2.0161 |
| | 1e-80 | 7.286891e-31 | +2.2e-11 | -1.0537e-58 | 2.0000 |

Reading by the power rule (`power.log`): D 245.6366 quadratic (p 2.0000, 2.0000), D 250.1676 neither (p 2.0006, then a sign change between 1e-75
and 1e-80), D 252.6135 quadratic (p 2.0161, 2.0000). At D 252.6135 the 1e-70 run's pivot is 24% off, and the other two rels are within 3e-6.
The `--ref` check at D 252.6135 passes: the unperturbed dDelta equals #840's Mac value as a double.

The coefficient c = |dev| / rel^2 (`coef851.log`) at rel 1e-75, pivot-clean at all three D: 9.2441e96, 8.7280e99, 1.0537e102. The slope of ln c
against D is 1.5119 from 245.6366 to 250.1676 and 1.9598 from 250.1676 to 252.6135 per unit D, least squares over the three 1.6492, against
#805's 1.44 (ratio 1.145) and twice it (ratio 0.573). Three points, one seed, so the slope is a three-point fit, not an error bar.

At D 250.1676 the 1e-80 deviation (+1.8029e-61) is not c rel^2 (-8.728e-61): it differs by 1.05e-60. That state's own max|F| is 3.05e-61,
five orders above the other two (#840's discrepancy 4). Not tested whether the two are related.
