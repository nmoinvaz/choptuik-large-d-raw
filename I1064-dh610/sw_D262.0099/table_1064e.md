| run | --od_accept | --elim_switch | exit | wall s | start max\|F\| (first `on 0:`) | first two `on` lines | step 0 after/before | step 1 after/before | verdict | Delta - Delta(293) |
|---|---|---|---|---|---|---|---|---|---|---|
| ks293 | own | 1e-9 | 0 | 90 | 3.93e-36 | on 0: \|F\| 3.93e-36 converged, Delta 1.68309109015459857 -7.1515e-17 | - | - | converged: last octo-double Newton line 1 steps, max\|F\| 3.9e-36, converged, base saved True | - |
| ks315own | own | 1e-9 | 0 | 3721 | 1.67e-30 | on 0 chord 0: max\|F\| 8.60e+29, \|dw\| 1.515e+30<br>on 0: strong chord (4 weak directions), 1 steps after the full first step; theta at its point inf (bound 0.750): refused, 304.72 s | - | - | failed: last octo-double Newton line 1 steps, max\|F\| 1.7e-30, not converged, base saved False | - |
| ks315nat | natural | 1e-9 | 0 | 3211 | 1.67e-30 | on 0 chord 0: max\|F\| 8.60e+29, \|dw\| 1.515e+30<br>on 0: strong chord (4 weak directions), 1 steps after the full first step; theta at its point inf (bound 0.750): refused, 300.07 s | - | - | failed: last octo-double Newton line 1 steps, max\|F\| 1.7e-30, not converged, base saved False | - |

Wall is each run's own, in 30 s polls. The start |F| is the first `on 0: |F|` value of the log; step 0 and 1 are the first two `on N: |F| a -> b` lines (the accepted step's |F|, lam in the log).
