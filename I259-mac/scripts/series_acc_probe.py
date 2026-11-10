"""#259 step 1: is the series blocks' non-smooth entry error in the sums or in the terms? (criteria in ../README.md,
written before the runs)

    python series_acc_probe.py HP_DIR STATE.npz KF LAM_PHYS OUT.json [--threads=2] [--accs=0,1]

HP_DIR is the worktree's hp/ (its modecount_cx/build has CSolver.series_matrix). At z = lam_phys + 0.2 e^{2 pi i / 20}
(as #252's matrix_noise.py) the mode matrix's series-block columns (CSolver.series_matrix, the segments not computed)
at z, z + d, z + 2d, d = 2^-46, for acc 0 (double-double, the production sums) and the --accs given: 1 (the series'
final Horner sums in quad-double from the same double-double coefficients), 2 (also the series' Cauchy products with
exact products and quad-double sums), 3 (also the series' D f in quad-double). Per block (centre rows, horizon rows):

* rel_d2[acc] = max |M(z + 2d) - 2 M(z + d) + M(z)| / max |M|, the non-smooth entry error (#252);
* wiring = max |M_acc(z) - M_acc0(z)| / max |M| (the switch must act, and only at rounding level);
* floor = 2^-106 T / max |M|, T the largest |tangent term| c_k h^k of the series' Horner sums: the error that rounding
  each stored double-double coefficient leaves in the sum, whatever the summation.
"""
import json
import sys
import time

import numpy as np

hp_dir, path, kf, lam, out = sys.argv[1:6]
threads = next((int(a.split("=")[1]) for a in sys.argv[6:] if a.startswith("--threads=")), 2)
accs = next(([int(x) for x in a.split("=")[1].split(",")] for a in sys.argv[6:] if a.startswith("--accs=")), [0, 1])
assert accs[0] == 0
sys.path.insert(0, hp_dir)
import modecount_common as mc  # noqa: E402

kf = None if kf == "none" else int(kf)
lam = float(lam)
st = mc.setup(path, M=None, kf=kf, fmax=1e-15, threads=threads)
M, K = st.M, st.K
import modecount_cx  # noqa: E402

print(f"modecount_cx {modecount_cx.__file__}", flush=True)
z = lam + 0.2 * np.exp(2j * np.pi / 20)
d = 2.0 ** -46
assert 2 <= z.real < 4


def mat(w, acc):
    t = time.time()
    r = st.c.series_matrix(st.zh, st.zl, float(w.real), float(w.imag), acc)
    print(f"  acc {acc} at {w!r}: T centre {r[4]:.3e}, horizon {r[5]:.3e} ({time.time() - t:.0f} s)", flush=True)
    return tuple(np.asarray(x) for x in r[:4]), (r[4], r[5])


def d2(a0, a1, a2):
    """second difference in double-double: hi parts by exact differences, then the lo parts"""
    re = ((a2[0] - a1[0]) - (a1[0] - a0[0])) + ((a2[1] - a1[1]) - (a1[1] - a0[1]))
    im = ((a2[2] - a1[2]) - (a1[2] - a0[2])) + ((a2[3] - a1[3]) - (a1[3] - a0[3]))
    return np.hypot(re, im)


def diff(a, b):
    return np.hypot((a[0] - b[0]) + (a[1] - b[1]), (a[2] - b[2]) + (a[3] - b[3]))


res = {}
for acc in accs:
    m0, t = mat(z, acc)
    m1, _ = mat(z + d, acc)
    m2, _ = mat(z + 2 * d, acc)
    res[acc] = dict(m0=m0, t=t, d2=d2(m0, m1, m2))
mag = np.hypot(res[0]["m0"][0], res[0]["m0"][2])
blk = 4 * M
rows = []
print(f"D {st.D} M {M} ks {st.ks} at {z}", flush=True)
for name, b, ti in (("centre", 0, 0), ("horizon", K, 1)):
    r0, r1 = b * blk, min((b + 1) * blk, mag.shape[0])
    big = float(mag[r0:r1].max())
    row = dict(block=name, rows=[r0, r1], max_abs=big)
    for acc in accs:
        row[f"rel_d2_acc{acc}"] = float(res[acc]["d2"][r0:r1].max()) / big
        row[f"T_acc{acc}"] = res[acc]["t"][ti]
        if acc:
            row[f"wiring_acc{acc}"] = float(diff(res[acc]["m0"], res[0]["m0"])[r0:r1].max()) / big
            row[f"ratio_acc0_over_acc{acc}"] = row["rel_d2_acc0"] / max(row[f"rel_d2_acc{acc}"], 1e-300)
    row["floor"] = 2.0 ** -106 * row["T_acc0"] / big
    row["rel_d2_acc0_over_floor"] = row["rel_d2_acc0"] / row["floor"]
    rows.append(row)
    print(f"  {name:>8s}: max |M| {big:.2e}; rel D2 acc0 {row['rel_d2_acc0']:.2e}; T {row['T_acc0']:.2e}, "
          f"floor 2^-106 T / max|M| {row['floor']:.2e} (rel D2 / floor {row['rel_d2_acc0_over_floor']:.1f})",
          flush=True)
    for acc in accs[1:]:
        print(f"           acc{acc}: rel D2 {row[f'rel_d2_acc{acc}']:.2e} (acc0 / acc{acc} "
              f"{row[f'ratio_acc0_over_acc{acc}']:.2f}); wiring {row[f'wiring_acc{acc}']:.2e}", flush=True)
json.dump(dict(state=path, D=st.D, M=M, ks=st.ks, z=[z.real, z.imag], d=d, accs=accs, rows=rows), open(out, "w"), indent=1)
