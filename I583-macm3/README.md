# I583-macm3: the pmin bound B = 3e-15 for the double-double noise floor, read on circle caches nobody had read (win2's I573 and I574)

Machine: macm3. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/583 (recommended by macm3 in #579's closing summary; B and its direction were fixed on the issue by the coordinator before the data were read: a point is at the noise floor when pmin < B = 3e-15; the prediction is that a circle closes if and only if every point on it has pmin >= B). Reading only, no computation: read_pmin.py (this folder) reads, in each circle folder of win2's raw output, the closure (res.jsonl: resolved, winding) and pmin of every evaluation of the cache (*_evals.jsonl), nothing else.

Test data read so far: I573-win2 (28 circle folders) and I574-win2 (16) from the raw repository (the push worktree of macm3 at origin/main after the fetch of 09:08 UTC). Not yet read: I582-win2 (not in the raw repository at that time) and macm3's own #518 circles (still running).

Acceptance (the issue's). The rule holds if every closed circle in the test data has all its points at pmin >= B; one closed circle with a point below B fails it, and then #569's and #571's verdicts stay open. The count of test points within a factor 2 of B is the margin.

## Results

Command: python3 read_pmin.py I573-win2 I574-win2 from the push worktree (exit 1 = a closed circle with a point below B); the full per-circle table is read_573_574.md.
