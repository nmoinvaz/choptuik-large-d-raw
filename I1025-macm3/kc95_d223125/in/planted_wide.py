#!/usr/bin/env python3
"""#1025 kc95_d22375 (dh610) planted_wide.py [--mutate]: planted truth for the WIDE reading through the real reader (read_lower.py, blob 89309d3c, with d185_scan_read.py, d18c_read.py): synthetic hybrid-sign rows on the
wide grid lambda -0.10 to 0.50 by 0.04 plus a repeat of 0.14, for det(lambda) = (lambda + 0.04)(lambda - 0.11)(lambda - 0.40) (roots at -0.04, 0.11, 0.40), all noise-robust, float64 sign equal. The reader must find exactly
three robust changes in the brackets (-0.06, -0.02), (0.10, 0.14) and (0.38, 0.42), each estimate inside its bracket, and the repeat must agree. --mutate flips the hybrid sign of the point 0.30: the reader must then find two
more changes ((0.26, 0.30) and (0.30, 0.34)) and this script reports the planted brackets as NOT matched (exit 1). usage (from this folder): python3 -I planted_wide.py [--mutate] [IN_DIR]"""
import json, math, os, subprocess, sys, tempfile

MUT = "--mutate" in sys.argv
IN = next((a for a in sys.argv[1:] if not a.startswith("--")), "in")
lams = [round(-0.10 + 0.04 * k, 2) for k in range(16)] + [0.14]
det = lambda l: (l + 0.04) * (l - 0.11) * (l - 0.40)
rows = []
for l in lams:
    d = det(l)
    s = 1.0 if d > 0 else -1.0
    if MUT and abs(l - 0.30) < 1e-9:
        s = -s
    rows.append(dict(D=22.375, kc=95, lam=l, sign=s, ln=math.log(abs(d)), noise=[s, s], noise_robust=True, f64_sign=s, f64_ln=math.log(abs(d)), state="planted", sec=1))
with tempfile.TemporaryDirectory() as t:
    with open(os.path.join(t, "scan_D22.375_p0.jsonl"), "w") as f:
        for r in rows:
            f.write(json.dumps(r) + "\n")
    env = dict(os.environ, D18_DIR=os.path.abspath(IN))
    out = subprocess.run([sys.executable, "-W", "ignore", os.path.join(IN, "read_lower.py"), t, "-0.10", "0.50"], capture_output=True, text=True, env=env).stdout
print(out)
import re
ch = [(float(a), float(b), float(x)) for a, b, x in re.findall(r"robust change \((-?[\d.]+), (-?[\d.]+)\), .*?det-linear (-?[\d.]+)", out)]
want = [(-0.06, -0.02), (0.10, 0.14), (0.38, 0.42)]
ok = [(a, b) for a, b, _ in ch] == want and all(a < x < b for a, b, x in ch) and "repeated points: [(0.14, 'agree')]" in out
print("planted wide reading:", "matches the planted brackets" if ok else "DOES NOT match the planted brackets", ch)
sys.exit(0 if ok else 1)
