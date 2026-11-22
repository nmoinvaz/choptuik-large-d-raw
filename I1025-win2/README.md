# I1025-win2: win2's share of #1025: k_c 63 lambda_1 at D 15 and 15.5 is in I1025-win2c, the full double-double M determinant signs at D 18 and D 17.5 are here

Machine win2 (desktop-pc, Windows 11, Core Ultra 7 265K, 20 threads, 95 GB), the win2 build session. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1025.

This folder holds the dd-M work only; each subfolder has its own README.md (first line `# I1025-win2/<name>: ...`) with its setup, the readings fixed before the run and its result.

| subfolder | what it holds |
|---|---|
| `d18/` | `ell_ddm.py det` at D 18, k_c 63 (winb's leap state), at lambda 1.788704083622953, 1.8 and the two outer grid points 1.752930001950494 and 1.824478165295412, with xfkappa's criteria quoted, the selftests and the readings. The four points (selftests, then 1.7887, the two outer points, 1.8); pushed whole after the last point ended |
| `d18_snapshot_outer/` | copies of the finished files of the three D 18 points (the two outer points and 1.7887) at the time of the #1025 post of the outer result (raw 521b13f2), with the README of `d18/` as it stood |
| `d17p5/` | `ell_ddm.py det` at D 17.5, k_c 63 (winb's state `sol_l1kc63Fw1025_D17.5000.npy`) at lambda 1.9072222575778963 and 1.9472222575778963 around winb's hybrid root 1.9272222575778963. The two points; pushed whole after they ended |

Other win2 folders of this issue: `I1025-win2b/` (win2b's k_c 55 re-solves), `I1025-win2c/` (k_c 63 lambda_1 at D 15 and 15.5 with signtests), `I1025-win2d/` (the venv with multidouble 5.1.0 and its planted dd_logdet check).

## d18mid (2026-11-21)

[d18mid/](d18mid/README.md): xfkappa's hybrid sign scan at D 18.1875 (k_c 63), lambda 1.70 to 1.95 at 0.01, two processes; README first, readings fixed before the run.

## d18hi (2026-11-21)

[d18hi/](d18hi/README.md): the cross-machine control (the Mac's D 18 point at lambda 1.8: agrees) and the D 18.1875 hybrid scan above the d18mid window, lambda 1.95 to 2.35: no robust change; README first, readings fixed before the run.

## d185map (2026-11-21)

[d185map/](d185map/README.md): the k_c 63 map at D 18.5 over lambda 1.00 to 2.60 (windows A = 2.40 to 2.60 and B = 1.00 to 1.55, B split in two) beside xfkappa's scans: two roots, 1.677016 (- to +) and 2.420394 (+ to -); README first, the restart record at its top.

## kc71_d185 (2026-11-21/22)

[kc71_d185/](kc71_d185/README.md): a third k_c at D 18.5: the k_c 63 state regridded to k_c 71 (--no-gamma, accepted at |F| 2.83e-10, 2772 steps) and scanned over lambda 1.55 to 2.49 at 0.02: roots 1.675995 (- to +, 63-near) and 1.809322 (+ to -, near neither); overall neither; README first.
