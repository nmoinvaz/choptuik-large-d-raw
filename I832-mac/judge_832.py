#!/usr/bin/env python3
"""#832's criteria R1 and E1 from reduced_cubic.py curve --weak_delta=1 --g0_only=1's JSON. R1: g(0)'s chord converged
from w0 and from w0 (1 + 1e-5) (curve's g0_ok, |dw| < 1e-40 |w0|); |g(0) - U^T F(z0)| of |B a| reported. E1 (with
--elim=1): the largest max|F| on the eliminated rows over every projected point below 1e-20 |B a|; a run without the
elimination has no E1 (reported as such).
usage: python3 judge_832.py CURVE.json [--selftest]    exit 0 when R1 and E1 (if any) pass; --selftest plants three
records (passing, failing R1, failing E1) and must give pass, fail, fail."""
import json
import sys


def judge(rec):
    cv, st = rec.get("curve", {}), rec.get("elim_stats")
    Ba = cv.get("Ba")
    r1 = bool(cv.get("g0_ok"))
    e1 = None if st is None else bool(Ba is not None and st.get("hrows") is not None and st["hrows"] < 1e-20 * Ba)
    return dict(R1=r1, E1=e1, Ba=Ba, hrows=None if st is None else st.get("hrows"), g0_dw=cv.get("g0_dw"),
                g0_UF0=cv.get("g0_UF0"), k=len(cv.get("g0", [])))


def ok(j):
    return j["R1"] and j["E1"] is not False


def main(argv):
    if "--selftest" in argv:
        good = dict(curve=dict(g0_ok=True, Ba=1e-35, g0=[0] * 5), elim_stats=dict(hrows=1e-90))
        bad1 = dict(curve=dict(g0_ok=False, Ba=1e-35, g0=[0] * 5), elim_stats=dict(hrows=1e-90))
        bad2 = dict(curve=dict(g0_ok=True, Ba=1e-35, g0=[0] * 5), elim_stats=dict(hrows=1e-50))
        got = [ok(judge(r)) for r in (good, bad1, bad2)]
        res = got == [True, False, False]
        print(f"judge_832 selftest: {got} (want [True, False, False]): {'PASS' if res else 'FAIL'}")
        return 0 if res else 1
    j = judge(json.load(open(argv[0])))
    print(f"  R1: {'pass' if j['R1'] else 'FAIL'}; E1: " + ("none (horizon data free)" if j["E1"] is None else
                                                          ("pass" if j["E1"] else "FAIL")))
    print(f"  g has {j['k']} components; |B a| {j['Ba']}; max|F| on the eliminated rows {j['hrows']} (bound 1e-20 "
          f"|B a|); g(0)'s |dw| per step {j['g0_dw']}; |g(0) - U^T F(z0)| / |B a| {j['g0_UF0']}")
    return 0 if ok(j) else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
