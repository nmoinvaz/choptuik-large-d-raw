#!/usr/bin/env python3
"""relabel_B.py: roots87.txt labeled by t5's reading B (hc 25 Nov ~18:50 UTC, ruling, quoted): "lambda_1 runs 0.4425 (22.25), 0.216 (22.75), 0.167 (22.8125), 0.128 (22.875), 0.056 (22.9375), -0.0215 (23.0), slopes -0.45, -0.78, -0.62,
-1.15, -1.24, smooth. The newcomer runs >0.50 (22.8125), 0.162 (22.875), -0.226 (22.9375), slopes < -5.4 and -6.2, a steady fast dive like S. ... Unfreeze and label by B: F lines = lambda_1 as listed; #N lines for the newcomer
(0.162 at 22.875, -0.226 at 22.9375)."
F lines (label F, read by the chain) are lambda_1; #N comment lines (the chain ignores them) are the newcomer. The numbers come from the merged readings, not from typing: 22.75_both (one change: lambda_1), 22.875_F (two changes: the lower
is lambda_1, the upper the newcomer), 22.9375_low (two changes: the negative root is the newcomer, the other is lambda_1 and must equal the line already there), 22.8125_F2 (one change: lambda_1).
usage: relabel_B.py [--roots=PATH] [--dry]     prints the file it writes (or would write)
       relabel_B.py selftest [--mutate=swap|check]
"""
import os, re, sys, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import label_roots

L = label_roots.L
MUT = next((a.split("=", 1)[1] for a in sys.argv if a.startswith("--mutate=")), None)


def fline(D, c, label="F"):
    return "%r %.6f %.6f %.6f macm3 bracket %.3f %.3f %s" % (D, c[3], c[4], c[5], c[0], c[1], label)


def nline(D, c):
    return "#N %r %.6f %.6f %.6f macm3 bracket %.3f %.3f (N: the newcomer, a fast dive from above 0.50 like S; the F line of this D is lambda_1)" % (D, c[3], c[4], c[5], c[0], c[1])


def transform(lines, e):
    """e: dict with c75 (lambda_1 at 22.75), c8125 (lambda_1 at 22.8125), c875 = (lambda_1, newcomer) at 22.875, c9375 = (newcomer, lambda_1) at 22.9375. -> new lines"""
    out, did = [], set()
    for ln in lines:
        w = ln.split()
        D = float(w[1]) if ln.startswith("#L ") or ln.startswith("#N ") else (float(w[0]) if w and not ln.startswith("#") else None)
        if ln.startswith("#L ") and abs(D - 22.875) < 1e-9:
            out.append(nline(22.875, e["c875"][1])); did.add("n875"); continue
        if D is None or ln.startswith("#"):
            out.append(ln); continue
        if abs(D - 22.8125) < 1e-9:
            if MUT != "check" and abs(float(w[1]) - e["c8125"][3]) > 1e-6:
                raise SystemExit("STOP the line of D 22.8125 (%s) is not lambda_1 %.6f" % (w[1], e["c8125"][3]))
            out.append(fline(22.75, e["c75"])); did.add("f75")
            out.append(fline(22.8125, e["c8125"])); did.add("f8125"); continue
        if abs(D - 22.875) < 1e-9:
            out.append(fline(22.875, e["c875"][0])); did.add("f875"); continue
        if abs(D - 22.9375) < 1e-9:
            if MUT != "check" and abs(float(w[1]) - e["c9375"][1][3]) > 1e-6:
                raise SystemExit("STOP the line of D 22.9375 (%s) is not lambda_1 %.6f" % (w[1], e["c9375"][1][3]))
            out.append(fline(22.9375, e["c9375"][1])); out.append(nline(22.9375, e["c9375"][0])); did.add("f9375"); continue
        if abs(D - 23.0) < 1e-9:
            out.append(ln if ln.endswith(" F") else ln + " F"); did.add("f23"); continue
        out.append(ln)
    if did != {"n875", "f75", "f8125", "f875", "f9375", "f23"}:
        raise SystemExit("STOP not every line was found: done %s" % sorted(did))
    return out


def readings():
    def chg(path, n_want):
        n, ch = label_roots.changes(open(L + "/" + path).read())
        assert n == n_want and len(ch) == n_want, "%s: %d changes (%d wanted)" % (path, n, n_want)
        return ch
    c75 = chg("22.75_both/read_lower_merged.txt", 1)[0]
    c8125 = chg("22.8125_F2/read_lower_merged.txt", 1)[0]
    a = chg("22.875_F/read_lower_merged.txt", 2)
    b = chg("22.9375_low/read_lower_merged.txt", 2)
    assert c75[2] == "- to +" and c8125[2] == "- to +" and a[0][2] == "- to +" and a[1][2] == "+ to -" and b[0][2] == "- to +" and b[1][2] == "+ to -"
    return dict(c75=c75, c8125=c8125, c875=(a[0], a[1]), c9375=(b[0], b[1]))


