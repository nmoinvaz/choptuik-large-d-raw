# I779-mac: the first step's harmonic-13 remainder against a, on main's build, against the own test's W

Machine: the Mac (Apple M5, the coordinator's machine), one process at a time, 4 threads, nice 10. Issue:
https://github.com/nmoinvaz/choptuik-large-d/issues/779 (pre-registration in its comments). Code: branch `wip/xf-779` at
0feb1bd1 (`hp/junk_err.py`, cases as arguments; `hp/crawl_probe.py` as on main 66bc57ac). Build: main's i599/site2
(3c35f0c, exact freeze projector). Inputs: `I742-win/L/anm_pin13_D117.0000.npz`.

## Files

- `run_779.sh`: the attempts and the roots (`bash run_779.sh RAW OUT` from the checkout's `hp/`). `exits.txt`: each start and exit.
- `anm.log`, `R/`: `crawl_probe.py anm --stop 1 --attempts 3` on #742's FLAGS with `--steps 1 --h_max 1.0 --a0 1.0`, the own test.
  The base polish took 5 steps to 1.5e-106, as in #752's AB_main. The three attempts' iterates are
  `R/crawl_iter_D{118,117.5,117.25}00_s1.npz`, each equal to newton_od's records, with their predictions.
- `fix_*.log`, `fix/`: `fixrun --switch 0 --accept own --steps 8 --tol 1e-60` from each iterate. Each one's first step reproduces
  the attempt's step 1, and each converged: 1.98e-79, 5.72e-89 and 3.04e-62.
- `junk_err.log`, `junk_err.json`: `junk_err.py` on the three cases (command in `junk_err.log`'s run below).
  `junk_err_mutate_k17.log` is its control.

W is the own test's correction at the step-1 trial λ = 1. At every a that trial was accepted, so W is the next iterate's
|dz|, taken from the iterate's saved `hist[1]['dz_new']`. Y is the iterate's |dz| after step 0.

## Results

| a | Y | W | W / Y | the trial's error, max | its harmonic 13, e13 | W / e13 | verdict (10%) |
|---|---|---|---|---|---|---|---|
| 1 (D 118) | 1.0549e-16 | 4.1504e-17 | 0.393 | 4.15e-17 | 3.8744e-17 | 1.071 | equal |
| 1/2 (D 117.5) | 2.3418e-17 | 4.1282e-18 | 0.176 | 4.13e-18 | 4.0442e-18 | 1.021 | equal |
| 1/4 (D 117.25) | 6.0380e-18 | 1.5670e-18 | 0.260 | 1.57e-18 | 1.4250e-18 | 1.0997 | equal, by 0.03 points |

- **W is the trial's error.** At each a, W equals the trial's whole distance from the root to three digits. Harmonic 13 is 91–98% of it,
  and the rest is mostly harmonic 11 (2.9e-18, 1.6e-19, 1.4e-19).
- **The harmonic-13 error, prediction then iterate.**
  - The prediction's is 4.74e-8, 2.25e-8 and 1.10e-8, linear in a.
  - The step-1 iterate's is 3.95e-17, 4.18e-18 and 1.00e-18, falling 9.4 times from a = 1 to 1/2 and 4.2 times from 1/2 to 1/4.
  - On the old build (#752) the iterate's was 2.92e-15 at a = 1 and 3.59e-17 at a = 1/2, 81 times apart. Here it is 74 times smaller at a = 1.
- **The control.** `--mutate k17` reads the planted 1e-20 in harmonic 17 of the first case's iterate as 1.00e-20.
