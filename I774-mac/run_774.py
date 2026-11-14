#!/usr/bin/env python3
"""#774: re-polish full-system and held states in octo-double (anm_run.py --steps 0 --save_base 1) on two hpkernel
builds, one job after the other, each at nice 10 with 4 threads.
usage: python3 run_774.py JOB [JOB ...]      (from anywhere; the jobs are listed in JOBS)
       python3 run_774.py --list
Builds: E = main 3c35f0c's hpkernel (exact freeze projector of #523), loaded with PYTHONPATH=SITE2; R = venv-314's
installed hpkernel of 2026-11-09 (before #523, the rounded projector, as win's venv-t151 of #725-#769). Python is the
worktree's hp/ at main 3e096e26 for both, and multidouble's Python package is main's pin (f092018d) for both.
Each job writes into I774-mac/<JOB>/ and logs to logs/<JOB>.log, whose first line names the hpkernel file the job's
interpreter loads; logs/run_774.log gets the start, the end, the exit code, the wall and the CPU seconds."""
import os
import resource
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.dirname(HERE)
HP = "/Users/nathan/Source/choptuik-large-d-774/hp"
PY = "/Users/nathan/venv-314/bin/python"
SITE2 = "/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/df65b01f-07cd-4aee-8283-07a856363b66/scratchpad/site2"

# #682's flags as #727 and #742 ran them (run_727.py, run_742.py), with the octo-double corrector of #727/#739
F682 = ["--kfreeze", "13", "--N", "24", "--eps", "1e-14", "--D_max", "400", "--qd_it", "12", "--jet_q", "1", "--pred_q", "1",
        "--reseed", "2", "--reseed_q", "1", "--save_pred", "1", "--a_grow", "1.25", "--a_hold", "1", "--lam_stall", "0.04"]
OD = ["--corrector", "od", "--tol_od", "1e-60", "--reseed_o", "3", "--elim_switch", "0"]
S727 = ["--h_max", "0.0625", "--a0", "0.0625", "--steps", "0", "--save_base", "1"]      # #727's X2c job
S742 = ["--h_max", "1.0", "--a0", "1.0", "--steps", "0", "--save_base", "1"]            # #742's, polish only
# T138-win2's held chain (its README): --kfreeze 3 on the 1/n fit, quad-double corrector at 1e-28; here its corrector
# is swapped for the octo-double one as #727 swapped cont3's, and its switch is the default (T138 had no --elim_switch)
F138 = ["--kfreeze", "3", "--held_fit", "data/held_fit.json", "--N", "24", "--eps", "1e-14", "--h_max", "1.0", "--D_max", "1000",
        "--qd_it", "12", "--jet_q", "1", "--pred_q", "1", "--reseed", "2", "--reseed_q", "1", "--save_pred", "1"]
OD138 = ["--corrector", "od", "--tol_od", "1e-60", "--reseed_o", "3", "--steps", "0", "--save_base", "1"]

JOBS = {
    # the control: #727's X2c job from its start, on the rounded build (3 Newton steps on win)
    "C_X2c": ("R", "I727-win/states/X2_on_cont3plan.npz", F682 + OD[:4] + S727 + OD[4:]),
    # the five full-system states on the exact build
    "E_117": ("E", "I742-win/L/anm_pin13_D117.0000.npz", F682 + OD + S742),
    "E_113": ("E", "I742-win/P/base_pin13_D113.0000.npz", F682 + OD + S742),
    "E_120": ("E", "I742-win/M/anm_pin13_D120.0000.npz", F682 + OD + S742),
    "E_cont3": ("E", "I682-win/cont3/anm_pin13_D99.8750.npz", F682 + OD[:4] + S727 + OD[4:]),
    "E_X2c": ("E", "I727-win/X2c/base_pin13_D99.8750.npz", F682 + OD[:4] + S727 + OD[4:]),
    # the held states of #742's table, on both builds
    **{f"H_{b}{D}": (b, f"T138-win2/chain/anm_pin3_D{D}.0000.npz", F138 + OD138) for b in "RE" for D in (113, 117, 120)},
}


def env_for(build):
    e = dict(os.environ, OPENBLAS_NUM_THREADS="1", OMP_NUM_THREADS="1", MKL_NUM_THREADS="1", VECLIB_MAXIMUM_THREADS="1",
             PYTHONDONTWRITEBYTECODE="1")
    e.pop("PYTHONPATH", None)
    if build == "E":
        e["PYTHONPATH"] = SITE2
    return e


def say(msg):
    line = f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())} UTC {msg}"
    print(line, flush=True)
    with open(os.path.join(HERE, "logs", "run_774.log"), "a") as f:
        f.write(line + "\n")


def run(name):
    build, state, flags = JOBS[name]
    out = os.path.join(HERE, name)
    os.makedirs(out, exist_ok=True)
    env = env_for(build)
    which = subprocess.run([PY, "-c", "import hpkernel; print(hpkernel.__file__)"], env=env, cwd=HP, capture_output=True,
                           text=True).stdout.strip()
    want_site2 = build == "E"
    if (SITE2 in which) != want_site2:
        say(f"{name}: build {build} loads {which}, the wrong kernel; not run")
        return 3
    cmd = ["nice", "-n", "10", PY, "-u", "anm_run.py", RAW, out, "--state", state, *flags, "--threads", "4"]
    log = os.path.join(HERE, "logs", f"{name}.log")
    with open(log, "w") as f:
        f.write(f"# build {build}: hpkernel {which}\n# cwd {HP}\n# {' '.join(cmd)}\n")
    t0 = time.time()
    c0 = resource.getrusage(resource.RUSAGE_CHILDREN)
    say(f"start {name} (build {build}) from {state}")
    rc = subprocess.run(cmd, cwd=HP, env=env, stdout=open(log, "a"), stderr=subprocess.STDOUT).returncode
    c1 = resource.getrusage(resource.RUSAGE_CHILDREN)
    cpu = (c1.ru_utime - c0.ru_utime) + (c1.ru_stime - c0.ru_stime)
    say(f"{name} exit {rc} after {time.time() - t0:.0f} s wall, {cpu:.0f} s cpu")
    return rc


if __name__ == "__main__":
    if sys.argv[1:] == ["--list"]:
        for k, (b, s, f) in JOBS.items():
            print(k, b, s, " ".join(f))
        sys.exit(0)
    os.makedirs(os.path.join(HERE, "logs"), exist_ok=True)
    bad = [j for j in sys.argv[1:] if j not in JOBS]
    if bad:
        raise SystemExit(f"unknown jobs {bad}; run_774.py --list")
    for j in sys.argv[1:]:
        if run(j) != 0:
            say(f"stopping after {j}")
            sys.exit(2)
