#!/usr/bin/env python3
"""delta_rows.py REC [REC ...] : one row per record point that carries delta_reg (ell_leap.py blob 5816d7b3 on: |Delta component| of the four smallest regular modes, #1085's period-mode label; t5, 24 Nov 20:3x UTC:
"keep delta_reg in every tracker row"). The pinned mode_tracker.py (807c2d95) does not print it, so this companion table is made from the records themselves.
Columns: D, h, n_null, then for the four smallest regular modes (smallest first, the order of sv_reg_small): sigma, delta_reg, cos_t_reg.
usage: delta_rows.py REC...            markdown table on stdout (n_null changes shown, rows with psi-constraint above 1e-2 flagged reduced quality)
       delta_rows.py --selftest [--mutate=swap|flag]   planted records; the mutations pair delta_reg with the wrong mode, or drop the quality flag, and must fail"""
import json, sys
MUT = next((a.split("=", 1)[1] for a in sys.argv if a.startswith("--mutate=")), None)

def rows(recs):
    out = []
    for r in recs:
        if "delta_reg" not in r:
            continue
        d = list(reversed(r["delta_reg"])) if MUT == "swap" else r["delta_reg"]
        out.append((r["D"], r["h"], r["n_null"], [(s, x, c) for s, x, c in zip(r["sv_reg_small"], d, r["cos_t_reg"])], r["constraint"]))
    return out

def flag(c):
    """t5, 25 Nov: every row with psi-constraint above 1e-2 is reduced quality (part c2 runs with --cmax 2e-2)"""
    return "" if (MUT == "flag" or c <= 1e-2) else " **REDUCED QUALITY (constraint above 1e-2)**"

def table(rs):
    L = ["| D | h | n_null | mode 1: sigma, delta_reg, cos | mode 2 | mode 3 | mode 4 | psi-constraint |", "|---|---|---|---|---|---|---|---|"]
    prev = None
    for D, h, nn, ms, c in rs:
        ch = "" if prev is None or prev == nn else " (was %d)" % prev
        prev = nn
        L.append("| %r | %g | %d%s | %s | %.3e%s |" % (D, h, nn, ch, " | ".join("%.3e, %.4f, %.4f" % m for m in ms), c, flag(c)))
    return "\n".join(L)

def selftest():
    rec = {"D": 22.0, "h": 0.03125, "n_null": 79, "sv_reg_small": [2.0e-11, 5.0e-11, 7.0e-11, 3.0e-10], "cos_t_reg": [0.01, 0.02, 0.03, 0.04], "delta_reg": [0.1, 0.2, 0.3, 0.4], "constraint": 9.0e-3}
    rec2 = dict(rec, D=22.03125, n_null=80, constraint=1.2e-2)
    old = {"D": 21.0, "h": 0.0625, "n_null": 79, "sv_reg_small": [1.0] * 4, "cos_t_reg": [0.0] * 4, "constraint": 1e-3}
    rs = rows([old, rec, rec2])
    t = table(rs).splitlines()
    ok = len(rs) == 2 and rs[0][3][0] == (2.0e-11, 0.1, 0.01) and rs[0][3][3] == (3.0e-10, 0.4, 0.04) and "0.1000" in t[2].split("|")[4]
    ok = ok and "REDUCED QUALITY" not in t[2] and "REDUCED QUALITY" in t[3] and "(was 79)" in t[3] and "(was" not in t[2]     # the row above 1e-2 is flagged, the one below is not; n_null 79 to 80 is shown
    print("selftest:", "PASS" if ok else "FAIL")
    return 0 if ok else 1

if __name__ == "__main__":
    if sys.argv[1] == "--selftest":
        sys.exit(selftest())
    recs = []
    for p in [a for a in sys.argv[1:] if not a.startswith("--")]:
        recs += [json.loads(l) for l in open(p) if l.strip()]
    print(table(rows(recs)))
