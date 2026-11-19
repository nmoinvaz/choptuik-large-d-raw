"""#989 control: the `zero` solve at xi1 0.15 (rtol 1e-14, h3 1e-4, Z and S of #964), run from the worktree at origin/main, must
reproduce #976's `zero` log from main 5e603e30 apart from seconds and memory addresses (r_1, |r_3|, every printed residual line).

    python control989.py [--mutate=ref]       exit 0 when the two logs agree, 1 when they differ
--mutate=ref compares against #975's rtol 1e-13 `zero` log instead, which must differ (the control must be able to fail).
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
if "--mutate=ref" not in sys.argv:
    cmd = [rj.PY, "-u", "hier_nb.py", "7", f"{rj.Z_A:.9g}", f"{rj.Z_W:.9g}", f"--x={rj.Z_X}", "--xi1=0.15"] + rj.S
    t0 = time.time()
    rc = rj.run(cmd, log, time.time() + 3 * 3600, lambda s: print(time.strftime("%H:%M:%S", time.gmtime()), s, flush=True))
    print(f"solve exit {rc} after {time.time() - t0:.0f} s", flush=True)


def norm(path):
    t = open(path, encoding="utf-8", errors="replace").read().replace("\r", "")
    t = re.sub(r"0x[0-9A-Fa-f]+", "ADDR", t)
    t = re.sub(r"[0-9.]+ s\b", "T s", t)
    return [l for l in t.splitlines() if "Exception ignored" not in l]


a, b = norm(log), norm(REF)
same = a == b
res = rj.parse(open(log, encoding="utf-8", errors="replace").read()) if os.path.exists(log) else None
print(f"{os.path.basename(log)} against {os.path.basename(REF)}: {len(a)} and {len(b)} lines, identical apart from seconds and addresses: {same}")
print(f"r_1, |r_3|, end state of the new log: {res[:2] if res else None}")
sys.exit(0 if same else 1)
