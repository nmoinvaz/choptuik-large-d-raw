#!/usr/bin/env python3
"""#697: the horizon series of #693 (hp/horizon_radius.py) at another M. The state's horizon data (m_h odd, a_h even in tau, eight parts) on the M-point half grid
theta_j = pi j / M are resampled to M2 points by zero-padding their harmonics (the trigonometric polynomial of harmonics below M evaluated at M2 points), summed in
mpmath at 140 digits and split into eight parts; Delta and D are kept; the rest of the state is zero (the horizon rows of the two-node residual do not read it, which
is #693's control C1 and the reason the terms c_k u0^k, k >= 1, do not depend on the nodes). Then horizon_radius.Series.terms gives the quad-double terms.

    cd hp && python3 -u M48_697 RAWDIR STATE OUTPREFIX [--M2=48] [--kmax=300] [--threads=12] [--mutate=scale_h] [--controls]

--controls: the resampling M -> M returns the data to 1e-60 relative, and M -> M2 -> M too (printed, exit 1 when not). --mutate=scale_h scales the first harmonic of m_h by
1 + 1e-6 before the series (the control: the order-1 terms must move by about that)."""
import json
import os
import sys
import time

HP = "/home/nathan/Source/choptuik-large-d-685/hp"
sys.path.insert(0, HP)
import mpmath as mp  # noqa: E402
import numpy as np  # noqa: E402
import horizon_radius as H  # noqa: E402

mp.mp.dps = 140


def to_mp(parts, sl):
    return [mp.fsum(mp.mpf(float(p[i])) for p in parts) for i in range(sl.start, sl.stop)]


def split8(v):
    out = []
    for _ in range(8):
        f = float(v)
        out.append(f)
        v = v - f
    return out


def harm(f, odd):
    """c_k, k = 0..M of the full-grid DFT (2M points, antiperiodic when odd), /(2M): c_k = (1/2M) sum_j F_j exp(-i k theta_j)"""
    M = len(f)
    full = list(f) + [(-x if odd else x) for x in f]
    th = [mp.pi * j / M for j in range(2 * M)]
    return [mp.fsum(full[j] * mp.expjpi(-mp.mpf(k) * j / M) for j in range(2 * M)) / (2 * M) for k in range(M + 1)]


def evaluate(c, M, M2, scale1=1.0):
    """f(theta'_j), theta'_j = pi j / M2, from the half-grid DFT c of M points: c_0 + sum_(k=1..M-1) 2 Re(c_k e^(i k theta')) + c_M cos(M theta')"""
    out = []
    for j in range(M2):
        v = c[0].real
        for k in range(1, M):
            ck = c[k] * (scale1 if k == 1 else 1)
            v += 2 * (ck * mp.expjpi(mp.mpf(k) * j / M2)).real
        v += (c[M] * mp.expjpi(mp.mpf(M) * j / M2)).real
        out.append(v)
    return out


def resample(parts, off, M, M2, odd, scale1=1.0):
    f = to_mp(parts, slice(off, off + M))
    c = harm(f, odd)
    vals = evaluate(c, M, M2, scale1)
    return vals, f


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    opts = dict(a[2:].split("=", 1) for a in sys.argv[1:] if a.startswith("--") and "=" in a)
    mutate = opts.get("mutate", "")
    raw, st, prefix = args
    M2 = int(opts.get("M2", 48))
    kmax = int(opts.get("kmax", 300))
    threads = int(opts.get("threads", 12))
    z, meta = H.load_state(os.path.join(raw, st))
    sr0 = H.Series(z, meta, threads=threads)
    M, K = sr0.M, sr0.K
    ok = True
    # the data: m_h (odd), a_h (even), Delta
    mh, ah = sr0.off["mh"], sr0.off["ah"]
    new = {}
    for name, off, odd in (("mh", mh, True), ("ah", ah, False)):
        s1 = (1 + 1e-6) if (mutate == "scale_h" and name == "mh") else 1.0
        v2, f = resample(z, off, M, M2, odd, s1)
        new[name] = [split8(v) for v in v2]
        if "--controls" in sys.argv:
            v1, _ = resample(z, off, M, M, odd)
            e1 = max(abs(a - b) for a, b in zip(v1, f)) / max(abs(x) for x in f)
            # the round trip M -> M2 -> M: the M2 values back to M points through their own DFT
            c = harm(v2, odd)
            back = []
            for j in range(M):
                v = c[0].real
                for k in range(1, M2):
                    v += 2 * (c[k] * mp.expjpi(mp.mpf(k) * j / M)).real
                v += (c[M2] * mp.expjpi(mp.mpf(M2) * j / M)).real
                back.append(v)
            e2 = max(abs(a - b) for a, b in zip(back, f)) / max(abs(x) for x in f)
            good = e1 < mp.mpf("1e-60") and e2 < mp.mpf("1e-60")
            print(f"  control {name}: M->M {mp.nstr(e1, 3)}, M->{M2}->M {mp.nstr(e2, 3)} relative -> {'ok' if good else 'FAIL'}", flush=True)
            ok = ok and good
    L2 = 4 * M2 * (K + 1) + 1
    z2 = [np.zeros(L2) for _ in range(8)]
    off2 = dict(mh=2 * M2 + 4 * M2 * K, ah=3 * M2 + 4 * M2 * K)
    for q in range(8):
        z2[q][off2["mh"]:off2["mh"] + M2] = [p[q] for p in new["mh"]]
        z2[q][off2["ah"]:off2["ah"] + M2] = [p[q] for p in new["ah"]]
        z2[q][-1] = z[q][-1]
    meta2 = dict(meta)
    meta2["M"] = M2
    sr = H.Series(z2, meta2, threads=threads)
    t0 = time.time()
    b, Hr = sr.terms("qd", kmax)
    sec = time.time() - t0
    np.save(prefix + f"_M{M2}_qd.npy", b)
    t = np.abs(b).max(axis=(1, 2))
    kp = 100 + int(np.argmax(t[100:]))
    est = H.estimate(b, sr.u0)
    rec = dict(state=st, D=float(meta["D"]), M=M2, kmax=kmax, prec="qd", mutate=mutate, u0=sr.u0, H=dict(zip(H.FIELDS, Hr)), k_peak=kp, t_peak=float(t[kp]),
               t_min=float(t[40:kp].min()), t_last=float(t[-1]), profile=H.profile(b), est=est, seconds=round(sec, 1))
    with open(prefix + f"_M{M2}.jsonl", "a") as fo:
        fo.write(json.dumps(rec) + "\n")
    print(f"M {M2}, D {float(meta['D']):.4f}, {kmax} orders in quad-double ({sec:.0f} s): peak {t[kp]:.4e} at order {kp}, min before it {rec['t_min']:.2e}, t_{kmax} {t[-1]:.2e}; "
          f"H(u0) at ks {meta['ks']}: " + " ".join(f"{f} {v:.1e}" for f, v in zip(H.FIELDS, Hr)), flush=True)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
