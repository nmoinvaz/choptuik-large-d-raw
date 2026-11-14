# I377-mac: the kappa-model CSS's oscillatory mode followed in kappa at D = 4, 6, 10, 20, 40, infinity, and kappa_c(D)

Machine: the coordinator's Mac (Apple M5), agent xfkappa, one process at nice 10.
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/377
Code: `solver/matter/css_kappa_crit.py` (finite D, through css_lateral.py and css_pert.py), `css_inner_pert.py kpath` and
`kcrit` (D = infinity), on branch wip/xf-kappa of choptuik-large-d.

| file | what |
|---|---|
| `queue5.sh`, `queue5.log`; `queue6.sh`, `queue6.log` | the runs, in order, with their exits |
| `bgpath_D4.jsonl` | control: the D = 4 background continued in kappa from 0 to 1 (ends on HHS96's axion-dilaton solution) |
| `bgpath_D4_k10.jsonl` | the D = 4 background continued to kappa = 10 (for gamma against HE97 Table 1) |
| `scan_D4.jsonl` | collocation (css_scan.py, N 40/56) at D = 4, kappa = 0.0754, 0.0757329315, 0.076 and 10 |
| `path_D{4,6,10,20,40}.jsonl` | background, lambda_osc and lambda_phys at R = 0.85 x_h and 0.6 x_h along kappa |
| `crit.jsonl` | kappa_c at each D and radius (Re lambda_osc = 0), lambda_osc and gamma there |
| `kpath_inf.jsonl`, `kcrit_inf.jsonl` | D = infinity: lambda_osc of the inner solution along kappa (settings A, B) and kappa_c(infinity) |
| `inner_check.jsonl` | css_inner_pert.py check at kappa = 0 and 0.5 (for #376) |
| `failed_v1/`, `stopped_q4/` | a first queue whose paths stopped at kappa = 0 (a bug in the kappa history, fixed), and a queue stopped to put the D = 4 checks first; kept for the record |
