# I499-mac: the pinned system's curvature on its weak subspace at D 237.13 and 242.36 (hp/weak_curv.py)

Machine: the M5 Mac (coordinator). Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/499.

States: `I461-win2/crawlI/anm_pin3_D237.1312.npz` and `I461-win2/crawlJ/anm_pin3_D242.3642.npz` (nodes 0.3-0.7, M 32,
kfreeze 3, L 769, their stored plans). Code: `hp/weak_curv.py` at choptuik-large-d f9b8b8f (branch
`wip/i499-coordinator`), k 4, h 1e-20, the basis refined by 3 steps of block inverse iteration in octo-double,
mpmath at 140 digits, 2 threads, nice 10.

The logs and json files are those of the last runs in `exits.txt` (after "rerun with omega"), all from f9b8b8f's code.
The earlier lines of `exits.txt` are runs of earlier versions whose logs were overwritten: an f64 basis (check (b)
failed, since its 1e-16 rounding along J's strong directions gives a linear term of about 1e18 |a|), and the
planted point at |a| = 100 h, beyond the quadratic regime of that basis.

| file | command | exit |
|---|---|---|
| `weak_curv_D242.log`, `.json` | `weak_curv.py RAW <crawlJ D 242.36> --threads=2 --json=...` | 0, (a) and (b) pass |
| `weak_curv_D237.log`, `.json` | the same on crawlI's D 237.13 state | 0, (a) and (b) pass |
| `weak_curv_D242_ctl_offdiag.log` | `--mutate=offdiag` (the model without the cross terms) | 1, (b) fails as it must (0.41) |
| `weak_curv_D242_ctl_h12.log` | `--h=1e-12` (outside the quadratic regime) | 1, (a) fails as it must (0.99) |

Results:

| quantity | D 237.13 | D 242.36 |
|---|---|---|
| sigma_1..4 (refined basis) | 3.00e-25, 3.06e-25, 1.50e-23, 2.71e-23 | 2.52e-27, 2.56e-27, 4.39e-26, 7.93e-26 |
| (a) F'' at h against h/10 | 1.6e-13 | 2.4e-13 |
| quadratic regime on span(V) | to about 2.5e-14 | to about 2.0e-14 |
| max F''(v_j, v_k) | up to 3.3e32 | up to 1.9e33 |
| share of F'' on the weak left subspace U | 3.4e-16 to 8.4e-14 | 1.0e-14 to 1.25e-13 |
| max ||Q_i||, rho = sigma_min / max ||Q_i|| | 8.1e19, 3.7e-45 | 7.6e20, 3.3e-48 |
| omega = max |J^-1 F''(v_j, v_k)|, 2 / omega | 3.07e43, 6.5e-44 | 3.00e46, 6.7e-47 |
| (b) quadratic model at a planted point, |a| 2e-20 | 2.1e-13 | 3.3e-13 |
