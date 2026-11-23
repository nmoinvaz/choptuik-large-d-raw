"""#1079 macm3b: a read-only breakdown of certify_M.py's Krawczyk test on a saved box run (my own script; it imports certify_M.py's functions, changes nothing, writes nothing).
    python diagnose.py data/A_M_box_M3x1_1e-10.json [data/A_M_point_M3x1.json]
(with a point run, g(p^) and Y come from it, as in krawczyk --point; Dg over the box from the box run)
For each component i of K(X) = -Y g(0) + (I - Y Dgt(X)) X: the box half-width w_i, |mid| and radius of (Y g)_i, and for each column j the term |mid|(I - YJ)_ij w_j and the radius rad(I - YJ)_ij w_j,
the same arithmetic as certify_M.krawczyk_test (lines 345-417), so that the sum of the pieces is |K_i|'s upper bound."""
import sys, os, json
sys.path.insert(0, "/Users/nathan/Source/choptuik-large-d-1079/solver/proof")
import numpy as np
from flint import arb, arb_mat, ctx
import certify_M as C
import certify_M_sys as CS
import certify_M_lohner as CL
bx = json.load(open(sys.argv[1]))
M = bx["M"]; m = M + 1
ctx.prec = C.KPREC
s = CS.SysM(M)
ell = C.jump_rows(s, None)
Cm = [[arb(x) for x in r] for r in bx["C"]]
cb, Qb, qb, varb = CL.load_lohner(bx["sets"])
pt = json.load(open(sys.argv[2])) if len(sys.argv) > 2 else None
if pt is not None:
    assert pt["p"] == bx["p"] and pt["M"] == bx["M"]
    c0, Q0, q0, var0 = CL.load_lohner(pt["sets"])
    Tm = arb_mat(C.T_matrix(Cm, M))
    Dgt0 = arb_mat(C.apply_var(ell, var0)) * Tm
else:
    c0, Q0, q0 = cb, Qb, qb
    Dgt0 = arb_mat(C.apply_var(ell, varb))
g = C.apply_set(ell, c0, Q0, q0)
Dmid = arb_mat([[arb(Dgt0[i, j].mid()) for j in range(m)] for i in range(m)])
Y = arb_mat([[arb(x.mid()) for x in row] for row in Dmid.inv().tolist()])
Yl = Y * ell
Yg = C.apply_set(Yl, c0, Q0, q0)
YJ = C.apply_var(Yl, varb)
h = arb(bx["h"])
widths = [h, h] + [arb(bx["w"][(i // 2) % len(bx["w"])]) for i in range(M - 1)]
names = ["A", "w/w_inf", "B3", "C3"]
print("box h %s w %s" % (bx["h"], bx["w"]))
print("g(p^) components: " + ", ".join("%s: |mid| %.2e rad %.2e" % (names[i], abs(float(g[i].mid())), float(g[i].rad())) for i in range(m)))
print("Y rows' max |entry|: " + ", ".join("%.2e" % max(abs(float(Y[i, j].mid())) for j in range(m)) for i in range(m)))
print("midpoint of Dgt(X) (the matrix Y inverts):")
for i in range(m): print("   " + "  ".join("%11.3e" % float(Dmid[i, j].mid()) for j in range(m)))
tot = []
for i in range(m):
    w_i = float(widths[i].mid())
    yg_mid = abs(float(Yg[i].mid())); yg_rad = float(Yg[i].rad())
    terms = []
    for j in range(m):
        Mij = (arb(1) if i == j else arb(0)) - YJ[i][j]
        wj = float(widths[j].mid())
        terms.append((abs(float(Mij.mid())) * wj, float(Mij.rad()) * wj))
    K = -Yg[i]
    for j in range(m):
        Mij = (arb(1) if i == j else arb(0)) - YJ[i][j]
        K = K + Mij * arb(0, widths[j])
    ub = float(abs(K).upper())
    print("row %-8s w_i %.2e: |K| <= %.3e = %.1f w_i;  (Y g): |mid| %.2e (%.1f w_i) rad %.2e (%.1f w_i)" % (names[i], w_i, ub, ub / w_i, yg_mid, yg_mid / w_i, yg_rad, yg_rad / w_i))
    print("    (I - Y Dgt(X)) X terms per column [|mid| w_j ; rad w_j] in units of w_i: " + "  ".join("%s [%.1f ; %.1f]" % (names[j], terms[j][0] / w_i, terms[j][1] / w_i) for j in range(m)))
