"""#858: two stored states (four or eight parts) compared: max |z_a - z_b| / max |z_a| from their octo-double difference's
leading part, and Delta_a - Delta_b at 140 digits. Exit 0 when both are at most LIMIT ("agree"), else 1.

    python compare.py HPDIR A.npz B.npz [LIMIT]
"""
import sys

import numpy as np

sys.path.insert(0, sys.argv[1])
import mpmath as mp  # noqa: E402
from multidouble import od_axpy  # noqa: E402
from octo_corrector import _delta, load_o, o8  # noqa: E402

a, b = load_o(sys.argv[2])[0], load_o(sys.argv[3])[0]
lim = float(sys.argv[4]) if len(sys.argv) > 4 else 1e-50
d = o8(od_axpy(-1.0, *b, *a))                       # a - b in octo-double
rel = float(np.abs(d[0]).max() / np.abs(a[0]).max())
with mp.workdps(140):
    dD = _delta(a) - _delta(b)
    ok = rel <= lim and abs(dD) <= lim
    print(f"max|z_a - z_b| / max|z_a| {rel:.3e}; Delta_a - Delta_b {mp.nstr(dD, 5)}; limit {lim:.0e}: "
          f"{'agree' if ok else 'differ'}")
sys.exit(0 if ok else 1)
