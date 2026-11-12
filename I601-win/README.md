# I601-win: #533's chirp hold-outs for ln sigma_1 and ln sigma_2 with the second harmonic in the waveform (analysis only)

Machine win (Surface Laptop 4, i7-1185G7), issue https://github.com/nmoinvaz/choptuik-large-d/issues/601 (recommended by win in #534; the coordinator's message `choptuik-large-d/2026-11-12/135852Z-coordinator-52ea.md`). Analysis only, one thread, venv-t151 (numpy 2.2.6, scipy 1.15.3, Python 3.10). The script reads #533's code and #525's data from an up-to-date raw worktree (`I533-win2/period_p2_533.py` and its siblings), nothing is copied from it. Run from this folder: `python holdout2_601.py --raw=<raw worktree> planted --scenario=P1|P2|P3 --seeds=200`, `summarize FILES`, `data --verdict=results_planted_601_v1.txt`.

## Method

The chirp of #533 (cubic trend in u = (D - 228) / 10, period P0 + p1 x + p2 x^2, x = D - 228) with the waveform A1 cos phi + B1 sin phi + A2 cos 2 phi + B2 sin 2 phi: six linear parameters by least squares (rho = a2 / a1 and theta = delta2 - 2 delta1 derived as in #534), (P0, p1, p2) by Nelder-Mead from #533's single-harmonic fits (grid best, then p2 = 0, +-0.0005). Hold-outs exactly as #533: H1 fits D <= 232.7 (42 states) and predicts D 233.13 to 237.13 (9); H2 fits D >= 214 (43) and predicts D 210.13 to 213.63 (8); three models each: the p2 chirp, the p2 = 0 chirp and the control p1 = p2 = 0 (a constant period). The single-harmonic columns are #533's own `holdouts()` on the same series (they reproduce its table: 0.0079, 0.0173, 0.0082, 0.0119 for the p2 chirp).

## Planted truth first (the whole pipeline, 200 seeds per scenario, fixed on the issue before the real series was read: comment 6825705064)

a1 = 0.11, rho = 0.065, phi from P0 2.62, p1 +0.0165, p2 +0.0003; P1 theta 0 (sigma_1-like) and P2 theta pi (sigma_2-like), noise 0.003; P3 as P1 at noise 0.006 (information). Rules PR1 to PR4 on P1 and P2 (the script's header and the issue).

**Verdict (`results_planted_601_v1.txt`): PASS.** PR1: the median errors of P0, p1 are 0.0009 and 0.0003 (P1), 0.0009 and 0.0004 (P2), median rho_hat 0.065, median |theta_hat - theta| 0.053 and 0.064 rad. PR2: the 2-harmonic p2 chirp predicts at most 0.014 in 98% (H1) and 98% (H2) of P1 seeds and 99% and 100% of P2 seeds (median rms 0.0054, 0.0054, 0.0054, 0.0051). PR3: the control is worse in 100% of seeds in every case (median 0.08 to 0.11). PR4: the 2-harmonic median is below the 1-harmonic one (0.0054 against 0.0084, 0.0054 against 0.0080, 0.0054 against 0.0086, 0.0051 against 0.0078). P3 at noise 0.006 (information): recovery passes, but only 72% (H1) and 79% (H2) of seeds reach 0.014 (median rms 0.0110, 0.0102). Control of the script (`control_guard_601.txt`): the `data` command refuses a verdict file that does not say PASS (exit 1).

## Results (`results_601.txt`, `results_601.json`; run after the verdict)

The 2-harmonic chirp over all 51 states: ln sigma_1 P0 2.616, p1 +0.0160, p2 +0.00027, rho 0.068, theta +0.01, rms 0.0027 (one harmonic: 0.0060); ln sigma_2 P0 2.618, p1 +0.0173, p2 +0.00034, rho 0.065, theta +3.12, rms 0.0011 (0.0052).

Prediction rms (max) of the hold-outs, the p2 chirp (the acceptance) and the controls:

| series | hold-out | 2 harmonics: p2 chirp | 1 harmonic: p2 chirp (#533) | meets 0.014 (2h) | 2 harmonics: p2 = 0 chirp | 2 harmonics: p1 = p2 = 0 | control worse |
|---|---|---|---|---|---|---|---|
| ln sigma_1 | H1 | 0.0094 (0.0157) | 0.0079 (0.0162) | yes | 0.0187 (0.0350) | 0.0964 (0.1916) | yes |
| ln sigma_1 | H2 | **0.0146** (0.0242) | 0.0173 (0.0300) | **NO** | 0.0184 (0.0364) | 0.1017 (0.1718) | yes |
| ln sigma_2 | H1 | 0.0027 (0.0057) | 0.0082 (0.0134) | yes | 0.0140 (0.0266) | 0.0937 (0.1887) | yes |
| ln sigma_2 | H2 | 0.0070 (0.0150) | 0.0119 (0.0198) | yes | 0.0141 (0.0292) | 0.0913 (0.1529) | yes |

**Acceptance: NOT MET**, on one cell. ln sigma_1's H2 is 0.0146 against the bound 0.014 (4% over; it was 0.0173 with one harmonic). The other three cells meet it (0.0094, 0.0027, 0.0070) and the p1 = p2 = 0 control is worse in all four, by a factor of 7 to 35 (0.0964/0.0094, 0.1017/0.0146, 0.0937/0.0027, 0.0913/0.0070). The second harmonic helps ln sigma_2 a lot (H1 0.0082 -> 0.0027, H2 0.0119 -> 0.0070, both now with a wide margin) and ln sigma_1's H2 (0.0173 -> 0.0146), but not ln sigma_1's H1 (0.0079 -> 0.0094, still under the bound). The p2 = 0 chirp reaches 0.0140 and 0.0141 for ln sigma_2 (at the bound's edge) and 0.0187 and 0.0184 for ln sigma_1, so p2 still matters.

**Post hoc (after the data were read, not in the protocol): where the observed values sit in the planted distribution** (P1 for ln sigma_1, P2 for ln sigma_2; the planted noise 0.003 gives a global 2-harmonic rms of 0.0026, ln sigma_1's own is 0.0027, so P1 is the right comparison for it; ln sigma_2's own rms 0.0011 is lower): ln sigma_1's H1 0.0094 is exceeded in 16% of P1 seeds (the 84th percentile, unremarkable), its **H2 0.0146 in only 1.0%** of P1 seeds (P1's H2 median 0.0054, 98th percentile 0.0119, maximum 0.0178). So at ln sigma_1's noise the model with the planted truth would almost never miss H2 by this much: the miss is not noise alone, and ln sigma_1 has structure near D 210 to 214 (or in the trend extrapolated there) that the cubic trend and the two harmonics do not carry. For ln sigma_2, H1 and H2 (0.0027, 0.0070) lie below P2's medians (0.0054, 0.0051) in H1 and above in H2 (the 23% level), which is consistent with its lower noise.

## Caveats

- The planted noise is 0.003; ln sigma_2's own is lower (0.0011), ln sigma_1's the same. At noise 0.006 the bound would be reached in only 72 to 79% of seeds by the true model (P3), so the bound is a statement about this noise level.
- The trend is a cubic polynomial extrapolated over 4.5 to 6 units in each hold-out; #533 found that this extrapolation limits the hold-outs and that the best degree differs by series. No other degree was tried here.
- The windows' phase of the second harmonic is taken as free (theta fitted), not fixed at 0 or pi.
