# I820-mac: r's constancy against planted shifts of lam_g's fold, a bound on the two folds' separation

Machine: the coordinator's Mac (Apple M5), agent xfkappa. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/820.
Code: `hp/fold_cancel.py calibrate`, registered at wip/xf-820 e7cec5c2 (the design posted on the issue before the run),
the post hoc `--cont` option at 2380c015, on main 04c98733. Input: `I603-win2/chain_nsr` jets at raw f65c5e43 (the real
low orders of #818's 26 bases) and `hp/data/fold_cancel_coeffs.json` (#819). One process at nice 10.

## Runs

- `calibrate.log`, `calibrate.json`: the registered run, contamination 0.3 (#819's plant). Not bounded, exit 1.
- `calibrate_cont{0,0.003,0.01,0.03,0.1}.{log,json}`: post hoc, the contamination at those amplitudes.
- `check_numbers.log`: `check_numbers.py --selftest` at 2380c015, 1939 of 1939, selftest 1939 of 1939.
- The registered run and `--cont=0.01` rerun byte-identical.

## Result

r's relative range (max - min)/median over the 26 bases. Real: 1.19e-4.

| contamination | delta 0 | 1e-6 | 1e-5 | 1e-4 | 1e-3 | -1e-6 | verdict |
|---|---|---|---|---|---|---|---|
| 0.3 (registered) | 2.74e-3 | 3.14e-3 | 6.72e-3 | 4.26e-2 | 4.11e-1 | 2.54e-3 | not bounded: the floor is 23 times the real range |
| 0 | 2e-11 | 3.98e-4 | 3.98e-3 | 3.98e-2 | 4.08e-1 | 3.98e-4 | < 1e-6 |
| 0.003 | 2.73e-5 | 4.25e-4 | 4.00e-3 | 3.99e-2 | | 3.70e-4 | < 1e-6 |
| 0.01 | 9.11e-5 | 4.89e-4 | 4.07e-3 | 3.99e-2 | 4.08e-1 | 3.28e-4 | < 1e-6 |
| 0.03 | 2.73e-4 | 6.71e-4 | 4.25e-3 | 4.01e-2 | 4.08e-1 | 2.88e-4 | not bounded |
| 0.1 | 9.12e-4 | 1.31e-3 | 4.89e-3 | 4.08e-2 | | 7.56e-4 | not bounded |

The range grows strictly with delta at every contamination, by about 400 delta. The robust range (the smallest over a
shift of both folds by -4e-4 to +4e-4) is at least 0.84 of the nominal one, and still exceeds the real range at
delta 1e-6 for contamination 0 to 0.01. The contamination amplitude is that of #782's near singularities (260.17 and
259.47 +- 1.17i) against the fold's amplitude b1 sqrt(s), + for lam_g and - for Delta.

## Recommended task

*The contamination's size in the real series.* What: fit lam_g's and Delta's orders 4-24 at each base with the fold's
three terms plus #782's near singularities (260.17 and the pair 259.47 +- 1.17i) as free amplitudes, and read their
amplitude against the fold's. Why: #820's bound holds only if that amplitude is at most 0.01 (at 0.03 the plant's r
already varies more than the real one). Acceptance (can fail): a plant with known amplitudes 0.003, 0.01, 0.03 and 0.3
is recovered to 30% first; then the real amplitude is read, and #820's conditional bound applies when it is at most
0.01, or is reported as not applying. Depends on: #820, #782.
