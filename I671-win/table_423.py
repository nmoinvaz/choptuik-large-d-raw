#!/usr/bin/env python3
"""#423: the table of rt_sigma.py's bounds and x's content per (state, start kind), and the (H) / (C) / neither verdict per D, by the rules fixed in README.md before the data.
usage: python table_423.py [--selftest]          (from this folder; reads logs/<label>_<smooth|rough>.log)
Per run (state, kind): the best (smallest) bound over its starts, the spread of the starts' bounds, the worst solve residual, and the content of the best start's x: |mu| / max|x|, F = the largest field maximum
of x / max|x|, and relative to F the edge content E = max_f max(P_f, M_f), the centre content C0 = max_f C_f and the omega_4 centre content C4 = C_w4 (P, C, M: column maxima at xi = +1, near 0, -1).
Class: edge if E >= 0.5 and E >= 3 C0; centre in omega_4 if C4 >= 0.5 and C4 >= 3 E; mixed otherwise. Smooth against rough: seen by smooth if bound_smooth <= 100 bound_rough. D trend on 32x121:
the rough bound's decades per step of 10 in D between D 30, 40, 50, 54.996085; horizon-like if it falls by more than 3 decades per 10 in D, not horizon-like within 1 decade either way, in between otherwise.
Verdict per D: (H) = edge + seen only by rough + horizon-like; (C) = centre in omega_4 + seen by smooth + not horizon-like; neither otherwise, naming the three. --selftest: planted logs of known class."""
import glob
import math
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
NUM = r"[0-9.]+(?:e[+-]?[0-9]+)?"
START = re.compile(rf"start (\d+): max\|x\| ({NUM}), bound on the smallest gain ({NUM}), max\|J x - v\| ({NUM}), (\d+) products")
CONT = re.compile(r"start (\d+), x / max\|x\|: (.*)")
FIELD = re.compile(rf"(w\d) max ({NUM}) \(harmonics 0-3 (.*?), 16 ({NUM}); xi=\+1 ({NUM}), ~0 ({NUM}), -1 ({NUM})\)")
HEAD = re.compile(rf"(\S+\.npz): D ({NUM}) (\d+)x(\d+) K (\d+), max\|F\| ({NUM})")


def parse(text):
    r = dict(head=None, rough=None, starts={}, content={})
    for ln in text.splitlines():
        m = HEAD.search(ln)
        if m and r["head"] is None:
            r["head"] = dict(state=m.group(1), D=float(m.group(2)), Nt=int(m.group(3)), N=int(m.group(4)), K=int(m.group(5)), F=float(m.group(6)))
        if "right-hand sides:" in ln:
            r["rough"] = "rough" in ln
        m = START.search(ln)
        if m:
            r["starts"][int(m.group(1))] = dict(maxx=float(m.group(2)), bound=float(m.group(3)), res=float(m.group(4)), prods=int(m.group(5)))
        m = CONT.search(ln)
        if m:
            body = m.group(2)
            mu = re.search(r"mu ([+-]" + NUM + ")", body)
            fields = {f[0]: dict(max=float(f[1]), P=float(f[4]), C=float(f[5]), M=float(f[6])) for f in FIELD.findall(body)}
            r["content"][int(m.group(1))] = dict(mu=abs(float(mu.group(1))) if mu else None, fields=fields)
    return r


def summarize(r):
    if not r["starts"]:
        return None
    best = min(r["starts"], key=lambda i: r["starts"][i]["bound"])
    b = [s["bound"] for s in r["starts"].values()]
    out = dict(best=best, bound=r["starts"][best]["bound"], spread=max(b) / min(b), res=max(s["res"] for s in r["starts"].values()), prods=max(s["prods"] for s in r["starts"].values()), n=len(b))
    c = r["content"].get(best)
    if c and c["fields"]:
        fl = c["fields"]
        F = max(f["max"] for f in fl.values())
        E = max(max(f["P"], f["M"]) for f in fl.values()) / F
        C0 = max(f["C"] for f in fl.values()) / F
        C4 = fl["w4"]["C"] / F if "w4" in fl else float("nan")
        cls = "edge" if E >= 0.5 and E >= 3 * C0 else ("centre in w4" if C4 >= 0.5 and C4 >= 3 * E else "mixed")
        out.update(mu=c["mu"], E=E, C0=C0, C4=C4, cls=cls)
    return out


