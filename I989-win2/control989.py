"""#989 control: the `zero` solve at xi1 0.15 (rtol 1e-14, h3 1e-4, Z and S of #964), run from the worktree at origin/main, must
reproduce #976's `zero` log from main 5e603e30 apart from seconds and memory addresses (r_1, |r_3|, every printed residual line).

    python control989.py [--mutate=ref]       exit 0 when the two logs agree, 1 when they differ
--mutate=ref compares against #975's rtol 1e-13 `zero` log instead, which must differ (the control must be able to fail).
--compare-only skips the solve and compares the log already there.

Version 2 (written after the first version fired at 00:45:46 UTC 19 Nov, see the README): the exit-time `BytesIO` Traceback block after
the FIXED-A line (interpreter-exit race in multiprocessing.Pool.__del__, harmless, present in some runs of the same code and absent in
others) is dropped from both logs before comparing. Version 1 is kept as control989_v1_strict.py.
"""
import os, re, subprocess, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import run_job981 as rj

HERE = os.path.dirname(os.path.abspath(__file__)); R = os.path.dirname(HERE)
REF = f"{R}/I976-win2/logs/hier_nb_M7_win2_rtol14_xi015_zero.log"
if "--mutate=ref" in sys.argv:
    REF = f"{R}/I975-win2/logs/hier_nb_M7_win2_rtol13_xi015_zero.log"
log = os.path.join(HERE, "logs", "hier_nb_M7_win2_rtol14_ctrl_xi015_zero.log")
os.makedirs(os.path.dirname(log), exist_ok=True)
if "--mutate=ref" in sys.argv and not os.path.exists(log):
    sys.exit("run the control first: --mutate=ref compares its log against the wrong reference")
if "--mutate=ref" not in sys.argv and "--compare-only" not in sys.argv:
    cmd = [rj.PY, "-u", "hier_nb.py", "7", f"{rj.Z_A:.9g}", f"{rj.Z_W:.9g}", f"--x={rj.Z_X}", "--xi1=0.15"] + rj.S
    t0 = time.time()
    rc = rj.run(cmd, log, time.time() + 3 * 3600, lambda s: print(time.strftime("%H:%M:%S", time.gmtime()), s, flush=True))
    print(f"solve exit {rc} after {time.time() - t0:.0f} s", flush=True)


def norm(path):
    t = open(path, encoding="utf-8", errors="replace").read().replace("\r", "")
    t = re.sub(r"0x[0-9A-Fa-f]+", "ADDR", t)
    t = re.sub(r"[0-9.]+ s\b", "T s", t)
    ls = [l for l in t.splitlines() if "Exception ignored" not in l]
    k = next((i for i, l in enumerate(ls) if "FIXED-A M" in l), len(ls))
    out, i = ls[:k + 1], k + 1
    while i < len(ls):                                  # after FIXED-A: drop a Traceback block that ends in the BytesIO AttributeError
        if ls[i].startswith("Traceback (most recent call last)"):
            j = i
            while j < len(ls) and not ls[j].startswith("AttributeError"):
                j += 1
            if j < len(ls) and "BytesIO" in ls[j]:
                i = j + 1
                continue
        out.append(ls[i]); i += 1
    return out


a, b = norm(log), norm(REF)
same = a == b
res = rj.parse(open(log, encoding="utf-8", errors="replace").read()) if os.path.exists(log) else None
print(f"{os.path.basename(log)} against {os.path.basename(REF)}: {len(a)} and {len(b)} lines, identical apart from seconds and addresses: {same}")
print(f"r_1, |r_3|, end state of the new log: {res[:2] if res else None}")
sys.exit(0 if same else 1)
