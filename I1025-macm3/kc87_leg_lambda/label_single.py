#!/usr/bin/env python3
"""label_single.py: a single root of a scan labeled lambda_1 by continuity (t5, hc 25 Nov ~18:50 and ~19:00 UTC: "label later roots by continuity; I'll rule pairs").
usage: label_single.py D READING [--roots=PATH]   writes 'D root lo hi macm3 bracket a b F' into roots87.txt when the reading has exactly one robust change, noise-robust, repeat PASS, and the root lies within 0.06 of the line through
       the two lambda_1 roots (F lines) nearest D (below and above, else the two nearest below); otherwise STOP and nothing is written. A D that already has a line is not touched.
       label_single.py selftest [--mutate=far]"""
import os, re, sys, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import label_roots, chain_next

L = label_roots.L
MUT = next((a.split("=", 1)[1] for a in sys.argv if a.startswith("--mutate=")), None)
TOL = 0.06


def line_pred(roots, D):
    below = sorted(x for x in roots if x < D); above = sorted(x for x in roots if x > D)
    if below and above:
        a, c = below[-1], above[0]
    elif len(below) >= 2:
        a, c = below[-2], below[-1]
    else:
        return None
    return roots[a] + (roots[c] - roots[a]) * (D - a) / (c - a)


def decide(text, roots, D):
    n, ch = label_roots.changes(text)
    if n != 1 or len(ch) != 1:
        return None, "robust changes: %d (one wanted)" % n
    if not re.search(r"not noise-robust: none", text) or "PASS" not in text:
        return None, "a point is not noise-robust or the repeat check did not pass"
    pred = line_pred(roots, D)
    if pred is None:
        return None, "no line of lambda_1 roots to compare with"
    c = ch[0]
    if MUT != "far" and abs(c[3] - pred) > TOL:
        return None, "the root %.6f is %.4f from the lambda_1 line (%.4f): not labeled by continuity" % (c[3], c[3] - pred, pred)
    return (c, pred), ""


def write(path, D, c):
    lines = open(path).read().splitlines()
    for ln in lines:
        w = ln.split()
        if w and not ln.startswith("#") and abs(float(w[0]) - D) < 1e-9:
            return "STOP D %r already has a line" % D
    lines.append(label_roots.line_f(D, c))
    open(path + ".tmp", "w").write("\n".join(lines) + "\n"); os.replace(path + ".tmp", path)
    return "OK " + label_roots.line_f(D, c)


def selftest():
    ok = True
    def chk(name, cond):
        nonlocal ok
        print("planted:", name, "PASS" if cond else "FAIL"); ok = ok and cond
    roots = {22.25: 0.442516, 22.75: 0.216086}
    body = "not noise-robust: none\nrobust changes: 1; touching\n  robust change (0.300, 0.340), + to -, det-linear %.6f, range [0.30, 0.34]\nrepeat ... agree -> PASS\n"
    r, why = decide(body % 0.339638, roots, 22.5)
    chk("D 22.5: 0.339638 against the line 0.3293: labeled", r is not None and abs(r[1] - 0.329301) < 1e-6)
    r, why = decide(body % 0.45, roots, 22.5)
    chk("a root 0.12 above the line: STOP, not labeled by continuity", r is None and "continuity" in why)
    chk("two changes: STOP", decide(body.replace("changes: 1", "changes: 2"), roots, 22.5)[0] is None)
    chk("no line to compare with (one root only): STOP", decide(body % 0.34, {22.25: 0.44}, 22.5)[0] is None)
    with tempfile.TemporaryDirectory() as t:
        open(t + "/r.txt", "w").write("22.25 0.442516 0.44 0.44 macm3 bracket 0.440 0.445 F\n")
        c = label_roots.changes(body % 0.339638 + "")[1][0]
        chk("the F line is appended and the chain reads it", write(t + "/r.txt", 22.5, c).startswith("OK") and chain_next.read_roots(t + "/r.txt").get(22.5) == 0.339638)
        chk("a D that already has a line is not touched", write(t + "/r.txt", 22.5, c).startswith("STOP"))
    print("selftest:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    if sys.argv[1] == "selftest":
        sys.exit(selftest())
    D = float(sys.argv[1]); text = open(sys.argv[2]).read()
    path = next((a.split("=", 1)[1] for a in sys.argv if a.startswith("--roots=")), L + "/roots87.txt")
    r, why = decide(text, chain_next.read_roots(path), D)
    if r is None:
        print("STOP D %r: %s" % (D, why)); sys.exit(1)
    msg = write(path, D, r[0]); print(msg + "  (lambda_1 line predicts %.4f, root %+.4f from it)" % (r[1], r[0][3] - r[1])); sys.exit(0 if msg.startswith("OK") else 1)
