#!/usr/bin/env python3
"""#969 (win): read-only, no run. From the stored K = 0 states of samples a, b, c at D 40.020065 (32 x 121, zh + zl), the differences a - c and b - c are formed in double-double (rt_perturb.dd_add) and rounded to
double vectors. Reported: their sizes against max|z_C|; the component of b - c orthogonal (2-norm) to a - c, o = (b - c) - t (a - c) with t = (b - c).(a - c) / (a - c).(a - c), its size and its size relative to b - c
(2-norm and max-norm); the cosines; and mu's share in a - c, b - c and o, where mu is the last entry of z (rt_model.RT.pack, unpack: z = [w1 half, w2, w3, w4, mu]): |mu| / max-norm of the vector, and
mu^2 / 2-norm^2. The 2-norm share of each block (w1 half, w2, w3, w4, mu) in the three vectors is printed too.

usage: python -I orth_969.py [--selftest]      (venv-t151 python)
--selftest: planted b - c = 1.5 (a - c) + 0.3 u, u orthogonal to a - c with a known mu entry; the function must return the planted relative size and mu shares to 1e-12, and the mutated projection
(t left out) must fail."""
import sys

import numpy as np

sys.path.insert(0, r"C:\Users\nathan\Source\choptuik-i968\solver\rt")
import rt_perturb as P

R = r"C:\Users\nathan\Source\choptuik-large-d-raw"
F = {"a": R + r"\I671-win\solves\k0_D40_mutnorows_D40.0201_32x121.npz",
     "b": R + r"\I701-win\solves\k0b_D40_mutnorows_D40.0201_32x121.npz",
     "c": R + r"\I951-win\solves\k0c_D40_mutnorows_D40.0201_32x121.npz"}


def analyse(ac, bc, mutate=False):
    t = 0.0 if mutate else float(bc @ ac / (ac @ ac))
    o = bc - t * ac
    out = dict(t=t, o=o, rel2=float(np.linalg.norm(o) / np.linalg.norm(bc)), relmax=float(np.abs(o).max() / np.abs(bc).max()),
               cos_ac_bc=float(ac @ bc / (np.linalg.norm(ac) * np.linalg.norm(bc))), orthcheck=float(abs(o @ ac) / (np.linalg.norm(o) * np.linalg.norm(ac))))
    for nm, v in (("ac", ac), ("bc", bc), ("o", o)):
        out["mu_" + nm] = float(v[-1])
        out["mushare_max_" + nm] = float(abs(v[-1]) / np.abs(v).max())
        out["mushare_2_" + nm] = float(v[-1] ** 2 / (v @ v))
    return out


def selftest():
    rng = np.random.default_rng(3)
    L = 13665
    ac = rng.normal(size=L) * 1e-20
    ac[-1] = 4e-21
    u = rng.normal(size=L) * 1e-20
    u[-1] = -7e-21
    u -= (u @ ac) / (ac @ ac) * ac
    bc = 1.5 * ac + 0.3 * u
    want_rel2 = 0.3 * np.linalg.norm(u) / np.linalg.norm(bc)
    want_mu_o = 0.3 * u[-1]
    want_share2 = bc[-1] ** 2 / (bc @ bc)
    r = analyse(ac, bc)
    ok = (abs(r["rel2"] / want_rel2 - 1) < 1e-12 and abs(r["t"] / 1.5 - 1) < 1e-12 and abs(r["mu_o"] / want_mu_o - 1) < 1e-9
          and abs(r["mushare_2_bc"] / want_share2 - 1) < 1e-12 and r["orthcheck"] < 1e-12)
    print(f"  planted: rel2 {r['rel2']:.6f} (want {want_rel2:.6f}), t {r['t']:.9f} (want 1.5), mu of o {r['mu_o']:.4e} (want {want_mu_o:.4e}), mu 2-norm share of b - c {r['mushare_2_bc']:.3e} (want {want_share2:.3e}), "
          f"orthogonality {r['orthcheck']:.1e}: {'ok' if ok else 'WRONG'}")
    m = analyse(ac, bc, mutate=True)
    okm = not (abs(m["rel2"] / want_rel2 - 1) < 1e-3) and m["orthcheck"] > 1e-3
    print(f"  mutated projection (t left out): rel2 {m['rel2']:.6f}, orthogonality {m['orthcheck']:.2e}: {'the test sees it, ok' if okm else 'WRONG, the test cannot see it'}")
    bad = (not ok) + (not okm)
    print("selftest", "FAILED" if bad else "passed")
    return bad


