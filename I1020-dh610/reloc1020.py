#!/usr/bin/env python3
"""reloc1020.py [--dir m3] [--in inputs1013] [--tol 1e-4] [--selftest] [--mutate=shift|sign|norb]: #1020 step 1. Each small box (count_reloc_<name>.json, argcount.py at xi1 0.3, second radius 0.17)
must contain a zero of the expected sign located at both radii within tol (absolute, in A and in wf) of its xi1 0.25 place: the partners' places are the located zeros of #1013's xi1 0.25 count
(inputs1013/count_M3_cand_r0.25.json, sign -1 'minus', +1 'plus'), the control's is the known zero of #1013's step 2 (inputs1013/count_M3_cand.json). Prints per box the count's unresolved cells and
winding, each zero's places and the shifts; exit 0 when every box passes (the control included), 1 otherwise. A box that fails is a failed partner (or a failed control, which makes the partners'
verdicts uninterpretable). Controls (--selftest, exit 1 on a failed control): a synthetic pass passes; a shift of 2e-4, a flipped sign and a missing second radius each fail. --mutate=shift|sign|norb applies
the same on the real data (it must fail)."""
import json
import os
import sys

TOL = 1e-4


def expect(indir):
    c25 = json.load(open(os.path.join(indir, "count_M3_cand_r0.25.json")))
    c2 = json.load(open(os.path.join(indir, "count_M3_cand.json")))
    ex = {}
    for z in c25["zeros"]:
        ex["minus" if z["W"] < 0 else "plus"] = (z["W"], z["located"]["A"], z["located"]["wf"])
    z = c2["zeros"][0]
    ex["control"] = (z["W"], z["located"]["A"], z["located"]["wf"])
    return ex


def judge(exp, count, tol, mut=""):
    """-> (pass, lines) for one box: its zeros of the expected sign, located at r1 and at r1b"""
    s, a0, w0 = exp
    if mut == "shift":
        a0 += 2 * tol
    if mut == "sign":
        s = -s
    lines, ok = [], False
    un = count["unresolved"]
    lines.append(f"   xi1 {count['r1']} (second {count['r1b']}), box A {count['box'][0]}, wf {count['box'][1]}: boundary winding {count['boundary_winding']:.3f}, leaf sum {count['leaf_sum']}, "
                 f"{count['nleaves']} leaves, {count['npoints']} points, {len(un)} unresolved cells, {len(count['zeros'])} zero(s)")
    for z in count["zeros"]:
        loc, locb = z.get("located"), z.get("located_r1b")
        if mut == "norb":
            locb = None
        if not loc:
            lines.append(f"   zero of sign {z['W']:+d} in cell A {z['cell'][0]:.4f}-{z['cell'][1]:.4f}: not located at xi1 {count['r1']}")
            continue
        d1 = (loc["A"] - a0, loc["wf"] - w0)
        d2 = (locb["A"] - a0, locb["wf"] - w0) if locb else None
        same = z["W"] == s and loc["sign"] == s and (locb is None or locb["sign"] == s)
        good = same and abs(d1[0]) <= tol and abs(d1[1]) <= tol and d2 is not None and abs(d2[0]) <= tol and abs(d2[1]) <= tol
        lines.append(f"   zero of sign {z['W']:+d}: xi1 {count['r1']} at ({loc['A']:.6f}, {loc['wf']:.6f}) shift ({d1[0]:+.2e}, {d1[1]:+.2e}) |R| {loc['absF']:.1e}; xi1 {count['r1b']} "
                     + (f"at ({locb['A']:.6f}, {locb['wf']:.6f}) shift ({d2[0]:+.2e}, {d2[1]:+.2e}) |R| {locb['absF']:.1e}" if locb else "not located")
                     + f" -> {'PASS' if good else 'no'}")
        ok = ok or good
    if not count["zeros"]:
        lines.append("   no zero found")
    return ok, lines


def selftest(tol):
    c = dict(r1=0.3, r1b=0.17, box=[[0, 1], [0, 1]], boundary_winding=1.0, leaf_sum=1, nleaves=1, npoints=1, unresolved=[],
             zeros=[dict(W=1, cell=[0, 1, 0, 1], located=dict(A=2.00001, wf=0.5, absF=1e-8, sign=1), located_r1b=dict(A=2.00002, wf=0.50003, absF=1e-8, sign=1))])
    e = (1, 2.0, 0.5)
    r = {m: judge(e, c, tol, m)[0] for m in ("", "shift", "sign", "norb")}
    ok = r[""] and not r["shift"] and not r["sign"] and not r["norb"]
    print(f"selftest: synthetic pass passes {r['']}, a shift of {2 * tol:.0e} fails {not r['shift']}, a flipped sign fails {not r['sign']}, a missing second radius fails {not r['norb']}: {'PASS' if ok else 'FAIL'}")
    return ok


def main(argv):
    tol = float(argv[argv.index("--tol") + 1]) if "--tol" in argv else TOL
    if "--selftest" in argv:
        return 0 if selftest(tol) else 1
    d = argv[argv.index("--dir") + 1] if "--dir" in argv else os.path.join(os.path.dirname(os.path.abspath(__file__)), "m3")
    indir = argv[argv.index("--in") + 1] if "--in" in argv else os.path.join(os.path.dirname(os.path.abspath(__file__)), "inputs1013")
    mut = next((a.split("=")[1] for a in argv if a.startswith("--mutate=")), "")
    ex = expect(indir)
    allok = True
    for name in ("control", "minus", "plus"):
        s, a, w = ex[name]
        print(f"{name}: expected sign {s:+d} at ({a:.6f}, {w:.6f}) (tolerance {tol:g} in A and in wf, at both radii)")
        p = os.path.join(d, f"count_reloc_{name}.json")
        if not os.path.exists(p):
            print("   no count file")
            allok = False
            continue
        ok, lines = judge(ex[name], json.load(open(p)), tol, mut)
        print("\n".join(lines))
        print(f"   {name}: {'PASS' if ok else 'FAIL'}")
        allok = allok and ok
    return 0 if allok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
