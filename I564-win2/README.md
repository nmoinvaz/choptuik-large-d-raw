# I564-win2: the antiphase pair model for the sigma oscillation, tested on #558's states

Machine win2 (Windows 11 desktop, Intel Core Ultra 7 265K, 20 threads, 96 GB), issue https://github.com/nmoinvaz/choptuik-large-d/issues/564 (follows from #557 and #558). Analysis only, one thread, venv-t177.
`antiphase_564.py`: each sigma pair as one smooth sum S plus an antiphase oscillation of one amplitude with a shared period law (the model, the degree rule fixed before any fit, the planted-truth selftest are in the script's docstring). `--predict` writes the model's predictions of ln sigma at #558's twelve states to `predictions_564.json` without reading any file of I558-win2; they are posted on the issue before #558's states are read. `eval_564.py` (written after the posting) compares them with #558's states. Results follow in this README.

## Results

**Registration.** The model (M0 as the issue wrote it, M1 with a linear term c1 u in the difference T, made after the first fit and before any #558 state was read), the degree rule for the polynomial sum S, the fit to the 63 states and the predictions of ln sigma at #558's twelve states were posted on #564 at 05:48 UTC (comment 6815822818) and committed at raw 950e85a6 (`antiphase_564.py`, `results_predict_564.txt`, `predictions_564.json`). `eval_564.py` checks `predictions_564.json` against the committed file before using it (equal: yes). Planted truth first (`results_selftest_564.txt`, ok): a planted antiphase pair with equal amplitudes 0.111 and a linear term in the difference is recovered (P0 2.618, p1 +0.0171, p2 +0.00036, difference amplitude 0.2228 against 0.222, c1 +0.0613 against 0.063), M0's difference rms is 0.0594 against M1's 0.0068, the sum-oscillation null fraction is 69%, and M1's extrapolation to twelve states below the 51 above has rms 0.0055 and 0.0103; a planted pair with amplitudes 0.12 and 0.08 in antiphase is flagged (null fraction 0.0%).

**Fit to the 63 states (registered).** M1, degree of S by the rule 3 (sigma_1 + sigma_2) and 4 (sigma_3 + sigma_4): rms of ln sigma_1 and ln sigma_2 0.0061 and 0.0055, of ln sigma_3 and ln sigma_4 0.0079 and 0.0074, with 11 or 12 parameters per pair against 18 for the separate fits (whose residuals are 0.0059 and 0.0053 for sigma_1 and sigma_2). M0: 0.0308 and 0.0306, 0.0315 and 0.0314.

**Evaluation on #558's twelve states** (`eval_564.py` -> `results_eval_564.txt`; the measured values are the equilibrated singular values of #558's `near_null_eq.py` runs, read for the first time after the registration):

| model | sigma_1 prediction rms | sigma_2 | sigma_3 | sigma_4 | meets 0.014 for sigma_1 and sigma_2 |
|---|---|---|---|---|---|
| M0 (the issue's) | 0.0676 | 0.0472 | 0.1049 | 0.0342 | no |
| M1 (with the linear term) | **0.0091** | **0.0206** | 0.0464 | 0.0383 | **no** (sigma_1 yes, sigma_2 no) |
| separate cubic p2 chirps (fitted to the same 63 states) | 0.0157 | 0.0123 | 0.0425 | 0.0223 | no (sigma_2 yes, sigma_1 no) |

Mean error of M1 (predicted minus measured): sigma_1 -0.0029, sigma_2 -0.0179, sigma_3 -0.0404, sigma_4 -0.0313; maximum absolute error 0.0157, 0.0433, 0.0828, 0.0684. For the pair sigma_1 + sigma_2 the error splits into the sum S and the difference T: the rms of the sum error is 0.0237 (0.0118 of each series) and of the difference error 0.0213 (0.0106 of each), so the extrapolation of the sum and of the difference's linear-plus-oscillation form contribute equally; for sigma_3 + sigma_4 the sum's quartic dominates (0.0830, 0.0415 of each series, against 0.0184 for the difference). The per-state errors of sigma_2 are negative at all twelve states (-0.003 to -0.043), the bias that makes it miss.

**Acceptance (the rms of ln sigma_1 and ln sigma_2 at most 0.014, the separate cubic fits beside it): fails for M0 and for M1.** M1 meets it for sigma_1 (0.0091, better than the separate fit's 0.0157) and misses it for sigma_2 (0.0206, worse than the separate fit's 0.0123); M0, the model as the issue wrote it, misses by a factor 3 to 5 because it does not hold the linear term in the difference.

**The antiphase structure holds out of sample** (`structure_564.py` -> `results_structure_564.txt`, a side test on the twelve new states alone at the registered period law, not an acceptance): the oscillation amplitude in the sum ln sigma_a + ln sigma_b is 0.0009 for sigma_1 + sigma_2 and 0.0039 for sigma_3 + sigma_4, against 0.2206 and 0.2622 in the difference; the cos coefficients of the two series are -0.1100 and +0.1104 (sigma_1, sigma_2) and +0.1291 and -0.1330 (sigma_3, sigma_4): equal in size and opposite in sign, to within 0.5% and 3%. The structure was found on the 63 states (#557) and is confirmed on states it had not seen; what fails is the extrapolation of the smooth parts.
