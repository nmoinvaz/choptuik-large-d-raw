#!/usr/bin/env python3
"""#1109 stages 1c and 1d: per state the weak band, U_w^T F, |F|, the full Gauss-Newton dDelta (valley's line), seconds, and the
composition of each weak vector (rep json: right = field, node, tau-harmonic band, Delta's share; left = blocks, fields).
usage (from I1109-mm5): table_d.py TAG=REPJSON:VALLEYLOG:SECONDS ...   (SECONDS: the state's total or its jac+svd+report+valley s)"""
import json, re, sys

def top(dct, n):
    return ", ".join(f"{k} {v:.3g}" for k, v in sorted(dct.items(), key=lambda kv: -kv[1])[:n])

rows, comp, ctl = [], [], []
for a in sys.argv[1:]:
    tag, rep, val, sec = a.split(":", 3)
    r = json.load(open(rep))
    st = r["states"][0]
    vl = open(val).read()
    m = re.search(r"weak vectors below 1e-8: (\d+) \(s/s_max ([^)]*)\); Gauss-Newton step \|dz\| ([\d.e+-]+), dDelta ([+-][\d.e+-]+)", vl)
    nb, sbel, dz, dd = m.group(1), m.group(2), m.group(3), m.group(4)
    weak = r["weak"]
    below = [w for w in weak if w["s_rel"] < 1e-8]
    above = [w for w in weak if w["s_rel"] >= 1e-8]
    uw = {w["index_from_smallest"]: u for w, u in zip(weak, st["uwF"])}
    fmt = lambda ws: ", ".join(f"idx {w['index_from_smallest']} {w['s_rel']:.3e}" for w in ws) or "none in the weak band"
    rows.append((tag, r["kc"], r["kappa"], r["steps"], st["F"], fmt(below),
                 ", ".join(f"{uw[w['index_from_smallest']]:+.4e}" for w in below), fmt(above),
                 ", ".join(f"{uw[w['index_from_smallest']]:+.3e}" for w in above), st["F_weak"], dd, dz, sec))
    for rt, lf, w in zip(r["right"], r["left"], weak):
        i = w["index_from_smallest"]
        assert rt["index_from_smallest"] == i == lf["index_from_smallest"]
        flds = dict(rt["fields"])
        comp.append(f"| {tag} | {i} | {w['s_rel']:.3e} | {uw[i]:+.4e} | {top(flds, 3)}; Delta {rt['nodes'].get('Delta', 0):.3g} | "
                    f"{top({k: v for k, v in rt['nodes'].items() if k != 'Delta'}, 2)} | {' '.join(f'{v:.3g}' for v in rt['hbands'])} | "
                    f"{', '.join(f'{k} {v:.3g}' for k, v in rt['top_k'][:3])} | {top(lf['blocks'], 2)}; {top(lf['fields'], 2)}; "
                    f"k {', '.join(f'{k} {v:.3g}' for k, v in lf['top_k'][:2])} |")
    g, gc = r["g"], r["g_control"]
    ctl.append((tag, g["rel_mismatch"], gc["rel_mismatch"], [(x["h"], x["control"], x["inner_rel"]) for x in r["gauge"]]))
print("| state | k_c | kappa | steps | \\|F\\| | weak below 1e-8 (s/s_max) | U_w^T F on them | weak above 1e-8 | U_w^T F on them | \\|F\\| weak part | full GN dDelta | GN \\|dz\\| | s |")
print("|---|---|---|---|---|---|---|---|---|---|---|---|---|")
for x in rows:
    print(f"| {x[0]} | {x[1]} | {x[2]} | {x[3]} | {x[4]:.4e} | {x[5]} | {x[6]} | {x[7]} | {x[8]} | {x[9]:.3e} | **{x[10]}** | {x[11]} | {x[12]} |")
print()
print("Field names as the report prints them (the unknown's part: d, c0, the node fields p m c q, mS aS qS, Delta). Weak vector composition (right: field shares and Delta's share, the two largest nodes, tau-harmonic bands [k 0], [1-3], [4-7], [8-15], [16-31], [32-] (HBANDS of i1101_weakdir.py), the three largest harmonics; left: the two largest blocks, fields, harmonics):")
print()
print("| state | idx | s/s_max | U_w^T F | right: fields (three largest), Delta share | right: nodes | right: tau-harmonic bands | right: top harmonics | left: blocks; fields; harmonics |")
print("|---|---|---|---|---|---|---|---|---|")
print("\n".join(comp))
print()
print("Controls (the check passes when its value is small; a control must read >= 1e-3, else it did not fire):")
for tag, gv, gcv, gl in ctl:
    print(f"- {tag}: tau generator {gv:.3e}, tau control {gcv:.3e} ({'fired' if gcv >= 1e-3 else 'DID NOT FIRE'}); "
          + "; ".join(f"{h} {'control ' if c else ''}{v:.3e}" + (f" ({'fired' if v >= 1e-3 else 'DID NOT FIRE'})" if c else "") for h, c, v in gl))
