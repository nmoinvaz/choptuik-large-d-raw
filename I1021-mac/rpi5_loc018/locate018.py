"""#1013 loc018 (rpi5): the zeros in recount3's two lower unions at xi1 0.18, located by argcount's Newton and then
counted in relocation boxes under 0.02, as #1021's loc did.
    python locate018.py run CODE CACHE SEED OUT.json [--procs 4]
        argcount's locate_many (Newton on the unguarded values, finite-difference Jacobians from the cell's centre)
        from the centres of U1 and U2 on the plain map, and from the centre of the control box C0 on the map with a
        +1 planted at P0. New points go to CACHE (its records are the plain f_M3 values; the plant is applied after).
    python locate018.py check OUT.json [--mutate=shift|sign]
    python locate018.py boxes OUT.json > LEAVES.jsonl        relocation boxes B1, B2 around the located zeros, and C0
    python locate018.py check2 COUNT_PLAIN.json OUT.json [--mutate=shift|sign]
    python locate018.py --selftest
Criteria (fixed before the run):
  check (stage 1): for U1 and U2, Newton ends (not None, that is inside the cell's double), inside U, with Jacobian
    sign W(U) (U1 +1, U2 -1), and |R| at the end at most 10 sigma (its rounding floor). For C0 on the planted map, it
    ends within 0.05 of C0's size of P0 in each coordinate, with sign +1.
  check2 (stage 2, argcount's plain recount of B1, B2 and C0): B1 lies inside U1 and B2 inside U2; B1 winds +1 and
    B2 -1, each resolved, with no unresolved leaf and exactly one zero of that sign, located inside the box and within
    0.1 of the box's size of stage 1's point in each coordinate; C0 winds 0, resolved, with no zero.
  The planted recount (--plant=P0) is checked against the plain one by plant_check.py.
--mutate=shift moves the expected point by one box width in A (P0 in check, stage 1's points in check2); --mutate=sign
flips the expected signs. Each must make its check fail. --selftest runs check and check2 on synthetic results, plain
and with each mutation (must give PASS FAIL FAIL, twice)."""
import json
import math
import sys

U = {"U1": ((4.0498456, 4.0810956, 0.50654321, 0.53154321), +1),   # recount3's unions (union_winding.py: W(U))
     "U2": ((4.2373456, 4.2998456, 0.53154321, 0.55654321), -1)}
C0 = (3.9560956, 3.9717206, 0.5565432, 0.5690432)                  # control box, in a resolved W = 0 leaf of cell 7
P0 = (3.9623456, 0.5615432)                                         # the plant, at 0.4 of each of C0's ranges
DA, DW = 0.015625, 0.0125                                           # relocation box size (under --hzero 0.02)
BOUNDS = dict(rhs=1e7, wall=3600.0, noise3=1e7, starts=[0.2, 0.25])  # recount3's --m3maxrhs, --m3wall, ... --m3starts


def inside(p, c):
    return c[0] <= p[0] <= c[1] and c[2] <= p[1] <= c[3]


def run(code, cache, seed, out, procs):
    sys.path.insert(0, code + "/solver/inner_stokes")
    import argcount as ac

    def mult(plant):
        F = ac.Multiplier(3, cache, procs, plant, r1=0.18, m3fix=True, retry=True, bounds=dict(BOUNDS))
        F.extra[(-1.0, -1.0)] = dict(F3re=float(((2.7264758856 / 2j) * (0.0532 + 0.0041j)).real),   # as argcount's main
                                     F3im=float(((2.7264758856 / 2j) * (0.0532 + 0.0041j)).imag), info=0.0)
        for r in map(json.loads, open(seed)):
            F.extra.setdefault((r["A"], r["wf"]), ac.Multiplier.seed_record(r))
        return F
    res = {}
    F = mult(None)
    for (name, (c, W)), z in zip(U.items(), ac.locate_many(F, [c for c, _ in U.values()])):
        res[name] = dict(cell=list(c), W=W, start=[(c[0] + c[1]) / 2, (c[2] + c[3]) / 2], located=z)
        print(f"{name}: {z}", flush=True)
    F.close()
    Fp = mult(P0)
    z = ac.locate_many(Fp, [C0])[0]
    res["C0"] = dict(cell=list(C0), W=1, plant=list(P0), start=[(C0[0] + C0[1]) / 2, (C0[2] + C0[3]) / 2], located=z)
    print(f"C0 (planted at {P0}): {z}", flush=True)
    Fp.close()
    json.dump(res, open(out, "w"), indent=1)


