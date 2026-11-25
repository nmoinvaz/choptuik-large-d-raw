#!/usr/bin/env python3
"""label_roots.py: the two roots of a pair in roots87.txt, one line per root with a branch label (t5, hc 25 Nov, after 15:48 UTC, quoted): "keep one line per root with a branch label: F (the upper, flat
branch = lambda_1) and L (the lower root of D 22.8125-22.875); the chain's lambda_1 line at D 22.8125 and 22.875 becomes F's once (a) and (b) are read, with L's root kept beside it, annotated."
A merged reading with exactly two robust changes, '- to +' (the lower root L) then '+ to -' (the upper root F, the flat branch lambda_1), gives
  the F line   "D root lo hi macm3 bracket a b F"                       (the chain reads it: first two fields)
  the L line   "#L D root lo hi macm3 bracket a b (L: ...)"             (a comment: the chain does not read it)
Any other count of changes or order: STOP (nothing written). An existing line for D (the chain's, which was L's) is replaced by the pair; it must equal L's det-linear root.
usage: label_roots.py D READING [--roots=PATH]      prints the two lines it wrote, or STOP why
       label_roots.py selftest [--mutate=swap|replace|freeze]
"""
import os, re, sys, tempfile

L = os.path.expanduser("~/Source/choptuik-large-d-raw-903/I1025-macm3/kc87_leg_lambda")
MUT = next((a.split("=", 1)[1] for a in sys.argv if a.startswith("--mutate=")), None)
CH = re.compile(r"robust change \((-?[\d.]+), (-?[\d.]+)\), ([-+]) to ([-+]), det-linear (-?[\d.]+), range \[(-?[\d.]+), (-?[\d.]+)\]")


def frozen(base=None):
    """t5, hc 25 Nov ~16:50 UTC: \"Leave every label as is until D 22.75's both-roots scan reads\": while LABELS_FROZEN.txt exists nothing is written; returns its first line or None"""
    f = (base or L) + "/LABELS_FROZEN.txt"
    if MUT == "freeze" or not os.path.exists(f):
        return None
    return open(f).readline().strip() or "LABELS_FROZEN.txt exists"


def changes(text):
    m = re.search(r"robust changes: (\d+);", text)
    return int(m.group(1)) if m else -1, [(float(a), float(b), o + " to " + n, float(d), float(lo), float(hi)) for a, b, o, n, d, lo, hi in CH.findall(text)]


def pair(text):
    """-> (L, F) as (bracket_a, bracket_b, orientation, root, lo, hi) or None with a reason"""
    n, ch = changes(text)
    if n != 2 or len(ch) != 2:
        return None, "robust changes: %d (two wanted)" % n
    lo_, up_ = ch
    if MUT == "swap":
        lo_, up_ = up_, lo_
    if lo_[2] != "- to +" or up_[2] != "+ to -":
        return None, "the two changes read %s then %s ('- to +' then '+ to -' wanted)" % (lo_[2], up_[2])
    if not lo_[3] < up_[3]:
        return None, "the lower root %.6f is not below the upper %.6f" % (lo_[3], up_[3])
    if not re.search(r"not noise-robust: none", text) or "PASS" not in text:
        return None, "a point is not noise-robust or the repeat check did not pass"
    return (lo_, up_), ""


def line_f(D, f):
    return "%r %.6f %.6f %.6f macm3 bracket %.3f %.3f F" % (D, f[3], f[4], f[5], f[0], f[1])


def line_l(D, l):
    return "#L %r %.6f %.6f %.6f macm3 bracket %.3f %.3f (L: the lower root of the pair at this D; the F line above is lambda_1)" % (D, l[3], l[4], l[5], l[0], l[1])


def rewrite(path, D, lf):
    """replace the line(s) of D by the F line and the L comment, atomically; an existing line of D must be L's root"""
    l, f = lf
    old = open(path).read().splitlines() if os.path.exists(path) else []
    out, replaced = [], False
    for ln in old:
        w = ln.split()
        if w and not ln.startswith("#") and abs(float(w[0]) - D) < 1e-9:
            if MUT != "replace" and abs(float(w[1]) - l[3]) > 1e-6:
                return "STOP the existing line of D %r (%s) is not the lower root %.6f" % (D, w[1], l[3])
            out += [line_f(D, f), line_l(D, l)]; replaced = True
        else:
            out.append(ln)
    if not replaced:
        out += [line_f(D, f), line_l(D, l)]
    tmp = path + ".tmp"
    open(tmp, "w").write("\n".join(out) + "\n")
    os.replace(tmp, path)
    return "OK %s | %s" % (line_f(D, f), line_l(D, l))


