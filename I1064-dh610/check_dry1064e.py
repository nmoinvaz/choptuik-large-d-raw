#!/usr/bin/env python3
"""check_dry1064e.py MODE DIR CAP | --selftest [--break]: the pass test of run1064e.sh's two dry runs (OUT1064=DIR, CAP1064=CAP, the state of the real run).
MODE pass (CAP 300): ks293 exits 0 on its own, converged, below CAP by 30 s; ks315own and ks315nat start after it, each is TERMed by its exact pid at CAP (exit 143, gate failed);
the control's delta lines against the stored state and against the re-seeded control have exit 0 and xcheck 0; the three command lines carry --elim_switch 1e-9 and no --reseed_base, ks293 and ks315own
carry --od_accept own, ks315nat --od_accept natural and not own; the summary has the control's 'first two on-lines'; the table has the two rung rows, marked capped; the script ends with 'done'.
MODE ctlfail (CAP 45): ks293 is TERMed by its exact pid (exit 143, gate failed), 'control failed: rungs not started' is logged, neither rung is started, and it ends with 'done'.
Exit 0 pass, 1 otherwise. --selftest runs planted folders through the same function: the pass cases must pass, each broken case must fail; --break expects a pass case to fail and so must exit 1."""
import os
import re
import sys
import tempfile

CMD = "# 2026-11-21 09:00:00 UTC cmd: python3 -u anm_run.py R O --state S --od_accept {acc} --elim_switch 1e-9 --steps 0 --ks {k} --keep_plan 0\n"


def rd(p):
    return open(p).read() if os.path.exists(p) else ""


def check(mode, d, cap):
    ex = rd(f"{d}/exits_1064e.txt")
    bad = []

    def get(pat, what):
        m = re.search(pat, ex)
        if not m:
            bad.append(f"missing: {what}")
        return m
    if mode == "pass":
        m1 = get(r"1064 ks293 exit 0 wall (\d+) s gate 0", "ks293 exit 0, gate 0")
        for L in ("ks315own", "ks315nat"):
            s = get(rf"1064 {L} started, pid \d+ ", f"{L} started")
            get(rf"1064 {L} cap {cap} s: TERM to pid \d+", f"TERM to {L}'s pid at the cap")
            get(rf"1064 {L} exit 143 wall (\d+) s gate 1", f"{L} exit 143, gate 1")
            if s and ex.find("ks293 exit") > ex.find(f"{L} started"):
                bad.append(f"{L} started before ks293 ended")
            if not rd(f"{d}/gate_{L}.txt").startswith("failed"):
                bad.append(f"gate_{L}.txt does not start with 'failed'")
        get(r"1064 delta1064_ctl_vs_state exit 0 xcheck 0", "the control's delta against the stored state and its xcheck")
        get(r"1064 delta1064_ctl_vs_reseeded exit 0 xcheck 0", "the control's delta against the re-seeded control and its xcheck")
        if m1 and not int(m1.group(1)) < cap - 30:
            bad.append(f"ks293 wall {m1.group(1)} s is not below the cap {cap} s by 30 s")
        for L, acc in (("ks293", "own"), ("ks315own", "own"), ("ks315nat", "natural")):
            c = (re.search(r"cmd: (.*)", rd(f"{d}/{L}.log")) or [None, ""])[1]
            if "--elim_switch 1e-9" not in c:
                bad.append(f"{L}.log's command has no --elim_switch 1e-9")
            if "--reseed_base" in c:
                bad.append(f"{L}.log's command has --reseed_base")
            if f"--od_accept {acc}" not in c or (acc == "natural" and "--od_accept own" in c):
                bad.append(f"{L}.log's command is not --od_accept {acc}")
        if not re.search(r"^ks293 first two on-lines: on ", rd(f"{d}/summary_1064e.txt"), re.M):
            bad.append("summary_1064e.txt has no 'ks293 first two on-lines: on ...' line")
        t = rd(f"{d}/table_1064e.md")
        for L, acc in (("ks315own", "own"), ("ks315nat", "natural")):
            if not re.search(rf"\| {L} \| {acc} \| 1e-9 \| 143 \(capped\) \|", t):
                bad.append(f"table_1064e.md has no '| {L} | {acc} | 1e-9 | 143 (capped) |' row")
    else:
        get(rf"1064 ks293 cap {cap} s: TERM to pid \d+", "TERM to ks293's pid at the cap")
        get(r"1064 ks293 exit 143 wall (\d+) s gate 1", "ks293 exit 143, gate 1")
        get(r"1064 control failed: rungs not started", "control failed line")
        for L in ("ks315own", "ks315nat"):
            if re.search(rf"1064 {L} started", ex):
                bad.append(f"{L} was started after a failed control")
        if not rd(f"{d}/gate_ks293.txt").startswith("failed"):
            bad.append("gate_ks293.txt does not start with 'failed'")
    get(r"1064 done ", "done")
    return bad


