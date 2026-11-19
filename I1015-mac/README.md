# I1015-mac: logs of P6 route 3's head j < 2 nu, certified uniformly in nu

Machine: mac (Apple M5), agent xfkappa. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1015

Code: branch wip/p6-route3-head of choptuik-large-d (c9876111), `solver/proof/route3_head.py`, venv-314 (python-flint
0.9.0, FLINT 3.6.0). One process at nice 10, two at most. Notes: notes/P6_route3.md section 11.

- `route3_head_scope.log`: `--scope`, the exact recursion over the head at nu = 3..21, its sums and termwise majorants
- `route3_head_lemmas.log`: `--lemmas`, the closed forms and inequalities of the closed form G; PASS
- `route3_head_check.log`: `--check`, B7 against the exact recursion at every head j, nu = 3..21, and sum B <= G at
  nu = 3..201; PASS
- `route3_head_check_plant.log`: `--check --mutate=plant`, the planted violation caught in all 30 runs; FAIL, exit 1
- `route3_head_check_gsmall.log`: `--check --mutate=gsmall`, G / 100; FAIL, exit 1
- `route3_head_certify.log`: `--certify`, the head sums for nu <= 99 at 512 bits, Lambda_head and the whole sum's
  constants
