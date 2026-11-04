# formula-mac: the search for a non-series representation of Delta(D), its planted tests and fits

Mac, 2026-11-04, two coordinator subagents (read-only on the code repository). The first pass is in the top
folder (float64 and 60-digit scans; its low-D numbers are float64 artifacts, see v2/cond_probe.py). v2/ is the second
pass at 256 bits (python-flint): the pass criteria are frozen in v2/planted.py's docstring, the plants P0 (pole-only),
P7 (cut [-9, 3]), P8 (cut misplaced at -6), Pz and Pe in v2/planted_*.log/json, the real fits in v2/real.log, the
closed forms in v2/closed_*.log, the cut density in v2/density.log, the Taylor-radius check in v2/radius.log, and the
recommended series in v2/export_rec.log and v2/rec_coefficients.json. The code repository's hp/formula_cut_fit.py
reproduces that series from hp/data/delta_dd.csv and delta_dd_lowD.csv, and hp/formula_cut.py evaluates and checks it.
The scripts carry the scratch paths they ran from.
