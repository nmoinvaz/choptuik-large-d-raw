#!/usr/bin/env python3
"""#985 (win): the checks block, T1 and T2 of #983's commands, one step at a time, 2 BLAS threads, BelowNormal. From I972-win/run_972.py.

usage: python run_985.py                 (venv-t151 python, from this folder; writes logs/<label>.log and .exit, logs/run_985.log, logs/run_985.exit)
       python run_985.py --selftest      the driver on dummy steps

Steps in order: the checks block (xc_selftest, xc_selftest_mutate, planted_p2, xc_p2_expect2, planted_p4, xc_p4_expect4, xc_p2_expect4; wanted exits 0 1 0 0 0 0 1), T1_c (rt_sigma 12 rough starts, --save_x),
T1_c_xcount, the control (T1's start lines against #951's), then T2: perturb m35, T2_35, m35_d1e-20, T2_35_xcount, perturb m20, T2_20, m20_d1e-26, T2_20_xcount.
Stop rules: a step whose exit is not a wanted one stops the work (driver exit 7); a control mismatch stops it (8); a sigma run over its cap of 2 h is killed and the next step still starts, a step whose
input file is missing is skipped (both give driver exit 5 at the end); a file STOP_985 in this folder stops what runs (4).
Exit codes of logs/run_985.exit: 0 all as wanted, 5 a cap hit or a skipped step and no failure, 7 a failure, 8 the control, 4 stopped."""
import os
import subprocess
import sys
import tempfile
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import table_985  # noqa: E402

WT = r"C:\Users\nathan\Source\choptuik-i985"
RT = os.path.join(WT, "solver", "rt")
PY = r"C:\Users\nathan\Source\venv-t151\Scripts\python.exe"
RAW = r"C:\Users\nathan\Source\choptuik-large-d-raw"
S_C = RAW + r"\I951-win\solves\k0c_D40_mutnorows_D40.0201_32x121.npz"
CH_A = RAW + r"\I671-win\solves\k0_D40_mutnorows_D40.0201_32x121.npz"
CH_B = RAW + r"\I701-win\solves\k0b_D40_mutnorows_D40.0201_32x121.npz"
S_35 = RAW + r"\I145-mac\fol\fol_32x121_D34.9933_32x121.npz"
S_20 = RAW + r"\I105-mac\controls\res_32x121_D20.0437_D20.0437_32x121.npz"
CAP_RUN = 2.0 * 3600
CAP_SHORT = 20 * 60
THREADS = "2"
BELOW_NORMAL_NO_WINDOW = 0x00004000 | 0x08000000


def say(logdir, msg):
    line = f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())} UTC {msg}"
    print(line, flush=True)
    with open(os.path.join(logdir, "run_985.log"), "a") as f:
        f.write(line + "\n")


def kill_tree(p):
    subprocess.run(["taskkill", "/T", "/F", "/PID", str(p.pid)], capture_output=True)


def run_one(step, logdir, stopfile, poll=10.0):
    """step: dict label, cmd, cwd, env, cap_s, want (tuple of wanted exits). Returns the code: the exit code, 4 for STOP, 5 for the cap"""
    lab, cap_s = step["label"], step["cap_s"]
    t = time.time()
    p = subprocess.Popen(step["cmd"], cwd=step["cwd"], stdout=open(os.path.join(logdir, f"{lab}.log"), "w"), stderr=subprocess.STDOUT, env=step["env"], creationflags=BELOW_NORMAL_NO_WINDOW)
    say(logdir, f"start {lab} (pid {p.pid}), cap {cap_s / 60:.0f} min")
    while True:
        time.sleep(poll)
        if os.path.exists(stopfile):
            kill_tree(p)
            code, text = 4, "killed 4 (STOP_985)"
        elif time.time() - t > cap_s:
            kill_tree(p)
            code, text = 5, f"killed 5 (cap {cap_s / 60:.0f} min)"
        else:
            rc = p.poll()
            if rc is None:
                continue
            code, text = rc, f"exit {rc}"
        break
    open(os.path.join(logdir, f"{lab}.exit"), "w").write(text + "\n")
    say(logdir, f"{lab} {text} after {time.time() - t:.0f} s")
    return code


