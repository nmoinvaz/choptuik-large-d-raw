| run | K | exit | wall s | start max\|F\| (first `on 0:`) | verdict | od lines (|F| before -> after) | p_min (smallest pivot) | Delta(K) - Delta(307) |
|---|---|---|---|---|---|---|---|---|
| ks395 | 395 | 143 (capped) | 330 | - | failed: no octo-double Newton line | no od lines | - | - |
| ks443 | 443 | 143 (capped) | 330 | - | failed: no octo-double Newton line | no od lines | - | - |

p_min against K (the log's `piv min..max`, per step; p_min is the smallest over the steps):

| K | source | steps with a pivot | p_min | p_max |
|---|---|---|---|---|
| 307 | ho2_D237.7132 (i1064o) | 3 | 3.2e-15 | 6.3e+42 |
| 331 | ho2_D237.7132 (i1064o) | 3 | 3.2e-15 | 6.3e+42 |
| 347 | ho2_D237.7132 (i1064o) | 3 | 3.2e-15 | 6.3e+42 |
| 395 | this run | 0 | - | - |
| 443 | this run | 0 | - | - |

Wall is each run's own, in 30 s polls. The od lines are the first strong chord and each `on N:` step of the octo-double corrector; Delta(K) - Delta(307) is against the ks 307 control base of ho2_D237.7132 for a converged rung.
