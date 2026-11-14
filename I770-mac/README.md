# I770-mac: winding counts of the D = infinity perturbation determinant of the axion-dilaton (kappa = 1) inner CSS

Machine: the coordinator's Mac (Apple M5), agent xfkappa, one process at nice 10.
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/770
Code: `solver/matter/css_inner_pert.py` (count, root, det, check) of choptuik-large-d, main 3e096e26 (worktree
choptuik-large-d-xf-770); `check` from branch wip/xf-kappa 7dc93151, whose error metric is the one valid at kappa != 0.

| file | what |
|---|---|
| `pilot.sh`, `pilot.log` | the pilot: `check 1`, the secant roots from 2.1 and 1.1 at settings A, B, C, det M at conjugate points, box B at setting A |
| `check_k1.jsonl` | `css_inner_pert.py check 1` (PASS): exact modes' series, M singular at lambda = 0, 1, 2 |
| `roots_k1.jsonl` | lambda = 2 and 1 by secant at settings A, B, C |
| `conj_k1.jsonl` | det M at 1.3 +- 2.1i and 0.7 +- 6.5i, settings A and B (det M(conj lam) = conj det M(lam)) |
| `queue1.sh`, `queue1.log`, `counts_k1.jsonl` | winding counts of boxes A, B, S, C and the wide box W (0.05 < Re < 8, \|Im\| < 3 omega) at settings A and B |
| `controls_k1.jsonl` | box B with a zero planted at 3 + 1i, and with `--mutate=nometric` |
