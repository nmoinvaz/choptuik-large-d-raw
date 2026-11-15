#!/usr/bin/env python3
"""#828's criteria R1, E1 and E2 from reduced_cubic.py curve --elim=1's JSON (R2 is I823-mac/verdict_823.py's).
R1: g(0)'s chord converged from w0 and from w0 (1 + 1e-5) (curve's g0_ok, |dw| < 1e-40 |w0|); |g(0) - U^T F(P(z0))|
of |B a| reported. E1: the largest max|F| on the eliminated rows over every projected point below 1e-20 |B a|. E2: the
reduced Newton step's Delta part within 1e-3 of ElimO's +1.100878e-5 (#823's proj_shift).
usage: python3 judge_828.py CURVE.json [--selftest]    exit 0 when all three pass, 1 otherwise; --selftest plants
three records (one passing, one failing E1, one failing E2) and must give pass, fail, fail."""
import json
import sys

E2_REF, E2_TOL, E1_TOL = 1.100878e-5, 1e-3, 1e-20


def judge(rec):
    cv, el, st = rec.get("curve", {}), rec.get("elim", {}), rec.get("elim_stats", {})
    Ba = cv.get("Ba")
    r1 = bool(cv.get("g0_ok"))
    e1 = Ba is not None and st.get("hrows") is not None and st["hrows"] < E1_TOL * Ba
    d = el.get("dz0_last")
    e2 = d is not None and abs(d - E2_REF) / E2_REF < E2_TOL
    return dict(R1=r1, E1=bool(e1), E2=bool(e2), Ba=Ba, hrows=st.get("hrows"), dDelta=d, g0_dw=cv.get("g0_dw"),
                g0_UF0=cv.get("g0_UF0"))


def main(argv):
    if "--selftest" in argv:
        good = dict(curve=dict(g0_ok=True, Ba=1e-35), elim=dict(dz0_last=1.1009e-5), elim_stats=dict(hrows=1e-90))
        bad1 = dict(curve=dict(g0_ok=True, Ba=1e-35), elim=dict(dz0_last=1.1009e-5), elim_stats=dict(hrows=1e-50))
        bad2 = dict(curve=dict(g0_ok=True, Ba=1e-35), elim=dict(dz0_last=3.311e-8), elim_stats=dict(hrows=1e-90))
        got = [all(judge(r)[k] for k in ("R1", "E1", "E2")) for r in (good, bad1, bad2)]
        ok = got == [True, False, False]
        print(f"judge_828 selftest: {got} (want [True, False, False]): {'PASS' if ok else 'FAIL'}")
        return 0 if ok else 1
    j = judge(json.load(open(argv[0])))
    for k in ("R1", "E1", "E2"):
        print(f"  {k}: {'pass' if j[k] else 'FAIL'}")
    print(f"  |B a| {j['Ba']}, max|F| on the eliminated rows {j['hrows']} (bound {E1_TOL:g} |B a|), the reduced step's "
          f"Delta {j['dDelta']} (against {E2_REF:+.6e}, bound {E2_TOL:g} relative), g(0)'s |dw| per step {j['g0_dw']}, "
          f"|g(0) - U^T F(P(z0))| / |B a| {j['g0_UF0']}")
    return 0 if all(j[k] for k in ("R1", "E1", "E2")) else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
