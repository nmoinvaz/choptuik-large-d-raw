"""#1078: mode_qd.qd_det on multidouble's own planted matrices (python/tests/test_logdet.py at 8c4360ac: float64 A with |det A| about 1e-45 det B, the sign wrong in double-double), with and without equilibration,
against the test's mpmath 200-digit reference (within 1e-6), and its control update_dd, which must miss the same check. usage (a stub pytest.py on the path):
    cd hp && PYTHONPATH=<dir with pytest.py stub> python3 mdtest_planted_check.py <dir with test_logdet_8c4360ac.py>      exit 0 iff the method passes and the control fires in every case"""
import sys
import numpy as np
sys.path.insert(0, sys.argv[1])
sys.path.insert(0, ".")
import mode_qd as Q          # noqa: E402
import test_logdet_8c4360ac as T   # noqa: E402
ok_all = True
for n, seed in ((12, 4), (40, 5)):
    A, ref = T.planted(n, 1e-45, seed, T.dd_sign)
    z = np.zeros_like(A)
    for equil in (False, True):
        a, b = Q.qd_det(A, z, equil=equil), Q.qd_det(A, z, equil=equil, control="update_dd")
        okA = a["sign"] == ref[0] and abs(a["ln"] - ref[1]) < 1e-6
        okB = b["sign"] == ref[0] and abs(b["ln"] - ref[1]) < 1e-6
        ok_all &= okA and not okB
        print(f"n {n} seed {seed} equil {equil}: mpmath {ref[0]:+.0f} {ref[1]:.6f}; mode_qd.qd_det none {a['sign']:+.0f} {a['ln']:.6f} ({'PASS' if okA else 'FAIL'}); update_dd {b['sign']:+.0f} {b['ln']:.6f} ({'fires' if not okB else 'DOES NOT FIRE'})")
sys.exit(0 if ok_all else 1)
