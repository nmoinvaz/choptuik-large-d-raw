#!/usr/bin/env python3
"""check_dry1064h.py MODE DIR CAP | --selftest [--break]: the pass test of run1064h.sh's two dry runs (OUT1064=DIR, CAP1064=CAP, the state and flags of the real run).
MODE pass (CAP 300): the worktree line names the ks 307 control base with its pinned blob and 'gate passed'; ks395 and ks443 start together, each is TERMed by its exact pid at CAP (exit 143, gate failed);
no ks307 run exists (the control is not rerun); the two command lines carry --od_accept own, --od_floor_delta 0, --tol_od 1e-60, their own --ks and neither --elim_switch nor --reseed_base; the table has the two rung
rows, marked capped, and the p_min rows of K 307, 331 and 347; the script ends with 'done'.
MODE nocontrol (CTL1064H names a missing file): 'the ks 307 control base is missing ... stop' is logged and neither rung is started.
Exit 0 pass, 1 otherwise. --selftest runs planted folders through the same function: the pass cases must pass, each broken case must fail; --break expects a pass case to fail and so must exit 1."""
import os
import re
import sys
import tempfile

CMD = "# 2026-11-21 09:00:00 UTC cmd: python3 -u anm_run.py R O --state S --od_accept own --tol_od 1e-60 --od_floor_delta 0 --steps 0 --ks {k} --keep_plan 0\n"


def rd(p):
    return open(p).read() if os.path.exists(p) else ""


def check(mode, d, cap):
    ex = rd(f"{d}/exits_1064h.txt")
    bad = []

    def get(pat, what):
        m = re.search(pat, ex)
        if not m:
            bad.append(f"missing: {what}")
        return m
    if mode == "pass":
        get(r"1064 worktree .* ks 307 control base \S+ \(blob [0-9a-f]{40}, gate passed\)", "the worktree line with the control base, its blob and 'gate passed'")
        for L in ("ks395", "ks443"):
            get(rf"1064 {L} started, pid \d+ ", f"{L} started")
            get(rf"1064 {L} cap {cap} s: TERM to pid \d+", f"TERM to {L}'s pid at the cap")
            get(rf"1064 {L} exit 143 wall (\d+) s gate 1", f"{L} exit 143, gate 1")
            if not rd(f"{d}/gate_{L}.txt").startswith("failed"):
                bad.append(f"gate_{L}.txt does not start with 'failed'")
        if os.path.exists(f"{d}/ks307.log") or re.search(r"1064 ks307 started", ex):
            bad.append("a ks307 run exists: the control must not be rerun")
        for L, k in (("ks395", 395), ("ks443", 443)):
            c = (re.search(r"cmd: (.*)", rd(f"{d}/{L}.log")) or [None, ""])[1]
            for need in ("--od_accept own", "--od_floor_delta 0 ", "--tol_od 1e-60 ", f"--ks {k} "):
                if need not in c + " ":
                    bad.append(f"{L}.log's command has no {need.strip()}")
            for fl in ("--elim_switch", "--reseed_base"):
                if fl in c:
                    bad.append(f"{L}.log's command has {fl}")
        t = rd(f"{d}/table_1064h.md")
        for L, k in (("ks395", 395), ("ks443", 443)):
            if not re.search(rf"\| {L} \| {k} \| 143 \(capped\) \|", t):
                bad.append(f"table_1064h.md has no '| {L} | {k} | 143 (capped) |' row")
        for k in (307, 331, 347):
            if not re.search(rf"\| {k} \| ho2_D237\.7132 \(i1064o\) \| 3 \| 3\.2e-15 \|", t):
                bad.append(f"table_1064h.md has no p_min row of K {k}")
        get(r"1064 done ", "done")
    else:
        get(r"1064 the ks 307 control base is missing \(\S+\): stop", "the missing control base line")
        for L in ("ks395", "ks443"):
            if re.search(rf"1064 {L} started", ex) or os.path.exists(f"{d}/{L}.log"):
                bad.append(f"{L} was started without the control base")
    return bad


