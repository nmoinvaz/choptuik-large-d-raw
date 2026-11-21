# I1035-mac/stage1b: the curvature test of FACTORED_HORIZON 5.2 (stage 1b), Q_fact against Q_old at D 73 and 242.36

Machine: the coordinator's M5 Mac, a subagent, one process at nice 10. Issue:
https://github.com/nmoinvaz/choptuik-large-d/issues/1035

Code: `hp/factored_horizon.py` (commands curvjac, curv, curvx, curvxq) on the branch `feat/factored-horizon-curvature`
of choptuik-large-d (from main 276aa1cd), venv-314 (Python 3.14, mpmath 1.3.0, numpy 2.5.4). Measure, gates and
controls are in notes/FACTORED_HORIZON.md 5.2, committed before any run (204ce9e4 and the commit after it).
The controls' options came after the first runs: `--mutate` in e788ad15, `--plant_c` in d6e18642.

Inputs (read from this repository with `git show origin/main:<path>`): `T81/conv_pin5_D73.0000_D73.000000.npz` and
`I461-win2/crawlJ/anm_pin3_D242.3642.npz`; the cross-check starts from stage 1's references `../ref_D73_288.json` and
`../ref_D242_288.json` (as written in stage 1).

Files, one `<name>.log` (stdout) and `<name>.json` (record) per run, `queue.log` (start, end and exit of each) and
`queue.sh`, `queue2.sh`, `queue3.sh` (the run order, with the scratch paths they ran from):
- `curvjac_<D>`: the base (exact 1/k, a_h re-solved so a's sum at u0 equals the node's a) and the M x M Jacobian of
  a(u0) in a_h, cached in `cache_<D>.json`.
- `curv_<D>_<move>`: Q_old (fixed a_h, four t pairs) and Q_fact (fixed a_K, method A, t = 1e-20 and 1e-19), the t^2
  checks, the ratio and its gate, for the moves D (Delta), m1 and m3 (m_h along cos theta and cos 3 theta).
- `plant_<D>`: the planted quadratic term along Delta at the gate-1 level, recovered to 1% or not.
- `plant_D242_c1e16`: the planted term at D 242.36 with c = 1e16 (`--plant_c`), an amendment made after `plant_D242`
  failed (its gate-1 level, c = 1.65e49, moves Delta by 1.7e9 at t = 1e-20 and A's Newton overflows).
- `mut_r0_D73` and `mut_plant1_D73`: the controls that must exit 1 (`--mutate=r0`, R(0) shifted by 1e-40;
  `--mutate=plant1`, the term planted at +t only).
- `curvx_<D>_<t>` and `curvxq_<D>`: the stage-1 fixed point along Delta at t = +-1e-20 and 0, against method A.
