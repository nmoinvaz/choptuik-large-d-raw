# T106-win2: hp built with the jet residual at every M, and the exact Taylor predictor at M 320, on win2

Machine: win2 (Windows desktop, Intel Core Ultra 7 265K, 20 cores: 8 P + 12 E, no SMT, AVX2; 95.6 GB RAM; on AC). Worktree `..\choptuik-t106` at origin/feat/jet-all-sizes a2f5d9a; venv-t106 (Python 3.12.8, numpy, scipy, maturin, mpmath). All cores, normal priority. Separate from T105's venv-hp and worktree (not touched).
Comms entry: 2026-11-04 06:14 UTC cloud to win2.

A: build hp (jet residual) via `hp/build.sh`, log in `hp_build/build.log`; record wall time and peak memory. Stops: compile error (first 60 lines, the fix is the coordinator's), or build above 3 h / 32 GB.
B: `ref` (M 48/64/80), `scaled` (M 192/256), `jet_check` (--N 16 --hs 1e-14,1e-13,1e-12 --kfreeze 13); ref.log, scaled.log, jet_check.log, jet_check.jsonl.
C: `anm_lowd` smoke (smoke/anm_lowd.jsonl).
D: the `anm_lowd` pilot at M 320, `--threads T` with T = max(4, 16 - N*) = 4 (N* = 12 from T105 B); pilot_M320.log.