def planted(mode, d, drop=None, extra=None, bad_cmd=None, bad_ks=False, ks307=False, prow=True):
    if mode == "pass":
        lines = ["1064 worktree x at y, venv-i1058, load 1 2 3, state S, ks 307 control base /x/base.npz (blob 861c79ff8ffc4b10067c487287ff46286b4ed4ba, gate passed) 2026-11-21 09:00:00 UTC",
                 "1064 ks395 started, pid 5 2026-11-21 09:00:01 UTC", "1064 ks443 started, pid 6 2026-11-21 09:00:01 UTC",
                 "1064 ks395 cap 300 s: TERM to pid 5 2026-11-21 09:05:01 UTC", "1064 ks443 cap 300 s: TERM to pid 6 2026-11-21 09:05:01 UTC",
                 "1064 ks395 exit 143 wall 330 s gate 1 2026-11-21 09:05:31 UTC", "1064 ks443 exit 143 wall 330 s gate 1 2026-11-21 09:05:31 UTC",
                 "1064 done 2026-11-21 09:05:40 UTC"]
        for L, k in (("ks395", 395), ("ks443", 443)):
            c = CMD.format(k=k + 1 if (bad_ks and L == "ks443") else k)
            if bad_cmd and L == "ks395":
                c = c.replace("--steps", bad_cmd + " --steps")
            open(f"{d}/{L}.log", "w").write(c)
            open(f"{d}/gate_{L}.txt", "w").write("failed: no octo-double Newton line\n")
        if ks307:
            open(f"{d}/ks307.log", "w").write(CMD.format(k=307))
        t = "| ks395 | 395 | 143 (capped) | 330 |\n| ks443 | 443 | 143 (capped) | 330 |\n"
        if prow:
            t += "".join(f"| {k} | ho2_D237.7132 (i1064o) | 3 | 3.2e-15 | 6.3e+42 |\n" for k in (307, 331, 347))
        open(f"{d}/table_1064h.md", "w").write(t)
    else:
        lines = ["1064 worktree x at y 2026-11-21 09:00:00 UTC", "1064 the ks 307 control base is missing (/nonexistent/base.npz): stop 2026-11-21 09:00:01 UTC"]
    if drop is not None:
        lines = [x for x in lines if drop not in x]
    if extra:
        lines.append(extra)
    open(f"{d}/exits_1064h.txt", "w").write("\n".join(lines) + "\n")


def selftest(brk):
    cases = [("pass", "pass case", {}, True),
             ("pass", "no TERM line for ks443", {"drop": "ks443 cap"}, False),
             ("pass", "ks395 exit not 143", {"drop": "ks395 exit 143"}, False),
             ("pass", "a ks307 run exists", {"ks307": True}, False),
             ("pass", "ks395's command has --elim_switch", {"bad_cmd": "--elim_switch 1e-9"}, False),
             ("pass", "ks395's command has --reseed_base", {"bad_cmd": "--reseed_base 1"}, False),
             ("pass", "ks443's command has the wrong --ks", {"bad_ks": True}, False),
             ("pass", "table lacks the p_min rows", {"prow": False}, False),
             ("pass", "no worktree line with the control base", {"drop": "worktree"}, False),
             ("nocontrol", "nocontrol case", {}, True),
             ("nocontrol", "ks395 started without the control base", {"extra": "1064 ks395 started, pid 9 x"}, False),
             ("nocontrol", "no missing-control line", {"drop": "missing"}, False)]
    if brk:
        cases[0] = cases[0][:3] + (False,)
    n = 0
    for mode, name, kw, want in cases:
        with tempfile.TemporaryDirectory() as d:
            planted(mode, d, **kw)
            bad = check(mode, d, 300)
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
