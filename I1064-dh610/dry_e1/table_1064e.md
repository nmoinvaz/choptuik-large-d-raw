| run | --od_accept | --elim_switch | exit | wall s | start max\|F\| (first `on 0:`) | first two `on` lines | step 0 after/before | step 1 after/before | verdict | Delta - Delta(293) |
|---|---|---|---|---|---|---|---|---|---|---|
| ks293 | own | 1e-9 | 0 | 90 | 3.93e-36 | on 0: \|F\| 3.93e-36 converged, Delta 1.68309109015459857 -7.1515e-17 | - | - | converged: last octo-double Newton line 1 steps, max\|F\| 3.9e-36, converged, base saved True | - |
| ks315own | own | 1e-9 | 143 (capped) | 330 | - | none | - | - | failed: no octo-double Newton line | - |
| ks315nat | natural | 1e-9 | 143 (capped) | 330 | - | none | - | - | failed: no octo-double Newton line | - |

Wall is each run's own, in 30 s polls. The start |F| is the first `on 0: |F|` value of the log; step 0 and 1 are the first two `on N: |F| a -> b` lines (the accepted step's |F|, lam in the log).