def main():
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    from rt_model import RT
    Z, D = {}, None
    for k, p in F.items():
        d = np.load(p)
        Z[k] = (np.asarray(d["zh"], float), np.asarray(d["zl"], float))
        D = (float(d["D"]), int(d["Nt"]), int(d["N"]), int(d["horizon"]))
    rt = RT(D[0], D[1], D[2], horizon=D[3])
    scale = float(np.abs(Z["c"][0] + Z["c"][1]).max())

    def diff(x, y):
        h, l = P.dd_add(Z[x][0], Z[x][1], -Z[y][0], -Z[y][1])
        return h + l

    ac, bc = diff("a", "c"), diff("b", "c")
    r = analyse(ac, bc)
    o = r["o"]
    print(f"D {D[0]}, {D[1]}x{D[2]}, K {D[3]}, z has {ac.size} entries, max|z_C| {scale:.6e}, mu of z_C {Z['c'][0][-1] + Z['c'][1][-1]:+.6e}, block sizes w1 half {rt.n1}, w2 = w3 = w4 {rt.nf}, mu 1")
    print("\n| vector | max-norm / max abs z | 2-norm / max abs z |\n|---|---|---|")
    for nm, v in (("a - c", ac), ("b - c", bc), ("o = b - c orthogonal to a - c", o)):
        print(f"| {nm} | {np.abs(v).max() / scale:.4e} | {np.linalg.norm(v) / scale:.4e} |")
    print(f"\ncosine of a - c and b - c: {r['cos_ac_bc']:.12f}. b - c = t (a - c) + o with t = {r['t']:.6f}; check cosine of o and a - c: {r['orthcheck']:.1e} (zero to the rounding of the double vectors).")
    print(f"Orthogonal component o against b - c: 2-norm {r['rel2']:.6f}, max-norm {r['relmax']:.6f}.  Its part along a - c, t (a - c): 2-norm {np.sqrt(1 - r['rel2'] ** 2):.6f} of b - c.")
    print("\n| vector | mu entry | mu / max-norm | mu^2 / 2-norm^2 |\n|---|---|---|---|")
    for nm, key in (("a - c", "ac"), ("b - c", "bc"), ("o", "o")):
        print(f"| {nm} | {r['mu_' + key]:+.4e} | {r['mushare_max_' + key]:.4e} | {r['mushare_2_' + key]:.4e} |")
    n1, nf = rt.n1, rt.nf
    sl = {"w1 half": slice(0, n1), "w2": slice(n1, n1 + nf), "w3": slice(n1 + nf, n1 + 2 * nf), "w4": slice(n1 + 2 * nf, n1 + 3 * nf), "mu": slice(n1 + 3 * nf, n1 + 3 * nf + 1)}
    assert n1 + 3 * nf + 1 == ac.size
    print("\nShare of the squared 2-norm by block:\n\n| vector | " + " | ".join(sl) + " |\n|---|" + "---|" * len(sl))
    for nm, v in (("a - c", ac), ("b - c", bc), ("o", o)):
        print(f"| {nm} | " + " | ".join(f"{float(v[s] @ v[s]) / float(v @ v):.4e}" for s in sl.values()) + " |")


if __name__ == "__main__":
    main()
