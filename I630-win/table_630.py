#!/usr/bin/env python3
"""#630: Delta at eta = 20 beside #623's eta = inf, 10, 5 and the verdict of the pre-registered rule (README.md).
usage: python table_630.py [--selftest] [--shift X]       (from this folder; needs data/sigdss_i630.jsonl, data/sigdss_refine_i630_kc{23,39}_eta20.jsonl here and ../I623-win/{kc15_values.json,data/})
Quantities: d = Delta(20) - Delta(inf), e = Delta(20) - Delta(10), at k_c 15, 23, 39. A quantity is RESOLVED when its sign is the same at k_c 23 and 39 and its magnitude at both exceeds its change between
them (c_d = |d_39 - d_23|, c_e = |e_39 - e_23|); otherwise OPEN. --selftest: the rule on planted pairs (some must stay open). --shift X: adds X to Delta(20) at k_c 39 (a mutation)."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
I623 = os.path.join(HERE, "..", "I623-win")


def resolved(v23, v39):
    c = abs(v39 - v23)
    if (v23 > 0) != (v39 > 0):
        return False, c, f"signs differ ({v23:+.3e}, {v39:+.3e})"
    if not (abs(v23) > c and abs(v39) > c):
        return False, c, f"a magnitude does not exceed its change c = {c:.3e} ({abs(v23):.3e}, {abs(v39):.3e})"
    return True, c, f"same sign {'+' if v23 > 0 else '-'}, magnitudes {abs(v23):.3e} and {abs(v39):.3e} both exceed c = {c:.3e}"


def selftest():
    cases = [((-6e-5, -7e-5), True), ((6e-5, -7e-5), False), ((-6e-5, -1.5e-4), False), ((-1e-4, -3e-4), False), ((3e-5, 3.2e-5), True), ((0.0, 1e-9), False)]
    bad = 0
    for (a, b), want in cases:
        got = resolved(a, b)[0]
        print(f"  planted ({a:+.1e}, {b:+.1e}): {'resolved' if got else 'open'} (expected {'resolved' if want else 'open'}) {'ok' if got == want else 'WRONG'}")
        bad += got != want
    print("selftest", "FAILED" if bad else "passed")
    return bad


def last(path):
    if not os.path.exists(path):
        return None
    return [json.loads(ln) for ln in open(path) if ln.strip()][-1]


def main():
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    shift = float(sys.argv[sys.argv.index("--shift") + 1]) if "--shift" in sys.argv else 0.0
    k15 = json.load(open(os.path.join(I623, "kc15_values.json")))
    R = {15: {}, 23: {}, 39: {}}
    for e in ("inf", "10.0000", "5.0000"):
        R[15][e] = dict(Delta=k15[e]["Delta"], F=k15[e]["F"], constraint=k15[e]["constraint"], N=k15[e]["N"])
        for kc in (23, 39):
            R[kc][e] = last(os.path.join(I623, "data", f"sigdss_refine_i623_kc{kc}_eta{e}.jsonl"))
    cont = last(os.path.join(HERE, "data", "sigdss_i630.jsonl"))
    if cont:
        print("continuation record:", {k: cont[k] for k in cont if k in ("par", "eps", "Delta", "F", "ok", "kc", "target")}, "\n")
    R[15]["20.0000"] = None if cont is None else dict(Delta=cont["Delta"], F=cont.get("F"), constraint=cont.get("constraint"), N=cont.get("N"))
    for kc in (23, 39):
        R[kc]["20.0000"] = last(os.path.join(HERE, "data", f"sigdss_refine_i630_kc{kc}_eta20.jsonl"))
    if shift and R[39]["20.0000"]:
        R[39]["20.0000"] = dict(R[39]["20.0000"], Delta=R[39]["20.0000"]["Delta"] + shift)
        print(f"MUTATION: Delta(20) at k_c 39 shifted by {shift:+.1e}\n")
    fmt = lambda v, f: "n/a" if v is None else f % v
    print("| eta | k_c | N | Delta | F | constraint |\n|---|---|---|---|---|---|")
    for e in ("inf", "20.0000", "10.0000", "5.0000"):
        for kc in (15, 23, 39):
            r = R[kc][e]
            if r is None:
                print(f"| {e} | {kc} | | not yet | | |")
            else:
                print(f"| {e} | {kc} | {r.get('N') or ''} | {r['Delta']:.10f} | {fmt(r.get('F'), '%.2e')} | {fmt(r.get('constraint'), '%.4e')} |")
    runs = [R[kc]["20.0000"] for kc in (23, 39)]
    conv = all(r is not None and r["F"] < 1e-10 for r in runs)
    print(f"\nboth refines present and converged (F < 1e-10): {conv if all(runs) else 'n/a until both are present'}")
    q = {}
    print("\n| quantity | k_c 15 | k_c 23 | k_c 39 | change |d_39 - d_23| |\n|---|---|---|---|---|")
    for name, ref in (("d = Delta(20) - Delta(inf)", "inf"), ("e = Delta(20) - Delta(10)", "10.0000")):
        v = [None if R[kc]["20.0000"] is None or R[kc][ref] is None else R[kc]["20.0000"]["Delta"] - R[kc][ref]["Delta"] for kc in (15, 23, 39)]
        q[name[0]] = v
        c = abs(v[2] - v[1]) if v[1] is not None and v[2] is not None else None
        print(f"| {name} | " + " | ".join("n/a" if x is None else f"{x:+.3e}" for x in v) + f" | {fmt(c, '%.3e')} |")
    print()
    for k, name in (("d", "Delta(20) - Delta(inf)"), ("e", "Delta(20) - Delta(10)")):
        v = q[k]
        if v[1] is not None and v[2] is not None:
            ok, c, why = resolved(v[1], v[2])
            print(f"{k} = {name}: {'RESOLVED' if ok and conv else ('OPEN' if not ok else 'OPEN (a refine did not converge)')}: {why}")
    if q["e"][1] is not None and q["e"][2] is not None:
        ok = resolved(q["e"][1], q["e"][2])[0] and conv
        sign = "positive" if q["e"][2] > 0 else "negative"
        print(f"READING (README): e {'resolved ' + sign if ok else 'open'}: " + (
            "the rise toward eta = inf is under way at eta = 20 (Delta(20) above Delta(10))" if ok and q["e"][2] > 0 else
            "Delta(20) is still below Delta(10), the minimum lies at larger eta" if ok else "the sign of Delta(20) - Delta(10) is not settled"))
    for kc, name in ((23, "k_c 23"), (39, "k_c 39")):
        rs = [R[kc][e] for e in ("inf", "20.0000", "10.0000", "5.0000")]
        if all(rs):
            order = sorted(zip(("inf", "20", "10", "5"), [r["Delta"] for r in rs]), key=lambda t: t[1])
            print(f"order of Delta at {name} (low to high): " + " < ".join(f"Delta({a})" for a, _ in order))


if __name__ == "__main__":
    main()
