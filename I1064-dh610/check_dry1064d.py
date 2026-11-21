#!/usr/bin/env python3
"""check_dry1064d.py MODE DIR CAP | --selftest [--break]: the pass test of run1064d.sh's two dry runs (OUT1064=DIR, CAP1064=CAP, the state of the real run).
MODE pass (R_1064D="294", CAP 240): ks293 exits 0 on its own, converged, below CAP by 30 s; ks294 starts after it, is TERMed by its exact pid at CAP (exit 143, gate failed);
the control's delta lines against the stored state and against the earlier control have exit 0 and xcheck 0; the control's log has the 'base re-seeded at ks 293' line and the summary copies it;
the table marks ks294 capped; the script ends with 'done'.
MODE ctlfail (R_1064D="294", CAP 45): ks293 is TERMed by its exact pid (exit 143, gate failed), 'control failed: rungs not started' is logged, ks294 is never started, and it ends with 'done'.
Exit 0 pass, 1 otherwise. --selftest runs planted folders through the same function: the pass cases must pass, each broken case must fail; --break expects a pass case to fail and so must exit 1."""
import os
import re
import sys
import tempfile


def check(mode, d, cap):
    ex = open(f"{d}/exits_1064d.txt").read()
    bad = []

    def get(pat, what):
        m = re.search(pat, ex)
        if not m:
            bad.append(f"missing: {what}")
        return m
    if mode == "pass":
        m1 = get(r"1064 ks293 exit 0 wall (\d+) s gate 0", "ks293 exit 0, gate 0")
        s1 = get(r"1064 ks294 started, pid \d+ ", "ks294 started")
        get(rf"1064 ks294 cap {cap} s: TERM to pid \d+", "TERM to ks294's pid at the cap")
        get(r"1064 ks294 exit 143 wall (\d+) s gate 1", "ks294 exit 143, gate 1")
        get(r"1064 delta1064_ctl_vs_state exit 0 xcheck 0", "the control's delta against the stored state and its xcheck")
        get(r"1064 delta1064_ctl_vs_earlier exit 0 xcheck 0", "the control's delta against the earlier control and its xcheck")
        l = open(f"{d}/ks293.log").read() if os.path.exists(f"{d}/ks293.log") else ""
        if not re.search(r"^base re-seeded at ks 293 \(--reseed_base 1\), [0-9.]+ s: octo-double max\|F\| \S+", l, re.M):
            bad.append("ks293.log has no 'base re-seeded at ks 293 (--reseed_base 1)' line with its max|F|")
        sm = open(f"{d}/summary_1064d.txt").read() if os.path.exists(f"{d}/summary_1064d.txt") else ""
        if not re.search(r"^ks293 re-seed: base re-seeded at ks 293", sm, re.M):
            bad.append("summary_1064d.txt does not copy the control's re-seed line")
        if m1 and not int(m1.group(1)) < cap - 30:
            bad.append(f"ks293 wall {m1.group(1)} s is not below the cap {cap} s by 30 s")
        if s1 and ex.find("ks293 exit") > ex.find("ks294 started"):
            bad.append("ks294 started before ks293 ended")
        g = open(f"{d}/gate_ks294.txt").read() if os.path.exists(f"{d}/gate_ks294.txt") else ""
        if not g.startswith("failed"):
            bad.append(f"gate_ks294.txt does not start with 'failed': {g[:60]!r}")
        t = open(f"{d}/table_1064d.md").read() if os.path.exists(f"{d}/table_1064d.md") else ""
        if not re.search(r"\| 294 \| 143 \(capped\) \|", t):
            bad.append("table_1064d.md has no '| 294 | 143 (capped) |' row")
    else:
        get(rf"1064 ks293 cap {cap} s: TERM to pid \d+", "TERM to ks293's pid at the cap")
        get(r"1064 ks293 exit 143 wall (\d+) s gate 1", "ks293 exit 143, gate 1")
        get(r"1064 control failed: rungs not started", "control failed line")
        if re.search(r"1064 ks294 started", ex):
            bad.append("ks294 was started after a failed control")
        g = open(f"{d}/gate_ks293.txt").read() if os.path.exists(f"{d}/gate_ks293.txt") else ""
        if not g.startswith("failed"):
            bad.append(f"gate_ks293.txt does not start with 'failed': {g[:60]!r}")
    get(r"1064 done ", "done")
    return bad


def planted(mode, d, drop=None, extra=None, gate="failed: no octo-double Newton line", w1=100, reseed=True):
    if mode == "pass":
        lines = ["1064 worktree x 2026-11-21 09:00:00 UTC",
                 f"1064 ks293 exit 0 wall {w1} s gate 0 2026-11-21 09:01:40 UTC",
                 "1064 ks294 started, pid 5 2026-11-21 09:01:40 UTC",
                 "1064 ks294 cap 240 s: TERM to pid 5 2026-11-21 09:05:40 UTC",
                 "1064 ks294 exit 143 wall 270 s gate 1 2026-11-21 09:06:10 UTC",
                 "1064 delta1064_ctl_vs_state exit 0 xcheck 0 2026-11-21 09:06:20 UTC",
                 "1064 delta1064_ctl_vs_earlier exit 0 xcheck 0 2026-11-21 09:06:20 UTC",
                 "1064 done 2026-11-21 09:06:21 UTC"]
        gf = "gate_ks294.txt"
        open(f"{d}/table_1064d.md", "w").write("| 294 | 143 (capped) | 270 | failed | - | - |\n")
        line = "base re-seeded at ks 293 (--reseed_base 1), 41.5 s: octo-double max|F| 3.2e-37, refinement rung max|R| 1e-20 -> 3e-37"
        open(f"{d}/ks293.log", "w").write((line if reseed else "base polish adopted") + "\n")
        open(f"{d}/summary_1064d.txt", "w").write(("ks293 re-seed: " + line if reseed else "ks293 re-seed: NO base re-seed line in the log") + "\n")
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
    open(f"{d}/exits_1064d.txt", "w").write("\n".join(lines) + "\n")
    open(f"{d}/{gf}", "w").write(gate + "\n")


def selftest(brk):
    cases = [("pass", "pass case", {}, True),
             ("pass", "ks293 too slow", {"w1": 230}, False),
             ("pass", "no TERM line", {"drop": "TERM"}, False),
             ("pass", "ks294 gate converged", {"gate": "converged: x"}, False),
             ("pass", "no control delta line", {"drop": "ctl_vs_state"}, False),
             ("pass", "no delta against the earlier control", {"drop": "ctl_vs_earlier"}, False),
             ("pass", "no re-seed line in the control's log", {"reseed": False}, False),
             ("ctlfail", "ctlfail case", {}, True),
             ("ctlfail", "ks294 started after a failed control", {"extra": "1064 ks294 started, pid 9 x"}, False),
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
