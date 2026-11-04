# T105-win2: thread scaling at M 320 and the low-D leg restarted from D 3.044375, on win2

Machine: win2 (Windows desktop, Intel Core Ultra 7 265K, 20 cores: 8 P + 12 E, no SMT, AVX2; 95.6 GB RAM; on AC). From `hp\` of the t98 worktree (origin/main, pulled to the fixed main that refuses a killed-run checkpoint). hp/src changed for the jet feature, but `test_ckpt_resume.py` and the kernel functions this task uses run on the installed T98 build, so no rebuild (venv-hp). All cores, normal priority, no affinity.
Comms entry: 2026-11-04 06:07 UTC cloud to win2.

A: `test_ckpt_resume.py` — ckpt_resume.log ("all 5 cases pass", exit 0); ckpt_resume_mutate.log (cases 2-4 fire, exit 1).
B: thread scaling — `highm_check.py profile --M=320 --threads=N --reps=1 --no_dtau_split` at N = 4, 8, 12, 16 (profile_M320.jsonl, profile_M320_tN.log) and `scaled --Ms=192,256 --threads=N` at N = 4, 16 (scaled_tN.log). N* = smallest N with newton_mixed within 1.1x of the fastest.
C: the `down25f` leg from D 3.044375 (targets 3.04375 .. 3.005), `lowD_highM.py --threads N*` from the 6.6e-04 predictor on the fixed main; down25f.jsonl, down25f_points.jsonl, down25f.log, states/.
