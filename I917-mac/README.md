# I917-mac: the sigma-model kernel's chain in D at eta = 1 past D 10.475, to D 11

Machine: mac (Apple M5 Mac). Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/917. Code: branch `wip/sa-917`
on main 56e60fbb. The kernel module is the build of #652 (`I652-mac/README.md`), run with python 3.14 and `PYTHONPATH`
at that build's site directory, one process with 2 threads at nice 10, every run behind `gate.sh` (1-minute load below
31 at its start: 21.9 to 30.8 in `out/gate.log`). Local paths are removed from the copies here.

## The chain (`run_chain.sh`, `run_polish.sh`, `out/`)

`chain.py --eta 1` with `--solver band` for every point, M = 32, from #652's states at D 10.475 and 10.4375
(`I652-mac/out/`): to D 10.5 (`chain_first.txt`), then in steps of 0.0625 to D 11 (`chain_up.txt`, 8 points), D
10.475 again from the secant through the new D 10.5625 and 10.5 (`chain_closure.txt`), and three points at sigdss's
own D (`chain_x*.txt`: 10.1, 10.3796875, 10.474609375). Then one more Newton step (`--tol 1e-30`, `polish_D*.txt`) at
the four points that had stopped between 1e-30 and 1e-28 (D 10.5625, 10.8125, 10.875, 10.9375).

No run failed and no step was halved. Every point from D 10.5625 to 11 took the band solver's deflated steps, two
resolved and three band steps each, in about 10 minutes; the points with Newton's own steps only (D 10.5, the
closure, 10.3796875, 10.474609375) took 3 to 5 minutes. #652's chain, with plain Newton, had 18 failed runs and steps
halved down to 1/128 below D 10.475.

`out/chain_table.txt` is `matter/sigma_ms/chain_table.py <raw clone> --folder I917-mac --eta 1 --also I652-mac
--Dmin 10 --D0 10.475 --ref I652-mac,I845-mac,I913-mac --sigdss ...m1up.jsonl,...m1hi.jsonl` (csv in the repository,
`matter/sigma_ms/data/delta_D_eta1.csv`). Its three checks pass:

| check | result |
|---|---|
| every D from 10 to 11 converged, max \|F\| <= 1e-28 | 21 values of D (#652's from 10 to 10.475 and this chain's), largest max \|F\| 1.04e-30 |
| closure at D 10.475 against #652's, #845's and #913's states, to 1e-20 | largest difference 1.72e-23 over 5 records; the chain's value is 1.0e-23 from #652's |
| smoothness on the 17 multiples of 0.0625 from D 10 to 11 | third and fourth differences of one sign each, largest fourth 0.17% of largest second; second derivative from -3.79e-3 to -2.0e-3 |

Its mutations `closure` and `kink` each exit 1.

| D | Delta, kernel | sigdss's Delta (march, prior) | kernel minus sigdss |
|---|---|---|---|
| 10 | 1.023437249542784 | 1.0261416 (m1up, 1e-8) | -2.70e-3 |
| 10.1 | 1.022800653369061 | 1.0269908 (m1hi, 1e-7) | -4.19e-3 |
| 10.25 | 1.021777377751899 | 1.0295102 (m1hi, 1e-7) | -7.73e-3 |
| 10.3796875 | 1.020832176522758 | 1.0298300 (m1up, 1e-8) | -9.00e-3 |
| 10.474609375 | 1.020107834653079 | 1.0340058 (m1up, 1e-8) | -1.39e-2 |
| 10.475 | 1.020104800025155 | 0.9934860 (m1hi, 1e-7) | +2.66e-2 |
| 10.5 | 1.019909692894059 | 0.9942924 (m1hi, 1e-7) | +2.56e-2 |
| 10.75 | 1.017868267483358 | | |
| 11 | 1.015682192797883 | | |

sigdss has no eta = 1 value above D 10.5. The kernel's Delta(D) falls smoothly from D 10 to 11, with slope -0.0063
at D 10 and -0.0089 at D 11. sigdss's values rise from D 10 to 10.4746 on one march and drop by 0.04 to the other
at D 10.475, where the kernel has one solution (#845).
