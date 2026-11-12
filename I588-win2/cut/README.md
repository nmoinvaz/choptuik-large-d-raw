# I588-win2/cut: the replica spread of the R 0.06 circle on lambda_phys against the cut kf

Machine win2 (Windows 11 desktop, 20 threads), 3 workers of one thread each. Issue https://github.com/nmoinvaz/choptuik-large-d/issues/588 (closed; this is the recommended task of its closing summary, approved by the coordinator at 16:22 UTC, 2026-11-12, and posted as a comment on #588).
Code: worktree `D:\choptuik-i573` at main 80b5056 (`hp/modecount_circle.py` `circle()`, `hp/modecount_common.py` `setup`), venv-t126's python, the same replica machinery as `../replicas_588.py`.

**Design (fixed before any replica was evaluated: `predictions_cut.json`).** One circle per cut, centre (2.044645, -0.00032), R 0.06, n0 20, tol pi/4: the circle of #573 that holds lambda_phys = 2.0435 at kf 22 and 25.
Cuts kf 21, 23, 24, 26, 28, 29; per cut 10 shifted replicas (tags 1..10, every argument of `circle()` moved by 1 to 3 ulp in Re and Im) and 2 controls (tags a, b: rep 0, no move, each evaluated freshly; they must agree bit for bit).
The kf 22 and kf 25 values of the same circle come from `../replicas_588.jsonl` (s 1.80e-8 and 1.10e-6); kf 27 has no lambda_phys circle in #588.

Files: `cut_588.py` (`run`, `pilot KF`, `--selftest`), `analyze_cut.py` (`--selftest`, `--mutate=control`), `predictions_cut.json` (the predicted s per cut, criteria P1 to P8), `cut_588.jsonl` and `cut_588_evals.jsonl` (written by the run), `cut_588.log`.

Command: `cd I588-win2/cut && python cut_588.py run --workers 3` (resumes), then `python analyze_cut.py`.

Results follow below when the run ends.
