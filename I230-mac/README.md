# I230-mac: positions of the extra zeros of det M at D 61.03, M 48 (kf 21 and kf 23), and small circles around them

Machine: mac (Apple M5, 10 cores, macOS 27, shared with #208's two CAPD processes), venv-314 (Python 3.14.7 by uv,
hpkernel and multidouble NEON, python-flint 0.9.0, modecount_cx cp314 build of 2026-11-08 16:26 from the main
checkout). Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/230. Code: branch wip/i230 of the main
repository (hp/modecount_moment.py, hp/modecount_moment_planted.py, hp/modecount_circle.py,
hp/modecount_circle_planted.py). Inputs, read from the raw-data repository at 6e2e394 (git archive into a scratch
directory, nothing pulled here): I212-macm3/data (kf 23 count, 776 determinants), I212-macm3/reeval159/data (#159's
kf 21 count re-evaluated, 707 determinants), the saved states I212-macm3/hp_data_after/ (kf 23) and
I159-macm3/hp_data_after_kf21/ (kf 21, byte-identical to reeval159's copy), copied into the worktree's hp/data for the
circles and not committed.

Files:
- planted/: the planted tests' logs, each named by the commit it ran at (the moment code's v1 and v2 failed, v3
  passed; the circle test's v1 passed, v2 failed at n0 = 16 in one case, v3 at n0 = 20 passed; each with its
  controls).
- moments.jsonl, moments_kf23.log, moments_kf21.log: hp/modecount_moment.py on the two caches (no new determinant).
- repro_check.py, .log, .jsonl: two of #212's determinants recomputed here.
- noise_check.py, .log, .jsonl: the same matrix through hpkernel's LU, the noise floor of ln|det M|.
- data/: the circles' determinants (modecount_<tag>_evals.jsonl), logs and records (circles_*.jsonl).
- circles_*.log: the circle runs' output.
- t_check.py and its output: the stretch of #212's edge Im = y2 that the kf 23 count left at the initial spacing.
