# T107-win2: the low-D leg with the Taylor predictor, from D 3.0438 toward D 3.03 at M 320 and M 384

Machine: win2 (Windows desktop, Intel Core Ultra 7 265K, 20 cores: 8 P + 12 E, no SMT, AVX2; 95.6 GB RAM; on AC). Worktree `..\choptuik-t106` at 10b2fd8 (feat/jet-all-sizes; the diff from e8e7b6f is hp/lowD_taylor_leg.py only, Python, so venv-t106's kernel stands, no rebuild). Run from `hp\` of choptuik-t106, venv-t106. Started after T106 D'' and D''' passed the start condition (each Newton < 1e-26 in <= 6 calls with the calls up to the crossing all lam 1; dd-Delta vs T105's p1 state 2.22e-31 at M 320 and 3.46e-29 at M 384, both <= 1e-20).
Comms entry: 2026-11-05 01:12 UTC cloud to win2 (Nathan's decision, LOW_D.md 15).

A: three M 48 smokes (none, halve, const), expected exits 0, 0, 1 as the Mac's T107-mac.
B: the two legs at once -- `leg_M320` (--state the p1 D3.0438 M 320 state, --targets 3.0425..3.03, --N 4 --newton_its 6 --halvings 2 --threads 8) and `leg_M384` (--threads 12). The Taylor predictor gives the start at each D from the previous point's z_1..z_4. The first target 3.0425 is where T105 C's cubic predictor stalled.
