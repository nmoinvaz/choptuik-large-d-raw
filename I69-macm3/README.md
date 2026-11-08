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

Second attempt (the coordinator chose option a on 2026-11-08 07:29 UTC: --data=<raw folder>/I69-macm3/data_A or data_B; main d9fab0bc).
The two python lines of jobs 1 and 2 of modecount_local.sh, in parallel, 1 thread each, nice 10, caffeinate -is. Awake time equals wall
time in every run (awake.log).
  Round A (data_A holds copies of the October caches): both exit 0 in 0 s. "done: 73 evaluations in the cache (0 new)" and "68 ... (0 new)".
    The 8 box lines of each log equal October's (october_logs/, which have Windows line endings, so a byte diff flags every line).
  Round B (data_B empty; for D 8.25 the saved hp/data/modecount_state_D8.2500_M32.npz kept in october_inputs/): D 16.76 exit 0, 267 s,
    73 new determinants; D 8.25 exit 0, 711 s, re-converged from the M 48 state (|F| 7.5e-08 in the layout, 8.6e-28 after Newton, as in October),
    68 new determinants. compare_B_october.py against the October caches (data_A) and logs:
      D 16.76: 73 of 73 points shared, ln|det|, arg and pivot minimum differ by exactly 0; 8 of 8 box lines identical.
      D 8.25: 68 of 68 points shared, ln|det| differs by at most 2.8e-14 (relative 1.7e-16, one ulp), arg by 0, pivot minimum by 0; 8 of 8 box
        lines identical. The re-converged state equals October's saved one in all 1409 entries (state_B_vs_october.txt).
  hp/data: the only tracked file changed was modecount_state_D8.2500_M32.npz (rewritten by round B), copied to hp_data_after_B/ and
  restored; hp/data is clean.
  Provenance of the October files, from line endings: the D 16.76 and D 8.25 caches and logs were written on Windows (every line ends in CR),
  the D 30 M 48 cache, circles and log were not (no CR), and the D 30 M 48 kf13 cache is mixed (80 of 98 lines).
