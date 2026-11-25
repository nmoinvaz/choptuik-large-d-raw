#!/usr/bin/env python3
"""n_null of a saved state, counted as ell_leap.py --fold records it (#1025): the number of singular values of the state's
Jacobian J (S.jacobian(z) after S.freeze_from(z, kappa), the same DSSEll the checks build) at or below 1e-12 sigma_max
(n_null = len(sv) - len(reg), reg = sv > 1e-12 sv[0]), the cutoff, sigma_max, and the four smallest singular values above
the cutoff (sv_reg_small). Written for t5's question whether the number of near-null directions changes parity between
k_c 103 and k_c 111 at D 21.125 (an overall sign flip of the determinant).

usage: nnull_count.py --selftest [--mutate=cut]
       nnull_count.py record.jsonl state.npy D wtm [label]      (wtm = solver/matter of the worktree)
The selftest plants a matrix with 7 singular values at 1e-14 of sigma_max among 193 others between 1 and 1e-3 and wants
n_null 7, a full-rank matrix wants 0, and a matrix with a gap at 1e-9 wants 0 at the 1e-12 cutoff; --mutate=cut moves
the cutoff to 1e-2 and must make the selftest fail (exit 1).
"""
import json
import os
import sys
import time


def count(sv, rel=1e-12):
    import numpy as np
    sv = np.asarray(sv, dtype=float)
    reg = np.nonzero(sv > rel * sv[0])[0]
    return int(len(sv) - len(reg)), reg


def planted(n_null, seed):
    import numpy as np
    rng = np.random.default_rng(seed)
    n = 200
    sv = np.concatenate([np.geomspace(1.0, 1e-3, n - n_null), np.full(n_null, 1e-14) * (1 + rng.random(n_null))])
    U, _ = np.linalg.qr(rng.standard_normal((n, n)))
    V, _ = np.linalg.qr(rng.standard_normal((n, n)))
    return U @ np.diag(sv) @ V.T


def selftest(mutate=None):
    import numpy as np
    rel = 1e-2 if mutate == "cut" else 1e-12
    cases = []
    for k, seed in ((7, 1), (0, 2), (31, 3)):
        sv = np.linalg.svd(planted(k, seed), compute_uv=False)
        cases.append(("planted %d near-null directions" % k, count(sv, rel)[0], k))
    gap = np.linalg.svd(planted(0, 4), compute_uv=False)
    gap[-3:] = 1e-9 * gap[0]
    cases.append(("three values at 1e-9 sigma_max are above the 1e-12 cutoff", count(gap, rel)[0], 0))
    ok = True
    for name, got, want in cases:
        print("planted: %s: n_null %d, expected %d: %s" % (name, got, want, "PASS" if got == want else "FAIL"))
        ok = ok and got == want
    print("selftest: " + ("PASS" if ok else "FAILS"))
    return 0 if ok else 1


if __name__ == "__main__":
    if sys.argv[1] == "--selftest":
        sys.exit(selftest(next((a.split("=", 1)[1] for a in sys.argv if a.startswith("--mutate=")), None)))
    recf, st, D, wtm = sys.argv[1], sys.argv[2], float(sys.argv[3]), sys.argv[4]
    label = sys.argv[5] if len(sys.argv) > 5 else ""
    sys.path.insert(0, wtm)
    os.chdir(wtm)
    import numpy as np
    from dss_ell import DSSEll, NODES_STD
    rec = [json.loads(x) for x in open(recf) if x.strip() and json.loads(x).get("D") == D][-1]
    z = np.load(st)
    t0 = time.time()
    S = DSSEll(kc=rec["kc"], nodes=NODES_STD, n=D - 2, ell=1, Delta_ref=z[-1], Ks=rec["Ks"], u0=rec["u0"], rk=rec.get("rk", 1))
    steps = S.freeze_from(z, rec["kappa"])
    t1 = time.time()
    _, J = S.jacobian(z)
    t2 = time.time()
    sv = np.linalg.svd(J, compute_uv=False)
    t3 = time.time()
    n_null, reg = count(sv)
    last = reg[-4:][::-1]
    out = dict(label=label, kc=rec["kc"], D=D, N=int(len(z)), J_shape=list(J.shape), steps=int(sum(steps.values())),
               record_steps=rec["steps"], sigma_max=float(sv[0]), cutoff=float(1e-12 * sv[0]), n_null=n_null,
               n_null_parity="odd" if n_null % 2 else "even", n_regular=int(len(reg)),
               sv_reg_small=[float(sv[i]) for i in last], sv_null_largest=[float(x) for x in sv[len(reg):len(reg) + 3]],
               seconds=dict(freeze=round(t1 - t0), jacobian=round(t2 - t1), svd=round(t3 - t2)))
    print(json.dumps(out), flush=True)
