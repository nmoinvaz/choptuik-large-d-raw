"""Issue #164, the time-resolution control: two rt_run.py jsonl files (48x95 and 32x95, both from start a at
D 60.001952). It takes A's last record and B's last record at the same D, and compares their Delta in arb from the
30-digit Delta_str against the criterion of README.md (|difference| < 1e-13). Exits 1 when that fails or either record
is not converged.

    python3 nt_check.py A.jsonl B.jsonl [--tol 1e-13]
"""
import sys
import json
import flint

flint.ctx.prec = 192
tol = float(sys.argv[sys.argv.index("--tol") + 1]) if "--tol" in sys.argv else 1e-13
ra = [json.loads(line) for line in open(sys.argv[1])][-1]
rb = [x for x in (json.loads(line) for line in open(sys.argv[2])) if abs(x["D"] - ra["D"]) < 1e-9][-1]   # same D
r = [ra, rb]
d = float((flint.arb(r[0]["Delta_str"]) - flint.arb(r[1]["Delta_str"])).mid())
ok = r[0]["ok"] and r[1]["ok"] and abs(d) < tol
for x in r:
    print(f"{x['grid'][0]}x{x['grid'][1]} D {x['D']}: Delta {x['Delta_str']}, - hp {x['diff']:+.3e}, ok {x['ok']}")
print(f"difference {d:+.3e}, criterion |.| < {tol:g}: {'ok' if ok else 'FAIL'}")
sys.exit(0 if ok else 1)
