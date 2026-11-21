#!/usr/bin/env python3
"""check_dry1064c.py MODE DIR CAP | --selftest [--break]: the pass test of run1064c.sh's two dry runs (OUT1064=DIR, CAP1064=CAP, the state of the real run).
MODE pass (R_1064C="297", CAP 240): ks293 exits 0 on its own, converged, below CAP by 30 s; ks297 starts after it, is TERMed by its exact pid at CAP (exit 143, gate failed);
the control's delta line against the stored state has exit 0 and xcheck 0; the table marks ks297 capped; the script ends with 'done'.
MODE ctlfail (R_1064C="297", CAP 45): ks293 is TERMed by its exact pid (exit 143, gate failed), 'control failed: rungs not started' is logged, ks297 is never started, and it ends with 'done'.
Exit 0 pass, 1 otherwise. --selftest runs planted folders through the same function: the pass cases must pass, each broken case must fail; --break expects a pass case to fail and so must exit 1."""
import os
import re
import sys
import tempfile


def check(mode, d, cap):
    ex = open(f"{d}/exits_1064c.txt").read()
    bad = []

    def get(pat, what):
        m = re.search(pat, ex)
        if not m:
            bad.append(f"missing: {what}")
        return m
    if mode == "pass":
        m1 = get(r"1064 ks293 exit 0 wall (\d+) s gate 0", "ks293 exit 0, gate 0")
        s1 = get(r"1064 ks297 started, pid \d+ ", "ks297 started")
        get(rf"1064 ks297 cap {cap} s: TERM to pid \d+", "TERM to ks297's pid at the cap")
        get(r"1064 ks297 exit 143 wall (\d+) s gate 1", "ks297 exit 143, gate 1")
        get(r"1064 delta1064_ctl_vs_state exit 0 xcheck 0", "the control's delta against the stored state and its xcheck")
        if m1 and not int(m1.group(1)) < cap - 30:
            bad.append(f"ks293 wall {m1.group(1)} s is not below the cap {cap} s by 30 s")
        if s1 and ex.find("ks293 exit") > ex.find("ks297 started"):
            bad.append("ks297 started before ks293 ended")
        g = open(f"{d}/gate_ks297.txt").read() if os.path.exists(f"{d}/gate_ks297.txt") else ""
        if not g.startswith("failed"):
            bad.append(f"gate_ks297.txt does not start with 'failed': {g[:60]!r}")
        t = open(f"{d}/table_1064c.md").read() if os.path.exists(f"{d}/table_1064c.md") else ""
        if not re.search(r"\| 297 \| 143 \(capped\) \|", t):
            bad.append("table_1064c.md has no '| 297 | 143 (capped) |' row")
    else:
        get(rf"1064 ks293 cap {cap} s: TERM to pid \d+", "TERM to ks293's pid at the cap")
        get(r"1064 ks293 exit 143 wall (\d+) s gate 1", "ks293 exit 143, gate 1")
        get(r"1064 control failed: rungs not started", "control failed line")
        if re.search(r"1064 ks297 started", ex):
            bad.append("ks297 was started after a failed control")
        g = open(f"{d}/gate_ks293.txt").read() if os.path.exists(f"{d}/gate_ks293.txt") else ""
        if not g.startswith("failed"):
            bad.append(f"gate_ks293.txt does not start with 'failed': {g[:60]!r}")
    get(r"1064 done ", "done")
    return bad


def planted(mode, d, drop=None, extra=None, gate="failed: no octo-double Newton line", w1=100):
    if mode == "pass":
        lines = ["1064 worktree x 2026-11-21 09:00:00 UTC",
                 f"1064 ks293 exit 0 wall {w1} s gate 0 2026-11-21 09:01:40 UTC",
                 "1064 ks297 started, pid 5 2026-11-21 09:01:40 UTC",
                 "1064 ks297 cap 240 s: TERM to pid 5 2026-11-21 09:05:40 UTC",
                 "1064 ks297 exit 143 wall 270 s gate 1 2026-11-21 09:06:10 UTC",
                 "1064 delta1064_ctl_vs_state exit 0 xcheck 0 2026-11-21 09:06:20 UTC",
                 "1064 done 2026-11-21 09:06:21 UTC"]
        gf = "gate_ks297.txt"
        open(f"{d}/table_1064c.md", "w").write("| 297 | 143 (capped) | 270 | failed | - | - |\n")
    else:
        lines = ["1064 worktree x 2026-11-21 09:00:00 UTC",
                 "1064 ks293 cap 45 s: TERM to pid 5 2026-11-21 09:00:45 UTC",
                 "1064 ks293 exit 143 wall 60 s gate 1 2026-11-21 09:01:15 UTC",
                 "1064 control failed: rungs not started 2026-11-21 09:01:15 UTC",
                 "1064 done 2026-11-21 09:01:16 UTC"]
        gf = "gate_ks293.txt"
    if drop is not None:
        lines = [x for x in lines if drop not in x]
    if extra:
        lines.append(extra)
    open(f"{d}/exits_1064c.txt", "w").write("\n".join(lines) + "\n")
    open(f"{d}/{gf}", "w").write(gate + "\n")


def selftest(brk):
    cases = [("pass", "pass case", {}, True),
             ("pass", "ks293 too slow", {"w1": 230}, False),
             ("pass", "no TERM line", {"drop": "TERM"}, False),
             ("pass", "ks297 gate converged", {"gate": "converged: x"}, False),
             ("pass", "no control delta line", {"drop": "ctl_vs_state"}, False),
             ("ctlfail", "ctlfail case", {}, True),
             ("ctlfail", "ks297 started after a failed control", {"extra": "1064 ks297 started, pid 9 x"}, False),
             ("ctlfail", "no control failed line", {"drop": "control failed"}, False),
             ("ctlfail", "ks293 gate converged", {"gate": "converged: x"}, False)]
    if brk:
        cases[0] = cases[0][:3] + (False,)
    n = 0
    for mode, name, kw, want in cases:
        with tempfile.TemporaryDirectory() as d:
            planted(mode, d, **kw)
            bad = check(mode, d, 240 if mode == "pass" else 45)
        ok = (not bad) == want
        print(f"  {mode}: {name}: {'pass' if not bad else 'fail'} (expected {'pass' if want else 'fail'}): {'ok' if ok else 'WRONG'}")
        n += not ok
    print("selftest", "FAIL" if n else "PASS")
    return 1 if n else 0


if __name__ == "__main__":
    if sys.argv[1] == "--selftest":
        sys.exit(selftest("--break" in sys.argv))
    bad = check(sys.argv[1], sys.argv[2], int(sys.argv[3]))
    for b in bad:
        print("FAIL:", b)
    print("dry test", sys.argv[1], "FAILED" if bad else "PASSED")
    sys.exit(1 if bad else 0)
