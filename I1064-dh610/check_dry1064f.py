#!/usr/bin/env python3
"""check_dry1064f.py MODE DIR CAP [TOL] | --selftest [--break]: the pass test of run1064f.sh's two dry runs (OUT1064=DIR, CAP1064=CAP, the state of the real run).
MODE pass (CAP 600): ks307 exits 0 on its own, converged, below CAP by 30 s; ks331 and ks347 start after it, each is TERMed by its exact pid at CAP (exit 143, gate failed);
the control's delta line against the stored state has exit 0 and xcheck 0; the three command lines carry --od_accept own, --tol_od TOL (TOL 2e-34 for the dry run, whose env TOL1064F and GMAX1064F set it; the real run's default is 1e-60), their own --ks, and neither --elim_switch nor --reseed_base; the summary has the control's
'first two on-lines'; the table has the two rung rows, marked capped; the script ends with 'done'.
MODE ctlfail (CAP 45): ks307 is TERMed by its exact pid (exit 143, gate failed), 'control failed: rungs not started' is logged, neither rung is started, and it ends with 'done'.
Exit 0 pass, 1 otherwise. --selftest runs planted folders through the same function: the pass cases must pass, each broken case must fail; --break expects a pass case to fail and so must exit 1."""
import os
import re
import sys
import tempfile

CMD = "# 2026-11-21 09:00:00 UTC cmd: python3 -u anm_run.py R O --state S --od_accept own --tol_od {tol} --steps 0 --ks {k} --keep_plan 0\n"


def rd(p):
    return open(p).read() if os.path.exists(p) else ""


def check(mode, d, cap, tol="1e-60"):
    ex = rd(f"{d}/exits_1064f.txt")
    bad = []

    def get(pat, what):
        m = re.search(pat, ex)
        if not m:
            bad.append(f"missing: {what}")
        return m
    if mode == "pass":
        m1 = get(r"1064 ks307 exit 0 wall (\d+) s gate 0", "ks307 exit 0, gate 0")
        for L in ("ks331", "ks347"):
            s = get(rf"1064 {L} started, pid \d+ ", f"{L} started")
            get(rf"1064 {L} cap {cap} s: TERM to pid \d+", f"TERM to {L}'s pid at the cap")
            get(rf"1064 {L} exit 143 wall (\d+) s gate 1", f"{L} exit 143, gate 1")
            if s and ex.find("ks307 exit") > ex.find(f"{L} started"):
                bad.append(f"{L} started before ks307 ended")
            if not rd(f"{d}/gate_{L}.txt").startswith("failed"):
                bad.append(f"gate_{L}.txt does not start with 'failed'")
        get(r"1064 delta1064_ctl_vs_state exit 0 xcheck 0", "the control's delta against the stored state and its xcheck")
        if m1 and not int(m1.group(1)) < cap - 30:
            bad.append(f"ks307 wall {m1.group(1)} s is not below the cap {cap} s by 30 s")
        for L, k in (("ks307", 307), ("ks331", 331), ("ks347", 347)):
            c = (re.search(r"cmd: (.*)", rd(f"{d}/{L}.log")) or [None, ""])[1]
            if "--od_accept own" not in c:
                bad.append(f"{L}.log's command has no --od_accept own")
            if f"--tol_od {tol} " not in c:
                bad.append(f"{L}.log's command has no --tol_od {tol}")
            if f"--ks {k} " not in c + " ":
                bad.append(f"{L}.log's command has no --ks {k}")
            for fl in ("--elim_switch", "--reseed_base"):
                if fl in c:
                    bad.append(f"{L}.log's command has {fl}")
        if not re.search(r"^ks307 first two on-lines: on ", rd(f"{d}/summary_1064f.txt"), re.M):
            bad.append("summary_1064f.txt has no 'ks307 first two on-lines: on ...' line")
        t = rd(f"{d}/table_1064f.md")
        for L, k in (("ks331", 331), ("ks347", 347)):
            if not re.search(rf"\| {L} \| {k} \| 143 \(capped\) \|", t):
                bad.append(f"table_1064f.md has no '| {L} | {k} | 143 (capped) |' row")
    else:
        get(rf"1064 ks307 cap {cap} s: TERM to pid \d+", "TERM to ks307's pid at the cap")
        get(r"1064 ks307 exit 143 wall (\d+) s gate 1", "ks307 exit 143, gate 1")
        get(r"1064 control failed: rungs not started", "control failed line")
        for L in ("ks331", "ks347"):
            if re.search(rf"1064 {L} started", ex):
                bad.append(f"{L} was started after a failed control")
        if not rd(f"{d}/gate_ks307.txt").startswith("failed"):
            bad.append("gate_ks307.txt does not start with 'failed'")
    get(r"1064 done ", "done")
    return bad


