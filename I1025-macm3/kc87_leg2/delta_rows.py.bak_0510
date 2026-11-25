#!/usr/bin/env python3
"""delta_rows.py REC [REC ...] : one row per record point that carries delta_reg (ell_leap.py blob 5816d7b3 on: |Delta component| of the four smallest regular modes, #1085's period-mode label; t5, 24 Nov 20:3x UTC:
"keep delta_reg in every tracker row"). The pinned mode_tracker.py (807c2d95) does not print it, so this companion table is made from the records themselves.
Columns: D, h, n_null, then for the four smallest regular modes (smallest first, the order of sv_reg_small): sigma, delta_reg, cos_t_reg.
usage: delta_rows.py REC...            markdown table on stdout
       delta_rows.py --selftest [--mutate=swap]   planted record; the mutation pairs delta_reg with the wrong mode and must fail"""
import json, sys
MUT = next((a.split("=", 1)[1] for a in sys.argv if a.startswith("--mutate=")), None)

def rows(recs):
    out = []
    for r in recs:
        if "delta_reg" not in r:
            continue
        d = list(reversed(r["delta_reg"])) if MUT == "swap" else r["delta_reg"]
        out.append((r["D"], r["h"], r["n_null"], [(s, x, c) for s, x, c in zip(r["sv_reg_small"], d, r["cos_t_reg"])]))
    return out

def table(rs):
    L = ["| D | h | n_null | mode 1: sigma, delta_reg, cos | mode 2 | mode 3 | mode 4 |", "|---|---|---|---|---|---|---|"]
    for D, h, nn, ms in rs:
        L.append("| %r | %g | %d | %s |" % (D, h, nn, " | ".join("%.3e, %.4f, %.4f" % m for m in ms)))
    return "\n".join(L)

def selftest():
    rec = {"D": 22.0, "h": 0.03125, "n_null": 79, "sv_reg_small": [2.0e-11, 5.0e-11, 7.0e-11, 3.0e-10], "cos_t_reg": [0.01, 0.02, 0.03, 0.04], "delta_reg": [0.1, 0.2, 0.3, 0.4]}
    old = {"D": 21.0, "h": 0.0625, "n_null": 79, "sv_reg_small": [1.0] * 4, "cos_t_reg": [0.0] * 4}
    rs = rows([old, rec])
    ok = len(rs) == 1 and rs[0][3][0] == (2.0e-11, 0.1, 0.01) and rs[0][3][3] == (3.0e-10, 0.4, 0.04) and "0.1000" in table(rs).splitlines()[2].split("|")[4]
    print("selftest:", "PASS" if ok else "FAIL")
    return 0 if ok else 1

if __name__ == "__main__":
    if sys.argv[1] == "--selftest":
        sys.exit(selftest())
    recs = []
    for p in [a for a in sys.argv[1:] if not a.startswith("--")]:
        recs += [json.loads(l) for l in open(p) if l.strip()]
    print(table(rows(recs)))
