# I557-win2: a joint fit of each sigma pair with a shared oscillation and a pre-registered trend degree

Machine win2 (Windows 11 desktop, Intel Core Ultra 7 265K, 20 threads, 96 GB), issue https://github.com/nmoinvaz/choptuik-large-d/issues/557 (follows from #533 and #535). Analysis only, one thread, venv-t177.
`joint_557.py`: sigma_1 + sigma_2 and sigma_3 + sigma_4, each pair with one shared period law (P0, p1, p2) and phase, separate amplitudes and separate trends, the trend degree chosen by the rule documented in the script (fixed before any fit to the data, applied to the training states only), #533's hold-outs H1 and H2 and #535's twelve states as H3; the separate fits beside them. Planted truth first (`results_selftest_557.txt`). Results follow in this README.

## Results (2026-11-12 05:21 to 05:27 UTC)

**Planted truth first** (`results_selftest_557.txt`, 100 merge trials; ok). P1, a planted shared oscillation (P0 2.62, p1 +0.0165, p2 +0.0003, shared phase 0.7, amplitudes 0.112 and 0.110, cubic trends, noise 0.006, at the D of the 63 states): the shared fit (J2) recovers P0 2.618, p1 +0.0160, p2 +0.00028, phase 0.683, residual rms 0.0050; the merge test (J2 against a phase of its own for each series, J1) has null fraction 97.0%, so the merge is kept; the rule picks degrees (3, 3) and the H1 prediction rms is 0.0078 and 0.0089. P2, planted phases 0.6 rad apart: J2's rms is 0.0236 against J1's 0.0054, null fraction 0.0%, so the merge is rejected.

