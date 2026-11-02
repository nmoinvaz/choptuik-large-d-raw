# T100-win2: the continuation below D = 3.045 (lowD_highM.py), a leg from T82-win's down25c: the half step to 3.04375, then steps of 0.0025 to 3.005

Machine: win2 (Windows desktop, Intel Core Ultra 7 265K, 20 cores: 8 P + 12 E, no SMT, AVX2; 95.6 GB RAM; on AC). Run from `hp\` of the t98 worktree (origin/main 87099ba) with venv-hp active (Python 3.12.8, numpy 2.5.4, scipy 1.18.1, mpmath 1.3.0). hpkernel is the T98 build (avx2, multidouble 1.8.0 commit 00c6dfd; hp source unchanged since 0f0e20c, so no rebuild). `--threads 6`, below-normal priority, run beside T99.
Comms entry: 2026-11-02 22:34 UTC cloud to win2.

The leg `down25d` from T82-win's `down25c.jsonl.progress.json` (targets 3.04375, 3.0425, ..., 3.005), with the history states from the worktree's `data/lowD_states` and `T82-win/states`. Output here: `down25d.jsonl`, `down25d_points.jsonl`, `down25d.log`, and `states/`.
