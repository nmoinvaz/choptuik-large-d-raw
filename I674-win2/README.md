# I674-win2: the strong-row chord (--od_strong 4) on #603's class A refusals, A/B

Machine win2 (Windows 11 desktop, Intel Core Ultra 7 265K, 20 threads, 96 GB), 9 threads per run. Issue https://github.com/nmoinvaz/choptuik-large-d/issues/674 (queued by the coordinator on the agent-msg channel, message 1794568351271-0, 2026-11-13: after #664, before #657).
Code: worktree `D:\choptuik-i674` at origin/main 58628d94 ("octo_corrector: a strong-row chord after the corrector's first step"); venv-i600 (the #600 build, hpkernel sha256 4ede9afe..., the kernel #603 runs on; the change is Python only). #603's chain is read in place and left running.
Runs (`run_674.sh`, one after the other): `anm_run.py ... --steps 1 --a0 <a> --od_accept natural [--od_strong 4]` from `I603-win2/chain/anm_pin3_D<base>.npz`, #603's other flags, at #603's own a for the attempt (attempt 0 of the step in its `anm_run.jsonl`, exact):

| attempt (class A) | base state | a0 | arms |
|---|---|---|---|
| 244.637 -> 245.637 | D244.6366 | 1.0 | A (chord), B (control: natural only) |
| 247.043 -> 248.019 | D247.0429 | 0.9765625 | A, B |
| 248.630 -> 249.393 | D248.6298 | 0.762939453125 | A; B is #644's natural run (`../I644-win2/natural/`) |
| 251.886 -> 252.613 | D251.8859 | 0.7275957614183426 | A, B |

Arm A: `--od_accept natural --od_strong 4`; arm B: `--od_accept natural`. A refused first attempt halves a and the run goes on to the retry. Outputs `<attempt>_armA/`, `<attempt>_armB/`, logs `<attempt>_armA.log`, `<attempt>_armB.log`, starts and exits in `exits_674.txt`.

Report (#674, the coordinator's message): per attempt and arm, the chord lines ("on 0 chord j: max|F| ..., |dw| ...") and its verdict line, then each Newton step's |F| and |dz|, converged or refused, and the seconds; where arm A converges, its Delta against #603's state at the same D_str to 1e-40, or the task fails. Acceptance of #674: `hp/newton_od_toy.py` passes with the chord on and its controls fire (the coordinator's); on each refused attempt max|F| <= 1e-60 at the attempt's D, or the task reports where the chord or the following Newton steps stop.

Results follow when the runs end.
