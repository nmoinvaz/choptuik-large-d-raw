# I565-win2: a trend for the sigma pair sums that extrapolates in every hold-out

Machine win2 (Windows 11 desktop, Intel Core Ultra 7 265K, 20 threads, 96 GB), issue https://github.com/nmoinvaz/choptuik-large-d/issues/565 (follows from #557). Analysis only, one thread, venv-t177. Results follow in this README.

## Results (2026-11-12 05:48 to 05:58 UTC)

`trend_565.py`: the sums ln sigma_a + ln sigma_b of the pairs (sigma_1, sigma_2) and (sigma_3, sigma_4) over the 63 states D 204.13 to 237.13, eleven trend forms fixed before any hold-out was computed (polynomials in D of degree 2, 3, 4; polynomials in 1/D and in ln D of degree 2, 3, 4; the bases {1, z, z ln z, z^2} and {1, z, ln z, z^2} with z = D / 228), fitted by least squares on the training states of #533's hold-outs H1 (fit D <= 232.7, 42 states, predict 233.13 to 237.13), H2 (fit D >= 214, 43 states, predict 210.13 to 213.63) and H3 (fit D >= 210.13, 51 states, predict 204.13 to 209.63). Full tables: `results_565.txt`.

**Planted truth first** (`results_selftest_565.txt`, ok): a wrong form (poly(2) for a planted ln D cubic) misses 0.007 by far; with noise 0.004 (the noise of the real sum of sigma_1 + sigma_2, the in-sample rms of its cubic being 0.0039) the TRUE form's median prediction rms over 100 seeds is 0.0048, 0.0052, 0.0058 (lnD(3)) and 0.0049, 0.0050, 0.0055 (poly(3)) in H1, H2, H3, below 0.007, but **it meets 0.007 in all three windows in only 48% and 53% of the seeds**; at noise 0.02 the true form misses 0.007 (the check can fail). A calibration beyond the selftest (200 seeds): at noise 0.0025 the true form meets it in 89% to 92% of seeds, at noise 0.004 in 48% to 53%, and a true quartic at noise 0.004 in 14%. The real sum of sigma_3 + sigma_4 has an in-sample rms of 0.0126 (cubic) and 0.0064 (quartic), so at that noise level the criterion is unlikely to be met even by its true form (I did not simulate that noise).

**Prediction rms of the sum in H1, H2, H3** (the polynomials of degree 2 to 4 first; the criterion is 0.007 in all three):

| sum | form | parameters | H1 | H2 | H3 | meets 0.007 in all three |
|---|---|---|---|---|---|---|
| sigma_1 + sigma_2 | poly(2) | 3 | 0.0679 | 0.0332 | 0.0659 | no |
| sigma_1 + sigma_2 | poly(3) | 4 | 0.0113 | 0.0177 | 0.0127 | no |
| sigma_1 + sigma_2 | poly(4) | 5 | 0.0063 | 0.0433 | 0.0040 | no |
| sigma_1 + sigma_2 | invD(2), invD(3), invD(4) | 3, 4, 5 | 0.4814, 0.0523, 0.0119 | 0.2856, 0.0463, 0.0454 | 0.5877, 0.0797, 0.0177 | no |
| sigma_1 + sigma_2 | lnD(2), lnD(3), lnD(4) | 3, 4, 5 | 0.2407, 0.0213, 0.0077 | 0.1341, 0.0254, 0.0452 | 0.2722, 0.0283, 0.0067 | no |
| sigma_1 + sigma_2 | B1 {1, z, z ln z, z^2}; B2 {1, z, ln z, z^2} | 4, 4 | 0.0129; 0.0137 | 0.0193; 0.0200 | 0.0152; 0.0165 | no |
| sigma_3 + sigma_4 | poly(2) | 3 | 0.2935 | 0.1644 | 0.2812 | no |
| sigma_3 + sigma_4 | poly(3) | 4 | 0.0693 | 0.0593 | 0.0860 | no |
| sigma_3 + sigma_4 | poly(4) | 5 | 0.0132 | 0.0327 | 0.0443 | no |
| sigma_3 + sigma_4 | invD(4); lnD(4) | 5, 5 | 0.0387; 0.0237 | 0.0203; 0.0286 | 0.1068; 0.0676 | no |
| sigma_3 + sigma_4 | B1; B2 | 4, 4 | 0.0764; 0.0799 | 0.0652; 0.0681 | 0.0976; 0.1036 | no |

**Acceptance (a form that meets 0.007 in H1, H2 and H3): fails for both sums, none of the eleven forms tried does.** The polynomials in D are the best family: the best single entry for sigma_1 + sigma_2 is poly(3) (0.0113, 0.0177, 0.0127, so 1.6 to 2.5 times the criterion; each series' half 0.0057, 0.0089, 0.0064), poly(4) meets 0.007 in H1 and H3 (0.0063, 0.0040) and misses H2 by a factor 6 (0.0433). The polynomials in 1/D and in ln D, and the two bases with a logarithm, are worse than the polynomials of the same number of parameters at every degree (e.g. lnD(3) 0.0213, 0.0254, 0.0283 against poly(3)). So no form tried improves on the polynomial of #557, and eleven forms were tried: the failure is not a result of choosing among few.
