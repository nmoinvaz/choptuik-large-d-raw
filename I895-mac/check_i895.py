#!/usr/bin/env python3
"""Do the five commands that #895 documents reproduce their stored files when run as written? (#895)

    python3 check_i895.py <checkout> <python's bin directory> [--mutate=kappa1]

Each command is read from its reproduce block (proof/B8_constants.md section 13, proof/B_chain.md section 11), with
its comment cut off, and run by bash from solver/proof of the checkout, with the given directory first on PATH. The
result is compared with the stored file as committed (git show HEAD:...), numbers to --tol (1.7e-11 relative), wall
times dropped:
  - a scan appends its records to its --log: the appended records against the stored ones, in order;
  - the atoms run prints to stdout: against the second half of the stored log;
  - the (H8) run overwrites its log: against the stored log without its last line "exit 0".
Afterwards the files that the commands wrote are restored with git checkout. Exit 0 if all five reproduce.
--mutate=kappa1 runs the fixedZ command with kappa1 = 0.73, and the script must then exit 1."""
import json
import os
import re
import subprocess
import sys

NUM = re.compile(r"[-+]?(?:\d+\.\d*|\.\d+|\d+)(?:[eE][-+]?\d+)?")
TOL = 1.7e-11
CASES = [  # name, file with the block, text that picks the line, stored file, kind
    ("second atoms run", "proof/B8_constants.md", "b8m_atoms.py 4 2e-6 2e-6", "b8m_atoms_K4.log", "stdout-second-half"),
    ("scan with ln n0 = 58", "proof/B8_constants.md", "b8m_scan.py 4 73.89,70,66,62,58", "b8m_scan_K4_box.log", "append"),
    ("scan over d0", "proof/B_chain.md", "--log=b8m_scan_K4_d0.log", "b8m_scan_K4_d0.log", "append"),
    ("fixedZ", "proof/B_chain.md", "--log=b8m_scan_K4_fixedZ.log", "b8m_scan_K4_fixedZ.log", "append"),
    ("(H8) at kappa1 = 0.85", "proof/B_chain.md", "> b8m_h8_K4_L104.68_k0.85.log", "b8m_h8_K4_L104.68_k0.85.log", "overwrite"),
]


def leaves(o, p=""):
    if isinstance(o, dict):
        for k, v in o.items():
            yield from leaves(v, f"{p}/{k}")
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from leaves(v, f"{p}[{i}]")
    else:
        yield p, o


def unit(line):
    try:
        d = {k: v for k, v in leaves(json.loads(line)) if not k.endswith("/time")}
        num = {k: v for k, v in d.items() if isinstance(v, (int, float)) and not isinstance(v, bool)}
        return num, json.dumps({k: v for k, v in d.items() if k not in num}, sort_keys=True)
    except (ValueError, TypeError):
        return dict(enumerate(float(x) for x in NUM.findall(line))), NUM.sub("#", line).strip()


def compare(new, old):
    """(ok, largest relative difference, what differs) of two lists of lines"""
    if len(new) != len(old):
        return False, None, f"{len(new)} lines or records against {len(old)}"
    worst, text = 0.0, ""
    for i, (a, b) in enumerate(zip(new, old)):
        (na, ra), (nb, rb) = unit(a), unit(b)
        if ra != rb or set(na) != set(nb):
            text = text or f"line or record {i + 1} has other text or fields"
        for k in na:
            if k in nb:
                m = max(abs(na[k]), abs(nb[k]))
                worst = max(worst, abs(na[k] - nb[k]) / m if m > 0 else 0.0)
    return worst <= TOL and not text, worst, text


def command(root, md, pick):
    lines = [ln for ln in open(os.path.join(root, md)).read().splitlines() if pick in ln and "python3" in ln]
    assert len(lines) == 1, f"{md}: {len(lines)} lines with {pick!r}"
    return re.sub(r"\s+#.*$", "", lines[0]).strip()


def main():
    root, bindir = os.path.abspath(sys.argv[1]), sys.argv[2]
    mut = next((a.split("=", 1)[1] for a in sys.argv[3:] if a.startswith("--mutate=")), "")
    proof = os.path.join(root, "solver", "proof")
    env = dict(os.environ, PATH=bindir + os.pathsep + os.environ["PATH"])
    bad = 0
    for name, md, pick, stored, kind in CASES:
        if mut and name != "fixedZ":
            continue
        cmd = command(root, md, pick)
        if mut == "kappa1":
            assert "--kappa1=0.7308324141810887" in cmd
            cmd = cmd.replace("--kappa1=0.7308324141810887", "--kappa1=0.73")
        old = subprocess.run(["git", "show", f"HEAD:solver/proof/{stored}"], cwd=root, capture_output=True, text=True,
                             check=True).stdout.splitlines()
        r = subprocess.run(["bash", "-c", cmd], cwd=proof, env=env, capture_output=True, text=True)
        now = open(os.path.join(proof, stored)).read().splitlines()
        if kind == "append":
            new, ref = now[len(old):], old
        elif kind == "overwrite":
            new, ref = now, old[:-1] if old[-1].startswith("exit ") else old
        else:
            new, ref = r.stdout.splitlines(), old[len(old) // 2:]
        subprocess.run(["git", "checkout", "--", f"solver/proof/{stored}"], cwd=root, check=True)
        ok, worst, why = compare(new, ref)
        bad += not ok
        print(f"{name}: exit {r.returncode}; {len(new)} lines or records; "
              + (f"largest relative difference {worst:.1e}" if worst is not None else "") + (f"; {why}" if why else "")
              + f": {'REPRODUCED' if ok else 'DIFFERS'}\n    $ {cmd}", flush=True)
    print(f"CHECK 895{' (mutation ' + mut + ')' if mut else ''}: {'PASS' if not bad else 'FAIL'}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
