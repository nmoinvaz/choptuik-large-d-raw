# I519-win2: does the period 2.74 in D appear in sigma_2..4 and in Delta's deviation from its trend?

Machine win2, issue https://github.com/nmoinvaz/choptuik-large-d/issues/519 (follows from #516). Analysis of existing logs and states, no new run. Interpreter `venv-t177` (numpy 2.5.4, mpmath).
`analysis_519.py` (selftest ok: a planted period 2.74 in a smooth trend in 1/n plus noise is found with null fraction 0.0%, a series without it is not, null fraction 44%) uses `../I516-win2/fit_516.py` (line-plus-one-sinusoid fit, period scanned from 1.1) with a null test of 1000 trials (pure line + white noise of the observed rms, period scanned the same way; null fraction = the fraction of trials whose amplitude / error is at least the observed) on (1) ln sigma_1..4 over D 228.13 to 237.13 (16 distinct D; `results_519.txt`), and (2) Delta's deviation from a polynomial in 1/n (n = D - 2, Chebyshev basis) of degree 5 and 7 at the 40 stored states of the clean chain from D 216.13 to 242.53 (crawlG, crawlI, crawlJ, probe03125, crawlL, probeH00390625; Delta exact from the four double parts of each state's last entry). `extra_519.py` adds the table of deviations, sinusoids of fixed period, and polynomial windows (`results_519_extra.txt`).

## Part 1: the singular values (same oscillation = period within 0.15 of 2.74 and null fraction below 1%)

| series | fit | P (interval) | amplitude +- error (ratio) | rms residual | null fraction | same? |
|---|---|---|---|---|---|---|
| ln sigma_1 | line + sinusoid | 2.736 (2.662 to 2.814) | 0.1226 +- 0.019 (6.4) | 0.0444 | 0.2% | yes |
| ln sigma_1 | quadratic + sinusoid | 2.714 (2.704 to 2.724) | 0.1148 +- 0.0023 (49) | 0.0052 | 0.0% | yes |
| ln sigma_2 | line + sinusoid | 2.726 (2.628 to 2.816) | 0.1067 +- 0.018 (6.0) | 0.0419 | 0.3% | yes |
| ln sigma_2 | quadratic + sinusoid | 2.724 (2.714 to 2.736) | 0.111 +- 0.0025 (44) | 0.0056 | 0.0% | yes |
| ln sigma_3 | line + sinusoid | 2.342 (2.224 to 2.444) | 0.1105 +- 0.027 (4.1) | 0.0647 | 7.6% | no |
| ln sigma_3 | quadratic + sinusoid | 2.230 (2.222 to 2.238) | 0.1239 +- 0.0025 (50) | 0.0059 | 0.0% | no |
| ln sigma_4 | line + sinusoid | 2.194 (2.136 to 2.260) | 0.152 +- 0.028 (5.5) | 0.0695 | 0.3% | no |
| ln sigma_4 | quadratic + sinusoid | 2.244 (2.238 to 2.250) | 0.1272 +- 0.0022 (59) | 0.0051 | 0.0% | no |

sigma_1 and sigma_2 oscillate with the same period 2.72 to 2.74; sigma_3 and sigma_4 oscillate as clearly (amplitudes 0.11 to 0.15, rms residual 0.005 with the quadratic trend) but at another period, 2.23 to 2.24 with the quadratic trend (2.34 and 2.19 with the line).

## Part 2: Delta's deviation (`results_519.txt`, `results_519_extra.txt`)

Polynomials in 1/n fitted over all 40 states: rms deviation 4.5e-10 (degree 5) and 4.3e-10 (degree 7), largest 2.2e-9 and 2.0e-9, at the high-D end (D 238.76 to 242.53, where the states are 0.3 to 0.9 apart and Delta flattens). In D 224 to 237.6 the degree 5 deviation stays within 6.6e-11 and is a slow wave (+4.0e-11 at D 228.13, -6.6e-11 at 235.13), not a period of 2.7.
Scanned fits: all D, no period (degree 5: P 3.27, ratio 2.0, null fraction 99.9%; degree 7: P 1.13, ratio 2.2, 99.7%); D 228.13 to 237.13 (15 states): P = 6.0 at the edge of the scan (degree 5: amplitude 1.8e-11 +- 4.5e-12, null fraction 10%; degree 7: 7.3e-11 +- 2.3e-11, 37%). Not the same oscillation.
Fixed period, D 228.13 to 237.13: amplitude at P = 2.74 of **6.0e-12 +- 6.7e-12** (degree 5) and 2.3e-11 +- 2.8e-11 (degree 7), no detection (ratio 0.9 and 0.8); at P = 2.24 4.0e-12 +- 6.2e-12 and 4.7e-12 +- 2.7e-11.
Error bar over the degree: |polynomial of degree 5 - polynomial of degree 7| at D 230 is 1.08e-10 when fitted on all 40 states, 3.6e-10 on D 224 to 242.53, 8.5e-13 on D 228 to 237.2; the coordinator's "about 3e-11" is none of them. The rms of the degree 5 deviation in D 228.13 to 237.13 is 4.3e-11, comparable to 3e-11, with no 2.74 component above about 2e-11 (the fixed-period amplitude plus twice its error).
