#!/usr/bin/env python3
"""I229-win2: does sigma_16 of the K 33 J 1000 node at omega/omega_inf 1.10 follow the process count? (issue #229)

    python -I compare_229.py [NEW.json [WIN2_P3.json [MACM3_P2.json]]]
        defaults: ./sigF_w1.10_K33_J1000_procs2.json (win2, --procs 2), ../I202-win2/sigF_w1.10_K33_J1000.json (win2, --procs 3)
        and ../T153-macm3/sigF_w1.10_K33_J1000.json (macm3, --procs 2). Timing keys and `procs` are dropped before comparing
        (../I140-win2/compare.py's rule). Prints the first differing entry (and sigma string) against each file and the verdict.
        Exit 0: equal to one of the two bit for bit. Exit 1: differs from both.
    python -I compare_229.py --selftest
        a copy of each existing file gives its own verdict, and a file with one planted digit in one sigma string is
        'differs from both' with the digit's index (exit 1 inside if any of the three fails)."""
import copy, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "I202-win2"))
import compare_202 as K  # load(): canonical object without timing keys and procs; report(): first differing entry


def verdict(new, p3, m2, out=print):
    out("== against win2 --procs 3 (I202-win2)")
    eq3 = K.report(new, p3, out=lambda t: out(t.replace("win2 ", "new  ").replace("macm3", "#202 "))) == 0
    out("== against macm3 --procs 2 (T153-macm3)")
    eqm = K.report(new, m2, out=lambda t: out(t.replace("win2 ", "new  "))) == 0
    if eq3 and not eqm:
        v = "equal to the #202 file (--procs 3) and not to macm3's: the process count does not change the result on win2, so the win2/macm3 difference is not the process count"
    elif eqm and not eq3:
        v = "equal to macm3's file (--procs 2) and not to the #202 file (--procs 3): the difference follows the process count"
    elif eq3 and eqm:
        v = "equal to both (the #202 and macm3 files are equal): nothing to explain"
    else:
        v = "differs from both files: the difference does not follow the process count alone"
    out("verdict: " + v)
    return 0 if (eq3 or eqm) else 1, v


def selftest():
    p3 = K.load(os.path.join(os.path.dirname(HERE), "I202-win2", "sigF_w1.10_K33_J1000.json"))
    m2 = K.load(os.path.join(os.path.dirname(HERE), "T153-macm3", "sigF_w1.10_K33_J1000.json"))
    q = lambda s: None
    r1, v1 = verdict(copy.deepcopy(p3), p3, m2, out=q)
    r2, v2 = verdict(copy.deepcopy(m2), p3, m2, out=q)
    e = copy.deepcopy(p3)
    s = e["sigma_str"][9]
    e["sigma_str"][9] = [s[0], s[1][:-3] + ("0" if s[1][-3] != "0" else "1") + s[1][-2:]]
    log = []
    r3, v3 = verdict(e, p3, m2, out=log.append)
    ok = (r1, r2, r3) == (0, 0, 1) and "process count does not change" in v1 and "follows the process count" in v2 \
        and v3.startswith("differs from both") and any("sigma_9" in x for x in log)
    print("selftest:", "ok" if ok else "FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    if sys.argv[1:2] == ["--selftest"]:
        sys.exit(selftest())
    a = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "sigF_w1.10_K33_J1000_procs2.json")
    b = sys.argv[2] if len(sys.argv) > 2 else os.path.join(os.path.dirname(HERE), "I202-win2", "sigF_w1.10_K33_J1000.json")
    c = sys.argv[3] if len(sys.argv) > 3 else os.path.join(os.path.dirname(HERE), "T153-macm3", "sigF_w1.10_K33_J1000.json")
    sys.exit(verdict(K.load(a), K.load(b), K.load(c))[0])
