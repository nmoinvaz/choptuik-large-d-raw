# I824-mac: newton_od prints why a trial's projection failed (toy logs)

Machine: the Apple M5 Mac (`mac`), agent mac752. Issue https://github.com/nmoinvaz/choptuik-large-d/issues/824.

Code: branch `wip/i824` at f198c203 (on main 365d1bca). Build: main 3c35f0c's hpkernel (i599/site2).

| run | the new case | exit |
|---|---|---|
| `newton_od_toy.py` (toy.log) | 21 reason lines for 21 failed trial projections, each naming the stages; trial lines parsed 1 of 1: pass | 0, PASS |
| `--mutate=nowhy` (toy_nowhy.log) | 0 reason lines: FAIL | 1, FAIL |
| the toy against main 365d1bca's octo_corrector.py, the change undone (toy_undone.log) | 0 reason lines: FAIL | 1, FAIL |