def check(res, mutate=None, out=print):
    ok = True
    for name in ("U1", "U2"):
        r = res[name]
        c, z = r["cell"], r["located"]
        want = -r["W"] if mutate == "sign" else r["W"]
        g = z is not None and inside((z["A"], z["wf"]), c) and z["sign"] == want and z["absF"] <= 10 * z["floor"]
        ok &= g
        out(f"{name}: " + (f"A {z['A']:.7f}, w {z['wf']:.8f}, |R| {z['absF']:.3g} ({z['absF'] / z['floor']:.3g} sigma), "
                           f"sign {z['sign']:+d} (want {want:+d}), inside U {inside((z['A'], z['wf']), c)}"
                           if z else "not located") + f": {'PASS' if g else 'FAIL'}")
    r = res["C0"]
    c, z, p = r["cell"], r["located"], list(r["plant"])
    if mutate == "shift":
        p[0] += c[1] - c[0]
    want = -1 if mutate == "sign" else 1
    g = z is not None and abs(z["A"] - p[0]) <= 0.05 * (c[1] - c[0]) and abs(z["wf"] - p[1]) <= 0.05 * (c[3] - c[2]) \
        and z["sign"] == want
    ok &= g
    out("C0 (planted): " + (f"A {z['A']:.7f}, w {z['wf']:.8f} against P0 ({p[0]:.7f}, {p[1]:.7f}), sign {z['sign']:+d} "
                            f"(want {want:+d})" if z else "not located") + f": {'PASS' if g else 'FAIL'}")
    out(f"stage 1 check{' --mutate=' + mutate if mutate else ''}: {'PASS' if ok else 'FAIL'}")
    return ok


def boxes(res):
    out = []
    for name in ("U1", "U2"):
        z = res[name]["located"]
        out.append(dict(a0=z["A"] - 0.4 * DA, a1=z["A"] + 0.6 * DA, w0=z["wf"] - 0.4 * DW, w1=z["wf"] + 0.6 * DW, ok=False,
                        note=f"relocation box of {name}'s zero (#1013 loc018)"))
    out.append(dict(a0=C0[0], a1=C0[1], w0=C0[2], w1=C0[3], ok=False, note="control box C0, plant at P0 (#1013 loc018)"))
    return out


