#!/usr/bin/env python3
"""#1006 (win): T1 (rt_sigma --rough --save_x, then rt_xcount) at sample a and b with 12 starts and at sample c with 24, one step at a time, 2 BLAS threads, BelowNormal. From I985-win/run_985.py.

usage: python run_1006.py                (venv-t151 python, from this folder; writes logs/<label>.log and .exit, logs/run_1006.log, logs/run_1006.exit)
       python run_1006.py --selftest     the driver on dummy steps

Steps: xc_selftest (wanted exit 0), xc_selftest_mutate (1), T1_a, T1_a_xcount, T1_b, T1_b_xcount, T1_c24, T1_c24_xcount (code: main c6c1ee6a, solver/rt of origin/main 92a6c284 is the same).
Stop rules: a step whose exit is not a wanted one stops the work (driver exit 7); a sigma run over its cap of 2 h is killed and the next step still starts, a step whose input file is missing is skipped
(both give driver exit 5 at the end); a file STOP_1006 in this folder stops what runs (4).
Exit codes of logs/run_1006.exit: 0 all as wanted, 5 a cap hit or a skipped step and no failure, 7 a failure, 4 stopped."""
import os
import subprocess
import sys
import tempfile
import time

HERE = os.path.dirname(os.path.abspath(__file__))
WT = r"C:\Users\nathan\Source\choptuik-i985"
RT = os.path.join(WT, "solver", "rt")
PY = r"C:\Users\nathan\Source\venv-t151\Scripts\python.exe"
RAW = r"C:\Users\nathan\Source\choptuik-large-d-raw"
S = {"a": RAW + r"\I671-win\solves\k0_D40_mutnorows_D40.0201_32x121.npz", "b": RAW + r"\I701-win\solves\k0b_D40_mutnorows_D40.0201_32x121.npz",
     "c": RAW + r"\I951-win\solves\k0c_D40_mutnorows_D40.0201_32x121.npz"}
CAP_RUN = 2.0 * 3600
CAP_SHORT = 20 * 60
THREADS = "2"
BELOW_NORMAL_NO_WINDOW = 0x00004000 | 0x08000000


def say(logdir, msg):
    line = f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())} UTC {msg}"
    print(line, flush=True)
    with open(os.path.join(logdir, "run_1006.log"), "a") as f:
        f.write(line + "\n")


def kill_tree(p):
    subprocess.run(["taskkill", "/T", "/F", "/PID", str(p.pid)], capture_output=True)


def run_one(step, logdir, stopfile, poll=10.0):
    """step: dict label, cmd, cwd, env, cap_s, want. Returns the code: the exit code, 4 for STOP, 5 for the cap"""
    lab, cap_s = step["label"], step["cap_s"]
    t = time.time()
    p = subprocess.Popen(step["cmd"], cwd=step["cwd"], stdout=open(os.path.join(logdir, f"{lab}.log"), "w"), stderr=subprocess.STDOUT, env=step["env"], creationflags=BELOW_NORMAL_NO_WINDOW)
    say(logdir, f"start {lab} (pid {p.pid}), cap {cap_s / 60:.0f} min")
    while True:
        time.sleep(poll)
        if os.path.exists(stopfile):
            kill_tree(p)
            code, text = 4, "killed 4 (STOP_1006)"
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
    """Runs the steps in order; returns (driver exit code, {label: code or 'skipped'})."""
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


def build(env):
    L = os.path.join(HERE, "rt_launch.py")
    sig = os.path.join(RT, "rt_sigma.py")
    xc = os.path.join(RT, "rt_xcount.py")
    P = lambda *a: [PY, "-u", L, sig, *a]
    X = lambda *a: [PY, "-I", xc, *a]
    d = lambda *a: os.path.join(HERE, *a)
    s = [mk("xc_selftest", X("--selftest"), env), mk("xc_selftest_mutate", X("--selftest", "--mutate=transpose"), env, want=(1,))]
    for lab, root, n, others in (("T1_a", "a", 12, "bc"), ("T1_b", "b", 12, "ac"), ("T1_c24", "c", 24, "ab")):
        s += [mk(lab, P(S[root], "--rough", "--starts", str(n), "--save_x", d("x", f"{lab}.npz")), env, cap_s=CAP_RUN, soft_cap=True),
              mk(f"{lab}_xcount", X(d("x", f"{lab}.npz"), "--root", S[root], "--chords", ",".join(S[o] for o in others), "--out", d("x", f"{lab}.json")), env, needs=[d("x", f"{lab}.npz")])]
    return s


