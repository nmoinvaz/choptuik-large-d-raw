"""#1021: is the planted zero counted? PLANT is the count json of argcount's --plant=A0,W0 run over the 32 cells.
Criteria (the issue's "a planted zero inside one of the 32 cells is counted", fixed before the run):
  1. the count lists one zero of sign +1 whose cell contains (A0, W0);
  2. the box of the 32 that contains (A0, W0) has a resolved boundary winding (an integer to 0.1);
  3. with --record, that box winds the record's winding of it plus 1, every other box winds as in the record (both
     unresolved counts as the same), and the zeros outside the planted box are the record's (sign and cell).
Unresolved boxes and cells are listed. --mutate=shift moves (A0, W0) by +0.25 in A (one box), so criterion 1 must fail.
    python plant_check.py PLANT [--record RECORD] [--at 3.53,0.555] [--mutate=shift]
    python plant_check.py --selftest        synthetic counts: plain passes; shift, nozero (no planted zero) and norise
                                            (the planted box winds as in the record) must fail"""
import json, math, sys


def check(P, R, at, out=print):
    a0, w0 = at
    inside = lambda c: c[0] <= a0 <= c[1] and c[2] <= w0 <= c[3]
    inbox = lambda b: b[0][0] <= a0 <= b[0][1] and b[1][0] <= w0 <= b[1][1]
    ok = True
    hit = [z for z in P["zeros"] if z["W"] == 1 and inside(z["cell"])]
    loc = hit[0].get("located") if len(hit) == 1 else None
    out(f"1. zeros of sign +1 whose cell contains ({a0}, {w0}): {len(hit)}"
        + (f"; located at ({loc['A']:.6f}, {loc['wf']:.6f}), {math.hypot(loc['A'] - a0, loc['wf'] - w0):.2g} away" if loc else ""))
    ok &= len(hit) == 1
    pb = [i for i, b in enumerate(P["boxes"]) if inbox(b["box"])]
    wp = P["boxes"][pb[0]]["boundary_winding"] if len(pb) == 1 else float("nan")
    res = lambda w: isinstance(w, (int, float)) and math.isfinite(w) and abs(w - round(w)) < 0.1
    out(f"2. boxes containing it: {len(pb)}; its boundary winding {wp:.3f}")
    ok &= len(pb) == 1 and res(wp)
    nanP = [i for i, b in enumerate(P["boxes"]) if not res(b["boundary_winding"])]
    out(f"   unresolved boxes {len(nanP)} of {len(P['boxes'])}; unresolved cells {len(P['unresolved'])}")
    if R is not None:
        same = len(R["boxes"]) == len(P["boxes"]) and all(
            rb["box"] == pbx["box"] for rb, pbx in zip(R["boxes"], P["boxes"]))
        diff = []
        for i, (rb, pbx) in enumerate(zip(R["boxes"], P["boxes"])):
            wr, wq = rb["boundary_winding"], pbx["boundary_winding"]
            want = (round(wr) + 1 if res(wr) else None) if i in pb else (round(wr) if res(wr) else None)
            got = round(wq) if res(wq) else None
            if want != got:
                diff.append((i, wr, wq))
        pbox = P["boxes"][pb[0]]["box"] if len(pb) == 1 else None
        outside = lambda zs: sorted((z["W"], tuple(z["cell"])) for z in zs if not (pbox and inbox_cell(z["cell"], pbox)))
        zr, zp = outside(R["zeros"]), outside(P["zeros"])
        out(f"3. same 32 boxes: {same}; boxes whose winding is not the record's (+1 in the planted box): {len(diff)}"
            + "".join(f"\n     box {i}: record {wr}, plant {wq}" for i, wr, wq in diff[:8])
            + f"; zeros outside the planted box the same: {zr == zp} ({len(zr)} in the record, {len(zp)} in the plant)")
        ok &= same and not diff and zr == zp
    out(f"plant check: {'PASS' if ok else 'FAIL'}")
    return ok


def inbox_cell(c, b):
    return b[0][0] <= c[0] and c[1] <= b[0][1] and b[1][0] <= c[2] and c[3] <= b[1][1]


def selftest(mutate):
    box = lambda a, w, W: dict(box=[[a, a + 0.25], [w, w + 0.1]], boundary_winding=W)
    R = dict(boxes=[box(3.4123, 0.5065, 0.0), box(3.6623, 0.5065, -1.0), box(3.9123, 0.5065, float("nan"))],
             zeros=[dict(W=-1, cell=[3.7, 3.72, 0.52, 0.53])], unresolved=[[3.95, 3.97, 0.55, 0.56]])
    zp = [dict(W=1, cell=[3.52, 3.54, 0.55, 0.56], located=dict(A=3.53, wf=0.555))] if mutate != "nozero" else []
    P = dict(boxes=[box(3.4123, 0.5065, 0.0 if mutate == "norise" else 1.0), box(3.6623, 0.5065, -1.0),
                    box(3.9123, 0.5065, float("nan"))],
             zeros=zp + R["zeros"], unresolved=R["unresolved"])
    at = (3.53 + (0.25 if mutate == "shift" else 0), 0.555)
    return check(P, R, at, out=lambda s: None)


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        r = [selftest(None), selftest("shift"), selftest("nozero"), selftest("norise")]
        print(f"selftest plain, --mutate=shift, nozero, norise: {['PASS' if x else 'FAIL' for x in r]} "
              "(must be PASS FAIL FAIL FAIL)")
        sys.exit(0 if r == [True, False, False, False] else 1)
    args = [a for a in sys.argv[2:] if not a.startswith("--mutate=")]
    opt = dict(zip(args[0::2], args[1::2]))
    at = tuple(float(v) for v in opt.get("--at", "3.53,0.555").split(","))
    if "--mutate=shift" in sys.argv:
        at = (at[0] + 0.25, at[1])
        print(f"mutate=shift: plant point moved to {at}")
    P = json.load(open(sys.argv[1]))
    R = json.load(open(opt["--record"])) if "--record" in opt else None
    sys.exit(0 if check(P, R, at) else 1)
