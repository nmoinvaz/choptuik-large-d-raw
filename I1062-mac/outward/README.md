# I1062-mac/outward: route 3's constants rerun with outward-rounded printing (#1062's finding 1)

Mac (Apple silicon, macOS 27), python-flint 0.9.0, FLINT 3.6.0, venv-314. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1062

The coordinator's fix of the review's finding 1: `solver/proof/outward.py` prints each certified upper bound rounded up
(lower bounds rounded down), and `route3_head.py`'s `C_TAIL` holds the upper ends 28.4492, 56.8735 and 4.76611e6.
Run by `run.sh` from `solver/proof/` of branch fix/route3-outward, in this order (exits in `exits.txt`):

| log | command | exit |
|---|---|---|
| outward.log | `outward.py` (self-test) | 0 |
| outward_mut.log | `outward.py --mutate=nearest` (control, must fail) | 1 |
| bound_constants.log | `route3_bound.py --constants` | 0 |
| bound_constants_J100.log | `route3_bound.py --constants --J0=100` | 0 |
| head_certify.log | `route3_head.py --certify` | 0 |
| head_check.log | `route3_head.py --check` | 0 |

Λ^head = 0.011013, 0.058818, 3.3073; C = 28.4492, 56.8735, 4.76611e6; the whole sum 1.0534, 2.1427, 174640.
