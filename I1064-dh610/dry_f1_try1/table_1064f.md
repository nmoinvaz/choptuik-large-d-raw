| run | K | exit | wall s | start max\|F\| (first `on 0:`) | verdict | od lines (|F| before -> after) | Delta(K) - Delta(307) |
|---|---|---|---|---|---|---|---|
| ks307 | 307 | 0 | 90 | 5.71e-36 | converged: last octo-double Newton line 1 steps, max\|F\| 5.7e-36, converged, base saved True | step 0: 5.71e-36 converged | - |
| ks331 | 331 | 0 | 120 | 5.71e-36 | converged: last octo-double Newton line 1 steps, max\|F\| 5.7e-36, converged, base saved True | step 0: 5.71e-36 converged | +0.000000e+00 |
| ks347 | 347 | 0 | 120 | 5.71e-36 | converged: last octo-double Newton line 1 steps, max\|F\| 5.7e-36, converged, base saved True | step 0: 5.71e-36 converged | +0.000000e+00 |

Wall is each run's own, in 30 s polls. The od lines are the first strong chord and each `on N:` step of the octo-double corrector; Delta(K) - Delta(307) is for a converged rung.
