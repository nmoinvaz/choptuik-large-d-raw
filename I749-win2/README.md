# I749-win2: the kf 41 half of #749's box (D 61.0264, M 48), on win2

Machine win2 (desktop-pc, Core Ultra 7 265K, 20 threads), issue https://github.com/nmoinvaz/choptuik-large-d/issues/749.
macm3's `I749-macm3/` holds the kf 39 half, with the same criteria (its README).

`run_749w.sh` (written by the coordinator): the planted check `modecount_circle_planted.py --controls` (exit 0), then
#551's command (I551-win2/run_551.sh) at kf 41. That command runs one process with the lambda_phys control (R 0.2) and
the four R 0.36 circles at 2.85 +- 0.25i and 3.35 +- 0.25i, on 10 threads, from the worktree D:/choptuik-i749 at wip/i749
bd7df22f with #551's modecount_cx build and venv-t126. #551's build gave the same determinant digits as macm3's at D 30 (#442).
