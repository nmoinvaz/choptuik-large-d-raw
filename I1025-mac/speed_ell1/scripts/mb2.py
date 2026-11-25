import numpy as np, time
def t(f, n=30):
    f(); t0 = time.perf_counter()
    for _ in range(n): f()
    return (time.perf_counter() - t0) / n * 1e3
N, nf, no, ne = 312, 518, 104, 103
rng = np.random.default_rng(0)
G = rng.random((nf, N)); Dm = rng.random((N, N)); Bo = rng.random((no, N)); BBo = rng.random((no, 2 * N)); So = rng.random((N, no))
dc = rng.random((nf, 3 * no + 2 * ne)); c1 = dc[:, :no]
G5 = rng.random((5 * nf, N))
for rep in range(2):
    print(f"grid: (nf,N)@(N,N) {t(lambda: G @ Dm):.2f} ms; (5nf,N)@(N,N) {t(lambda: G5 @ Dm):.2f}; "
          f"coef: slice(nf,no)@(no,N) {t(lambda: c1 @ Bo):.2f}; contiguous {t(lambda: np.ascontiguousarray(c1) @ Bo):.2f}; "
          f"(nf,no)@(no,2N) {t(lambda: c1 @ BBo):.2f}; (nf,N)@(N,no) {t(lambda: G @ So):.2f}; "
          f"elem (nf,N) mul {t(lambda: G * G[0]):.3f}; axpy (nf,blk) {t(lambda: dc + 0.5 * dc):.3f}; axpy grid 5x {t(lambda: G5 + 0.5 * G5):.3f}")
