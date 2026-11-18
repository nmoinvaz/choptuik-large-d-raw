"""#957: the tables of the closing comment from the JSONs of jet_by_order_check957.py.

    python3 summary957.py FOLDER [--mutate]

Reads FOLDER/jbo_tangent1.json (D 229.0509), jbo_tangent1_D232.json (D 232.0), jbo_tangent3.json (D 229.0509) and jbo_default2.json
and prints, per tangent run: seconds of the twice-formed series and of the moved one, their ratio, the orders <= F that differ,
max rho of each form against its bound (2^10 times the twice-formed series' max), the control's rho, and max|z_k - z'_k|/max|z_k|
per order. Verdict per run, recomputed here from the stored numbers: pass needs no low order differing, rho moved <= the bound, the
control's rho above the bound. --mutate multiplies the moved series' rho by 2^11 first, and every tangent run must then fail
(exit 1). Exit 1 if a run fails."""
import json
import os
import sys

folder = sys.argv[1]
mutate = "--mutate" in sys.argv
runs = [("jbo_tangent1", "tangent_from 1, D 229.0509"), ("jbo_tangent1_D232", "tangent_from 1, D 232.0"),
        ("jbo_tangent3", "tangent_from 3, D 229.0509")]
bad = 0
for name, label in runs:
    d = json.load(open(os.path.join(folder, name + ".json")))
    rt = [x * (2.0 ** 11 if mutate else 1.0) for x in d["rho_tangent"]]
    bound = 2.0 ** 10 * max(d["rho_twice"])
    ok = not d["differ_low"] and max(rt) <= bound and max(d["rho_control"]) > bound
    bad += not ok
    rel = d["rel"]
    print(f"{label}: twice {d['s_twice']:.1f} s, moved {d['s_tangent']:.1f} s, ratio {d['s_twice'] / d['s_tangent']:.3f} (file {d['ratio']}); "
          f"low orders differing {d['differ_low']}; rho twice {max(d['rho_twice']):.3e}, moved {max(rt):.3e}, bound {bound:.3e}; control {max(d['rho_control']):.3e}; "
          f"{'PASS' if ok else 'FAIL'}")
    F = d["tangent_from"]
    dev = max(abs(b / a - 1) for a, b in zip(d["rho_twice"][F:], d["rho_tangent"][F:]))
    print(f"   rho_k moved / twice - 1 over orders {F + 1}..{len(rel)}: max {dev:.2e} (rho_k from the leading parts, range {min(d['rho_twice']):.2e} to {max(d['rho_twice']):.2e})")
    print(f"   rel at orders 1..{F}: {[f'{x:.1e}' for x in rel[:F]]}; orders {F + 1}..{len(rel)}: min {min(rel[F:]):.2e}, max {max(rel[F:]):.2e} (order {rel.index(max(rel[F:])) + 1})")
p = os.path.join(folder, "jbo_default2.json")
if os.path.exists(p):
    d = json.load(open(p))
    print(f"default path (jets against by order), D 229.0509: jets {d['s_jets']:.1f} s, by order {d['s_by_order']:.1f} s, ratio {d['ratio']}; "
          f"orders differing {d['differ']}, with the planted change {d['differ_hook']}, controls {d['control_keep']} and {d['control_hook']}; "
          f"{'PASS' if d['passed'] and d['controls_fired'] else 'FAIL'}")
    bad += not (d["passed"] and d["controls_fired"])
print(f"summary: {'all pass' if not bad else str(bad) + ' failing'}{' (--mutate: every tangent run must fail)' if mutate else ''}")
sys.exit(1 if bad else 0)
