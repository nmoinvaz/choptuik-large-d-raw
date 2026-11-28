# I1102-mac/fastjac: ell_fastm.jacobian_fast, the l = 1 solver's Jacobian by the variational map, and its checks

Machine: Nathan's Mac (coordinator t5), load 40-60 from other projects, 2 BLAS threads, nice 10. Issue
https://github.com/nmoinvaz/choptuik-large-d/issues/1102. Code: wip/i1101-weakdir d435afe4 (ell_fastm.py) and 693a4d79
(ell_refine.py --jac fast), venv-1025dd. Inputs: I1025-mac/out/sol_l1kc31r1025_D10.5000.npy with l1kc31r1025.jsonl, and
I1105-dh170/step1b/sol_l1kc55u040_D16.0000.npy with l1kc55u040.jsonl.

| check | result | control (must fail) |
|---|---|---|
| selftest, k_c 15 toy state (`selftest_none.log`) | PASS; J's block 12 1.2e-15, Delta column 9.6e-15 | dcol: exit 1; coef: exit 1 |
| jaccheck k_c 31, D 10.5 (`jac31_none.log`) | PASS; 3.8x (7.1 s against 26.8 s) | dcol: exit 1 (14 lines); coef: exit 1 (13 lines) |
| jaccheck k_c 55, D 16 (`jac55.log`) | PASS; 5.5x (28.9 s against 158.8 s); blocks 0-11 <= 7.5e-15, block 12 3.3e-10 and 1.1e-10 | — |
| ell_refine k_c 31 to 39 at D 10.5, both Jacobians (`e2e.log`) | the same state: Delta 4.2e-10 apart, \|z\| 3.5e-9 apart, \|F\| 4.230e-12 and 4.236e-12; 608 s against 280 s (2.2x) | — |

Bar change before the k_c 31 pass: block 12's Delta column first failed at 1.257e-12 against 1e-12. The batch size alone
moves the complex step's own Delta column there by 1.3e-12 (1 member against 2, the same arithmetic; 1-3e-15 in blocks 0
and 6), so the horizon block's Delta column takes the state columns' 1e-8 bar (ell_fastm.compare_jac's docstring).
