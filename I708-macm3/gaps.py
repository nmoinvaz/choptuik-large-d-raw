"""Open work of each circle from its evals cache, with modecount_circle.py's detrending (beta from c +- 2R), its step
tolerance pi/4 and its alias rule (arc length * local scale <= pi/2, 3 arcs each side). Control: the closed circles'
records (max_step, winding, points, alias_left) must be reproduced.
    python3 -I gaps.py <path to I708-macm3>"""
import json, math, glob, sys
TOL, ALIAS, NB, RAD = math.pi / 4, math.pi / 2, 3, 0.36
wrap = lambda x: (x + math.pi) % (2 * math.pi) - math.pi

def analyse(path, c):
    ev = {}
    for l in open(glob.glob(f"{path}/data/*evals.jsonl")[0]):
        if l.strip():
            e = json.loads(l); ev[(e["re"], e["im"])] = (e["lnabs"], e["arg"])
    near = lambda x, y: min(ev, key=lambda k: abs(complex(*k) - complex(x, y)))
    kp, km = near(c.real + 2 * RAD, c.imag), near(c.real - 2 * RAD, c.imag)
    assert abs(complex(*kp) - (c + 2 * RAD)) < 1e-12 and abs(complex(*km) - (c - 2 * RAD)) < 1e-12
    (lp, ap), (lm, am) = ev[kp], ev[km]
    beta = complex(lp - lm, wrap(ap - am)) / (4 * RAD)
    vals = {}
    for (x, y), (la, arg) in ev.items():
        lam = complex(x, y)
        if abs(abs(lam - c) - RAD) < 1e-9:
            s = (math.atan2((lam - c).imag, (lam - c).real) / (2 * math.pi)) % 1.0
            v = complex(la, arg) - beta * (lam - c)
            vals[round(s, 12)] = (v.real, wrap(v.imag))
    vals[1.0] = vals[min(vals)]  # s = 0 closes the circle
    ts = sorted(vals)
    L = 2 * math.pi * RAD
    st = [wrap(vals[b][1] - vals[a][1]) for a, b in zip(ts[:-1], ts[1:])]
    sc = [abs(complex(vals[b][0] - vals[a][0], s)) / ((b - a) * L) for (a, b), s in zip(zip(ts[:-1], ts[1:]), st)]
    local = lambda i: max(sc[(i + j) % len(sc)] for j in range(-NB, NB + 1))
    hs = [(b - a) * L * local(i) for i, (a, b) in enumerate(zip(ts[:-1], ts[1:]))]
    return dict(points=len(ts) - 1, winding=sum(st) / (2 * math.pi), max_step=max(abs(s) for s in st),
                above_tol=sum(abs(s) > TOL for s in st), alias_left=sum(h > ALIAS for h in hs),
                half_tol=sum(abs(s) > TOL / 2 for s in st))

if __name__ == "__main__":
    R0 = sys.argv[1]  # the I708-macm3 folder
    for kf in (35, 37):
        for path in sorted(glob.glob(f"{R0}/kf{kf}/c_*")):
            n = path.rsplit("/", 1)[1]
            cx = float(n.split("_")[1]); cy = float(n.split("_")[2].replace("p", "").replace("m", "-"))
            r = analyse(path, complex(cx, cy))
            rec = None
            try:
                rec = [json.loads(l) for l in open(f"{path}/data/modecount_circles.jsonl") if l.strip()][-1]
            except FileNotFoundError:
                pass
            line = (f"kf {kf} {n}: {r['points']} points, winding {r['winding']:+.3f}, max step {r['max_step']:.3f}, "
                    f"{r['above_tol']} arcs above pi/4, {r['alias_left']} failing the alias rule, {r['half_tol']} above pi/8")
            if rec:
                ok = (r["points"] == rec["points"] and abs(r["max_step"] - rec["max_step"]) < 1e-9
                      and abs(r["winding"] - rec["winding"]) < 1e-9 and r["alias_left"] == rec["alias_left"])
                line += f"   [closed; record: {rec['points']} points, winding {rec['winding']:+.0f}, max step {rec['max_step']:.3f}, alias_left {rec['alias_left']}; reproduced: {ok}]"
            print(line)
