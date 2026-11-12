# I583-macm3: the pmin bound B = 3e-15 for the double-double noise floor, read on circle caches nobody had read (win2's I573 and I574)

Machine: macm3. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/583 (recommended by macm3 in #579's closing summary; B and its direction were fixed on the issue by the coordinator before the data were read: a point is at the noise floor when pmin < B = 3e-15; the prediction is that a circle closes if and only if every point on it has pmin >= B). Reading only, no computation: read_pmin.py (this folder) reads, in each circle folder of win2's raw output, the closure (res.jsonl: resolved, winding) and pmin of every evaluation of the cache (*_evals.jsonl), nothing else.

Test data read so far: I573-win2 (28 circle folders) and I574-win2 (16) from the raw repository (the push worktree of macm3 at origin/main after the fetch of 09:08 UTC). Not yet read: I582-win2 (not in the raw repository at that time) and macm3's own #518 circles (still running).

Acceptance (the issue's). The rule holds if every closed circle in the test data has all its points at pmin >= B; one closed circle with a point below B fails it, and then #569's and #571's verdicts stay open. The count of test points within a factor 2 of B is the margin.

## Results

Command: python3 read_pmin.py I573-win2 I574-win2 from the push worktree (exit 1 = a closed circle with a point below B); the full per-circle table is read_573_574.md.

Result: 44 circles, all closed (resolved), 1532 evaluations. 38 circles have all their points at pmin >= B (their smallest pmin is 4.52e-15, 22 to 44 evaluations each). **6 closed circles have points below B, 40 points in all**: kf 22 2.35 +0.75i and 2.35 -0.75i (63 evaluations each, 9 below B, smallest pmin 1.284e-15; winding +1), kf 25 2.35 +0.25i and 2.35 -0.25i (61 each, 4 below B, smallest 2.69e-15; winding +1), kf 27 1.85 +1.25i and 1.85 -1.25i (48 each, 7 below B, smallest 1.419e-15; winding +1). The rule FAILS. The smallest pmin over all 1532 evaluations is 1.284e-15; the 40 points below B lie between 1.28e-15 and 3e-15. Points within a factor 2 of B: 78 (58 in the six circles, 20 in the others). The six failing circles are the six with the most evaluations (48 to 63 against 22 to 44 for the clean ones).