def planted(mode, d, drop=None, extra=None, gate="failed: no octo-double Newton line", w1=100, bad_cmd=None, f2=True, bad_ks=False, bad_tol=False):
    if mode == "pass":
        lines = ["1064 worktree x 2026-11-21 09:00:00 UTC",
                 f"1064 ks307 exit 0 wall {w1} s gate 0 2026-11-21 09:01:40 UTC",
                 "1064 ks331 started, pid 5 2026-11-21 09:01:40 UTC", "1064 ks347 started, pid 6 2026-11-21 09:01:40 UTC",
                 "1064 ks331 cap 600 s: TERM to pid 5 2026-11-21 09:11:40 UTC", "1064 ks347 cap 600 s: TERM to pid 6 2026-11-21 09:11:40 UTC",
                 "1064 ks331 exit 143 wall 630 s gate 1 2026-11-21 09:12:10 UTC", "1064 ks347 exit 143 wall 630 s gate 1 2026-11-21 09:12:10 UTC",
                 "1064 delta1064_ctl_vs_state exit 0 xcheck 0 2026-11-21 09:12:20 UTC",
                 "1064 done 2026-11-21 09:12:31 UTC"]
        for L, k in (("ks307", 307), ("ks331", 331), ("ks347", 347)):
            c = CMD.format(k=k + 1 if (bad_ks and L == "ks347") else k, tol="1e-60" if (bad_tol and L == "ks347") else "2e-34")
            if bad_cmd and L == "ks331":
                c = c.replace("--steps", bad_cmd + " --steps")
            open(f"{d}/{L}.log", "w").write(c)
        open(f"{d}/summary_1064f.txt", "w").write("ks307 first two on-lines: on 0: |F| 3.9e-36 converged|\n" if f2 else "ks307: exit 0\n")
        for L in ("ks331", "ks347"):
            open(f"{d}/gate_{L}.txt", "w").write(gate + "\n")
        open(f"{d}/table_1064f.md", "w").write("| ks331 | 331 | 143 (capped) | 630 |\n| ks347 | 347 | 143 (capped) | 630 |\n")
    else:
        lines = ["1064 worktree x 2026-11-21 09:00:00 UTC",
                 "1064 ks307 cap 45 s: TERM to pid 5 2026-11-21 09:00:45 UTC",
                 "1064 ks307 exit 143 wall 60 s gate 1 2026-11-21 09:01:15 UTC",
                 "1064 control failed: rungs not started 2026-11-21 09:01:15 UTC",
                 "1064 done 2026-11-21 09:01:16 UTC"]
        open(f"{d}/gate_ks307.txt", "w").write(gate + "\n")
    if drop is not None:
        lines = [x for x in lines if drop not in x]
    if extra:
        lines.append(extra)
    open(f"{d}/exits_1064f.txt", "w").write("\n".join(lines) + "\n")


def selftest(brk):
    cases = [("pass", "pass case", {}, True),
             ("pass", "ks307 too slow", {"w1": 580}, False),
             ("pass", "no TERM line for ks347", {"drop": "ks347 cap"}, False),
             ("pass", "ks331 gate converged", {"gate": "converged: x"}, False),
             ("pass", "no control delta against the stored state", {"drop": "ctl_vs_state"}, False),
             ("pass", "ks331's command has --elim_switch", {"bad_cmd": "--elim_switch 1e-9"}, False),
             ("pass", "ks331's command has --reseed_base", {"bad_cmd": "--reseed_base 1"}, False),
             ("pass", "ks347's command has the wrong --ks", {"bad_ks": True}, False),
             ("pass", "ks347's command has --tol_od 1e-60 where the dry sets 2e-34", {"bad_tol": True}, False),
             ("pass", "summary lacks the first two on-lines", {"f2": False}, False),
             ("ctlfail", "ctlfail case", {}, True),
             ("ctlfail", "ks331 started after a failed control", {"extra": "1064 ks331 started, pid 9 x"}, False),
             ("ctlfail", "no control failed line", {"drop": "control failed"}, False),
             ("ctlfail", "ks307 gate converged", {"gate": "converged: x"}, False)]
    if brk:
        cases[0] = cases[0][:3] + (False,)
    n = 0
    for mode, name, kw, want in cases:
        with tempfile.TemporaryDirectory() as d:
            planted(mode, d, **kw)
            bad = check(mode, d, 600 if mode == "pass" else 45, "2e-34")
        ok = (not bad) == want
        print(f"  {mode}: {name}: {'pass' if not bad else 'fail'} (expected {'pass' if want else 'fail'}): {'ok' if ok else 'WRONG'}")
        n += not ok
    print("selftest", "FAIL" if n else "PASS")
    return 1 if n else 0


if __name__ == "__main__":
    if sys.argv[1] == "--selftest":
        sys.exit(selftest("--break" in sys.argv))
    bad = check(sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4] if len(sys.argv) > 4 else "1e-60")
    for b in bad:
        print("FAIL:", b)
    print("dry test", sys.argv[1], "FAILED" if bad else "PASSED")
    sys.exit(1 if bad else 0)
