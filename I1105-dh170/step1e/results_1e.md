| re-solve | from | D | \|F\| | source \|F\| | steps | source steps | Delta | Delta change | psi-constraint | re-solve s |
|---|---|---|---|---|---|---|---|---|---|---|
| r165b | r165 | 16.5 | 2.0080e-10 | 2.0094e-10 | 2481 | 2481 | 1.0117784460020298 | -5.305e-11 | 3.8592e-04 | 1477 |
| r155 | continuation c155 | 15.5 | 2.1665e-10 | 2.1655e-10 | 2647 | 2647 | 0.9924204768837295 | -1.456e-07 | 9.1557e-05 | 2319 |

| D | state | role | run | status | final bracket | root (lam_lin) | evals |
|---|---|---|---|---|---|---|---|
| 16.5 | r165 | re-solve (step 1d) | widened | tol | (2.1459391706439113, 2.1459392206439114), width 5.00e-08 | 2.145939216 | 12 |
| 16.5 | r165b | re-solve of r165 | first | nonrobust | (2.1455491275663663, 2.1455572694142955), width 8.14e-06 | 2.145549303 | 11 |
| 15.5 | c155 | continuation | first | tol | (2.3365769908015386, 2.3365770408015387), width 5.00e-08 | 2.336577038 | 10 |
| 15.5 | r155 | re-solve | first | nonrobust | (2.336051290700417, 2.336092582233774), width 4.13e-05 | 2.336051462 | 9 |

- T = root(r165b) - root(r165): lam_lin difference -3.8991e-04; range from the brackets -3.9009e-04 .. -3.8190e-04
- verdict on T: |T| > 0.0003: the re-solve scatter at D 16.5 is itself of order 1e-3 or more (the whole bracket range is outside the bar)
- offset(15.5) = root(r155) - root(c155): lam_lin difference -5.2558e-04; range from the brackets -5.2575e-04 .. -4.8441e-04
- offset(D), re-solve minus continuation: D 15.0: -5.264e-04, D 15.5: -5.256e-04, D 16.0: +8.590e-04, D 16.5: +3.252e-03 (D 16: step 1b, 1c; D 15, 16.5: step 1d; D 15.5: this step)
- D 15.5 has no bar: reported as measured
