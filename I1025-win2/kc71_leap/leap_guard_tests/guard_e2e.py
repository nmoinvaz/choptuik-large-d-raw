"""End-to-end planted tests of leap_guard.py. Base: leg 3's 12 real records (--n0 12) or two seed records (--seeds), a fake exits file naming a dummy
process with ell_leap.py in its command line, a fake leap log. Point 1 is normal; point 2 is planted. Each rule has a case that must stop (STOP file, dummy
killed) and a control with that rule's mutation (no STOP, dummy alive); a case that looks like leg 3's D 20.75 (n_null falls, cos 0.051) must not stop."""
import copy, json, os, re, subprocess, sys, time

SP = os.path.dirname(os.path.abspath(__file__))
PY = sys.executable
G = "D:/choptuik-i935-raw/I1025-win2/kc71_leap/leap_guard.py"
SRC = "D:/choptuik-i935-raw/I1025-win2/kc71_leap/states/l1kc71Lw1025c.jsonl"
tag = time.strftime("%H%M%S")
base = [json.loads(x) for x in open(SRC) if x.strip()][:12]
assert len(base) == 12 and base[-1]["D"] == 20.75 and base[-1]["n_null"] == 63


def p1_of(last):
    p = copy.deepcopy(last)
    p.update(D=20.78125, Delta=last["Delta"] + 0.03125 * 0.0270, h=0.03125, cos_t_reg=[0.05, 0.02, 0.03, 0.04], n_null=63)
    return p


def run(case, mutate, plant, seeds=False, want_stop=True):
    d = os.path.join(SP, "guard_e2e_b_%s_%s" % (re.sub(r"[^A-Za-z0-9]+", "_", case), tag))
    os.makedirs(d)
    rec = d + "/rec.jsonl"
    dummy = subprocess.Popen([PY, "-c", "import time; time.sleep(300)", "ell_leap.py"])
    open(d + "/exits.txt", "w").write("kcl leap9 root pid %d, cap 43200 s, want exit 0 x\n" % dummy.pid)
    open(d + "/leap.log", "w").write("")
    args = [PY, "-I", G, "--rec", rec, "--exits", d + "/exits.txt", "--rootkey", "leap9 root pid", "--log", d + "/leap.log",
            "--out", d + "/points.txt", "--stop", d + "/STOP.txt", "--done", d + "/done", "--poll", "1", "--settle", "1"]
    if seeds:
        a, b = copy.deepcopy(base[-2]), copy.deepcopy(base[-1])
        for r in (a, b):
            for k in ("n_null", "cos_t_reg", "sv_reg_small", "sv_J_max", "tan_norm"):
                r.pop(k, None)
        open(d + "/seedA.jsonl", "w").write(json.dumps(a) + "\n")
        open(d + "/seedB.jsonl", "w").write(json.dumps(b) + "\n")
        open(rec, "w").write("")
        args += ["--seeds", d + "/seedA.jsonl", d + "/seedB.jsonl"]
        last = base[-1]
    else:
        open(rec, "w").write("".join(json.dumps(r) + "\n" for r in base))
        args += ["--n0", "12"]
        last = base[-1]
    if mutate:
        args.append("--mutate=" + mutate)
    gp = subprocess.Popen(args, stdout=open(d + "/guard.out", "w"), stderr=subprocess.STDOUT)
    p1 = p1_of(last)
    if seeds:
        p1.update(cos_t_reg=[0.05, 0.02, 0.03, 0.04])
        plant1 = plant
        p1 = plant1(p1)
        pts = [p1]
    else:
        p2 = copy.deepcopy(p1)
        p2.update(D=20.8125, Delta=p1["Delta"] + 0.03125 * 0.0271)
        pts = [p1, plant(p2)]
    for p in pts:
        open(d + "/leap.log", "a").write(json.dumps(p) + "\n")
        open(rec, "a").write(json.dumps(p) + "\n")
        time.sleep(5)
    t0 = time.time()
    while time.time() - t0 < 25 and not os.path.exists(d + "/STOP.txt") and gp.poll() is None:
        time.sleep(1)
    time.sleep(3)
    stopped = os.path.exists(d + "/STOP.txt")
    open(d + "/done", "w").write("x")
    gp.wait(timeout=60)
    alive = dummy.poll() is None
    if alive:
        dummy.kill()
    rows = open(d + "/points.txt").read().splitlines()[2:]
    ok = stopped == want_stop and alive == (not want_stop) and len(rows) == len(pts)
    msg = open(d + "/STOP.txt").read().splitlines()[0][:200] if stopped else "-"
    print("%-34s mutate=%-5s: STOP %-5s dummy alive %-5s rows %d  %s  [%s]" % (case, mutate, stopped, alive, len(rows), "OK" if ok else "WRONG", msg))
    return ok


def cos(c):
    return lambda p: dict(p, cos_t_reg=[c, 0.02, 0.03, 0.04])


def nn(n, c):
    return lambda p: dict(p, n_null=n, cos_t_reg=[c, 0.02, 0.03, 0.04])


def slope_turn(p):
    return dict(p, Delta=p["Delta"] - 0.01)


res = [run("cos 0.6 (rule 2)", None, cos(0.6)),
       run("cos 0.6, mutate=cos", "cos", cos(0.6), want_stop=False),
       run("n_null +1, cos 0.35 (rule 3)", None, nn(64, 0.35)),
       run("n_null +1, cos 0.35, mutate=nnull", "nnull", nn(64, 0.35), want_stop=False),
       run("slope turns (rule 1)", None, slope_turn),
       run("slope turns, mutate=slope", "slope", slope_turn, want_stop=False),
       run("D 20.75-like: n_null -1, cos .051", None, nn(62, 0.051), want_stop=False),
       run("n_null +1, cos 0.29", None, nn(64, 0.29), want_stop=False),
       run("seeds mode, first point cos 0.6", None, cos(0.6), seeds=True)]
print("E2E", "PASS" if all(res) else "FAIL", res)
sys.exit(0 if all(res) else 1)
