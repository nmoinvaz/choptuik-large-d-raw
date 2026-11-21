| run | K | exit | wall s | start max\|F\| (first `on 0:`) | verdict | od lines (|F| before -> after) | Delta(K) - Delta(307) |
|---|---|---|---|---|---|---|---|
| ks307 | 307 | 0 | 90 | 5.71e-36 | converged: last octo-double Newton line 1 steps, max\|F\| 5.7e-36, converged, base saved True | step 0: 5.71e-36 converged | - |
| ks331 | 331 | 143 (capped) | 631 | - | failed: no octo-double Newton line | first strong chord (4 weak directions), 1 steps after the full first step; theta at its point 6.113e-24 (bound 0.750) (accepted, 389.5 s) | - |
| ks347 | 347 | 143 (capped) | 631 | - | failed: no octo-double Newton line | first strong chord (4 weak directions), 1 steps after the full first step; theta at its point 1.639e-23 (bound 0.750) (accepted, 401.76 s) | - |

Wall is each run's own, in 30 s polls. The od lines are the first strong chord and each `on N:` step of the octo-double corrector; Delta(K) - Delta(307) is for a converged rung.