def drive(steps, logdir, stopfile, poll=10.0):
    """Runs the steps in order; returns (driver exit code, {label: code or 'skipped' or 'control ok/mismatch'})."""
    os.makedirs(logdir, exist_ok=True)
    codes, soft = {}, False
    for st in steps:
        lab = st["label"]
        if os.path.exists(stopfile):
            return 4, codes
        miss = [p for p in st.get("needs", []) if not os.path.exists(p)]
        if miss:
            codes[lab] = "skipped"
            soft = True
            say(logdir, f"skip {lab}, missing {miss}")
            continue
        if "control" in st:
            ok, why = st["control"]()
            codes[lab] = "control ok" if ok else "control mismatch"
            say(logdir, f"{lab}: {why}: {'equal' if ok else 'NOT EQUAL'}")
            if not ok:
                return 8, codes
            continue
        code = run_one(st, logdir, stopfile, poll)
        codes[lab] = code
        if code == 4:
            return 4, codes
        if code == 5 and st.get("soft_cap"):
            soft = True
        elif code not in st["want"]:
            return 7, codes
    return (5 if soft else 0), codes


def mk(label, cmd, env, want=(0,), cap_s=CAP_SHORT, **kw):
    return dict(label=label, cmd=cmd, cwd=RT, env=env, want=want, cap_s=cap_s, **kw)


def build(env, logdir):
    L = os.path.join(HERE, "rt_launch.py")
    sig = os.path.join(RT, "rt_sigma.py")
    xc = os.path.join(RT, "rt_xcount.py")
    pt = os.path.join(RT, "rt_perturb.py")
    P = lambda *a: [PY, "-u", L, sig, *a]
    X = lambda *a: [PY, "-I", xc, *a]
    d = lambda *a: os.path.join(HERE, *a)
    s = [mk("xc_selftest", X("--selftest"), env), mk("xc_selftest_mutate", X("--selftest", "--mutate=transpose"), env, want=(1,)),
         mk("planted_p2", P("--planted", "--deep", "2", "--save_x", d("planted", "p2.npz")), env),
         mk("xc_p2_expect2", X(d("planted", "p2.npz"), "--expect", "2"), env, needs=[d("planted", "p2.npz")]),
         mk("planted_p4", P("--planted", "--deep", "4", "--save_x", d("planted", "p4.npz")), env),
         mk("xc_p4_expect4", X(d("planted", "p4.npz"), "--expect", "4"), env, needs=[d("planted", "p4.npz")]),
         mk("xc_p2_expect4", X(d("planted", "p2.npz"), "--expect", "4"), env, want=(1,), needs=[d("planted", "p2.npz")]),
         mk("T1_c", P(S_C, "--rough", "--starts", "12", "--save_x", d("x", "T1_c.npz")), env, cap_s=CAP_RUN, soft_cap=True),
         mk("T1_c_xcount", X(d("x", "T1_c.npz"), "--root", S_C, "--chords", f"{CH_A},{CH_B}", "--out", d("x", "T1_c.json")), env, needs=[d("x", "T1_c.npz")]),
         dict(label="control", control=lambda: table_985.compare_control(os.path.join(logdir, "T1_c.log")))]
    for tag, root, dl, label in (("35", S_35, "1e-20", "m35_d1e-20"), ("20", S_20, "1e-26", "m20_d1e-26")):
        mv = d("states", f"{label}.npz")
        s += [mk(f"perturb_{tag}", [PY, "-I", pt, root, mv, "--delta", dl], env),
              mk(f"T2_{tag}", P(root, "--rough", "--starts", "12", "--save_x", d("x", f"T2_{tag}.npz")), env, cap_s=CAP_RUN, soft_cap=True),
              mk(label, P(mv, "--rough", "--starts", "12"), env, cap_s=CAP_RUN, soft_cap=True, needs=[mv]),
              mk(f"T2_{tag}_xcount", X(d("x", f"T2_{tag}.npz"), "--out", d("x", f"T2_{tag}.json")), env, needs=[d("x", f"T2_{tag}.npz")])]
    return s


def dummy(label, body, env, want=(0,), cap_s=30, **kw):
    return dict(label=label, cmd=[sys.executable, "-c", body], cwd=tempfile.gettempdir(), env=env, want=want, cap_s=cap_s, **kw)


