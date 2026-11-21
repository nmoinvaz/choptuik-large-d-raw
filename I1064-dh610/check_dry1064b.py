#!/usr/bin/env python3
"""check_dry1064b.py DIR CAP | --selftest [--break]: the pass test of run1064b.sh's dry run (R1_1064B="293 315", R2_1064B="", OUT1064=DIR, CAP1064=CAP). Pass when
ks293 exits 0 on its own, converged, well before CAP; ks315 is TERMed by its exact pid at CAP (exit 143, gate failed); the two walls differ (the own-wall measure; run1064.sh gave
both the rung's); Delta(293, dry) - Delta(293, control) has exit 0 and xcheck 0; the table marks ks315 capped; the script ends with 'done'. Exit 0 pass, 1 otherwise.
--selftest runs planted folders through the same function: the pass case must pass, each broken case must fail; --break expects the pass case to fail and so must exit 1."""
import os
import re
import sys
import tempfile


def check(d, cap):
    ex = open(f"{d}/exits_1064b.txt").read()
    bad = []

    def get(pat, what):
        m = re.search(pat, ex)
        if not m:
            bad.append(f"missing: {what}")
        return m
    m1 = get(r"1064 ks293 exit 0 wall (\d+) s gate 0", "ks293 exit 0, gate 0")
    c = get(rf"1064 ks315 cap {cap} s: TERM to pid \d+", "TERM to ks315's pid at the cap")
    m2 = get(r"1064 ks315 exit 143 wall (\d+) s gate 1", "ks315 exit 143, gate 1")
    get(r"1064 delta1064_K293 exit 0 xcheck 0", "the delta and its xcheck of ks293")
    get(r"1064 done ", "done")
    if m1 and m2:
        w1, w2 = int(m1.group(1)), int(m2.group(1))
        if not w1 < cap - 30:
            bad.append(f"ks293 wall {w1} s is not below the cap {cap} s by 30 s")
        if not w2 >= cap:
            bad.append(f"ks315 wall {w2} s is below the cap {cap} s")
        if not w2 - w1 >= 60:
            bad.append(f"the walls {w1} and {w2} s do not differ by 60 s (own-wall measure)")
    g = open(f"{d}/gate_ks315.txt").read() if os.path.exists(f"{d}/gate_ks315.txt") else ""
    if not g.startswith("failed"):
        bad.append(f"gate_ks315.txt does not start with 'failed': {g[:60]!r}")
    t = open(f"{d}/table_1064b.md").read() if os.path.exists(f"{d}/table_1064b.md") else ""
    if not re.search(r"\| 315 \| 143 \(capped\) \|", t):
        bad.append("table_1064b.md has no '| 315 | 143 (capped) |' row")
    return bad


def planted(d, w1=95, w2=272, drop=None, gate315="failed: no octo-double Newton line"):
    lines = ["1064 worktree x 2026-11-21 06:00:00 UTC",
             f"1064 ks293 exit 0 wall {w1} s gate 0 2026-11-21 06:01:35 UTC",
             "1064 ks315 cap 240 s: TERM to pid 123 2026-11-21 06:04:00 UTC",
             f"1064 ks315 exit 143 wall {w2} s gate 1 2026-11-21 06:04:30 UTC",
             "1064 delta1064_K293 exit 0 xcheck 0 2026-11-21 06:05:00 UTC",
             "1064 done 2026-11-21 06:05:01 UTC"]
    if drop is not None:
        lines = [x for x in lines if drop not in x]
    open(f"{d}/exits_1064b.txt", "w").write("\n".join(lines) + "\n")
    open(f"{d}/gate_ks315.txt", "w").write(gate315 + "\n")
    open(f"{d}/table_1064b.md", "w").write("| 315 | 143 (capped) | 272 | failed | - | - |\n")


def selftest(brk):
    cases = [("pass case", {}, True),
             ("equal walls (the rung's wall for both)", {"w1": 272, "w2": 272}, False),
             ("no TERM line", {"drop": "TERM"}, False),
             ("ks293 too slow", {"w1": 230}, False),
             ("ks315 gate converged", {"gate315": "converged: x"}, False),
             ("no delta line", {"drop": "delta1064_K293"}, False)]
    if brk:
        cases[0] = (cases[0][0], cases[0][1], False)
    n = 0
    for name, kw, want in cases:
        with tempfile.TemporaryDirectory() as d:
            planted(d, **kw)
            bad = check(d, 240)
        ok = (not bad) == want
        print(f"  {name}: {'pass' if not bad else 'fail'} (expected {'pass' if want else 'fail'}): {'ok' if ok else 'WRONG'}")
        n += not ok
    print("selftest", "FAIL" if n else "PASS")
    return 1 if n else 0


if __name__ == "__main__":
    if sys.argv[1] == "--selftest":
        sys.exit(selftest("--break" in sys.argv))
    bad = check(sys.argv[1], int(sys.argv[2]))
    for b in bad:
        print("FAIL:", b)
    print("dry test", "FAILED" if bad else "PASSED")
    sys.exit(1 if bad else 0)
