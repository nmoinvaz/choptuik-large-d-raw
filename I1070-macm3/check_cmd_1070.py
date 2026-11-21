#!/usr/bin/env python3
"""#1070 macm3b: the run command against the issue's, token by token. Usage: check_cmd_1070.py M128 | M160 LAM0 | --selftest
Allowed differences: the interpreter (the venv python), the two <raw> prefixes (output folder I1070-macm3, input I927-mac/inputs),
the TAG env appended to the output name (a rerun), one added --lam0=L (M160: any number; M128: only the LAM0 given on the command line).
Everything else must be the issue's token. Exit 0 pass, 1 fail."""
import os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
TAG = os.environ.get("TAG", "")
ISSUE = {"M128": f"python3 -u hp/lowD_gamma.py <raw>/I1070-macm3/lowD_gamma_D3.15_M128{TAG}.jsonl <raw>/I927-mac/inputs/lowDhm_x0.000625-0.9_D3.1500_M128.npz --threads=6 --polish=2 --xtol=1e-11",
         "M160": f"python3 -u hp/lowD_gamma.py <raw>/I1070-macm3/lowD_gamma_D3.15_M160{TAG}.jsonl <raw>/I927-mac/inputs/lowDhm_x0.000625-0.9_D3.1500_M160.npz --threads=6 --polish=2 --xtol=1e-11 --lam0=L128"}
def check(mode, cmd, want=None):
    a = ISSUE[mode].split(); b = cmd.split(); bad = []
    if mode == "M160": a = a[:-1]                       # the issue's --lam0 value is the pilot's result: any float is allowed
    lam = [t for t in b if t.startswith("--lam0=")]
    if mode == "M128":
        if want is None and lam: bad.append("--lam0 given for M128")
        if want is not None and lam != [f"--lam0={want}"]: bad.append(f"M128 needs exactly --lam0={want}, has {lam}")
        b = [t for t in b if not t.startswith("--lam0=")]
    if mode == "M160":
        if len(lam) != 1: bad.append("M160 needs exactly one --lam0")
        else:
            try: float(lam[0][7:])
            except ValueError: bad.append("--lam0 is not a number")
        b = [t for t in b if not t.startswith("--lam0=")]
    if len(a) != len(b): return bad + [f"token count {len(b)} vs {len(a)}"]
    if not b[0].endswith("/venv-macm3-1058b/bin/python"): bad.append("interpreter is not venv-macm3-1058b")
    for i, (x, y) in enumerate(zip(a, b)):
        if i == 0: continue
        if x.startswith("<raw>/"):
            if not y.endswith("/" + x[len("<raw>/"):]): bad.append(f"token {i}: {y} vs {x}")
        elif x != y: bad.append(f"token {i}: {y} vs {x}")
    return bad
def dry(mode, lam=None):  # TAG comes from the environment
    return subprocess.run([f"{HERE}/run_1070.sh", mode] + ([lam] if lam else []), env={**os.environ, "DRY": "1"}, capture_output=True, text=True).stdout.strip()
if sys.argv[1] == "--selftest":
    good128 = dry("M128"); good160 = dry("M160", "3.1"); good128l = dry("M128", "4.3977")
    cases = [("M128", good128, None, True), ("M160", good160, None, True), ("M128", good128l, "4.3977", True),
             ("M128", good128.replace("--threads=6", "--threads=8"), None, False), ("M128", good128.replace("--polish=2", "--polish=1"), None, False),
             ("M128", good128.replace("--xtol=1e-11", "--xtol=1e-10"), None, False), ("M128", good128 + " --lam0=3.1", None, False),
             ("M128", good128.replace("M128.npz", "M160.npz"), None, False), ("M160", good160.replace("--lam0=3.1", ""), None, False),
             ("M160", good160.replace("--lam0=3.1", "--lam0=abc"), None, False), ("M160", good160.replace("python -u", "python3 -u"), None, False),
             ("M128", good128.replace(" -u ", " "), None, False), ("M128", good128l.replace("4.3977", "4.3997"), "4.3977", False),
             ("M128", good128, "4.3977", False), ("M128", good128l.replace("--polish=2", "--polish=3"), "4.3977", False)]
    ok = True
    for i, (m, c, want, exp) in enumerate(cases):
        got = not check(m, c, want)
        print(f"case {i} {m}: expect {'pass' if exp else 'fail'}, got {'pass' if got else 'fail'}"); ok &= (got == exp)
    print("selftest", "ok" if ok else "FAILED", f"({len(cases)} cases, {sum(1 for x in cases if not x[3])} broken)"); sys.exit(0 if ok else 1)
mode = sys.argv[1]; lam = sys.argv[2] if len(sys.argv) > 2 else None
bad = check(mode, dry(mode, lam), lam if mode == "M128" else None)
print("check_cmd_1070:", "pass" if not bad else "FAIL " + "; ".join(bad)); sys.exit(0 if not bad else 1)
