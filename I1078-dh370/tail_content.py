"""#1078 check 2 (t5's comment of 20:45 UTC): the high-harmonic content |Pi_high f| / |f| of each block of a state, Pi_high = I - Pi_low, in the solver's own basis on the stored (computational) grid.

    python3 tail_content.py STATE.npz OUT.json [--ks=48,64,80] [--dps=50]      |      python3 tail_content.py selftest [--mutate=kf]

z = [p1 | c0 | node_0: p m a c | ... | m_h | a_h | Delta], M values per block, the field's value at the half-grid point theta_j = pi j / M (N = 2M, harmonics k of e^(i k theta); mapped states store values at the
uniform computational grid, to which the projectors apply; the tau-map is not undone). hp's fields: p, m odd (odd harmonics), a, c even (even harmonics) on the half grid (hp/src/model.rs line 4):
  Pi_low for an odd field   = hpkernel.driver.plow_odd(M, kf) (the odd harmonics k <= kf; double-double entries, used as stored);
  Pi_low for an even field  = (1/M)(1 + 2 sum_{k even, 2 <= k <= kf} cos(k (theta_i - theta_j))), the same construction for period pi, built here (mpmath).
plow_odd applied to an even field is also reported, as asked, but it is the wrong sector for p's partners (a, c). The state's entries (hi + lo) are applied in mpmath at --dps digits, the ratio is the
2-norm |f - Pi_low f| / |f|. Controls (selftest): planted single harmonics (odd k0 = kf - 1 in an odd field: ratio < 1e-25; kf + 1: ratio 1; even k0 = kf - 2 / kf + 2 the same), and this
script's odd projector equals driver.plow_odd to 1e-30; --mutate=kf lowers kf by 4 in the projector and must exit 1."""
import json
import sys

import mpmath as mp

MUT = next((a.split("=", 1)[1] for a in sys.argv if a.startswith("--mutate=")), None)
M = 96


def opt(name, default):
    return next((a.split("=", 1)[1] for a in sys.argv if a.startswith(f"--{name}=")), default)


mp.mp.dps = int(opt("dps", "50"))


def theta(j, m=M):
    return mp.pi * j / m


def build(parity, kf, m=M):
    """mp matrix (list of rows) of the projector onto harmonics <= kf of the given parity ('odd' or 'even') of a field on the m-point half grid"""
    kf = kf - 4 if MUT == "kf" else kf
    ks = list(range(1, kf + 1, 2)) if parity == "odd" else list(range(2, kf + 1, 2))
    # cos(k (theta_i - theta_j)) depends on d = i - j only
    c = {d: sum(mp.cos(k * theta(d, m)) for k in ks) for d in range(-(m - 1), m)}
    if parity == "odd":
        return [[4 * c[i - j] / (2 * m) for j in range(m)] for i in range(m)]
    return [[(1 + 2 * c[i - j]) / m for j in range(m)] for i in range(m)]


def from_driver(kf, m=M):
    from hpkernel.driver import plow_odd
    hi, lo = plow_odd(m, kf)
    return [[mp.mpf(float(hi[i][j])) + mp.mpf(float(lo[i][j])) for j in range(m)] for i in range(m)]


def ratio(P, f):
    Pf = [mp.fsum(P[i][j] * f[j] for j in range(len(f))) for i in range(len(f))]
    num = mp.sqrt(mp.fsum((f[i] - Pf[i]) ** 2 for i in range(len(f))))
    den = mp.sqrt(mp.fsum(x * x for x in f))
    return num / den if den else mp.mpf(0)


def blocks(K=21):
    out = [("p1", "odd", 0), ("c0", "even", M)]
    for a in range(K):
        for q, (name, par) in enumerate((("p", "odd"), ("m", "odd"), ("a", "even"), ("c", "even"))):
            out.append((f"node {a} {name}", par, 2 * M + 4 * M * a + q * M))
    out += [("m_h", "odd", 2 * M + 4 * M * K), ("a_h", "even", 3 * M + 4 * M * K)]
    return out


def selftest():
    ok = True
    for kf in (48, 64):
        Po, Pe = build("odd", kf), build("even", kf)
        for par, P, k_in, k_out in (("odd", Po, kf - 1, kf + 1), ("even", Pe, kf - 2, kf + 2)):
            f_in = [mp.cos(k_in * theta(j) + mp.mpf("0.3")) for j in range(M)]
            f_out = [mp.cos(k_out * theta(j) + mp.mpf("0.3")) for j in range(M)]
            r_in, r_out = ratio(P, f_in), ratio(P, f_out)
            good = r_in < mp.mpf("1e-25") and abs(r_out - 1) < mp.mpf("1e-10")
            print(f"selftest kf {kf} {par}: planted harmonic {k_in} (inside) ratio {mp.nstr(r_in, 3)}, {k_out} (outside) ratio {mp.nstr(r_out, 12)}: {'PASS' if good else 'FAIL'}")
            ok &= bool(good)
    if MUT is None:
        from hpkernel.driver import plow_odd  # noqa: F401
        d = max(abs(a - b) for ra, rb in zip(build("odd", 48), from_driver(48)) for a, b in zip(ra, rb))
        print(f"selftest: this script's odd projector against driver.plow_odd(96, 48): largest difference {mp.nstr(d, 3)}: {'PASS' if d < mp.mpf('1e-30') else 'FAIL'}")
        ok &= bool(d < mp.mpf("1e-30"))
    return 0 if ok else 1


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    from hpkernel.driver import load
    zh, zl, meta = load(args[0])
    K = len(meta["nodes"])
    assert meta["M"] == M and len(zh) == 4 * M * (K + 1) + 1
    z = [mp.mpf(float(a)) + mp.mpf(float(b)) for a, b in zip(zh, zl)]
    ks = [int(k) for k in opt("ks", "48,64,80").split(",")]
    P = {(par, k): build(par, k) for par in ("odd", "even") for k in ks}
    D = {k: from_driver(k) for k in ks}
    rows = []
    for name, par, off in blocks(K):
        f = z[off:off + M]
        row = dict(block=name, parity=par, off=off, norm=float(mp.sqrt(mp.fsum(x * x for x in f))))
        for k in ks:
            row[f"k{k}"] = float(ratio(P[(par, k)], f))                     # the right sector for the field
            row[f"plow_odd_k{k}"] = float(ratio(D[k], f))                   # driver.plow_odd, as asked (right for odd, wrong for even)
        rows.append(row)
    json.dump(dict(state=args[0].split("/")[-1], ks=ks, rows=rows), open(args[1], "w"), indent=1)
    print(f"{'block':14s} {'parity':6s} {'|f|':>10s} " + " ".join(f"{'k=' + str(k) + ' (own)':>14s} {'plow_odd':>11s}" for k in ks))
    for r in rows:
        if r["block"] in ("p1", "c0", "a_h", "m_h"):
            print(f"{r['block']:14s} {r['parity']:6s} {r['norm']:10.3e} " + " ".join(f"{r[f'k{k}']:14.3e} {r[f'plow_odd_k{k}']:11.3e}" for k in ks))
    print("the node blocks (extra): the largest ratio over the nodes, by field")
    for fld in ("p", "m", "a", "c"):
        sel = [r for r in rows if r["block"].endswith(" " + fld)]
        print(f"  node field {fld} ({sel[0]['parity']}): " + ", ".join(f"k={k}: max {max(r[f'k{k}'] for r in sel):.3e} at {max(sel, key=lambda r: r[f'k{k}'])['block']}" for k in ks))


if __name__ == "__main__":
    sys.exit(selftest() if sys.argv[1:2] == ["selftest"] else main())
