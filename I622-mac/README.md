# I622-mac: lam_g(D) = 4 pi mu / Delta from D 4 to 244.64, its checks, and the fit in 1/n with its planted test

Machine: mac (Apple M5 Mac), a subagent of the coordinator, one process at nice 10. Issue
https://github.com/nmoinvaz/choptuik-large-d/issues/622.
Code: `hp/lam_gauge.py` and `hp/lam_gauge_fit.py` of the code repository (branch wip/i622-subagent, last commit before
this folder ce8ca93), Python 3.14 venv, mpmath. States read from this repository at 6913f312. The table itself is
`hp/data/lam_gauge.csv` of the code repository. The write-up is notes/MODE_COUNT.md section 10.

Files (RAW below is a checkout of this repository; each command runs from the code repository's root):

| file | command | exit |
|---|---|---|
| `rt.log`, `rt_mutate_n.log` | `lam_gauge.py rt RAW/T45-win/hp/data/lowD_states/d4hm15_D4.0000_M192.npz [--mutate=n]` | 0, 1 |
| `mu_check.log` | `solver/rt/mu_check.py` on the same state, for comparison | 0 |
| `identity.log`, `identity_mutate_n.log` | `lam_gauge.py identity RAW [--mutate=n]` | 0, 1 |
| `f64.log`, `f64_mutate_n.log` | `lam_gauge.py f64 --raw=RAW --live` (hpkernel of main) and `--mutate=n` | 0, 1 |
| `table.log` | `lam_gauge.py table RAW` (writes hp/data/lam_gauge.csv; the same-D spreads) | 0 |
| `summary.log` | `lam_gauge.py summary` | 0 |
| `planted.log`, `planted_mutate_limit.log` | `lam_gauge_fit.py planted [--mutate=limit]` (criteria frozen in its docstring) | 0, 1 |
| `fit.log` | `lam_gauge_fit.py fit` | 0 |
| `planted_posthoc_sigma5e-14.log` | `lam_gauge_fit.py planted --sigma=5e-14` (post hoc) | 0 |
| `planted_posthoc_step3e-13.log`, `planted_posthoc_step-3e-13.log` | `... planted --sigma=5e-14 --step=74:+-3e-13` (post hoc) | 0, 0 |
| `fit_dlo74.log` | `lam_gauge_fit.py fit --dlos=74,90,110` (diagnostic) | 0 |
| `lam_gauge_before603.csv` | the table before #603's states were the backbone from D 225.13 (I461's there) | |
| `fit_before603.log`, `planted_posthoc_junk.log` | `fit --csv=lam_gauge_before603.csv`; `planted --csv=... --sigma=2.5e-13 --junk=241.887:4.8e-11,240.514:-2.5e-11` | 0, 1 |

`exits.txt` lists every run with its exit status.
