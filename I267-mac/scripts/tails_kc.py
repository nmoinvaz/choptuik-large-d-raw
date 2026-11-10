"""tails of D 30's state at M 32 and resampled to M 48, for several kc (sizing the #267 planted state)"""
import sys
import time
sys.path.insert(0, sys.argv[1] + "/hp")
import gamma_dd as g  # noqa: E402
from hpkernel.driver import load  # noqa: E402

zh, zl, meta = load(sys.argv[1] + "/hp/data/states/up6_D30.0688.npz")
K = len(meta["nodes"])
hh, hl = g.resample_hi(zh, zl, 32, 48, K, None)
for kc in [int(x) for x in sys.argv[2].split(",")]:
    t = time.time()
    m = dict(meta, kc=kc)
    s, F, _ = g.best_solver(m, zh, zl, 1, force="none")
    t32 = g.tails_of(s, zh, zl, m)
    m48 = dict(m, M=48)
    s48, F48, _ = g.best_solver(m48, hh, hl, 1, M=48, force="none")
    t48 = g.tails_of(s48, hh, hl, m48)
    print(f"kc {kc}: M32 |F| {F:.1e} {g.mc.tails_text(t32)} | M48 start |F| {F48:.1e} {g.mc.tails_text(t48)} "
          f"({time.time() - t:.0f} s)", flush=True)
