# I588-win2/cut: the replica spread of the R 0.06 circle on lambda_phys against the cut kf

Machine win2 (Windows 11 desktop, 20 threads), 3 workers of one thread each. Issue https://github.com/nmoinvaz/choptuik-large-d/issues/588 (closed; this is the recommended task of its closing summary, approved by the coordinator at 16:22 UTC, 2026-11-12, and posted as a comment on #588).
Code: worktree `D:\choptuik-i573` at main 80b5056 (`hp/modecount_circle.py` `circle()`, `hp/modecount_common.py` `setup`), venv-t126's python, the same replica machinery as `../replicas_588.py`.

**Design (fixed before any replica was evaluated: `predictions_cut.json`).** One circle per cut, centre (2.044645, -0.00032), R 0.06, n0 20, tol pi/4: the circle of #573 that holds lambda_phys = 2.0435 at kf 22 and 25.
Cuts kf 21, 23, 24, 26, 28, 29; per cut 10 shifted replicas (tags 1..10, every argument of `circle()` moved by 1 to 3 ulp in Re and Im) and 2 controls (tags a, b: rep 0, no move, each evaluated freshly; they must agree bit for bit).
The kf 22 and kf 25 values of the same circle come from `../replicas_588.jsonl` (s 1.80e-8 and 1.10e-6); kf 27 has no lambda_phys circle in #588.

Files: `cut_588.py` (`run`, `pilot KF`, `--selftest`), `analyze_cut.py` (`--selftest`, `--mutate=control`), `predictions_cut.json` (the predicted s per cut, criteria P1 to P8), `cut_588.jsonl` and `cut_588_evals.jsonl` (written by the run), `cut_588.log`.

Command: `cd I588-win2/cut && python cut_588.py run --workers 3` (resumes), then `python analyze_cut.py`.

Note on the clock: `predictions_cut.json` says in its `written` field "16:30 UTC", a slip. The file was written at 16:26 UTC and committed at 16:27 UTC (raw commit 194c9351), before any replica was evaluated; the file is left as committed.

## Results (2026-11-12 16:32:59 to 20:59:25 UTC)

72 replica runs (6 cuts x 10 shifted replicas and 2 controls), 2160 determinants, 3 workers of one thread each, 15986 s (`cut_588.py run`, `cut_588.log`, exit 0; `cut_588.jsonl`, `cut_588_evals.jsonl`), the determinant 20 to 22 s while the machine also ran #603's chain, #594(b) and #551. All 60 shifted replicas resolve with winding +1. The analysis is `analysis_cut.txt` (`analyze_cut.py`; `--mutate=control` gives P4 FAILS, `mutate_control.txt`; `--selftest` passes), the per-odd-harmonic reading `odd_harmonics.txt` (post hoc).

