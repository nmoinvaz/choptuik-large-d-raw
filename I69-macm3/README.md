# I69-macm3: the D 16.76 and 8.25 mode counts recounted at M 32

Machine: macm3 (Apple M3, 4 performance + 4 efficiency cores, 24 GB RAM, macOS 26.3.1), venv-macm3 (python-flint 0.9.0, FLINT
3.6.0, hpkernel 0.1.0 neon), main d9fab0bc, modecount_cx built in I68-macm3. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/69

From the repository root with the venv's bin first on PATH (the jobs call python3), 1 thread each, the two in parallel, nice 10,
caffeinate -is: bash hp/modecount_local.sh 1 (D 16.76, M 32) and bash hp/modecount_local.sh 2 (D 8.25, M 32). Round A runs them
as written, which recounts from the evaluation caches hp/data/modecount_<tag>_evals.jsonl. Round B repeats them with those caches
(and any saved state) moved to october_inputs/, so that this build re-converges and re-evaluates every determinant. Each .cmd has the
exact line, exits.txt the exits and wall times, awake.log the awake times (pmset). The hp/data files a round creates or changes are
copied to hp_data_after_<round>/ and the tracked ones restored.

Round A, as written (2026-11-08 07:27:51 UTC; main d9fab0bc): both jobs exit 1 within 1 s (exits.txt). modecount_wind.py refuses to
write: "hp/data/modecount_D16.7600_M32.log: not in a task folder of the raw-data repository ... --allow_unraw writes it anyway"
(hp/raw_out.py, AGENTS.md "Raw output goes to the raw-data repository"). The script's own option for this is --data=DIR, which
holds the cache, the log and the record and must lie in a raw-data task folder. Neither --data nor --allow_unraw is in the
issue's commands, and either changes the command, so nothing was run beyond the refusal. hp/data is unchanged (git status
clean), job1_D16.76.log and job2_D8.25.log hold the refusal, job 2's also "resampled state from modecount_state_D8.2500_M32.npz".
