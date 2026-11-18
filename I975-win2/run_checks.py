"""#975 setup: the six commands of solver/inner_stokes/inner_nb_checks.sh, one by one, at BelowNormal priority.

    python run_checks.py SRC_DIR OUT_DIR

SRC_DIR is solver/inner_stokes of the code worktree, OUT_DIR the folder for the logs (the script's own logs/ holds tracked
files). Each log gets its command line first and "exit N" last, as the script writes it. The two mutation controls must
end with exit 1, the other four with exit 0. This driver's exit is 0 when all six end as stored.
"""
import os, subprocess, sys, time

BELOW_NORMAL = 0x00004000
CHECKS = [  # log name, extra env, args, expected exit
    ("inner_nb_capcheck", {}, ["inner_nb.py", "capcheck"], 0),
    ("inner_nb_capcheck_mutate", {"INNER_NB_MAXFEV": "100"}, ["inner_nb.py", "capcheck"], 1),
    ("inner_nb_check", {}, ["inner_nb.py", "check", "1", "3", "5", "7"], 0),
    ("inner_nb_check_mutate", {}, ["inner_nb.py", "check", "3", "5", "--mutate=sign"], 1),
    ("hier_nb_selftest", {}, ["hier_nb.py", "selftest"], 0),
    ("hier_nb_selftest_mutate", {}, ["hier_nb.py", "selftest", "--mutate=radius"], 1),
]


def main():
    src, out = os.path.abspath(sys.argv[1]), os.path.abspath(sys.argv[2])
    os.makedirs(out, exist_ok=True)
    ok = True
    for name, env, args, want in CHECKS:
        e = dict(os.environ, PYTHONIOENCODING="utf-8", **env)
        log = os.path.join(out, name + ".log")
        t0 = time.time()
        with open(log, "w", encoding="utf-8", newline="\n") as f:
            f.write(f"# {time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime())} env {env or '-'}: python -u {' '.join(args)}\n")
            f.flush()
            p = subprocess.Popen([sys.executable, "-u"] + args, cwd=src, env=e, stdout=f, stderr=subprocess.STDOUT,
                                 creationflags=BELOW_NORMAL)
            rc = p.wait()
            f.write(f"exit {rc}\n")
        good = rc == want
        ok = ok and good
        print(f"{time.strftime('%H:%M:%S', time.gmtime())} UTC {name}: exit {rc} (stored {want}) {'ok' if good else 'DIFFERS'}  "
              f"{time.time() - t0:.0f} s", flush=True)
    print("ALL SIX END AS STORED" if ok else "SOME CHECK DIFFERS FROM STORED", flush=True)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