def check2(K, res, mutate=None, out=print):
    ok = True
    bx = {tuple(map(tuple, b["box"])): b for b in K["boxes"]}
    want_boxes = boxes(res)
    for name, B in zip(("U1", "U2", "C0"), want_boxes):
        key = ((B["a0"], B["a1"]), (B["w0"], B["w1"]))
        b = bx.get(key)
        cb = (B["a0"], B["a1"], B["w0"], B["w1"])
        zs = [z for z in K["zeros"] if cb[0] <= z["cell"][0] and z["cell"][1] <= cb[1] and cb[2] <= z["cell"][2]
              and z["cell"][3] <= cb[3]]
        W = 0 if name == "C0" else res[name]["W"]
        if mutate == "sign":
            W = -W if W else 1
        wb = b["boundary_winding"] if b else float("nan")
        res_ok = b is not None and wb == wb and abs(wb - round(wb)) < 0.1 and round(wb) == W and b["unresolved"] == 0
        if name == "C0":
            g = res_ok and not zs
            out(f"C0: winding {wb:.4g} (want {W}), unresolved {b['unresolved'] if b else None}, zeros {len(zs)}: "
                f"{'PASS' if g else 'FAIL'}")
        else:
            u = res[name]["cell"]
            inU = u[0] <= cb[0] and cb[1] <= u[1] and u[2] <= cb[2] and cb[3] <= u[3]
            p = [res[name]["located"]["A"], res[name]["located"]["wf"]]
            if mutate == "shift":
                p[0] += DA
            z = zs[0]["located"] if len(zs) == 1 else None
            near = z is not None and inside((z["A"], z["wf"]), cb) and abs(z["A"] - p[0]) <= 0.1 * DA \
                and abs(z["wf"] - p[1]) <= 0.1 * DW and zs[0]["W"] == W
            g = res_ok and inU and near
            out(f"{name} box A {cb[0]:.7f}-{cb[1]:.7f} w {cb[2]:.8f}-{cb[3]:.8f} (inside {name} {inU}): winding {wb:.4g} "
                f"(want {W:+d}), unresolved {b['unresolved'] if b else None}, zeros {len(zs)}"
                + (f", located A {z['A']:.7f} w {z['wf']:.8f} against stage 1's ({p[0]:.7f}, {p[1]:.8f})" if z else "")
                + f": {'PASS' if g else 'FAIL'}")
        ok &= g
    out(f"stage 2 check{' --mutate=' + mutate if mutate else ''}: {'PASS' if ok else 'FAIL'}")
    return ok


def synthetic():
    loc = lambda a, w, s: dict(A=a, wf=w, absF=10.0, floor=5.0, sign=s)
    res = {"U1": dict(cell=list(U["U1"][0]), W=1, located=loc(4.0635, 0.5190, 1)),
           "U2": dict(cell=list(U["U2"][0]), W=-1, located=loc(4.2686, 0.5440, -1)),
           "C0": dict(cell=list(C0), W=1, plant=list(P0), located=loc(P0[0] + 1e-5, P0[1] - 1e-5, 1))}
    bs = boxes(res)
    K = dict(boxes=[dict(box=[[b["a0"], b["a1"]], [b["w0"], b["w1"]]], boundary_winding=float(w), unresolved=0)
                    for b, w in zip(bs, (1, -1, 0))],
             zeros=[dict(cell=[b["a0"], b["a1"], b["w0"], b["w1"]], W=w,
                         located=loc(res[n]["located"]["A"] + 1e-6, res[n]["located"]["wf"], w))
                    for b, w, n in zip(bs[:2], (1, -1), ("U1", "U2"))])
    return res, K


if __name__ == "__main__":
    a = sys.argv[1:]
    mut = next((x.split("=", 1)[1] for x in a if x.startswith("--mutate=")), None)
    if a[0] == "--selftest":
        res, K = synthetic()
        r1 = [check(res, m, out=lambda s: None) for m in (None, "shift", "sign")]
        r2 = [check2(K, res, m, out=lambda s: None) for m in (None, "shift", "sign")]
        f = lambda r: " ".join("PASS" if x else "FAIL" for x in r)
        print(f"selftest check: {f(r1)}; check2: {f(r2)} (must be PASS FAIL FAIL, twice)")
        sys.exit(0 if r1 == r2 == [True, False, False] else 1)
    if a[0] == "run":
        procs = int(a[a.index("--procs") + 1]) if "--procs" in a else 4
        run(a[1], a[2], a[3], a[4], procs)
    elif a[0] == "check":
        sys.exit(0 if check(json.load(open(a[1])), mut) else 1)
    elif a[0] == "boxes":
        for b in boxes(json.load(open(a[1]))):
            print(json.dumps(b))
    elif a[0] == "check2":
        sys.exit(0 if check2(json.load(open(a[1])), json.load(open(a[2])), mut) else 1)
