# I1025-win2: win2's share of #1025: k_c 63 lambda_1 at D 15 and 15.5 is in I1025-win2c, the full double-double M determinant signs at D 18 and D 17.5 are here

Machine win2 (desktop-pc, Windows 11, Core Ultra 7 265K, 20 threads, 95 GB), the win2 build session. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1025.

This folder holds the dd-M work only; each subfolder has its own README.md (first line `# I1025-win2/<name>: ...`) with its setup, the readings fixed before the run and its result.

| subfolder | what it holds |
|---|---|
| `d18/` | `ell_ddm.py det` at D 18, k_c 63 (winb's leap state), at lambda 1.788704083622953, 1.8 and the two outer grid points 1.752930001950494 and 1.824478165295412, with xfkappa's criteria quoted, the selftests and the readings. The four points (selftests, then 1.7887, the two outer points, 1.8); pushed whole after the last point ended |
| `d18_snapshot_outer/` | copies of the finished files of the three D 18 points (the two outer points and 1.7887) at the time of the #1025 post of the outer result (raw 521b13f2), with the README of `d18/` as it stood |
| `d17p5/` | `ell_ddm.py det` at D 17.5, k_c 63 (winb's state `sol_l1kc63Fw1025_D17.5000.npy`) at lambda 1.9072222575778963 and 1.9472222575778963 around winb's hybrid root 1.9272222575778963. The two points; pushed whole after they ended |

Other win2 folders of this issue: `I1025-win2b/` (win2b's k_c 55 re-solves), `I1025-win2c/` (k_c 63 lambda_1 at D 15 and 15.5 with signtests), `I1025-win2d/` (the venv with multidouble 5.1.0 and its planted dd_logdet check).
