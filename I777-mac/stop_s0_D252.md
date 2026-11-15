# I777-mac: the queue's stop at s0_D252 (mac752, 2026-11-14 22:47 UTC)

The queue stopped at s0_D252, which exited 1 where 0 was expected. Its corrector ended at pinned max|F| 2.54e-22 after
5 steps, not below 1e-40. The run did not have #713's re-seeder settings, so it is not #713's C2 with the option.

## Why it is not #713's C2

`octo_corrector.py planted` at 8e10d127 has no `reseed_o` or `reseed_start` option. Its `_parse` reads only the keys
of its defaults and drops every other flag without a word. So the queue's `--reseed_o 3 --reseed_start pred` were
ignored, and the re-seeder ran at `od=0, qd_start="ladder"`, which gives quad-double projections only (AGENTS.md).
`wall` at 8e10d127 reads `--reseed_o` but not `--reseed_start`, so s0_wall would lose `pred` the same way.

| check | result |
|---|---|
| `_parse` of the queue's planted flags with planted's defaults at 8e10d127 | `reseed_o` and `reseed_start` absent, the rest read |
| control: the same flags with `reseed_o` added to the defaults | `reseed_o` read as 3 |
| s0_D252.log's settings line, which #713's run printed | missing, since 8e10d127's planted no longer prints it |

The options come from commit 00c3963f ("octo_corrector: the re-seeder's options in planted and wall"). It is only on
`wip/i713-subagent`, which #713 ran from, and it is not on main (origin/main 7d7dab85 does not have it either).

## The run, against #713's

| step | #777 s0_D252 (8e10d127, re-seeder od 0, ladder start, full_drop 1e-6) | #713 s0_D252 (00c3963f, od 3, pred start, no option) |
|---|---|---|
| 0 | lam 1, \|F\| 3.40e-12 to 8.44e-16 (own test) | lam 1/64, 3.40e-12 to 3.34e-12. Its lam 1 trial gave 2.48e+22 |
| 1 | lam 1 by the drop, 8.44e-16 to 2.09e-25, while \|dz\| grew 8.69e-16 to 2.83e-11 | lam 1/16, 3.13e-12 |
| 2 | lam 1 (own test), 2.09e-25 to 2.58e-22, \|dz\| 8.77e-13 | lam 1, 7.19e-16 |
| 3 | lam 1/64, 2.54e-22. Six trials refused, three of them blew up to about 1e+23 | crawl, 7.13e-16 |
| 4 | nine trials refused (six blew up), stop | 12 steps in all, ended at 1.68e-16 |
| end | 5 steps, 2.54e-22, Delta - truth -2.6096e-11, 12836 s | 12 steps, 1.68e-16, Delta - truth -2.0184e-11, 27580 s |

The blown-up trials are the nine failed projections of the counts (`failed: 9`). The smallest pivot fell from 1.4e-19
at step 1 to 2.1e-27 at step 2. The planted truth's own octo-double residual is 3.58e-20.

## What a valid C2 needs (the coordinator's decision)

00c3963f's two options in planted and wall on the #777 code (main plus that commit), then the queue from s0_D252.
Nothing was rerun, and no file of the coordinator's was edited.

## Recommended task

Make `octo_corrector.py`'s `_parse` refuse a flag that is not in its defaults (exit 2 and name it), with a control
that passes a made-up `--reseed_x 1` and must fail. Why: the queue's two re-seeder flags were dropped without a word,
and the 3.6 h run did not test what its criterion says. It depends on nothing.

# The second stop: the rerun on 165b1da3 (2026-11-15 03:29 UTC)

The rerun had #713's re-seeder settings. Its first trial matched #713's to every printed digit (max|F| 2.48e+22, raw
|dz_t| 1.200e+17). It exited 1 where 0 was expected, after 5 steps at pinned max|F| 4.42e-32, above the 1e-40 bar.

| step | lam | \|F\| after | \|dz\| after | smallest pivot | taken by |
|---|---|---|---|---|---|
| 0 | 1/64 | 3.34e-12 | 1.99e-11 | 2.3e-14 | own test (as #713) |
| 1 | 1/16 | 3.13e-12 | 1.86e-11 | 2.3e-14 | own test (as #713) |
| 2 | 1 | 7.19e-16 | 7.41e-16 | 2.2e-14 | own test (as #713) |
| 3 | 1 | 4.42e-32 | 1.10e-05 | 1.2e-19 | the drop (`by_drop` in the JSON) |
| 4 | none | | | 7.3e-31 | all 9 trials refused, at max\|F\| 2.0e+51 down to 5.6e+34 |

The run used 16755 s and made 19 failed projections. Its Delta lies 2.0184e-11 below the planted truth, as #713's
does, and the two agree to 2.09e-17 (rerun minus #713). The stopped run on 8e10d127 lies 5.91e-12 lower. The truth's own
octo-double residual is 3.58e-20, twelve orders above the rerun's final point.

## Discrepancy: a step taken by the drop prints no trial line

In `newton_od`'s own-test branch, the outer condition prints when `by_drop` holds, but the inner one,
`verbose >= 2 or (verbose and not ok)`, does not. So at the default verbosity, a step accepted by the drop logs only
its `on N:` line. It never says "accepted by the full step's drop", and only the JSON's `by_drop` records it (step 3
here, step 1 of the stopped run).
