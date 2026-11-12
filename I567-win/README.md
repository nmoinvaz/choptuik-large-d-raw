# I567-win: a flexible trend (Gaussian process or smoothing spline) for the sigma pair sums and for sigma_1, with a noise-floor criterion (analysis only)

Machine win (Surface Laptop 4, i7-1185G7), issue https://github.com/nmoinvaz/choptuik-large-d/issues/567 (recommended by win2 in #565; moved to win by the coordinator's message `choptuik-large-d/2026-11-12/144337Z-coordinator-d463.md`). Analysis only, one thread, venv-t151 (numpy 2.2.6, scipy 1.15.3, Python 3.10). The scripts read #565's `trend_565.py`, #557's `joint_557.py`, #558's `period_558.py` and #533's code from an up-to-date raw worktree; `holdout2_601.py` is a copy of I601-win's. Run from this folder: `python flex_trend_567.py --raw=<raw worktree> planted|summarize|data` (Part 1), `python flex_osc_567.py --raw=<raw worktree> planted|summarize|data` (Part 2).

## Answer

**The flexible trends are not validated, and the real check fails for every method.** On planted sums the Gaussian process extrapolates the truths of a polynomial type to about the noise floor, but not an exponential-type truth, and the smoothing spline extrapolates none. On the real sum of ln sigma_1 + ln sigma_2 no method (the GP, the spline, the polynomials of degree 2 to 4) is within the planted-calibrated bound in all four windows (H1, H2, H3 and #558's twelve states), the best polynomial missing by a factor 1.2 to 3.0. The same holds for ln sigma_1 alone with the two-harmonic waveform.

## Part 1: the sums (`flex_trend_567.py`)

The sums y = ln sigma_a + ln sigma_b of the pairs (1, 2) (graded) and (3, 4) (information) at the 63 states D 204.13 to 237.13 and #558's twelve states D 198.13 to 203.63. Windows (explicit): H1 fit 210 <= D <= 232.7 (42 states), predict D > 232.7 (9); H2 fit D >= 214 (43), predict 210 <= D < 214 (8); H3 fit D >= 210 (51), predict 204 <= D < 210 (12); W558 fit all 63, predict #558's twelve. **A discrepancy in #565:** its docstring and table header say H1 is fitted on 42 states, but its code (`windows()`, `D <= 232.7`) fits 54, the twelve states below D 210 included; this folder uses the 42 of the docstring, so the polynomial columns match #565's in H2 and H3 (poly(3) 0.0177, 0.0127; poly(4) 0.0433, 0.0040) and differ in H1 (poly(3) 0.0087 here, 0.0113 there; poly(4) 0.0239, 0.0063).

Candidates (fixed on the issue before the real sums were read, comment 6826943134): **G**, a Gaussian process (universal kriging) with a degree-4 polynomial drift (flat prior), a Matern-5/2 kernel in u = (D - 228) / 10 and white noise, the hyperparameters by restricted marginal likelihood on the training states only (bounds and grid in the script's header); **S**, the natural cubic smoothing spline with the smoothing parameter by generalized cross-validation, continued linearly beyond the data. Planted-only design before the post: the drift degree of G was chosen among 2, 3, 4, 5 (`results_explore_planted_567_a.txt`, `_b.txt`; the first script ends in a KeyError at its third truth, which the second script covers; the numbers above it are the ones quoted on the issue).

**Planted truth** (the whole pipeline, noise 0.004, 100 seeds per truth, `planted_567.json`, `results_planted_567_v1.txt`): P_L = -230 - 160 l + 700 l^2 - 2500 l^3 (l = ln(D / 228)), P_P = -230 - 20 u + 3 u^2 - 0.4 u^3 (both #565's), P_E = -230 - 20 u + 3 exp(-(u + 1) / 1.2). The floor is the true form's median prediction rms (lnD(3), poly(3), and 1, u, exp with the scale known): H1 0.0051 / 0.0059 / 0.0042, H2 0.0050 / 0.0052 / 0.0045, H3 0.0069 / 0.0055 / 0.0049, W558 0.0053 / 0.0051 / 0.0045 for P_L / P_P / P_E. **The bound b_w = 1.5 x the largest floor per window: H1 0.0088, H2 0.0078, H3 0.0104, W558 0.0080.** The control (poly(2) on P_L exceeds 1.5 x the floor) fires.

**Verdict: FAIL; no method is planted-valid** (both rules, extrapolated and recovered, within 1.5 x the floor for all three truths and all four windows). G: P_L 1.09, 0.99, 1.11, **1.66** (the ratio of its median prediction rms to 1.5 x the floor in H1, H2, H3, W558), P_P 1.04, 0.93, 1.31, 1.07, **P_E 2.20, 2.15, 6.17, 11.07**; in-sample recovery fine except P_E (1.09 x 1.5 x the true form's). S: 6 to 160 times, in-sample 1.6 to 1.8 times the true form's. poly(4) is about as good as G on P_L and P_P and fails P_E like G.

**The real sum, reported as NOT VALIDATED** (the pre-registered fallback) (`results_567.txt`, `results_567.json`): prediction rms of ln sigma_1 + ln sigma_2 against b_w:

| method | H1 (0.0088) | H2 (0.0078) | H3 (0.0104) | W558 (0.0080) | within all four |
|---|---|---|---|---|---|
| G | 0.0063 ok | 0.0366 | 0.0339 | 0.0160 | no |
| S | 0.1284 | 0.1118 | 0.2019 | 0.2113 | no |
| poly(2) | 0.0456 | 0.0332 | 0.0659 | 0.1305 | no |
| poly(3) | 0.0087 ok | 0.0177 | 0.0127 | 0.0237 | no |
| poly(4) | 0.0239 | 0.0433 | 0.0040 ok | 0.0358 | no |

**The check fails for every method.** The best entries are poly(3) (H1 at the bound, H2 2.3 times over, H3 1.2, W558 3.0) and poly(4) (H3 ok, H2 5.5 times over); the GP is 4.7, 3.3 and 2.0 times over in H2, H3, W558. Pair (3, 4) (information, no bound): G 0.0162, 0.0146, 0.0757, 0.1154; poly(3) 0.0458, 0.0593, 0.0860, 0.0617; poly(4) 0.0415, 0.0327, 0.0443, 0.0830.

## Part 2: ln sigma_1 alone with the two-harmonic waveform (`flex_osc_567.py`)

Design posted before its planted runs (comment 6827082333; Part 1's sums had been read, ln sigma_1 not). **Gb**: backfitting of #601's two-harmonic chirp with the GP trend of Part 1 (start from the cubic-trend fit, four rounds of GP trend on y - oscillation then chirp and harmonics on y - trend, a last GP pass); **P3**, **P4**: #601/#602's polynomial trends of degree 3 and 4 (variant (a) of #602); **P2**: the control. Planted (noise 0.003, 50 seeds, `planted_567_part2.json`, `results_planted_567_part2_v1.txt`): the truth Q = -115 - 10 u + 1.5 u^2 - 0.2 u^3 plus the two-harmonic oscillation of #601; the true form is P3, floors H1 0.0057, H2 0.0057, H3 0.0051, W558 0.0046, **bounds H1 0.0086, H2 0.0085, H3 0.0077, W558 0.0069**.

**Verdict: FAIL, narrowly.** Gb's median planted rms is 0.95, 0.99, 1.11, 1.03 times b_w (H3 11% and W558 3% over); P4 passes (0.79, 0.95, 0.94, 0.97); the control P2 fires (40 to 150 times). So Gb is not planted-valid by the rule as posted.

Real ln sigma_1, **NOT VALIDATED** (`results_567_part2.txt`, `results_567_part2.json`):

| method | H1 (0.0086) | H2 (0.0085) | H3 (0.0077) | W558 (0.0069) | within all four |
|---|---|---|---|---|---|
| Gb | 0.0051 ok | 0.0280 | 0.0822 | 0.0071 | no |
| P3 | 0.0094 | 0.0146 | 0.0138 | 0.0145 | no |
| P4 | 0.0141 | 0.0280 | 0.0041 ok | 0.0297 | no |
| P2 | 0.0282 | 0.0170 | 0.0284 | 0.0632 | no |

The check fails for every method. P3's and P4's H1 and H2 equal #602's (0.0094, 0.0146; 0.0141, 0.0280), which checks the data loading and the reuse of #601's code. Gb is within the bound in H1 (0.0051) and 3% over it in W558 (0.0071), but 3.3 times over in H2 and 10.7 times in H3; its H2 value equals P4's to four digits (0.0280), as if the GP's correction contributed nothing there (not examined).

## Caveats

- The planted truths are three (Part 1) and one (Part 2) smooth forms; the verdict says what these methods do on them, not on every smooth form. A method with the right drift (G on P_P, poly(3) on P_P) meets the floor: the extrapolation is set by the form, which the data cannot tell.
- The bound is 1.5 x the floor of a true form at noise 0.004 (the sum's in-sample cubic rms 0.0039) or 0.003; the real series' noise is assumed to be that, with white noise. The real errors of the best polynomials are 1.2 to 3 times the bound, which is a bias beyond the noise (as #565 found).
- Two candidates were tried and the polynomial reference, with the hold-outs in view; the GP's drift degree was fixed on planted data only.
- Part 2's planted verdict failed narrowly (H3 1.11, W558 1.03), so its real numbers are reported as not validated; no rule was changed after the data.
