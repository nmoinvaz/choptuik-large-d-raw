# I1101-mac: the --kappa_mm option of d18_secant.py, tested on #1102's k_c 31 state (D 10.5, lambda 2.87)

Coordinator (t5), Mac, 2026-11-27 15:52 UTC. Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1101.
Code: `solver/matter/d18_secant.py` on `wip/ell1-kappa-mm` (the commit after d4b6b6ce), python ~/venv-1025dd
(its multidouble has dd_logdet; venv-314's does not), block 12 ddm, 1 thread. State and record: raw I1102-mac/in
(f07a8984, e5a87ec5).

| scan | steps | ln abs det | f64 ln abs det |
|---|---|---|---|
| plain | 1748 | -430.29522444239035 | -430.29522444197926 |
| --kappa_mm=0.7 (the record's kappa: the control) | 1748 | -430.29522444239035 | -430.29522444197926 |
| --kappa_mm=0.35 | 3490 | -429.6003578750087 | -429.60035787534053 |

The control is bit-identical to the plain scan; kappa 0.35 moves ln abs det by +0.695 at the same state.
