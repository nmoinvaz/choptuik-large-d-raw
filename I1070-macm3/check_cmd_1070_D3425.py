#!/usr/bin/env python3
"""#1070 macm3b: the D 3.425 run's command against the issue's pilot command, token by token.
Usage: check_cmd_1070_D3425.py M96|M128 LAM0 | --selftest. Allowed differences: the interpreter (the venv python), the output name
(lowD_gamma_D3.425_<MODE>.jsonl in I1070-macm3), the state (T39-win/hp/data/lowD_states/lowDvh41_D3.4250_<MODE>.npz) and the added
--lam0=LAM0 (the order). Everything else must be the issue's token. Exit 0 pass, 1 fail."""
import os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
TAG = os.environ.get("TAG", "")
ISSUE = "python3 -u hp/lowD_gamma.py <raw>/I1070-macm3/lowD_gamma_D3.15_M128.jsonl <raw>/I927-mac/inputs/lowDhm_x0.000625-0.9_D3.1500_M128.npz --threads=6 --polish=2 --xtol=1e-11"
def check(mode, cmd, lam):
    a = ISSUE.split(); b = cmd.split(); bad = []
    l = [t for t in b if t.startswith("--lam0=")]
    if l != [f"--lam0={lam}"]: bad.append(f"needs exactly --lam0={lam}, has {l}")
    b = [t for t in b if not t.startswith("--lam0=")]
    if len(a) != len(b): return bad + [f"token count {len(b)} vs {len(a)}"]
    if not b[0].endswith("/venv-macm3-1058b/bin/python"): bad.append("interpreter is not venv-macm3-1058b")
    for i, (x, y) in enumerate(zip(a, b)):
        if i == 0: continue
        if i == 3 and not y.endswith(f"/I1070-macm3/lowD_gamma_D3.425_{mode}{TAG}.jsonl"): bad.append(f"output {y}")
        elif i == 4 and not y.endswith(f"/T39-win/hp/data/lowD_states/lowDvh41_D3.4250_{mode}.npz"): bad.append(f"state {y}")
        elif i not in (3, 4) and x != y: bad.append(f"token {i}: {y} vs {x}")
    return bad
def dry(mode, lam): return subprocess.run([f"{HERE}/run_1070_D3425.sh", mode, lam], env={**os.environ, "DRY": "1"}, capture_output=True, text=True).stdout.strip()
if sys.argv[1] == "--selftest":
    g96 = dry("M96", "3.23409"); g128 = dry("M128", "3.1"); ok = True
    cases = [("M96", g96, "3.23409", True), ("M128", g128, "3.1", True), ("M96", g96, "3.2341", False),
             ("M96", g96.replace("--threads=6", "--threads=4"), "3.23409", False), ("M96", g96.replace("--polish=2", "--polish=1"), "3.23409", False),
             ("M96", g96.replace("--xtol=1e-11", "--xtol=1e-9"), "3.23409", False), ("M96", g96.replace("M96.npz", "M128.npz"), "3.23409", False),
             ("M96", g96.replace("D3.4250", "D3.3500"), "3.23409", False), ("M96", g96.replace("python -u", "python3 -u"), "3.23409", False),
             ("M96", g96.replace(" -u ", " "), "3.23409", False), ("M128", g128.replace("D3.425_M128", "D3.425_M96"), "3.1", False),
             ("M96", g96.replace(" --lam0=3.23409", ""), "3.23409", False), ("M96", g96 + " --lam0=3.23409", "3.23409", False)]
    for i, (m, c, lam, exp) in enumerate(cases):
        got = not check(m, c, lam); print(f"case {i} {m}: expect {'pass' if exp else 'fail'}, got {'pass' if got else 'fail'}"); ok &= (got == exp)
    print("selftest", "ok" if ok else "FAILED", f"({len(cases)} cases, {sum(1 for x in cases if not x[3])} broken)"); sys.exit(0 if ok else 1)
mode, lam = sys.argv[1], sys.argv[2]
bad = check(mode, dry(mode, lam), lam)
print("check_cmd_1070_D3425:", "pass" if not bad else "FAIL " + "; ".join(bad)); sys.exit(0 if not bad else 1)
