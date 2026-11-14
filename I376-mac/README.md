# I376-mac: perturbation spectrum of the kappa = 0 inner CSS solution at D = infinity

Machine: the coordinator's Mac (Apple M5), agent xfkappa, one process at nice 10.
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/376
Code: `solver/matter/css_inner_pert.py` and `css_inner_pert_eqs.py` on branch wip/xf-kappa of choptuik-large-d.

| file | what |
|---|---|
| `queue1.sh`, `queue1.log` | the runs, in order, with their exits |
| `roots_k0.jsonl` | secant roots of det M(lambda) at kappa = 0, settings A (r0 0.1, r1 0.3), B (0.1, 0.25), C (0.09, 0.3); the lambda = 2 and 1 controls, lambda_osc, and lambda_osc at rtol 1e-13 and 60 digits |
| `mut_k0.jsonl` | det M and its singular values at lambda = 1, 2, 1.5 with and without the mutations nometric and hamsign, and the secant from 2.1 under each mutation |
| `counts_k0.jsonl` | winding numbers of det M in the boxes A, B, C, S (matter/COMPLEX_CRITICAL.md section 2's boxes with the D = infinity omega), with a planted zero and a mutation as controls |
| `queue3.sh`, `queue3.log`, `conj_k0.jsonl` | det M at lambda and conj(lambda) (conjugation symmetry) and the secant from conj(lambda_osc), settings A, B; run at the end of I377-mac's queue5 |
| `inner_check.jsonl` | `css_inner_pert.py check` at kappa = 0 and 0.5 (run in I377-mac's queue5) |
