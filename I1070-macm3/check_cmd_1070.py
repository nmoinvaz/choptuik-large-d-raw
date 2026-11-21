#!/usr/bin/env python3
"""#1070 macm3b: the run command against the issue's, token by token. Usage: check_cmd_1070.py M128 | M160 LAM0 | --selftest
Allowed differences: the interpreter (the venv python), the two <raw> prefixes (output folder I1070-macm3, input I927-mac/inputs),
and for M160 one added --lam0=L. Everything else must be the issue's token. Exit 0 pass, 1 fail."""
import os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ISSUE = {"M128": "python3 -u hp/lowD_gamma.py <raw>/I1070-macm3/lowD_gamma_D3.15_M128.jsonl <raw>/I927-mac/inputs/lowDhm_x0.000625-0.9_D3.1500_M128.npz --threads=6 --polish=2 --xtol=1e-11",
         "M160": "python3 -u hp/lowD_gamma.py <raw>/I1070-macm3/lowD_gamma_D3.15_M160.jsonl <raw>/I927-mac/inputs/lowDhm_x0.000625-0.9_D3.1500_M160.npz --threads=6 --polish=2 --xtol=1e-11 --lam0=L128"}
def check(mode, cmd):
    a = ISSUE[mode].split(); b = cmd.split(); bad = []
    if mode == "M160": a = a[:-1]                       # the issue's --lam0 value is the pilot's result: any float is allowed
    lam = [t for t in b if t.startswith("--lam0=")]
    if mode == "M128" and lam: bad.append("--lam0 given for M128")
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
def dry(mode, lam=None):
    return subprocess.run([f"{HERE}/run_1070.sh", mode] + ([lam] if lam else []), env={**os.environ, "DRY": "1"}, capture_output=True, text=True).stdout.strip()
if sys.argv[1] == "--selftest":
    good128 = dry("M128"); good160 = dry("M160", "3.1")
    cases = [("M128", good128, True), ("M160", good160, True),
             ("M128", good128.replace("--threads=6", "--threads=8"), False), ("M128", good128.replace("--polish=2", "--polish=1"), False),
             ("M128", good128.replace("--xtol=1e-11", "--xtol=1e-10"), False), ("M128", good128 + " --lam0=3.1", False),
             ("M128", good128.replace("M128.npz", "M160.npz"), False), ("M160", good160.replace("--lam0=3.1", ""), False),
             ("M160", good160.replace("--lam0=3.1", "--lam0=abc"), False), ("M160", good160.replace("python -u", "python3 -u"), False),
             ("M128", good128.replace(" -u ", " "), False)]
    ok = True
    for i, (m, c, want) in enumerate(cases):
        got = not check(m, c)
        print(f"case {i} {m}: expect {'pass' if want else 'fail'}, got {'pass' if got else 'fail'}"); ok &= (got == want)
    print("selftest", "ok" if ok else "FAILED"); sys.exit(0 if ok else 1)
mode = sys.argv[1]; lam = sys.argv[2] if len(sys.argv) > 2 else None
bad = check(mode, dry(mode, lam))
print("check_cmd_1070:", "pass" if not bad else "FAIL " + "; ".join(bad)); sys.exit(0 if not bad else 1)
