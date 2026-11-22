#!/usr/bin/env python3
"""foldsig.py [JSONL] | --selftest [--break]: the signature of the D 18.75 fold-watch firing of #1025 kc71_leap (the coordinator's ruling (b), 2026-11-22), tested on the last record r of the leap's record file with
its predecessor p and p's predecessor: SAME SIGNATURE when (1) n_null fell by exactly one (p.n_null - r.n_null == 1), (2) the smallest regular singular value of r is within 2 times the cutoff 1e-12 sigma_max
of r (sv_reg_small[0] <= 2e-12 sigma_max) and (3) dDelta/dD of the last step is within 1% of the step before. Exit 0 on SAME SIGNATURE, 1 otherwise. --selftest runs planted records (the real D 18.5625 to 18.75
numbers and variants that each break one condition); --break skips condition (1) and the selftest must then exit 1."""
import json, sys

BREAK = "--break" in sys.argv


def verdict(pp, p, r):
    c1 = True if BREAK else (p["n_null"] - r["n_null"] == 1)
    cut = 1e-12 * r["sv_J_max"]
    c2 = r["sv_reg_small"][0] <= 2 * cut
    sl_r = (r["Delta"] - p["Delta"]) / (r["D"] - p["D"])
    sl_p = (p["Delta"] - pp["Delta"]) / (p["D"] - pp["D"])
    c3 = abs(sl_r / sl_p - 1) <= 0.01
    info = "n_null %d -> %d: %s; sv_reg_small[0] %.3e vs cutoff %.3e (ratio %.2f, bar 2): %s; dDelta/dD %.5f vs %.5f (ratio %.4f, bar 1%%): %s" % (
        p["n_null"], r["n_null"], c1, r["sv_reg_small"][0], cut, r["sv_reg_small"][0] / cut, c2, sl_r, sl_p, sl_r / sl_p, c3)
    return c1 and c2 and c3, info


def selftest():
    real = [json.loads(x) for x in open(sys.argv[0].replace("foldsig.py", "") + "selftest_records.jsonl")]
    pp, p, r = real[-3], real[-2], real[-1]
    cases = [("the real D 18.75 firing", pp, p, r, True),
             ("n_null unchanged", pp, p, dict(r, n_null=p["n_null"]), False),
             ("n_null down by two", pp, p, dict(r, n_null=p["n_null"] - 2), False),
             ("the new regular value 5e-11 (4.5 times the cutoff)", pp, p, dict(r, sv_reg_small=[5e-11] + r["sv_reg_small"][1:]), False),
             ("Delta's slope 3% off", pp, p, dict(r, Delta=p["Delta"] + 1.03 * (p["Delta"] - pp["Delta"]) / (p["D"] - pp["D"]) * (r["D"] - p["D"])), False),
             ("Delta's slope 0.5% off", pp, p, dict(r, Delta=p["Delta"] + 1.005 * (p["Delta"] - pp["Delta"]) / (p["D"] - pp["D"]) * (r["D"] - p["D"])), True)]
    ok = True
    for name, a, b, c, want in cases:
        got, _ = verdict(a, b, c)
        print("planted: %s: %s, expected %s: %s" % (name, got, want, "PASS" if got == want else "FAIL"))
        ok = ok and got == want
    print("selftest: %s" % ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    f = next((a for a in sys.argv[1:] if not a.startswith("--")), "D:/choptuik-i1025k71/solver/matter/data/l1kc71Lw1025.jsonl")
    rs = [json.loads(x) for x in open(f) if x.strip()]
    ok, info = verdict(rs[-3], rs[-2], rs[-1])
    print("D %g: %s" % (rs[-1]["D"], info))
    print("SAME SIGNATURE" if ok else "NOT THE SAME SIGNATURE")
    sys.exit(0 if ok else 1)