def planted(mode, d, drop=None, extra=None, gate="failed: no octo-double Newton line", w1=100, nat_cmd="natural", own_switch=True, rb=False, f2=True):
    if mode == "pass":
        lines = ["1064 worktree x 2026-11-21 09:00:00 UTC",
                 f"1064 ks293 exit 0 wall {w1} s gate 0 2026-11-21 09:01:40 UTC",
                 "1064 ks315own started, pid 5 2026-11-21 09:01:40 UTC", "1064 ks315nat started, pid 6 2026-11-21 09:01:40 UTC",
                 "1064 ks315own cap 300 s: TERM to pid 5 2026-11-21 09:06:40 UTC", "1064 ks315nat cap 300 s: TERM to pid 6 2026-11-21 09:06:40 UTC",
                 "1064 ks315own exit 143 wall 330 s gate 1 2026-11-21 09:07:10 UTC", "1064 ks315nat exit 143 wall 330 s gate 1 2026-11-21 09:07:10 UTC",
                 "1064 delta1064_ctl_vs_state exit 0 xcheck 0 2026-11-21 09:07:20 UTC", "1064 delta1064_ctl_vs_reseeded exit 0 xcheck 0 2026-11-21 09:07:30 UTC",
                 "1064 done 2026-11-21 09:07:31 UTC"]
        open(f"{d}/ks293.log", "w").write(CMD.format(acc="own", k=293))
        c = CMD.format(acc="own", k=315)
        open(f"{d}/ks315own.log", "w").write(c if own_switch else c.replace(" --elim_switch 1e-9", ""))
        n = CMD.format(acc=nat_cmd, k=315)
        open(f"{d}/ks315nat.log", "w").write(n.replace("--steps", "--reseed_base 1 --steps") if rb else n)
        open(f"{d}/summary_1064e.txt", "w").write("ks293 first two on-lines: on 0 chord 0: max|F| 3.7e-27|on 0: strong chord x|\n" if f2 else "ks293: exit 0\n")
        for L in ("ks315own", "ks315nat"):
            open(f"{d}/gate_{L}.txt", "w").write(gate + "\n")
        open(f"{d}/table_1064e.md", "w").write("| ks315own | own | 1e-9 | 143 (capped) | 330 |\n| ks315nat | natural | 1e-9 | 143 (capped) | 330 |\n")
    else:
        lines = ["1064 worktree x 2026-11-21 09:00:00 UTC",
                 "1064 ks293 cap 45 s: TERM to pid 5 2026-11-21 09:00:45 UTC",
                 "1064 ks293 exit 143 wall 60 s gate 1 2026-11-21 09:01:15 UTC",
                 "1064 control failed: rungs not started 2026-11-21 09:01:15 UTC",
                 "1064 done 2026-11-21 09:01:16 UTC"]
        open(f"{d}/gate_ks293.txt", "w").write(gate + "\n")
    if drop is not None:
        lines = [x for x in lines if drop not in x]
    if extra:
        lines.append(extra)
    open(f"{d}/exits_1064e.txt", "w").write("\n".join(lines) + "\n")


def selftest(brk):
    cases = [("pass", "pass case", {}, True),
             ("pass", "ks293 too slow", {"w1": 280}, False),
             ("pass", "no TERM line for ks315nat", {"drop": "ks315nat cap"}, False),
             ("pass", "ks315own gate converged", {"gate": "converged: x"}, False),
             ("pass", "no control delta against the stored state", {"drop": "ctl_vs_state"}, False),
             ("pass", "ks315nat's command is own", {"nat_cmd": "own"}, False),
             ("pass", "ks315own's command lacks the switch", {"own_switch": False}, False),
             ("pass", "ks315nat's command has --reseed_base", {"rb": True}, False),
             ("pass", "summary lacks the first two on-lines", {"f2": False}, False),
             ("ctlfail", "ctlfail case", {}, True),
             ("ctlfail", "ks315own started after a failed control", {"extra": "1064 ks315own started, pid 9 x"}, False),
             ("ctlfail", "no control failed line", {"drop": "control failed"}, False),
             ("ctlfail", "ks293 gate converged", {"gate": "converged: x"}, False)]
    if brk:
        cases[0] = cases[0][:3] + (False,)
    n = 0
    for mode, name, kw, want in cases:
        with tempfile.TemporaryDirectory() as d:
            planted(mode, d, **kw)
            bad = check(mode, d, 300 if mode == "pass" else 45)
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
