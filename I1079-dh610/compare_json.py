#!/usr/bin/env python3
"""#1079 dh610 compare_json.py [--mutate] | selftest: the box and point JSONs of this machine (worktree solver/proof/data) against macm3's (in/macm3/), per zero, and the pieces of certify_M.krawczyk_test
(c40fbc77's own functions, the body of krawczyk_test with its intermediate values exposed): steps, seconds, the charts bx['C'], the Jacobian columns' radii (max over rows per column, for the point run's
columns, which give Y, and for the box run's columns, which give YJ), the g radius (per component), |Yg| (midpoint and radius per row), the (I - YJ)X term per row (its radius), K per row and the relative margins.
Control: the margins recomputed here must equal krawczyk_test's own printed ones to 1e-12 (else exit 2). selftest: the control on macm3's own files for both zeros must pass, and a planted
change of one margin must be caught; --mutate doubles the widths in the (I - YJ)X term of the recomputation, which the control must then catch (exit 2).
usage (from this folder): ~/Source/venv-i1058/bin/python -I compare_json.py > compare_json.txt"""
import json, sys, os, io, contextlib, re
sys.path.insert(0, "/home/nathan/Source/choptuik-large-d-1079a/solver/proof")
os.chdir("/home/nathan/Source/choptuik-large-d-1079a/solver/proof")
import certify_M as CM
F = "/home/nathan/Source/choptuik-large-d-raw/I1079-dh610"
W = "/home/nathan/Source/choptuik-large-d-1079a/solver/proof"
ZERO = {1: ("x1E2", "M3x1E2_h1e-12_w1e-13"), 2: ("x2E2", "M3x2E2_h1e-12_w1e-12")}
MUT = "--mutate" in sys.argv


