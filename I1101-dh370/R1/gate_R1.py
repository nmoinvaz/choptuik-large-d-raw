"""#1101 R1 bar 1: the last record of RECORD must be D 23.0, k_c 127, kappa 0.5 with |F| <= 5e-10 and steps in 5734-5968 (5851 +- 2%). usage: gate_R1.py RECORD [--mutate=f|steps]
exit 0 only if all hold. Controls (each must exit 1): the k_c 127 kappa 0.7 records of I1101-dh370/inputs (A, B) and --mutate=f / --mutate=steps on a record forced to violate that clause."""
import json, sys
f = [a for a in sys.argv[1:] if not a.startswith("--")][0]
m = next((a.split("=", 1)[1] for a in sys.argv if a.startswith("--mutate=")), "")
r = [json.loads(l) for l in open(f) if l.strip()][-1]
if m == "f": r["F"] = 6e-10
if m == "steps": r["steps"] = 5733
c = dict(D=r["D"] == 23.0, kc=r["kc"] == 127, kappa=r["kappa"] == 0.5, F=r["F"] <= 5e-10, steps=5734 <= r["steps"] <= 5968)
print(f"|F| {r['F']:.6e}, steps {r['steps']}, Delta {r['Delta']!r}, kappa {r['kappa']}, kc {r['kc']}, D {r['D']}: " + " ".join(f"{k}={'ok' if v else 'FAIL'}" for k, v in c.items()))
sys.exit(0 if all(c.values()) else 1)