def selftest():
    ok = True
    def chk(name, cond):
        nonlocal ok
        print("planted:", name, "PASS" if cond else "FAIL"); ok = ok and cond
    body = ("points 20 in 0.110-0.400; not noise-robust: none\nrobust changes: 2; touching a non-robust point (not counted): none\n  robust change (0.160, 0.170), - to +, det-linear 0.166991, range [0.163666, 0.166991]\n"
            "  robust change (0.300, 0.320), + to -, det-linear 0.311000, range [0.305000, 0.311000]\nln|det| local minima without a sign change: none\nrepeat check x: lambda [0.2]: [2] evaluations each, agree -> PASS\n")
    r, why = pair(body)
    chk("two changes '- to +' then '+ to -': L 0.166991, F 0.311000", r is not None and r[0][3] == 0.166991 and r[1][3] == 0.311)
    chk("one change: STOP", pair(body.replace("robust changes: 2", "robust changes: 1").replace("  robust change (0.300, 0.320), + to -, det-linear 0.311000, range [0.305000, 0.311000]\n", ""))[0] is None)
    chk("three changes: STOP", pair(body.replace("robust changes: 2", "robust changes: 3"))[0] is None)
    chk("changes in the other order: STOP", pair(body.replace("- to +", "x to y").replace("+ to -", "- to +").replace("x to y", "+ to -"))[0] is None)
    chk("a failed repeat check: STOP", pair(body.replace("PASS", "FAIL"))[0] is None)
    with tempfile.TemporaryDirectory() as t:
        p = t + "/roots87.txt"
        open(p, "w").write("# header\n22.25 0.442516 0.441911 0.442516 macm3 bracket 0.440 0.445\n22.8125 0.166991 0.163666 0.166991 macm3 bracket 0.160 0.170\n22.9375 0.056199 0.043573 0.056199 macm3 bracket 0.040 0.060\n")
        r, _ = pair(body)
        msg = rewrite(p, 22.8125, r)
        txt = open(p).read().splitlines()
        chk("the chain's line of D 22.8125 (L's root) becomes the F line plus the L comment, the others stay", msg.startswith("OK") and txt[2].startswith("22.8125 0.311000 ") and txt[2].endswith(" F") and txt[3].startswith("#L 22.8125 0.166991 ") and len(txt) == 5 and txt[1].startswith("22.25 ") and txt[4].startswith("22.9375 "))
        import importlib.util
        spec = importlib.util.spec_from_file_location("chain_next", L + "/chain_next.py"); cn = importlib.util.module_from_spec(spec); sys.argv_backup = sys.argv; spec.loader.exec_module(cn)
        rr = cn.read_roots(p)
        chk("the chain reads the F root for D 22.8125 and ignores the L comment", rr.get(22.8125) == 0.311 and len(rr) == 3)
        open(p, "w").write("22.8125 0.150000 0.1 0.15 macm3 bracket 0.1 0.2\n")
        chk("an existing line that is not L's root: STOP, file unchanged", rewrite(p, 22.8125, r).startswith("STOP") and open(p).read().startswith("22.8125 0.150000"))
        open(p, "w").write("22.25 0.442516 0.44 0.44 macm3 bracket 0.440 0.445\n")
        rewrite(p, 22.75, r)
        chk("no line yet for D 22.75: F line and L comment are appended", open(p).read().splitlines()[1].startswith("22.75 0.311000 ") and open(p).read().splitlines()[2].startswith("#L 22.75 "))
    with tempfile.TemporaryDirectory() as t2:
        chk("frozen: no LABELS_FROZEN.txt: not frozen", frozen(t2) is None)
        open(t2 + "/LABELS_FROZEN.txt", "w").write("leave every label as is until D 22.75 reads\n")
        chk("frozen: LABELS_FROZEN.txt present: frozen, the reason is its first line", frozen(t2) == "leave every label as is until D 22.75 reads")
    print("selftest:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    if sys.argv[1] == "selftest":
        sys.exit(selftest())
    D = float(sys.argv[1]); text = open(sys.argv[2]).read()
    fr = frozen()
    if fr:
        print("STOP D %r: labels are frozen (%s); nothing written" % (D, fr)); sys.exit(1)
    path = next((a.split("=", 1)[1] for a in sys.argv if a.startswith("--roots=")), L + "/roots87.txt")
    lf, why = pair(text)
    if lf is None:
        print("STOP D %r: %s" % (D, why)); sys.exit(1)
    msg = rewrite(path, D, lf)
    print(msg); sys.exit(0 if msg.startswith("OK") else 1)