def selftest():
    bad = 0
    env = dict(os.environ)
    good, slow = "print('ok', flush=True)\n", "import time\ntime.sleep(60)\n"
    with tempfile.TemporaryDirectory() as td:
        stop = os.path.join(td, "STOP")
        f1 = os.path.join(td, "f1.txt")

        def case(name, steps, want_rc, want_codes=None, log="l"):
            nonlocal bad
            rc, codes = drive(steps, os.path.join(td, log), stop, 0.2)
            ok = rc == want_rc and (want_codes is None or codes == want_codes)
            print(f"  {name}: exit {rc} {codes} (want {want_rc}) {'ok' if ok else 'WRONG'}")
            bad += not ok

        case("all as wanted, an expected exit 1 counts", [dummy("a", good, env), dummy("b", "import sys; sys.exit(1)", env, want=(1,)), dummy("c", good, env)], 0, {"a": 0, "b": 1, "c": 0}, "l1")
        case("an unexpected exit 1 stops", [dummy("a", good, env), dummy("b", "import sys; sys.exit(1)", env), dummy("c", good, env)], 7, {"a": 0, "b": 1}, "l2")
        case("a wanted exit 1 that is 0 stops (the control passed)", [dummy("a", good, env), dummy("b", good, env, want=(1,)), dummy("c", good, env)], 7, {"a": 0, "b": 0}, "l3")
        case("a run over its cap is killed, the next still runs, exit 5", [dummy("r", slow, env, cap_s=1.0, soft_cap=True), dummy("n", good, env)], 5, {"r": 5, "n": 0}, "l4")
        case("a short step over its cap stops", [dummy("a", slow, env, cap_s=1.0), dummy("c", good, env)], 7, {"a": 5}, "l5")
        case("a missing input skips the step, exit 5", [dummy("a", good, env), dummy("x", good, env, needs=[f1]), dummy("c", good, env)], 5, {"a": 0, "x": "skipped", "c": 0}, "l6")
        case("a failed control stops with 8", [dummy("a", good, env), dict(label="ctl", control=lambda: (False, "1 of 12")), dummy("c", good, env)], 8, {"a": 0, "ctl": "control mismatch"}, "l7")
        case("a good control goes on", [dict(label="ctl", control=lambda: (True, "12 of 12")), dummy("c", good, env)], 0, {"ctl": "control ok", "c": 0}, "l8")
        open(stop, "w").write("x")
        case("STOP file", [dummy("a", slow, env)], 4, None, "l9")
        os.remove(stop)
        env2 = dict(env)
        steps = build(env2, os.path.join(td, "lx"))
        names = [s["label"] for s in steps]
        want = ["xc_selftest", "xc_selftest_mutate", "planted_p2", "xc_p2_expect2", "planted_p4", "xc_p4_expect4", "xc_p2_expect4", "T1_c", "T1_c_xcount", "control",
                "perturb_35", "T2_35", "m35_d1e-20", "T2_35_xcount", "perturb_20", "T2_20", "m20_d1e-26", "T2_20_xcount"]
        ok = names == want and steps[1]["want"] == (1,) and steps[6]["want"] == (1,) and steps[7]["cap_s"] == CAP_RUN and steps[12]["cap_s"] == CAP_RUN and steps[7]["soft_cap"] and steps[12]["soft_cap"]
        ok = ok and "--save_x" in steps[7]["cmd"] and "--save_x" not in steps[12]["cmd"] and "--save_x" in steps[11]["cmd"] and "1e-26" in steps[14]["cmd"] and "1e-20" in steps[10]["cmd"]
        ok = ok and all(os.path.exists(p) for p in (S_C, CH_A, CH_B, S_35, S_20, steps[7]["cmd"][2]))
        print(f"  the real step list: {len(names)} steps in the order of #983's commands, wanted exits, caps, flags and input files {'ok' if ok else 'WRONG'}")
        bad += not ok
    print("selftest", "FAILED" if bad else "passed")
    return bad


def main():
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    logdir = os.path.join(HERE, "logs")
    os.makedirs(logdir, exist_ok=True)
    for sub in ("states", "x", "planted"):
        os.makedirs(os.path.join(HERE, sub), exist_ok=True)
    env = dict(os.environ, OPENBLAS_NUM_THREADS=THREADS, OMP_NUM_THREADS=THREADS, MKL_NUM_THREADS=THREADS, PYTHONDONTWRITEBYTECODE="1", TMPDIR=tempfile.gettempdir())
    rc, codes = drive(build(env, logdir), logdir, os.path.join(HERE, "STOP_985"))
    open(os.path.join(logdir, "run_985.exit"), "w").write(f"{rc}\n")
    say(logdir, f"all done, codes {codes}, driver exit {rc}")
    sys.exit(rc)


if __name__ == "__main__":
    main()
