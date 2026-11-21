# I1062-mac: logs of the independent review of P6 route 3's tail bound and head (#990, #1015)

Machine: mac (Apple M5), the #1062 reviewer subagent. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1062

Code: branch review/p6-route3 of choptuik-large-d (43e2ca8a), `solver/proof/review_p6/`, venv-314 (mpmath 1.3.0,
sympy 1.14.0; python-flint 0.9.0 and FLINT 3.6.0 only for amp_flint.py and cert_digits). One process at a time at
nice 10. Notes: notes/P6_route3_review.md. Every log except cert_digits.log is the rerun of record at 43e2ca8a
(2026-11-21 03:16-03:44 UTC), after the bot reviews of #1063; its numbers equal the first run's, up to formatting.

- `ampcheck.log`: PC1, the review's model against amp_flint.py run as a black box; PASS, worst 2.5e-37
- `ampcheck_droppair.log`: M6, one ordered lapse pair dropped; FAIL, exit 1
- `explicit.log`, `explicit.json`: the seven explicit sups (mpmath.iv adaptive bisection), PC2 (explicit terms, and
  explicit plus interior against the increment), PC3; PASS
- `explicit_demix.log`, `explicit_dropfar.log`, `explicit_g2.log`: M1, M2, M4; FAIL, exit 1
- `interior.log`, `interior.json`: Cr in B4 mode and tight mode by direct summation to j = 2000, P, W; PASS
- `interior_nuprefac.log`, `interior_dropii.log`: M3, M5; FAIL, exit 1
- `head_certify.log`, `head.json`: H_mu(nu) for odd nu = 3..99 in mpmath.iv, G(101), Lambda_head
- `head_check.log`: PC7, B7 against every head term at nu = 3..21; PASS
- `head_check_a0.log`: M7 (A0 / 100), which does not fire, exit 0 (notes section 6)
- `head_check_b7.log`: M7' (B7 / 100); FAIL, exit 1
- `constants.log`, `constants.json`: the assembled C'_mu, whole-sum constants and Lambda_head against the certificate
- `tailcheck.log`: PC9, the constants against exact increments, odd nu = 3..21, j < 1000; PASS
- `tailcheck_plant.log`: the planted violation; FAIL, exit 1
- `controls.log`: every control in one run, a mutation caught only on exit 1 with a printed failed check; PASS
- `cert_digits.log`: route3_bound.py's certified constants printed to 12 digits (for finding 1)
