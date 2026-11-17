"""#935: od_axpy of the installed multidouble Python package, on the same seeded inputs as od_axpy_gap_test.py, one
run per package. `dump OUT.npz` writes each class's outputs; `compare A.npz B.npz` counts the trials whose eight parts
differ in any bit, per class."""
import sys
import numpy as np
exec(open("od_axpy_gap_test.py").read().split("for gap in (0, 60")[0].replace("N = 20000", "N = 20000"))
if sys.argv[1] == "dump":
    out_all = {}
    for gap in (0, 60, 150, 250, 400):
        rows = []
        for _ in range(N):
            a = float(rng.uniform(-3, 3))
            x, y = octo(gap), octo(gap)
            if not (normalized(x) and normalized(y)):
                continue
            o = md.od_axpy(a, *[np.array([p]) for p in x], *[np.array([p]) for p in y])
            rows.append([float(q[0]) for q in o])
        out_all[f"gap{gap}"] = np.array(rows)
        print(f"gap {gap}: {len(rows)} trials", flush=True)
    np.savez(sys.argv[2], **out_all)
else:
    A, B = np.load(sys.argv[2]), np.load(sys.argv[3])
    for k in A.files:
        a, b = A[k].view(np.uint64), B[k].view(np.uint64)
        print(f"{k}: {len(a)} trials, results that differ in any bit: {int(np.any(a != b, axis=1).sum())}")
