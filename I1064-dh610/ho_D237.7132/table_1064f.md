| run | K | exit | wall s | start max\|F\| (first `on 0:`) | verdict | od lines (|F| before -> after) | Delta(K) - Delta(307) |
|---|---|---|---|---|---|---|---|
| ks307 | 307 | 0 | 510 | 5.71e-36 | failed: last octo-double Newton line 2 steps, max\|F\| 1.1e-41, converged, base saved True; max\|F\| above 1e-60 | first strong chord (4 weak directions), 1 steps after the full first step; theta at its point 6.124e-24 (bound 0.750) (accepted, 182.14 s); step 0: 5.71e-36 -> 1.10e-41, lam 1, 332.19 s | - |

Wall is each run's own, in 30 s polls. The od lines are the first strong chord and each `on N:` step of the octo-double corrector; Delta(K) - Delta(307) is for a converged rung.