**The rule** (fixed in the script's docstring before any fit to the data): on the training states only, the last block of max(6, round(0.2 n)) states is left out, the shared fit is made to the rest for every (d_a, d_b) in {2, 3, 4}^2, the block is predicted, and the pair of degrees with the smallest summed squared error is taken (ties: the smaller d_a + d_b, then d_a). The benchmark "separate, rule" applies it to each series alone; "separate, cubic" is #533's fit (degree 3 fixed, chosen after the data were seen).

**The pairs share one oscillation** (`joint_557.py` -> `results_557.txt`, 300 merge trials, two noise conventions). Fits to the 51 states D >= 210.13:

| pair | rule degrees | shared P0, p1, p2 | shared phase | rms, shared | rms, a phase for each | merge null fraction |
|---|---|---|---|---|---|---|
| sigma_1 + sigma_2 | 3, 3 | 2.6166, +0.01713, +0.000339 | 3.222 | 0.0056 | 0.0056 | 97.7% / 97.3% |
| sigma_3 + sigma_4 | 4, 4 | 2.1971, +0.00617, +0.000130 | 3.129 | 0.0059 | 0.0059 | 68.7% / 70.0% |

Sharing the period law and the phase costs nothing in the residual, and the merge is not rejected for either pair. The shared phases are 3.22 and 3.13 (the script does not print the two amplitudes, whose signs would show it); the side look below shows that the two series of a pair oscillate in antiphase.

**Hold-outs** (prediction rms of ln sigma, both series of the pair; the shared fit with the rule's degrees against the separate fits):

| pair | hold-out | rule degrees | joint, rule | separate, rule | separate, cubic (#533) |
|---|---|---|---|---|---|
| sigma_1, sigma_2 | H1 (fit D <= 232.7, predict 233.13 to 237.13) | 2, 3 | **0.0260**, 0.0093 | 0.0283, 0.0082 | 0.0079, 0.0082 |
| sigma_1, sigma_2 | H2 (fit D >= 214, predict 210.13 to 213.63) | 4, 4 | **0.0421**, 0.0115 | 0.0407, 0.0120 | 0.0173, 0.0119 |
| sigma_1, sigma_2 | H3 (fit D >= 210.13, predict #535's twelve states) | 3, 3 | **0.0144**, 0.0083 | 0.0152, 0.0082 | 0.0152, 0.0082 |
| sigma_3, sigma_4 | H1 | 4, 4 | 0.0432, 0.0078 | 0.0430, 0.0068 | 0.0308, 0.0167 |
| sigma_3, sigma_4 | H2 | 3, 3 | 0.0398, 0.0206 | 0.0404, 0.0201 | 0.0404, 0.0201 |
| sigma_3, sigma_4 | H3 | 4, 4 | 0.0350, 0.0122 | 0.0331, 0.0388 | 0.0565, 0.0388 |

**Acceptance (sigma_1 and sigma_2 joint prediction rms at most 0.014 in H1, H2 and H3): fails.** sigma_2 meets it in all three (0.0093, 0.0115, 0.0083), sigma_1 in none (0.0260, 0.0421, 0.0144; H3 misses by 3%). The joint fit gives the same predictions as the separate fits with the same rule (within 0.0011 for sigma_2, and from 0.0023 better to 0.0014 worse for sigma_1) and is no better than #533's cubic fits where those met the limit. The pre-registered rule is what spoils sigma_1: the training windows make it choose degree 2 (H1) and degree 4 (H2), which extrapolate worse than the cubic that #533 fixed after the fact (0.0079 and 0.0173). A rule that does not see the test states reaches neither the limit nor #533's numbers, so the earlier cubic results owe part of their success to a degree chosen with the data in view.

**Side look: the pairs oscillate in antiphase, and the sums are oscillation-free** (`diff_557.py` -> `results_diff_557.txt`; not an acceptance, and found after seeing the full data, so it is not a pre-registered result). Over the 51 states, the rms residual of a polynomial of degree 1, 2, 3, 4 in u:

| quantity | range | degree 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| ln sigma_1 + ln sigma_2 | -264.8 to -207.7 | 0.7248 | 0.0104 | 0.0039 | 0.0038 |
| ln sigma_2 - ln sigma_1 | +1.12 to +1.72 | 0.1576 | 0.1572 | 0.1572 | 0.1569 |
| ln sigma_3 + ln sigma_4 | -249.9 to -188.1 | 0.9722 | 0.0461 | 0.0085 | 0.0038 |
| ln sigma_4 - ln sigma_3 | +3.91 to +4.53 | 0.1860 | 0.1851 | 0.1850 | 0.1845 |
| ln sigma_1 (for scale) | -133.1 to -104.6 | 0.3758 | 0.0789 | 0.0788 | 0.0787 |

The sums are smooth (a cubic reaches 0.0039 for sigma_1 + sigma_2, a quartic 0.0038 for sigma_3 + sigma_4) and the differences carry no trend at all (the residual does not fall from degree 1 to 4) and all of the oscillation (0.157 is twice the 0.079 of one series, 2 x 0.111 / sqrt 2). So in each pair the two oscillations have equal amplitudes and opposite signs: ln sigma_a = S / 2 - c / 2 - (a / 2) cos(phi + off), ln sigma_b = S / 2 + c / 2 + (a / 2) cos(phi + off), with one smooth sum S for the pair. The polynomial hold-out of the sums alone (no oscillation to confuse it):

| sum | H1: degree 2, 3, 4 | H2 | H3 |
|---|---|---|---|
| ln sigma_1 + ln sigma_2 | 0.0456, **0.0087**, 0.0239 | 0.0332, **0.0177**, 0.0433 | 0.0659, 0.0127, **0.0040** |
| ln sigma_3 + ln sigma_4 | 0.2050, 0.0458, **0.0415** | 0.1644, 0.0593, **0.0327** | 0.2812, 0.0860, **0.0443** |

No single degree extrapolates in every window (degree 3 is the best for sigma_1 + sigma_2 in H1 and H2, degree 4 in H3; degree 4 for sigma_3 + sigma_4 throughout, and still 0.03 to 0.04), so the polynomial trend of the sum is what limits the hold-outs, not the oscillation.
