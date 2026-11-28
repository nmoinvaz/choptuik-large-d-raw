# I1110-macm3: a chord state on R2's step map against R2's root, l = 1, k_c 127, D 23.0 (#1110)

Machine: macm3 (MacBook Air M3, 8 threads, 24 GB), runner t5-macm3, account claude-me2. Written 2026-11-28 08:39 UTC, before the runs.
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1110 (its body is the record). Order: the coordinator's hc task (2026-11-28 08:38 UTC), budget 6 threads, nice 10.
Git over SSH and gh do not work on this Mac: code and raw by anonymous HTTPS, nothing pushed, no gh; the coordinator pushes and posts from the bundle and the post files.

Code: worktree ~/Source/choptuik-ell1fast at 693a4d79 (db7f9c60, the issue's pin, is its ancestor; i1101_weakdir.py differs from db7f9c60 by 3 lines, the root command's --b12=rust and --b12_threads),
work from solver/matter. Venv: ~/Source/venv-macm3-1058b (Python 3.14.3, numpy 2.5.4, scipy 1.18.1, ellrs neon accelerate). The root command imports d18_secant from D18_DIR
(default ~/Source/choptuik-kmm/solver/matter, absent here): run with D18_DIR=$HOME/Source/choptuik-ell1fast/solver/matter, so it is the worktree's d18_secant.py.
Raw inputs (raw main 85ccc6df7, blobs checked with git hash-object --no-filters): R0 = I1101-dh170/in/sol_l1kc127k070w2_D23.0000.npy (90d3e655) and l1kc127k070w2.jsonl (d1a3a641);
R2 = I1101-dh170/in/sol_l1kc127k035w2_D23.0000.npy (25ba3a91) and l1kc127k035w2.jsonl (9111bfca; 8351 steps, |F| 3.1242e-10).
The jac and svd npz stay local, in ~/Source/I1110-macm3-local/ (outside the raw clones); everything else is in this folder.

Question (the issue): at k_c 55, D 16 a chord state on K35's map differed from the LM state by 1.95e-10 at equal |F| yet its root was 4e-3 away. At k_c 127, D 23.0 the order p = 2.39
was read from R0 0.045968, R1 0.09500769 and R2 0.117824909. This runs the same control: R0's state re-solved by chord steps on R2's map (kappa 0.35), its root against R2's.

## Commands (from solver/matter; OPENBLAS_NUM_THREADS=6 VECLIB_MAXIMUM_THREADS=6; run_1110.sh runs 1 to 6; caffeinate -is nice -n 10, each step capped at 7200 s)
1. python i1101_weakdir.py jac REC STATE 23.0 jac_r0.npz --pin=90d3e655,d1a3a641
2. python i1101_weakdir.py svd jac_r0.npz svd_r0.npz
3. python i1101_weakdir.py chord svd_r0.npz REC STATE 23.0 kappa=0.35 sol_chord035_D23.0000.npy
4. python i1101_weakdir.py chord svd_r0.npz REC STATE 23.0 kappa=0.34 sol_chord034_D23.0000.npy   (the control)
5. python i1101_weakdir.py coords svd_r0.npz STATE chord035=sol_chord035_D23.0000.npy
6. (added, for the issue's bar 3 "state difference |z_chord - z_R2| by band": the same command with R2's state as base) python i1101_weakdir.py coords svd_r0.npz R2STATE chord035=sol_chord035_D23.0000.npy
   (the bands are R0's SVD's; coords allows states of other step maps)
Then, RAYON_NUM_THREADS=2 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1, 14400 s cap (run_root.sh):
7. python i1101_weakdir.py root sol_chord035_D23.0000.npy 0.10 0.13 root_chord035.jsonl --tol=1e-6 --b12=rust --b12_threads=2
   (the issue says --b12=fast, the order says rust; rust, as in #1109's roots, is the order's.) Widen (0.10, 0.13) once to (0.05, 0.16) if it does not bracket, and say so.

## Bars (#1110's, written before the runs)
1. The chord state's .map.json has 8351 steps exactly (R2's) and |F| <= 5e-10; otherwise stop and report (the coordinator then adds a map from R2's own steps).
2. Control that must fail: kappa=0.34 gives a step count other than 8351; if it gives 8351 the count cannot tell maps apart and bar 1 means nothing: stop.
3. delta = root(chord) - 0.117824909 (R2's refined root), and the state difference |z_chord - z_R2| by band:
   |delta| <= 2e-3: the scatter does not hide R0-R2's order (#1104 may use it); |delta| >= 7e-3: it does (#1104's kappa step waits for #1111's roots); between: mixed.

## Log
- 2026-11-28 08:39 UTC: README written before the runs.