def selftest():
    def log(kind, bound, w4c, edge):
        return (f"x_D40.0201_32x81.npz: D 40.0 32x81 K 0, max|F| 1.0e-31\n  right-hand sides: {kind}\n"
                f"  start 0: max|x| {1 / bound:.3e}, bound on the smallest gain {bound:.3e}, max|J x - v| 1.0e-20, 50 products\n"
                f"  start 0, x / max|x|: mu +1.0e-01; w1 max 1.0e-01 (harmonics 0-3 1e-01 1e-02 1e-03 1e-04, 16 1e-10; xi=+1 {edge:.0e}, ~0 1e-03, -1 {edge:.0e}); "
                f"w4 max 1.0e+00 (harmonics 0-3 1e-01 1e-02 1e-03 1e-04, 16 1e-10; xi=+1 {edge:.0e}, ~0 {w4c:.0e}, -1 {edge:.0e})\n")
    cases = [("planted edge", log("smooth fields", 1e-30, 1e-3, 9e-1), "edge"), ("planted centre", log("smooth fields", 1e-30, 9e-1, 1e-3), "centre in w4"),
             ("planted mixed", log("smooth fields", 1e-30, 4e-1, 4e-1), "mixed")]
    bad = 0
    for name, text, want in cases:
        s = summarize(parse(text))
        ok = s is not None and s["cls"] == want and abs(s["bound"] - 1e-30) < 1e-40
        print(f"  {name}: class {s['cls'] if s else None} (expected {want}), bound {s['bound'] if s else None} {'ok' if ok else 'WRONG'}")
        bad += not ok
    print("selftest", "FAILED" if bad else "passed")
    return bad


