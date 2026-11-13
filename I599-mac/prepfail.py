#!/usr/bin/env python3
"""A failed preparation at hp's entry points (#599): with the horizon datum a_h's first point NaN, the horizon LUs of
the preparation have a non-finite pivot, and every entry point must raise that LU's error. The record of each call is
the exception's type and message and whether the call wrote a Rust panic to stderr. The control: the cheap entry
points at the unmodified states must return values.

    PYTHONPATH=<site> python3 prepfail.py dump HPDIR RAWDIR OUT.json
    python3 prepfail.py compare A.json B.json     # the type and message of every call; exit 1 on any difference

dump exits 1 when a call at the NaN state returns or a control call raises.
"""
import json
import os
import sys
import tempfile

import numpy as np


def call(f):
    """[outcome, message, panicked]: the exception's type name and message (or "returned"), and whether stderr got a
    panic message during the call"""
    sys.stderr.flush()
    fd = os.dup(2)
    tmp = tempfile.TemporaryFile()
    os.dup2(tmp.fileno(), 2)
    try:
        try:
            f()
            res = ["returned", ""]
        except BaseException as e:  # pyo3's PanicException derives from BaseException
            res = [type(e).__name__, str(e)]
    finally:
        os.dup2(fd, 2)
        os.close(fd)
    tmp.seek(0)
    err = tmp.read().decode(errors="replace")
    return res + ["panicked" in err]


def nan_ah(zh, m):
    """zh with a_h's first point NaN (z = [p1, c0, nodes, m_h, a_h, Delta])"""
    z = np.array(zh, dtype=float, copy=True)
    z[len(z) - 1 - m] = np.nan
    return z


def dump(hp, raw, out):
    import hpkernel
    from hpkernel.driver import load, make_solver
    sys.path.insert(0, hp)
    from octo_corrector import load_o
    rec = {"hpkernel": hpkernel.__file__, "states": {}}
    bad = []

    zh, zl, meta = load(os.path.join(hp, "data", "lowD_states", "lowDv_D3.7000_M48.npz"))
    zh, zl = np.array(zh, dtype=float), np.array(zl, dtype=float)
    s = make_solver(meta["D"], 48, nodes=meta["nodes"], kt=meta["kt"], kc=meta["kc"], ks=meta["ks"], threads=2)
    s.set_segs(meta["segs"] if meta.get("segs") else s.plan(zh, zl, 1e-30, 0.05))
    n = s.size
    vh, vl = np.linspace(-1, 1, n), np.zeros(n)
    yh = nan_ah(zh, 48)
    calls = {
        "residual": lambda z: s.residual(z, zl),
        "jacobian": lambda z: s.jacobian(z, zl),
        "jacobian_f64": lambda z: s.jacobian_f64(z, zl),
        "jacobian_f64/t1": lambda z: s.jacobian_f64(z, zl, tangents=1),
        "jacobian_f64/hdd4": lambda z: s.jacobian_f64(z, zl, horizon_dd=4),
        "jacobian_f64/hdd16": lambda z: s.jacobian_f64(z, zl, horizon_dd=16),
        "newton": lambda z: s.newton(z, zl),
        "newton_mixed": lambda z: s.newton_mixed(z, zl),
        "newton_mixed/dense": lambda z: s.newton_mixed(z, zl, block=False),
        "jvp": lambda z: s.jvp(z, zl, vh, vl, with_residual=True),
        "residual_jet": lambda z: s.residual_jet([z, z / 1000], [zl, zl / 1000], 3),
        "mode_matrix": lambda z: s.mode_matrix(z, zl, 1.7, 0.0),
        "mode_matrix/0": lambda z: s.mode_matrix(z, zl, 0.0, 0.0),
        "mode_det": lambda z: s.mode_det(z, zl, 1.7, 0.0),
    }
    r = {k: call(lambda f=f: f(yh)) for k, f in calls.items()}
    for k in ("residual", "jacobian_f64", "jvp", "mode_det"):
        r[f"control/{k}"] = call(lambda f=calls[k]: f(zh))
    rec["states"]["lowD3.7_M48"] = r

    st = "anm-mac/run_trend_pin3_qd3/anm_pin3_D79.7657.npz"
    z8, m = load_o(os.path.join(raw, st))
    z8 = [np.ascontiguousarray(np.array(p, dtype=float)) for p in z8]
    M = int(m["M"])
    D = m.get("D_str", repr(float(m["D"])))
    s = make_solver(D, M, nodes=list(m["nodes"]), kt=m.get("kt", 36), kc=m.get("kc", 146), ks=m.get("ks", 130),
                    threads=2, kfreeze=m.get("kfreeze", 3))
    s.set_segs(s.plan(z8[0], z8[1], 1e-32, 0.05))
    y8 = [nan_ah(z8[0], M)] + z8[1:]
    calls = {
        "residual": lambda z: s.residual(z[0], z[1]),
        "jacobian_f64/hdd4": lambda z: s.jacobian_f64(z[0], z[1], horizon_dd=4),
        "jacobian_f64/hdd12": lambda z: s.jacobian_f64(z[0], z[1], horizon_dd=12),
        "residual_q": lambda z: s.residual_q(*z[:4]),
        "jacobian_q": lambda z: s.jacobian_q(*z[:4]),
        "newton_q": lambda z: s.newton_q(*z[:4]),
        "residual_jet_q": lambda z: s.residual_jet_q([tuple(z[:4]), tuple(p / 1000 for p in z[:4])], 2),
        "residual_o": lambda z: s.residual_o(z),
        "jacobian_o": lambda z: s.jacobian_o(z),
        "newton_o": lambda z: s.newton_o(z),
        "residual_jet_o": lambda z: s.residual_jet_o([z, [p / 1000 for p in z]], 2),
    }
    r = {k: call(lambda f=f: f(y8)) for k, f in calls.items()}
    for k in ("residual", "jacobian_f64/hdd4", "residual_q", "residual_o"):
        r[f"control/{k}"] = call(lambda f=calls[k]: f(z8))
    rec["states"][st] = r

    for stn, r in rec["states"].items():
        for k, (outcome, msg, panicked) in r.items():
            ok = (outcome == "returned") == k.startswith("control/")
            print(f"{'ok ' if ok else 'BAD'}  {stn}  {k}: {outcome} {msg!r} panicked={panicked}")
            if not ok:
                bad.append(k)
    json.dump(rec, open(out, "w"), indent=1)
    print("wrote", out, "; bad:", bad)
    return 1 if bad else 0


def compare(a, b):
    A, B = json.load(open(a)), json.load(open(b))
    diff = 0
    n = 0
    for st in A["states"]:
        for k, v in A["states"][st].items():
            n += 1
            w = B["states"].get(st, {}).get(k)
            if w is None or v[:2] != w[:2]:
                diff += 1
                print(f"DIFFERS  {st}  {k}: {v[:2]} | {w if w is None else w[:2]}")
    print(f"{n - diff} of {n} outcomes and messages the same")
    return 1 if diff else 0


if __name__ == "__main__":
    if sys.argv[1] == "dump":
        sys.exit(dump(sys.argv[2], sys.argv[3], sys.argv[4]))
    sys.exit(compare(sys.argv[2], sys.argv[3]))