def dummy(label, body, env, want=(0,), cap_s=30, **kw):
    return dict(label=label, cmd=[sys.executable, "-c", body], cwd=tempfile.gettempdir(), env=env, want=want, cap_s=cap_s, **kw)


def selftest():
    bad = 0
    env = dict(os.environ)
    good, slow = "print('ok', flush=True)\n", "import time\ntime.sleep(60)\n"
    with tempfile.TemporaryDirectory() as td:
        stop = os.path.join(td, "STOP")

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
        case("a missing input skips the step, exit 5", [dummy("a", good, env), dummy("x", good, env, needs=[os.path.join(td, "f1")]), dummy("c", good, env)], 5, {"a": 0, "x": "skipped", "c": 0}, "l6")
        open(stop, "w").write("x")
        case("STOP file", [dummy("a", slow, env)], 4, None, "l7")
        os.remove(stop)
        steps = build(env)
        names = [s["label"] for s in steps]
        want = ["xc_selftest", "xc_selftest_mutate", "T1_a", "T1_a_xcount", "T1_b", "T1_b_xcount", "T1_c24", "T1_c24_xcount"]
        ok = names == want and steps[1]["want"] == (1,) and all(steps[i]["cap_s"] == CAP_RUN and steps[i]["soft_cap"] for i in (2, 4, 6))
        ok = ok and [steps[i]["cmd"][steps[i]["cmd"].index("--starts") + 1] for i in (2, 4, 6)] == ["12", "12", "24"] and all("--save_x" in steps[i]["cmd"] for i in (2, 4, 6))
        ok = ok and [os.path.basename(steps[i]["cmd"][4]) for i in (2, 4, 6)] == ["k0_D40_mutnorows_D40.0201_32x121.npz", "k0b_D40_mutnorows_D40.0201_32x121.npz", "k0c_D40_mutnorows_D40.0201_32x121.npz"]
        ok = ok and all(os.path.exists(p) for p in S.values()) and os.path.exists(os.path.join(RT, "rt_sigma.py")) and os.path.exists(os.path.join(RT, "rt_xcount.py"))
        chords = [steps[i]["cmd"][steps[i]["cmd"].index("--chords") + 1].split(",") for i in (3, 5, 7)]
        ok = ok and chords == [[S["b"], S["c"]], [S["a"], S["c"]], [S["a"], S["b"]]]
        print(f"  the real step list: {len(names)} steps, 12 / 12 / 24 starts, states a / b / c, chords the other two, caps and input files {'ok' if ok else 'WRONG'}")
        bad += not ok
    print("selftest", "FAILED" if bad else "passed")
    return bad


def main():
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    logdir = os.path.join(HERE, "logs")
    os.makedirs(logdir, exist_ok=True)
    os.makedirs(os.path.join(HERE, "x"), exist_ok=True)
    env = dict(os.environ, OPENBLAS_NUM_THREADS=THREADS, OMP_NUM_THREADS=THREADS, MKL_NUM_THREADS=THREADS, PYTHONDONTWRITEBYTECODE="1", TMPDIR=tempfile.gettempdir())
    rc, codes = drive(build(env), logdir, os.path.join(HERE, "STOP_1006"))
    open(os.path.join(logdir, "run_1006.exit"), "w").write(f"{rc}\n")
    say(logdir, f"all done, codes {codes}, driver exit {rc}")
    sys.exit(rc)


if __name__ == "__main__":
    main()