def main():
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    runs = {}
    for p in sorted(glob.glob(os.path.join(HERE, "logs", "*_*.log"))):
        base = os.path.basename(p)[:-4]
        if not (base.endswith("_smooth") or base.endswith("_rough")) or base.startswith("driver"):
            continue
        label, kind = base.rsplit("_", 1)
        r = parse(open(p, encoding="utf-8", errors="replace").read())
        if r["head"] is None or not r["starts"]:
            continue
        runs[(label, kind)] = (r["head"], summarize(r))
    print("| state | D | grid | kind | bound (best of starts) | starts' spread | worst residual | products | x: mu | E (edge) | C0 (centre) | C4 (w4 centre) | class |\n|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    for (label, kind), (h, s) in sorted(runs.items(), key=lambda kv: (kv[1][0]["D"], kv[1][0]["Nt"], kv[1][0]["N"], kv[0][1])):
        f = lambda k, fmt: fmt % s[k] if k in s and s[k] is not None else "n/a"
        print(f"| {h['state']} | {h['D']:.6f} | {h['Nt']}x{h['N']} | {kind} | {s['bound']:.3e} | {s['spread']:.1f} | {s['res']:.1e} | {s['prods']} | {f('mu', '%.2f')} | {f('E', '%.2f')} | {f('C0', '%.2f')} | {f('C4', '%.2f')} | {s.get('cls', 'n/a')} |")
    # smooth against rough, and the D trend on 32x121
    print("\n| state | rough bound | smooth bound | smooth / rough | seen by smooth (<= 100) |\n|---|---|---|---|---|")
    pairs = {}
    for (label, kind), (h, s) in runs.items():
        pairs.setdefault(label, {})[kind] = (h, s)
    for label, d in sorted(pairs.items(), key=lambda kv: (list(kv[1].values())[0][0]["D"], list(kv[1].values())[0][0]["N"])):
        if "rough" in d and "smooth" in d:
            ratio = d["smooth"][1]["bound"] / d["rough"][1]["bound"]
            print(f"| {d['rough'][0]['state']} | {d['rough'][1]['bound']:.3e} | {d['smooth'][1]['bound']:.3e} | {ratio:.2e} | {'yes' if ratio <= 100 else 'no'} |")
    g121 = sorted([(h["D"], s["bound"], label) for (label, kind), (h, s) in runs.items() if kind == "rough" and h["Nt"] == 32 and h["N"] == 121])
    print("\nD trend on 32x121 (rough bound):")
    trend = {}
    for (D1, b1, _), (D2, b2, _) in zip(g121, g121[1:]):
        dec = math.log10(b2 / b1) * 10.0 / (D2 - D1)
        cls = "horizon-like" if dec < -3 else ("not horizon-like" if abs(dec) <= 1 else "in between")
        trend[D2] = trend.setdefault(D1, (dec, cls)) and (dec, cls)
        print(f"  D {D1:.6f} -> {D2:.6f}: bound {b1:.3e} -> {b2:.3e}, {dec:+.2f} decades per 10 in D, {cls}")
    print("\nVerdict per D (32x121 runs; trend from the step ending at D, D 30 from the step starting at it):")
    Ds = [g[0] for g in g121]
    for i, D in enumerate(Ds):
        lab = [l for (DD, _, l) in g121 if DD == D][0]
        rough, smooth = runs.get((lab, "rough")), runs.get((lab, "smooth"))
        if rough is None or smooth is None:
            continue
        s_r, s_s = rough[1], smooth[1]
        seen_smooth = s_s["bound"] <= 100 * s_r["bound"]
        step = (math.log10(g121[i][1] / g121[i - 1][1]) * 10.0 / (g121[i][0] - g121[i - 1][0]) if i > 0
                else (math.log10(g121[1][1] / g121[0][1]) * 10.0 / (g121[1][0] - g121[0][0]) if len(g121) > 1 else None))
        tcls = None if step is None else ("horizon-like" if step < -3 else ("not horizon-like" if abs(step) <= 1 else "in between"))
        cls = s_r.get("cls")
        if cls == "edge" and not seen_smooth and tcls == "horizon-like":
            v = "(H)"
        elif cls == "centre in w4" and seen_smooth and tcls == "not horizon-like":
            v = "(C)"
        else:
            v = "neither"
        print(f"  D {D:.6f}: x {cls} (rough start); smooth {'sees it' if seen_smooth else 'does not see it'}; trend {tcls} ({'n/a' if step is None else f'{step:+.2f}'} decades per 10 in D) -> {v}")

    # the bounds against N at fixed D and N_t, and the N_t effect at D 40 on N = 141
    print("\nRough bound against N at fixed D and N_t (decades between neighbouring N):")
    byD = {}
    for (label, kind), (h, s) in runs.items():
        if kind == "rough":
            byD.setdefault((round(h["D"], 3), h["Nt"]), []).append((h["N"], s["bound"]))
    for (D, Nt), lst in sorted(byD.items()):
        lst.sort()
        steps = ", ".join(f"{n1}->{n2}: {math.log10(b2 / b1):+.2f}" for (n1, b1), (n2, b2) in zip(lst, lst[1:]))
        print(f"  D {D}, N_t {Nt}: " + "; ".join(f"N {n}: {b:.2e}" for n, b in lst) + (f"  ({steps} decades)" if steps else ""))
    for kind in ("rough", "smooth"):
        a, b = runs.get(("D40_32x141", kind)), runs.get(("D40_48x141", kind))
        if a and b:
            print(f"N_t effect at D 40.02, N 141, {kind}: {a[1]['bound']:.3e} (N_t 32) -> {b[1]['bound']:.3e} (N_t 48), factor {b[1]['bound'] / a[1]['bound']:.3f}; class {a[1].get('cls')} -> {b[1].get('cls')}")


if __name__ == "__main__":
    main()
