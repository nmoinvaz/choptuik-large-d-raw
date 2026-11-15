"""print newton_od_toy's full logs (both tests at verbose 2, the why case at 1, the drop cases) from the hp dir given,
with the seconds fields removed, for a diff of the default path before and after #854"""
import contextlib, io, re, sys
sys.path.insert(0, sys.argv[1])
import numpy as np
import newton_od_toy as t
from octo_corrector import newton_od
out = []
for accept in ("own", "natural"):
    conv, log = t.run(accept, 2)
    out.append(f"== {accept} conv {conv}\n{log}")
for k, y0 in ((1.0, 1e-3),):
    z = [np.array([y0, -k / 2 * y0 ** 2 * 1.001])] + [t.ZERO] * 7
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        z2, hist, conv = newton_od(t.Toy(k), z, tol=1e-20, it_max=40, accept="natural", strong_chord=1, verbose=2)
    out.append(f"== chord conv {conv} z {z2[0].tolist()}\n{buf.getvalue()}\n{hist}")
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    t.why_check()
out.append("== why\n" + buf.getvalue())
print(re.sub(r"[0-9.]+ s\b", "S s", re.sub(r"'seconds': [0-9.]+", "'seconds': S", "\n".join(out))))
