"""the re-seed with the u0 polish's divergence guard (rise_max) varied, on stored predictions"""
import sys
sys.path.insert(0, "/Users/nathan/Source/choptuik-large-d/hp")
import mpmath as mp
from hpkernel.driver import load_q
import reseed as RS
for path in sys.argv[2:]:
    z4, m = load_q(path)
    for rm in [float(x) for x in sys.argv[1].split(",")]:
        rs = RS.Reseeder(m, mp.mpf(m["D_str"]), threads=4, qd=True)
        inv = rs.invert_q
        rs.invert_q = lambda z, d, rm=rm, **kw: inv(z, d, rise_max=rm)
        _, diag = rs.reseed(z4)
        q = [r for r in diag["rungs"] if r.get("qd")][-1]
        print(f"{path.split('/')[-1]} rise_max {rm:.0e}: re-seed {'ok' if diag['ok'] else 'FAILED'}, u0 |R| {q['R']:.2e}, {q['its']} its", flush=True)
