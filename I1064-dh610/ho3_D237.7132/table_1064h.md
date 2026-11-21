| run | K | exit | wall s | start max\|F\| (first `on 0:`) | verdict | od lines (|F| before -> after) | p_min (smallest pivot) | Delta(K) - Delta(307) |
|---|---|---|---|---|---|---|---|---|
| ks395 | 395 | 0 | 1351 | 5.71e-36 | converged: last octo-double Newton line 4 steps, max\|F\| 1.1e-86, converged, base saved True | first strong chord (4 weak directions), 2 steps after the full first step; theta at its point inf (bound 0.750) (refused, 522.77 s); step 0: 5.71e-36 -> 6.94e-39, lam 1, 919.54 s; step 1: 6.94e-39 -> 4.05e-46, lam 1, 136.7 s; step 2: 4.05e-46 -> 1.15e-86, lam 1, 134.64 s; step 3: 1.15e-86 converged | 3.2e-15 | +4.771734e-27 |
| ks443 | 443 | 0 | 1501 | 5.71e-36 | converged: last octo-double Newton line 4 steps, max\|F\| 4.2e-86, converged, base saved True | first strong chord (4 weak directions), 2 steps after the full first step; theta at its point inf (bound 0.750) (refused, 654.8 s); step 0: 5.71e-36 -> 2.33e-38, lam 1, 1130.2 s; step 1: 2.33e-38 -> 9.37e-45, lam 1, 110.38 s; step 2: 9.37e-45 -> 4.23e-86, lam 1, 96.6 s; step 3: 4.23e-86 converged | 3.2e-15 | +4.771751e-27 |

Delta(443) - Delta(395) = +1.657102e-32 (information).

p_min against K (the log's `piv min..max`, per step; p_min is the smallest over the steps):

| K | source | steps with a pivot | p_min | p_max |
|---|---|---|---|---|
| 307 | ho2_D237.7132 (i1064o) | 3 | 3.2e-15 | 6.3e+42 |
| 331 | ho2_D237.7132 (i1064o) | 3 | 3.2e-15 | 6.3e+42 |
| 347 | ho2_D237.7132 (i1064o) | 3 | 3.2e-15 | 6.3e+42 |
| 395 | this run | 3 | 3.2e-15 | 6.3e+42 |
| 443 | this run | 3 | 3.2e-15 | 6.3e+42 |

Wall is each run's own, in 30 s polls. The od lines are the first strong chord and each `on N:` step of the octo-double corrector; Delta(K) - Delta(307) is against the ks 307 control base of ho2_D237.7132 for a converged rung.
