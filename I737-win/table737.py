#!/usr/bin/env python3
"""#737: the horizon series' transient at M = 32 against M = 48 at D 80 and 100, from horizon_radius.py run's terms.

    python -I table737.py C32 C48 [--mutate=scale48]
    python -I table737.py --selftest

C32 and C48 are the --coef folders of the M = 32 states (T138-win2/chain/anm_pin3_D<D>.npz) and of #636's M = 48
solutions of them (m48_anm_pin3_D<D>.npz), quad-double terms b[k, field, lane] = c_k u0^k at delta 0 and 1e-28.
t_k = max over fields and lanes |b_k|. Registered before the runs (#737):
- S1, the transient at M = 32: k_peak = the order of the largest t_k at k >= max(10, k_lo), k_lo = round(Re s) from
  the run's record; the valley = the smallest t_k from order 10 to k_peak. The transient is present when
  t_peak / t_valley >= 10 and k_peak <= kmax - 10 (it rises and falls again inside the orders run).
- S2, the M = 48 base suffices: a_h scaled by 1 + 1e-28 moves the terms at the M = 48 peak order by less than 0.1
  t_peak (max over fields and lanes). The base's own a_h error is taken to lie below 1e-28 (its pinned quad-double
  max|F| is 1e-35 to 3e-34, #636).
- Verdict where S1 and S2 hold: r = t_peak(48) / t_peak(32), each at its own peak order. 1/2 <= r <= 2: the
  transient is the solution's; r > 10 or r < 1/10: the grid's; otherwise reported as it is.
Exit 0 when every D present gives a verdict, 1 when S1 or S2 fails at one, 2 when a file is missing.
--mutate=scale48 multiplies the M = 48 terms past k_lo by 20, so the verdict must become the grid's.
--selftest: planted terms (a background 0.3^k under a hump of height 1e-12 at order 60), with the M = 48 copy equal
(the solution's), with its hump times 20 (the grid's), and with no hump (S1 fails); each must read as planted.
"""
import glob
import json
import os
import sys

import numpy as np

KMAX_MARGIN = 10


def tk(b):
    return np.abs(b).max(axis=(1, 2))


def transient(t, k_lo):
    kmax = len(t) - 1
    k0 = max(10, k_lo)
    kp = k0 + int(np.argmax(t[k0:]))
    tv = float(t[10:kp + 1].min())
    ok = t[kp] / tv >= 10 and kp <= kmax - KMAX_MARGIN
    return kp, float(t[kp]), tv, bool(ok)


def judge(b32, b48, b48d, k_lo, mutate=""):
    if mutate == "scale48":
        b48 = b48.copy(); b48[k_lo:] *= 20
        if b48d is not None:
            b48d = b48d.copy(); b48d[k_lo:] *= 20
    t32, t48 = tk(b32), tk(b48)
    k32, p32, v32, s1 = transient(t32, k_lo)
    k48, p48, v48, s1_48 = transient(t48, k_lo)
    move = float(np.abs(b48d[k48] - b48[k48]).max() / p48) if b48d is not None else float("nan")
    s2 = move < 0.1
    r = p48 / p32
    if not s1:
        v = "S1 fails: no transient at M = 32"
    elif not s2:
        v = "S2 fails: the M = 48 base does not suffice"
    elif 0.5 <= r <= 2:
        v = "the solution's"
    elif r > 10 or r < 0.1:
        v = "the grid's"
    else:
        v = "between (reported as it is)"
    return dict(k32=k32, t32=p32, valley32=v32, k48=k48, t48=p48, valley48=v48, s1=s1, s1_48=s1_48, move48=move, s2=s2,
                r=r, verdict=v, code=0 if s1 and s2 else 1)


def selftest():
    k = np.arange(201, dtype=float)
    bg = 0.3 ** k
    hump = 1e-12 * np.exp(-((k - 60) / 12) ** 2)
    def arr(h):
        a = np.zeros((201, 4, 32)); a[:, 0, 0] = bg + h; return a
    cases = [("equal", arr(hump), arr(hump), "the solution's"), ("hump x20", arr(hump), arr(20 * hump), "the grid's"),
             ("no hump", arr(0 * hump), arr(0 * hump), "S1 fails: no transient at M = 32")]
    ok = True
    for name, a32, a48, want in cases:
        j = judge(a32, a48, a48 * (1 + 1e-6), 38)
        good = j["verdict"] == want
        ok = ok and good
        print(f"  planted {name}: k_peak {j['k32']}/{j['k48']}, r {j['r']:.3g}, verdict {j['verdict']} -> {'ok' if good else 'WRONG'}")
    j = judge(arr(hump), arr(hump), arr(hump) * (1 + 0.5), 38)
    good = j["verdict"].startswith("S2 fails")
    ok = ok and good
    print(f"  planted S2 (terms move by 0.5): {j['verdict']} -> {'ok' if good else 'WRONG'}")
    print("selftest", "passed" if ok else "FAILED")
    return 0 if ok else 1


def main():
    if "--selftest" in sys.argv:
        return selftest()
    c32, c48 = [a for a in sys.argv[1:] if not a.startswith("--")]
    mutate = next((a.split("=", 1)[1] for a in sys.argv if a.startswith("--mutate=")), "")
    if mutate:
        print(f"MUTATION {mutate}: the verdict must become the grid's")
    recs = {}
    for jl in glob.glob(os.path.join(c32, "..", "*.jsonl")):
        for line in open(jl):
            r = json.loads(line)
            recs[(r["state"], r["delta"])] = r
    code = 0
    print("| D | k_lo | M 32 peak (order, t) | valley | M 48 peak | valley | a_h x (1 + 1e-28) moves M 48 by | r = t48/t32 | verdict |")
    print("|---|---|---|---|---|---|---|---|---|")
    for D in ("80.0000", "100.0000"):
        f32 = os.path.join(c32, f"anm_pin3_D{D}_qd_d0e+00.npy")
        f48 = os.path.join(c48, f"m48_anm_pin3_D{D}_qd_d0e+00.npy")
        f48d = os.path.join(c48, f"m48_anm_pin3_D{D}_qd_d1e-28.npy")
        if not all(os.path.exists(f) for f in (f32, f48, f48d)):
            print(f"| {D} | missing files |")
            code = max(code, 2)
            continue
        rec = recs.get((f"anm_pin3_D{D}.npz", 0.0))
        k_lo = int(round(rec["Re_s"])) if rec else 10
        j = judge(np.load(f32), np.load(f48), np.load(f48d), k_lo, mutate)
        print(f"| {D} | {k_lo} | {j['k32']}, {j['t32']:.3e} | {j['valley32']:.2e} | {j['k48']}, {j['t48']:.3e} | "
              f"{j['valley48']:.2e} | {j['move48']:.1e} of t_peak | {j['r']:.3g} | {j['verdict']} |")
        code = max(code, j["code"])
    print("exit", code)
    return code


if __name__ == "__main__":
    sys.exit(main())
