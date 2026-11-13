#!/usr/bin/env python3
"""#727: copies of A1 and X2 (D 99.875) with cont3's segment plan in their meta, beside the originals, which are not touched.
usage: python make_states_727.py [--selftest]       (venv-t151 python, from this folder; writes states/A1_on_cont3plan.npz, states/X2_on_cont3plan.npz, states/edit_log.txt)
Only meta["segs"] is replaced (meta is a JSON string, as hpkernel.save_q writes it); zh, zl, z2, z3 are copied bit for bit and every other meta key stays.
The check after each write: the arrays equal the original's bit for bit, the changed meta keys are exactly {segs}, and the new segs equal cont3's.
--selftest: the check is run on planted copies (one array entry changed; a second meta key changed besides segs) and must flag both."""
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.dirname(HERE)
CONT3 = "I682-win/cont3/anm_pin13_D99.8750.npz"
SRC = {"A1": "I710-win/A1/anm_pin13_D99.8750.npz", "X2": "I725-win/X2/anm_pin13_D99.8750.npz"}
KEYS = ("zh", "zl", "z2", "z3")


def load(path):
    d = np.load(path, allow_pickle=False)
    return {k: np.array(d[k]) for k in KEYS}, json.loads(str(d["meta"]))


def check(orig, new, plan):
    """(problems, changed meta keys): problems is empty when the arrays are bit-identical, only segs changed, and segs equal the plan"""
    (oa, om), (na, nm) = orig, new
    bad = []
    for k in KEYS:
        if oa[k].dtype != na[k].dtype or oa[k].shape != na[k].shape or oa[k].tobytes() != na[k].tobytes():
            bad.append(f"array {k} differs")
    changed = sorted(k for k in set(om) | set(nm) if om.get(k) != nm.get(k))
    if changed != ["segs"]:
        bad.append(f"changed meta keys {changed}, expected ['segs']")
    if nm.get("segs") != plan:
        bad.append("segs are not cont3's")
    return bad, changed


def selftest():
    arrs, meta = load(os.path.join(RAW, SRC["A1"]))
    plan = load(os.path.join(RAW, CONT3))[1]["segs"]
    good = (dict(arrs), dict(meta, segs=plan))
    bad0, _ = check((arrs, meta), good, plan)
    print(f"  untouched copy with cont3's plan: problems {bad0} {'ok' if not bad0 else 'WRONG'}")
    a2 = dict(arrs)
    a2["zh"] = arrs["zh"].copy()
    a2["zh"][5] = np.nextafter(a2["zh"][5], np.inf)
    b1, _ = check((arrs, meta), (a2, dict(meta, segs=plan)), plan)
    print(f"  planted one-ulp change in zh[5]: problems {b1} {'ok' if b1 else 'WRONG'}")
    b2, _ = check((arrs, meta), (dict(arrs), dict(meta, segs=plan, a=0.5)), plan)
    print(f"  planted second changed meta key: problems {b2} {'ok' if b2 else 'WRONG'}")
    b3, _ = check((arrs, meta), (dict(arrs), dict(meta)), plan)
    print(f"  planted copy that kept its own plan: problems {b3} {'ok' if b3 else 'WRONG'}")
    n = (not bad0) + bool(b1) + bool(b2) + bool(b3)
    print("selftest", "passed" if n == 4 else "FAILED")
    return 0 if n == 4 else 1


def main():
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    os.makedirs(os.path.join(HERE, "states"), exist_ok=True)
    plan = load(os.path.join(RAW, CONT3))[1]["segs"]
    log = []
    for name, rel in SRC.items():
        orig = load(os.path.join(RAW, rel))
        meta = dict(orig[1], segs=plan)
        out = os.path.join(HERE, "states", f"{name}_on_cont3plan.npz")
        np.savez(out, zh=orig[0]["zh"], zl=orig[0]["zl"], z2=orig[0]["z2"], z3=orig[0]["z3"], meta=json.dumps(meta))
        new = load(out)
        bad, changed = check(orig, new, plan)
        line = f"{name}: {rel} -> states/{name}_on_cont3plan.npz; changed meta keys {changed}; arrays zh zl z2 z3 bit-identical: {not any('array' in b for b in bad)}; problems {bad}"
        print(line)
        log.append(line)
        if bad:
            sys.exit(1)
    open(os.path.join(HERE, "states", "edit_log.txt"), "w").write("\n".join(log) + "\n")


if __name__ == "__main__":
    main()
