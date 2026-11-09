"""A chain state's residual by block in double-double (Solver.residual), quad-double (residual_q) and octo-double
(residual_o, all eight parts where stored), to see whether the dd horizon series of hp/series_truncation.py
represents the chain's own (od / qd) horizon block at large D.

    python3 chain_od_residual.py CODE_HP_DIR STATE.npz [...]
"""
import json
import sys

import numpy as np

sys.path.insert(0, sys.argv[1])
import modecount_common as mc  # noqa: E402

for f in sys.argv[2:]:
    d = np.load(f)
    meta = json.loads(str(d["meta"]))
    parts = [np.ascontiguousarray(np.asarray(d[k], float)) for k in ("zh", "zl", "z2", "z3", "z4", "z5", "z6", "z7")
             if k in d.files]
    while len(parts) < 8:
        parts.append(np.zeros_like(parts[0]))
    M, K = meta["M"], len(meta["nodes"])
    kf = meta.get("kfreeze")
    zh, zl = parts[0], np.ascontiguousarray(parts[1] + parts[2] + parts[3])
    s = mc.build_solver(meta, zh, zl, M, kf)
    out = {}
    out["dd"] = np.asarray(s.residual(zh, zl)[0]) + np.asarray(s.residual(zh, zl)[1])
    out["qd"] = np.asarray(s.residual_q(*parts[:4])[0])
    try:
        out["od"] = np.asarray(s.residual_o(parts)[0])
    except TypeError:
        out["od"] = np.asarray(s.residual_o(parts, 0)[0])
    print(f"{f.split('/')[-3:]}: D {meta['D']} kf {kf} ks {meta.get('ks')}")
    names = ["centre"] + [f"seg{b}" for b in range(1, K)] + ["horizon"]
    for k, F in out.items():
        cells = []
        for b in range(K + 1):
            for q, fld in enumerate("pmac"):
                o = b * 4 * M + q * M
                cells.append((names[b], fld, float(np.abs(F[o:o + M]).max())))
        hz = ", ".join(f"{fld} {v:.1e}" for n, fld, v in cells if n == "horizon")
        rest = max(v for n, fld, v in cells if n != "horizon")
        print(f"  {k}: |F| {np.abs(F).max():.2e}; horizon block {hz}; other blocks max {rest:.1e}", flush=True)