| kf | s (10 replicas) | predicted (band, factor 3) | in band | s per kf step from the previous cut | controls a = b | replicas' own estimate / s |
|---|---|---|---|---|---|---|
| 21 | 1.88e-8 | 4.6e-9 (1.5e-9 to 1.4e-8) | **no**, 4.1 times | | equal | 0.98 |
| 22 (#588) | 1.80e-8 | | | 0.96 | | 0.66 |
| 23 | 1.24e-7 | 7.1e-8 (2.4e-8 to 2.1e-7) | yes (1.74) | 6.85 | equal | 0.96 |
| 24 | 1.04e-7 | 2.8e-7 (9.3e-8 to 8.4e-7) | yes (0.37) | 0.84 | equal | 1.02 |
| 25 (#588) | 1.10e-6 | | | 10.58 | | 0.87 |
| 26 | 1.09e-6 | 2.9e-6 (9.7e-7 to 8.7e-6) | yes (0.37) | 0.99 | equal | 0.96 |
| 28 | 7.27e-6 | 2.0e-5 (6.8e-6 to 6.1e-5) | yes (0.36) | 2.58 per step from 26 | equal | 1.43 |
| 29 | 8.83e-5 | 5.4e-5 (1.8e-5 to 1.6e-4) | yes (1.64) | 12.15 | equal | 0.48 |

| criterion (predictions_cut.json, as committed in 194c9351) | verdict |
|---|---|
| P1 s within the factor-3 band at 5 or more of 6 cuts | **holds**: 5 of 6 (23, 24, 26, 28, 29); kf 21 is 4.1 times above its prediction |
| P2 s increases at every neighbour pair of the eight cuts | **FAILS as written**: s(21) > s(22) and s(23) > s(24) (and 25, 26 are equal within 1%) |
| P3 the per-step ratio between neighbours in 1.5 to 8 for at least 6 of 7 pairs | **FAILS as written**: 0.96, 0.84, 10.58, 0.99 and 12.15 are outside |
| P4 the two controls agree bit for bit at every cut | **holds**: 6 of 6 (`--mutate=control` makes it fail) |
| P5 at least 9 of 10 shifted replicas resolve at every cut | **holds**: 60 of 60 |
| P6 s below 1e-4 at all six new cuts | **holds**: the largest is 8.83e-5 at kf 29 (just under) |
| P7 replicas' own estimate / s between 0.5 and 2 at 5 or more of 6 cuts | **holds**: 5 of 6 (kf 29 gives 0.48, just outside) |
| P8 the control zero within 3 s of the replica mean at 5 or more of 6 cuts | **holds**: 6 of 6 (offsets 0.2 to 2.1 s) |

**Why P2 and P3 fail: the design, not the data** (the coordinator, 19:31 UTC; #498, `plow_odd`). The cut keeps the odd harmonics k <= kf, so an even kf is the odd cut below it (kf 22 is 21, 24 is 23, 26 is 25, 28 is 27), and s is flat within the pairs (21, 22), (23, 24), (25, 26) by construction, each odd step adding one harmonic and jumping. The predictions treated every kf as a new cut. My check on this machine's states: kf 23 and 24 are byte-identical (sha256 71451956...), kf 21 and 22, and 25 and 26, differ (zh by up to 5.4e-10 and 7.4e-10, the solve's final F in the 4th digit), so the pair (23, 24) is one function with two independent sets of ulp moves and its spreads differ by 19%; the other two pairs have the same operator and states that differ below the determinant's rounding noise, and their spreads agree to 4% and 1%.

**The real measurement, per odd harmonic** (`odd_harmonics.py`, post hoc, not one of P1 to P8; pooled over each pair as a geometric mean, kf 28 standing for 27, which has no lambda_phys circle in #588):

| odd cut | spreads used | pooled s | ratio to the previous odd cut |
|---|---|---|---|
| 21 | 21: 1.884e-8, 22: 1.803e-8 | 1.843e-8 | |
| 23 | 23: 1.235e-7, 24: 1.041e-7 | 1.134e-7 | 6.15 |
| 25 | 25: 1.102e-6, 26: 1.091e-6 | 1.096e-6 | 9.67 |
| 27 | 28: 7.268e-6 | 7.268e-6 | 6.63 |
| 29 | 29: 8.828e-5 | 8.828e-5 | 12.15 |

s grows by **8.3 per odd harmonic** (geometric mean of 6.15, 9.67, 6.63 and 12.15; 4790 over the four steps from 21 to 29), all four ratios between 6 and 12. The model of the predictions (3.9 per step to 25, 2.65 beyond) used the wrong step: per odd harmonic it should have been about 8.

**`hypothesis_pair.json`** (written at 19:27 UTC before any kf 28 or 29 result was read, raw e7ad0188): H1 s(28) / s(26) = 6.66, inside 3 to 15, holds; **H2 s(29) / s(28) = 12.15, inside 4 to 20, H_pair is supported** (the smooth model gave 1.7 to 4.2). kf 28 is kf 27 and kf 29 adds one harmonic, so this is the one-harmonic ratio the coordinator named.

**Where the double-double circles stop being usable** (the issue's acceptance: the cut at which s first exceeds 1e-4). Measured: none up to kf 29 (8.83e-5). By the ratio 8.3 per odd harmonic, s at kf 31 is about 7.3e-4, so **kf 31 is the first cut above 1e-4 (extrapolated, not measured)**, and kf 30 equals kf 29 by #498. This is the rounding noise of the double-double determinant on an R 0.06 circle around lambda_phys; it scales with the radius R of the circle (the spread of a W = 1 circle is R |eps| / sqrt(n0)), so an R 0.36 circle has six times these bars. The exact determinant (--ball, #584, #594, #551) is not subject to it where it is smooth in lambda.

**What the bars are not.** The noise of one circle at one zero (lambda_phys); the other zeros of #588 at the same cut differ by a factor of a few. They leave out the truncation and state errors of the cut itself and say nothing of the exact determinant. Eight cuts (the six here and 22, 25 of #588) give the growth per odd harmonic, not a law: five odd cuts, one circle.

**Predictions that failed, reported and not changed:** P2 and P3 (above), and kf 21's miss in P1 (4.1 times above its prediction: the model's fall-off below kf 22 does not exist, kf 21 and 22 being one cut).

