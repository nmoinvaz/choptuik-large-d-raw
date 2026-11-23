"""End-to-end planted test of leg4_guard.py: fake record file (leg 3's 12 real records), fake exits file naming a dummy
process with ell_leap.py in its command line, fake log. Case 1: a normal point, then a turned-back point: the guard must write
the table rows, STOP, kill the dummy. Case 2 (control): the same with --mutate=slope: the guard must not stop, the dummy lives."""
import json, os, subprocess, sys, time

SP = os.path.dirname(os.path.abspath(__file__))
PY = sys.executable
G = "D:/choptuik-i935-raw/I1025-win2/kc71_leap/leg4_guard.py"
SRC = "D:/choptuik-i935-raw/I1025-win2/kc71_leap/states/l1kc71Lw1025c.jsonl"
tag = time.strftime("%H%M%S")


def run(case, mutate):
    d = os.path.join(SP, "guard_e2e_%s_%s" % (case, tag))
    os.makedirs(d)
    rec = os.path.join(d, "rec.jsonl")
    base = [json.loads(x) for x in open(SRC) if x.strip()]
    open(rec, "w").write("".join(json.dumps(r) + "\n" for r in base))
    dummy = subprocess.Popen([PY, "-c", "import time; time.sleep(300)", "ell_leap.py"])
    open(os.path.join(d, "exits.txt"), "w").write("kcl leap4 root pid %d, cap 43200 s, want exit 0 x\n" % dummy.pid)
    open(os.path.join(d, "leap.log"), "w").write("")
    args = [PY, "-I", G, "--rec", rec, "--n0", "12", "--exits", d + "/exits.txt", "--log", d + "/leap.log", "--out", d + "/points.txt",
            "--stop", d + "/STOP.txt", "--done", d + "/done", "--poll", "1"] + (["--mutate=" + mutate] if mutate else [])
    gp = subprocess.Popen(args, stdout=open(d + "/guard.out", "w"), stderr=subprocess.STDOUT)
    last = base[-1]
    p1 = dict(last, D=20.78125, Delta=last["Delta"] + 0.0010, h=0.03125)
    p1["sv_reg_small"] = [1.2e-11] + last["sv_reg_small"][1:]
    open(d + "/leap.log", "a").write(json.dumps(p1) + "\nfold watch: sigma_reg 1.451e-11 -> 1.2e-11, |J^+ dF/dn| 0.557 -> 0.6; h -> 0.015625\n")
    open(rec, "a").write(json.dumps(p1) + "\n")
    time.sleep(12)
    p2 = dict(p1, D=20.8125, Delta=p1["Delta"] - 0.0002, h=0.015625)
    open(d + "/leap.log", "a").write(json.dumps(p2) + "\n")
    open(rec, "a").write(json.dumps(p2) + "\n")
    t0 = time.time()
    while time.time() - t0 < 40 and not os.path.exists(d + "/STOP.txt") and gp.poll() is None:
        time.sleep(1)
    time.sleep(3)
    stopped = os.path.exists(d + "/STOP.txt")
    open(d + "/done", "w").write("x")
    gp.wait(timeout=60)
    alive = dummy.poll() is None
    if alive:
        dummy.kill()
    rows = open(d + "/points.txt").read().splitlines()[2:]
    print("case %s mutate=%s: STOP %s, dummy alive %s, rows %d, guard exit %s" % (case, mutate, stopped, alive, len(rows), gp.returncode))
    for r in rows:
        print("   ", r[:200])
    if stopped:
        print("   ", open(d + "/STOP.txt").read().splitlines()[0][:220])
    return stopped, alive, len(rows)


a = run("turn", None)
b = run("ctrl", "slope")
ok = a == (True, False, 2) and b == (False, True, 2)
print("E2E", "PASS" if ok else "FAIL", a, b)
sys.exit(0 if ok else 1)
