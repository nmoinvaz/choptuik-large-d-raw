"""#957: how much the jets' series and the order-by-order series differ at the planted-hook line of jet_by_order_check.py.

    python3 diff957.py RAW STATE.npz [--threads 10] [--Np 6] [--out PREFIX]      (run from hp/ of the build under test)

Forms the series to order Np with jet_by_order_check's planted change in both forms (coefficients_o by_order=False and True), as
that script's second line does, and prints per order k: the entries whose bits differ in any of the eight parts, the lowest
part index that differs, and max|z_k - z'_k| / max|z_k| of the eight-part difference (od_axpy), leading part. Controls, which
must behave as stated: the jets' series against itself differs nowhere, and the jets' series against the order-by-order one with
the change in the order-by-order form only differs at every order 1..Np. Exit 1 if a control does not behave."""
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.getcwd())
from anm_run import coefficients_o  # noqa: E402
from jet_by_order_check import planted  # noqa: E402
from multidouble import od_axpy  # noqa: E402
from octo_corrector import truth_system  # noqa: E402


def opt_of(argv, name, default):
    return type(default)(argv[argv.index("--" + name) + 1]) if "--" + name in argv else default


def per_order(A, B, Np):
    rows = []
    for k in range(1, Np + 1):
        bits = [int(np.sum(np.asarray(p).view(np.uint64) != np.asarray(q).view(np.uint64))) for p, q in zip(A[k], B[k])]
        diff = od_axpy(-1.0, *(np.ascontiguousarray(np.asarray(p)) for p in B[k]), *(np.ascontiguousarray(np.asarray(p)) for p in A[k]))
        scale = max(float(np.max(np.abs(np.asarray(A[k][0])))), 1e-300)
        rows.append(dict(k=k, entries=bits, entries_any=int(sum(1 for i in range(len(np.asarray(A[k][0])))
                         if any(np.asarray(p).view(np.uint64)[i] != np.asarray(q).view(np.uint64)[i] for p, q in zip(A[k], B[k])))),
                         lowest_part=(min((i for i, b in enumerate(bits) if b), default=None)),
                         rel=float(np.max(np.abs(diff[0]))) / scale))
    return rows


def main(argv):
    raw, state = argv[0], argv[1]
    threads, Np, out = opt_of(argv, "threads", 10), opt_of(argv, "Np", 6), opt_of(argv, "out", "")
    z, meta, (s, _, _, _), info = truth_system(raw, state, threads=threads)
    zo = [np.ascontiguousarray(np.asarray(p)) for p in z]
    print(f"diff957 {state}: D {meta.get('D_str', meta.get('D'))!s:.18}, {info['plan']} plan, Np {Np}, {threads} threads", flush=True)
    s.newton_o(list(zo))
    Ap, _ = coefficients_o(s, zo, Np, perturb=planted, by_order=False)
    Bp, _ = coefficients_o(s, zo, Np, perturb=planted, by_order=True)
    Bn, _ = coefficients_o(s, zo, Np, by_order=True)
    main_rows = per_order(Ap, Bp, Np)
    self_rows = per_order(Ap, Ap, Np)
    ctl_rows = per_order(Ap, Bn, Np)
    print("jets vs by order, the planted change in both (the failing line):")
    print("  k  entries differing (any part)  per part (0..7)                      lowest part  max|z-z'|/max|z|")
    for r in main_rows:
        print(f"  {r['k']}  {r['entries_any']:<28}  {r['entries']}  {r['lowest_part']}  {r['rel']:.3e}")
    ok_self = all(r["entries_any"] == 0 for r in self_rows)
    ok_ctl = all(r["entries_any"] > 0 for r in ctl_rows)
    print(f"control, the jets' series against itself: differs at {[r['k'] for r in self_rows if r['entries_any']]} (must be none): "
          f"{'ok' if ok_self else 'FAIL'}")
    print(f"control, the change in the order-by-order form only: differs at {[r['k'] for r in ctl_rows if r['entries_any']]} "
          f"(must be every order): {'ok' if ok_ctl else 'FAIL'}")
    if out:
        with open(out + ".json", "w") as f:
            json.dump(dict(state=state, Np=Np, threads=threads, main=main_rows, control_self=self_rows, control_planted_one=ctl_rows,
                           controls_ok=ok_self and ok_ctl), f, indent=1)
    return 0 if ok_self and ok_ctl else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
