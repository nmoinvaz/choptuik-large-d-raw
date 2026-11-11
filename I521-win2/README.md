# I521-win2: do the weak subspace's two periods (2.74 and 2.23 in D) persist from D 217 to 227?

Machine win2 (Windows 11 desktop, Intel Core Ultra 7 265K, 20 threads, 96 GB), issue https://github.com/nmoinvaz/choptuik-large-d/issues/521 (follows from #519, #516).
Code: worktree `D:\choptuik-i505` at `origin/wip/i502-subagent` 0cce81e (Python only; interpreter and `hpkernel` build of `C:\Users\nathan\Source\venv-t126`), as in #505 to #516.
Eleven states, four at a time (2 threads each, below-normal priority, `run_i521.sh`): crawlG at D 217.1312 to 227.1312 (D 220.1312 and 224.1312 were measured in #510 and are run again here, a reproducibility check), with the control `--mutate=rows_only` at crawlG D 222.1312 beside the last wave. Exit codes in `exits.txt`.
Then `analysis_521.py`: #519's fit (trend + one sinusoid, period scanned, 1000-trial null test) on ln sigma_1..4 over D 216 to 237 and over D 216 to 227 alone. Results follow in this README.

## Results (2026-11-11 22:59:56 to 23:12:06 UTC; analysis 23:12 to 23:25)

Eleven runs exited 0 (wave 1 22:59:56 to 23:03:5x, wave 2 23:04 to 23:08, wave 3 23:08:04 to 23:12:06 UTC), the control `--mutate=rows_only` at crawlG D 222.1312 exited 1, as it must (`exits.txt`). The planted check passes at each state (1.7e-15 to 8.0e-14, bound 1e-3). The reruns of D 220.1312 and 224.1312 repeat #510's to every printed digit (spread 0.0). `analysis_521.py` (selftest ok: a planted period 2.5 at unit spacing is recovered as 2.490 with null fraction 0.0%, a pure line has null fraction 27.7%) makes `results_521.txt`.

Equilibrated sigma_1..4 of the eleven states: D 217.1312 5.8017e-49, 2.2907e-48, 2.0758e-45, 1.0655e-43; 218.1312 1.9920e-49, 9.3546e-49, 5.6637e-46, 4.8582e-44; 219.1312 8.8626e-50, 2.8711e-49, 2.4795e-46, 1.3500e-44; 220.1312 2.6221e-50, 1.3028e-49, 6.8858e-47, 5.7239e-45; 221.1312 1.0923e-50, 4.0723e-50, 2.7232e-47, 1.6544e-45; 222.1312 3.7334e-51, 1.5221e-50, 8.0301e-48, 6.2092e-46; 223.1312 1.2015e-51, 5.8624e-51, 2.7652e-48, 1.9245e-46; 224.1312 5.0687e-52, 1.6827e-51, 8.9379e-49, 6.2038e-47; 225.1312 1.4156e-52, 7.1473e-52, 2.6593e-49, 2.1091e-47; 226.1312 5.3411e-53, 2.1702e-52, 9.4186e-50, 5.7801e-48; 227.1312 1.8232e-53, 7.1562e-53, 2.4060e-50, 2.1049e-48.

Periods (the fit of #519, 1000-trial null test, scan step 0.005; quadratic trend in the first rows, line in brackets):

| series | D 216 to 227 (12 states, unit spacing, scan from 2.05) | D 228 to 237 (16 states) | drift | all D 216 to 237 (28 states) |
|---|---|---|---|---|
| ln sigma_1 | 2.530 (2.525 to 2.535), amplitude 0.110 +- 0.004, null 0.0% [line: 2.435, null 53%] | 2.715 [line 2.735, null 0.2%] | -0.185 | 2.600, rms residual 0.020 |
| ln sigma_2 | 2.525, amplitude 0.111 +- 0.005, null 0.0% [line: 2.575, null 12.5%] | 2.725 [2.725, null 0.3%] | -0.200 | 2.600, rms 0.021 |
| ln sigma_3 | 2.165, amplitude 0.131 +- 0.002, null 0.0% [line: 2.050 at the scan edge, null 13%] | 2.230 [2.340, null 7.6%] | -0.065 | 2.205, rms 0.019 |
| ln sigma_4 | 2.155, amplitude 0.133 +- 0.003, null 0.0% [line: 2.220, null 83%] | 2.245 [2.195, null 0.3%] | -0.090 | 2.200, rms 0.016 |

Rule of #521 (a period within 0.15 of its D 228 to 237 value with a null fraction below 1% persists; a drift of more than 0.3 between the halves changes with D): with the quadratic trend sigma_3 and sigma_4 persist (drifts -0.065 and -0.090, null 0.0%); sigma_1 and sigma_2 do not persist by the 0.15 bound (drifts -0.185 and -0.200) and do not change by the 0.3 bound: the periods shorten by 7% to 8% towards lower D, from 2.72 to 2.53. With the line trend nothing is detected in D 216 to 227 (null fractions 12.5% to 83%; the line cannot hold the curvature there, rms residual 0.06 to 0.08). A single period over all D 216 to 237 leaves residuals 3 to 4 times those of each half (0.016 to 0.021 against 0.005), as a drifting period would.
Caveat: unit spacing has a Nyquist period of 2, so a period P in D 216 to 227 cannot be told from its alias 1/(1 - 1/P) (2.53 from 1.65, 2.16 from 1.86); the scan excludes below 2.05, and the half-unit states of D 228 to 237 are what fixes the periods there.
