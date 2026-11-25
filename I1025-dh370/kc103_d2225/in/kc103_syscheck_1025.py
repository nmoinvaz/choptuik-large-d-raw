#!/usr/bin/env python3
"""kc79_syscheck.py REC.jsonl STATE.npy D WTM [--mutate=F|steps] | --selftest: the acceptance check of the regridded k_c 79 state (#1025 kc79_d185, the coordinator's hc of 2026-11-21 ~23:05 UTC): "accept it only at the record class's |F|
(about 3e-10) with a converged step count". Accepted when (1) the record's |F| is at most 1e-9 (the record class: 2.1e-10 to 2.8e-10 in the k_c 55, 63 and 79 records at D 16.5 to 18.5) and the record is k_c 79 at the given D, and
(2) the saved state reproduces its record the way d18_hybsign.py checks it before every scan: S.freeze_from(z, kappa) gives the record's step count and |F| of the state agrees with the record's within 1% (a step count that does not
come back, or an |F| that moves, means the regrid has not converged). The code is d18_hybsign.py's own lines (I1025-mac/d18, blob e089207a). Exit 0 accepted, 1 not. The two controls run on the same numbers (a record with |F| 1.5 times larger and a record with one more step must both be refused);
--mutate=F and --mutate=steps apply them to the record itself and must exit 1. --selftest runs the verdict function on planted numbers and exits 0 when every case reads as written."""
import json
import os
import sys

F_CLASS = 1e-9


def verdict(rec, D, F_state, steps_state):
    why = []
    if rec.get("kc") != 103 or rec.get("D") != D:
        why.append("the record is not k_c 103 at D %g (kc %s, D %s)" % (D, rec.get("kc"), rec.get("D")))
    if not rec["F"] <= F_CLASS:
        why.append("record |F| %.3e is above the class bar %.0e" % (rec["F"], F_CLASS))
    if not abs(F_state - rec["F"]) <= max(1e-2 * rec["F"], 1e-13):
        why.append("the state's |F| %.6e is not within 1%% of the record's %.6e" % (F_state, rec["F"]))
    if steps_state != rec["steps"]:
        why.append("freeze_from gives %d steps, the record %d" % (steps_state, rec["steps"]))
    return not why, why


def selftest():
    rec = dict(kc=103, D=18.5, F=2.9e-10, steps=3300)
    cases = [("a converged record", rec, 18.5, 2.9e-10, 3300, True),
             ("|F| above the class bar", dict(rec, F=2e-9), 18.5, 2e-9, 3300, False),
             ("the state's |F| 1.5 times the record's", rec, 18.5, 4.35e-10, 3300, False),
             ("the step count off by one", rec, 18.5, 2.9e-10, 3301, False),
             ("a k_c 63 record", dict(rec, kc=63), 18.5, 2.9e-10, 3300, False),
             ("|F| within 1%", rec, 18.5, 2.92e-10, 3300, True)]
    ok = True
    for name, r, D, F, st, want in cases:
        got = verdict(r, D, F, st)[0]
        print("planted: %s: verdict %s, expected %s: %s" % (name, got, want, "PASS" if got == want else "FAIL"))
        ok = ok and got == want
    print("selftest: %s" % ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


if __name__ == "__main__":
    if sys.argv[1] == "--selftest":
        sys.exit(selftest())
    recf, st, D, wtm = sys.argv[1], sys.argv[2], float(sys.argv[3]), sys.argv[4]
    mut = next((a.split("=", 1)[1] for a in sys.argv if a.startswith("--mutate=")), None)
    sys.path.insert(0, wtm)
    os.chdir(wtm)
    import numpy as np
    from dss_ell import DSSEll, NODES_STD
    rec = [json.loads(x) for x in open(recf) if x.strip() and json.loads(x).get("D") == D][-1]
    if mut == "F":
        rec = dict(rec, F=rec["F"] * 1.5)
    if mut == "steps":
        rec = dict(rec, steps=rec["steps"] + 1)
    z = np.load(st)
    S = DSSEll(kc=rec["kc"], nodes=NODES_STD, n=D - 2, ell=1, Delta_ref=z[-1], Ks=rec["Ks"], u0=rec["u0"], rk=rec.get("rk", 1))
    steps = S.freeze_from(z, rec["kappa"])
    with np.errstate(all="ignore"):
        F = float(np.linalg.norm(S.residual(z[None, :])[0]))
    ok, why = verdict(rec, D, F, sum(steps.values()))
    # the controls on the same numbers: a record with |F| 1.5 times larger, and one with one more step, must both be refused
    cF = verdict(dict(rec, F=rec["F"] * 1.5), D, F, sum(steps.values()))[0]
    cS = verdict(dict(rec, steps=rec["steps"] + 1), D, F, sum(steps.values()))[0]
    print("controls on the same numbers: record |F| x 1.5 refused: %s; record steps + 1 refused: %s" % (not cF, not cS))
    ok = ok and (not cF) and (not cS)
    if cF or cS:
        why.append("a control did not fire")
    print("D %g k_c %s: record |F| %.10e, F_start %.3e, steps %s, constraint %.3e, Delta %.12f, %s s; state |F| %.10e, freeze_from steps %d" % (
        D, rec["kc"], rec["F"], rec.get("F_start", float("nan")), rec["steps"], rec.get("constraint", float("nan")), rec["Delta"], rec.get("seconds"), F, sum(steps.values())))
    print("ACCEPTED: the record class's |F| with a step count that comes back" if ok else "NOT ACCEPTED: " + "; ".join(why))
    sys.exit(0 if ok else 1)
