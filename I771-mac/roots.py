"""the two zeros of D(lambda) for several settings of the method (#771); one record per setting and zero"""
import sys, json, time, math
sys.path.insert(0, '/Users/nathan/Source/choptuik-large-d-771/solver/matter')
import css_inf_jump as m
out = sys.argv[1]
settings = [dict(r0=0.1, r1=0.3, alpha=0.375, rtol=1e-13), dict(r0=0.1, r1=0.25, alpha=0.375, rtol=1e-13),
            dict(r0=0.09, r1=0.3, alpha=0.375, rtol=1e-13), dict(r0=0.11, r1=0.3, alpha=0.375, rtol=1e-13),
            dict(r0=0.1, r1=0.3, alpha=0.3, rtol=1e-13), dict(r0=0.1, r1=0.3, alpha=0.375, rtol=1e-12),
            dict(r0=0.1, r1=0.32, alpha=0.375, rtol=1e-13)]
for st in settings:
    t0 = time.time()
    P = m.Problem(r0=st['r0'], r1=st['r1'], alpha=st['alpha'] * math.pi, rtol=st['rtol'], N=160)
    x, j = P.select(log=lambda s: None)
    for start in (2.05, 0.53 + 7.93j):
        t = time.time()
        lam, it = P.root(start, log=lambda s: None)
        rec = dict(kind='root', **st, N=160, f0=x[0], omega=x[1], bg_jump=j, start=[complex(start).real, complex(start).imag],
                   lam=[lam.real, lam.imag], iterations=it, D_at_root=abs(P.det(lam)), seconds=round(time.time() - t, 1))
        print(json.dumps(rec), flush=True)
        open(out, 'a').write(json.dumps(rec) + '\n')