def selftest():
    ok = True
    def chk(name, cond):
        nonlocal ok
        print("planted:", name, "PASS" if cond else "FAIL"); ok = ok and cond
    lo = (0.120, 0.130, "- to +", 0.127834, 0.123345, 0.127834); up = (0.160, 0.170, "+ to -", 0.162334, 0.161448, 0.162334)
    e = dict(c75=(0.210, 0.220, "- to +", 0.216086, 0.212991, 0.216086), c8125=(0.160, 0.170, "- to +", 0.166991, 0.163666, 0.166991), c875=(lo, up),
             c9375=((-0.26, -0.22, "- to +", -0.226429, -0.259451, -0.226429), (0.040, 0.060, "+ to -", 0.056199, 0.043573, 0.056199)))
    lines = ["# header", "22.25 0.442516 0.441911 0.442516 macm3 bracket 0.440 0.445", "23.0 -0.021546 -0.035344 -0.021546 macm3 bracket -0.040 -0.020",
             "22.9375 0.056199 0.043573 0.056199 macm3 bracket 0.040 0.060", "22.875 0.162334 0.161448 0.162334 macm3 bracket 0.160 0.170 F",
             "#L 22.875 0.127834 0.123345 0.127834 macm3 bracket 0.120 0.130 (L: ...)", "22.8125 0.166991 0.163666 0.166991 macm3 bracket 0.160 0.170"]
    out = transform(lines, e)
    f = {float(l.split()[0]): float(l.split()[1]) for l in out if l.split() and not l.startswith("#")}
    n = {float(l.split()[1]): float(l.split()[2]) for l in out if l.startswith("#N ")}
    chk("F lines are lambda_1: 22.25 0.442516, 22.75 0.216086, 22.8125 0.166991, 22.875 0.127834, 22.9375 0.056199, 23.0 -0.021546", f == {22.25: 0.442516, 22.75: 0.216086, 22.8125: 0.166991, 22.875: 0.127834, 22.9375: 0.056199, 23.0: -0.021546})
    chk("#N lines are the newcomer: 22.875 0.162334, 22.9375 -0.226429; no #L line is left", n == {22.875: 0.162334, 22.9375: -0.226429} and not any(l.startswith("#L ") for l in out))
    chk("every F line carries the label F and the header is kept", all(l.endswith(" F") for l in out if l.split() and not l.startswith("#") and float(l.split()[0]) > 22.3) and out[0] == "# header")
    import importlib.util
    with tempfile.TemporaryDirectory() as t:
        open(t + "/r.txt", "w").write("\n".join(out) + "\n")
        spec = importlib.util.spec_from_file_location("chain_next", L + "/chain_next.py"); cn = importlib.util.module_from_spec(spec); spec.loader.exec_module(cn)
        rr = cn.read_roots(t + "/r.txt")
        chk("the chain reads exactly the six lambda_1 roots and ignores the #N lines", rr == {22.25: 0.442516, 22.75: 0.216086, 22.8125: 0.166991, 22.875: 0.127834, 22.9375: 0.056199, 23.0: -0.021546})
    bad = list(lines); bad[3] = "22.9375 0.060000 0.04 0.06 macm3 bracket 0.040 0.060"
    try:
        transform(bad, e); chk("a D 22.9375 line that is not lambda_1: STOP", False)
    except SystemExit:
        chk("a D 22.9375 line that is not lambda_1: STOP", True)
    print("selftest:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "selftest":
        if MUT == "swap":      # the two roots of D 22.875 swapped: the checks on the F and #N lines must fail
            _t = transform
            def transform(lines, e, _t=_t):
                e = dict(e); e["c875"] = (e["c875"][1], e["c875"][0]); return _t(lines, e)
        sys.exit(selftest())
    path = next((a.split("=", 1)[1] for a in sys.argv if a.startswith("--roots=")), L + "/roots87.txt")
    e = readings()
    out = transform(open(path).read().splitlines(), e)
    if "--dry" in sys.argv:
        print("\n".join(out)); sys.exit(0)
    open(path + ".tmp", "w").write("\n".join(out) + "\n"); os.replace(path + ".tmp", path)
    print("\n".join(l for l in out if l.split() and (l.startswith("#N ") or (not l.startswith("#") and float(l.split()[0]) > 22.3))))