def pieces(bx, pt):
    CM.ctx.prec = CM.KPREC
    M = bx["M"]; m = M + 1
    s = CM.CS.SysM(M); ell = CM.jump_rows(s, None)
    Cm = [[CM.arb(x) for x in r] for r in bx["C"]]
    T = CM.T_matrix(Cm, M); Tm = CM.arb_mat(T)
    cb, Qb, qb, varb = CM.CL.load_lohner(bx["sets"])
    c, Q, q, var = CM.CL.load_lohner(pt["sets"])
    Dgt0 = CM.arb_mat(CM.apply_var(ell, var)) * Tm
    g = CM.apply_set(ell, c, Q, q)
    Dmid = CM.arb_mat([[CM.arb(Dgt0[i, j].mid()) for j in range(m)] for i in range(m)])
    Yb = Dmid.inv()
    Y = CM.arb_mat([[CM.arb(Yb[i, j].mid()) for j in range(m)] for i in range(m)])
    Yl = Y * ell
    Yg = CM.apply_set(Yl, c, Q, q)
    YJ = CM.apply_var(Yl, varb)
    Jbox = CM.apply_var(ell, varb)
    h = CM.arb(bx["h"])
    widths = [h, h] + [CM.arb(bx["w"][(i // 2) % len(bx["w"])]) for i in range(M - 1)]
    K, term = [], []
    for i in range(m):
        t0 = -Yg[i]
        t = t0
        tm = CM.arb(0)
        for j in range(m):
            Mij = (CM.arb(1) if i == j else CM.arb(0)) - YJ[i][j]
            u = Mij * CM.arb(0, widths[j] * (2 if MUT else 1))
            t = t + u
            tm = tm + u
        K.append(t); term.append(tm)
    rel = [float((widths[i] - abs(K[i]).upper()).lower()) / float(widths[i].mid()) for i in range(m)]
    colrad = lambda A: [max(float(A[i][j].rad()) for i in range(m)) for j in range(m)]
    P = {"rel_margins": rel,
         "point Dgt0 column radii (max over rows)": colrad([[Dgt0[i, j] for j in range(m)] for i in range(m)]),
         "box Jbox column radii (max over rows)": colrad(Jbox),
         "g radius per component": [float(x.rad()) for x in g], "g_rad (max)": max(float(x.rad()) for x in g),
         "|Yg| midpoint per row": [float(abs(x.mid())) for x in Yg], "Yg radius per row": [float(x.rad()) for x in Yg],
         "(I-YJ)X term radius per row": [float(x.rad()) for x in term], "YJ max radius": max(float(YJ[i][j].rad()) for i in range(m) for j in range(m)),
         "|K| upper per row": [float(abs(x).upper()) for x in K]}
    with contextlib.redirect_stdout(io.StringIO()) as buf:
        r = CM.krawczyk_test(bx, pt, verbose=True)
    P["krawczyk_test rel_margins"] = [float(x) for x in r["rel_margins"]]
    return P


def load(N, mine):
    T, B = ZERO[N]
    if mine:
        return json.load(open(f"{W}/data/A_M_box_{B}.json")), json.load(open(f"{W}/data/A_M_point_M3{T}.json"))
    return json.load(open(f"{F}/in/macm3/A_M_box_{B}.json")), json.load(open(f"{F}/in/macm3/A_M_point_M3{T}.json"))


def fmt(v):
    return "[" + ", ".join(f"{x:.4g}" for x in v) + "]" if isinstance(v, list) else f"{v:.6g}"


def main():
    bad = 0
    for N in (1, 2):
        T, B = ZERO[N]
        print(f"## zero {N} ({B}): this machine (c40fbc77, python-flint 0.9.0) against macm3's JSONs (in/macm3/)\n")
        (bm, pm), (bo, po) = load(N, True), load(N, False)
        print("| item | this machine | macm3 |\n|---|---|---|")
        for k in ("kind", "M", "h", "w", "steps", "prec"):
            print(f"| box {k} | {bm[k]} | {bo[k]} |")
        print(f"| box sec | {bm['sec']:.0f} | {bo['sec']:.0f} |")
        print(f"| point steps, sec | {pm['steps']}, {pm['sec']:.0f} | {po['steps']}, {po['sec']:.0f} |")
        print(f"| box p equals point p; box p equals macm3's p | {bm['p'] == pm['p']}; {bm['p'] == bo['p']} | {bo['p'] == po['p']} |")
        mid = lambda s: float(re.search(r'[+-]?\d+\.?\d*(?:[eE][+-]?\d+)?', str(s)).group(0))
        dC = max(abs(mid(x) - mid(y)) for r1, r2 in zip(bm["C"], bo["C"]) for x, y in zip(r1, r2))
        print(f"| chart bx['C'] strings identical; max abs entry difference | {bm['C'] == bo['C']}; {dC:.3e} | |")
        print(f"| box path, start identical to macm3's | {bm['path'] == bo['path']}, {bm['start'] == bo['start']} | |")
        print(f"| point g_rad, Dg_rad | {pm['g_rad']:.4g}, {pm['Dg_rad']:.4g} | {po['g_rad']:.4g}, {po['Dg_rad']:.4g} |")
        a, b = pieces(bm, pm), pieces(bo, po)
        for k in a:
            print(f"| {k} | {fmt(a[k])} | {fmt(b[k])} |")
        ctl = max(abs(x - y) for x, y in zip(a["rel_margins"], a["krawczyk_test rel_margins"])) + max(abs(x - y) for x, y in zip(b["rel_margins"], b["krawczyk_test rel_margins"]))
        print(f"\ncontrol: the margins recomputed here against krawczyk_test's own: max difference {ctl:.2e} (bar 1e-12): {'ok' if ctl <= 1e-12 else 'CONTROL FAILED'}\n")
        bad |= ctl > 1e-12
    return 2 if bad else 0


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "selftest":
        MUT = "--mutate" in sys.argv
        P = pieces(*load(1, False))
        ctl = max(abs(x - y) for x, y in zip(P["rel_margins"], P["krawczyk_test rel_margins"]))
        caught = ctl > 1e-12
        print(f"  macm3's x1 files: recomputed margins against krawczyk_test's: max difference {ctl:.2e} (bar 1e-12)")
        print("selftest" + (" --mutate" if MUT else ""), "FAIL" if caught else "PASS")
        sys.exit(1 if caught else 0)
    sys.exit(main())
