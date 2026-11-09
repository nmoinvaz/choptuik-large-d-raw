"""The residual of a chain state by block and field (hp/modecount_probe.probe) in the double-double kernel with the
state's kfreeze, and its residual_q in quad-double, to see where the dd |F| of the chain states comes from.

    python3 chain_blocks.py CODE_HP_DIR STATE.npz [...]
"""
import sys

import numpy as np

sys.path.insert(0, sys.argv[1])
import modecount_probe as P  # noqa: E402
import modecount_common as mc  # noqa: E402
from hpkernel.driver import load_q  # noqa: E402

for f in sys.argv[2:]:
    z, meta = load_q(f)
    zh, zl = np.ascontiguousarray(z[0]), np.ascontiguousarray(z[1] + z[2] + z[3])
    kf = meta.get("kfreeze")
    print(f"{f}: D {meta['D']}, kf {kf}, ks {meta.get('ks')}", flush=True)
    P.probe(meta, zh, zl, kf, rows=4)
    s = mc.build_solver(meta, zh, zl, meta["M"], kf)
    try:
        r = s.residual_q(*z)
        F = np.abs(np.asarray(r[0])).max()
        print(f"    residual_q |F| (leading part) {F:.3e}", flush=True)
    except Exception as e:
        print(f"    residual_q: {type(e).__name__}: {e}", flush=True)
