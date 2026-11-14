# I771-mac: a second implementation of the D = infinity CSS perturbation determinant (kappa = 0), its checks and zeros

Machine: mac (Apple M5), agent xfchecks. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/771

Script `solver/matter/css_inf_jump.py` of choptuik-large-d (branch wip/i771), Python 3.14 venv-314 (numpy, scipy,
sympy, mpmath), written without reading css_inner_pert.py or css_inner_pert_eqs.py. From `solver/matter/`:

- `derive.log`: `css_inf_jump.py derive` (exit 0): the ODEs from the inner PDE in sympy, the exact modes (lambda = 2,
  1, 0, i omega, the reparametrizations) and the control (lambda = 2.01), which is not a solution.
- `planted.log`, `planted_mutate_coef.log`: the 2F0 test (exit 0) and its control with one coefficient off by 0.1%
  (exit 1, as it must).
- `bg.log`, `bg.jsonl`: `bg`, the background selection by Newton from CSS.md's ten digits.
- `probe.py`, `probe.log`: D(lambda) at sample points. `roots.py`, `roots.jsonl`, `roots.log`: the zeros near 2 and
  0.53 + 7.93i at seven settings (r0, r1, alpha, rtol). `exits.txt`: the exits.
