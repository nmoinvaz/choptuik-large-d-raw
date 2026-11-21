"""#1064 front test at D 262.7908 (I966-mac-sing README, fixed 2026-11-21 17:36:02 UTC): the real pole near 265.078 and
the pair P1 in jets (a) control, (b) re-planned, (c) ks 395, from their locate JSONs.
    python front_compare.py LOC_a.json LOC_b.json LOC_c.json [--mutate=move]
Real pole: the real stable pole (D_im <= 0.05) nearest 265.078 within 0.5. P1: the stable cluster off the axis with
the most approximants (ties: nearest 262.081 +- 0.973i). A move above 0.01 (in Re, and for P1 also in Im) from (a) to
(b) reads 'plan', from (b) to (c) 'truncation'; below 0.01 in both, 'neither'. --mutate=move adds 0.02 to (c)'s real
pole, which must read 'truncation'. Reported, not read: all clusters near the pair, and the recurrence fit."""
import json, sys
mut = "--mutate=move" in sys.argv
L = [json.load(open(f))[0] for f in sys.argv[1:4]]
names = ["(a)", "(b)", "(c)"]
ref = complex(262.081, 0.973)


def real_pole(r):
    q = [p for p in r["pade"] if p["D_im"] <= 0.05 and abs(p["D_re"] - 265.078) <= 0.5]
    return min(q, key=lambda p: abs(p["D_re"] - 265.078)) if q else None


def p1(r):
    q = [p for p in r["pade"] if p["D_im"] > 0.05 and abs(complex(p["D_re"], p["D_im"]) - ref) <= 0.05]
    return max(q, key=lambda p: (p["n"], -abs(complex(p["D_re"], p["D_im"]) - ref))) if q else None


rp = [real_pole(r) for r in L]
if mut and rp[2]:
    rp[2] = dict(rp[2], D_re=rp[2]["D_re"] + 0.02)
pp = [p1(r) for r in L]
for n, r, x, y in zip(names, L, rp, pp):
    near = [p for p in r["pade"] if p["D_im"] > 0.05 and abs(complex(p["D_re"], p["D_im"]) - ref) <= 0.05]
    rec = r["recurrence"]
    print(f"{n} D0 {r['D0']:.4f}, root test {r['root_radius']:.4f}: real pole " + (f"{x['D_re']:.4f} (n {x['n']})" if x else "none")
          + "; P1 " + (f"{y['D_re']:.4f} +- {y['D_im']:.4f}i (n {y['n']})" if y else "none")
          + "; clusters near the pair " + ", ".join(f"{p['D_re']:.4f}+-{p['D_im']:.4f}i n{p['n']}" for p in near)
          + (f"; recurrence {rec['D_re']:.4f} +- {rec['D_im']:.4f}i" if rec else ""))


def move(u, v, im=False):
    if u is None or v is None:
        return None
    return max(abs(u["D_re"] - v["D_re"]), abs(u["D_im"] - v["D_im"]) if im else 0.0)


verdict = {}
for label, f in (("real pole", lambda i: rp[i]), ("P1", lambda i: pp[i])):
    im = label == "P1"
    ab, bc = move(f(0), f(1), im), move(f(1), f(2), im)
    v = ("not read (a jet lacks it)" if ab is None or bc is None else
         "plan" if ab > 0.01 and bc <= 0.01 else "truncation" if bc > 0.01 and ab <= 0.01 else
         "plan and truncation" if ab > 0.01 and bc > 0.01 else "neither")
    verdict[label] = v
    print(f"{label}: (a)-(b) {'none' if ab is None else f'{ab:.4f}'}, (b)-(c) {'none' if bc is None else f'{bc:.4f}'}: {v}"
          + (" (--mutate=move)" if mut else ""))
sys.exit(0)
