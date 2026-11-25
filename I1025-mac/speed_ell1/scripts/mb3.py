import numpy as np, time
def t(f, n=50):
    f(); t0 = time.perf_counter()
    for _ in range(n): f()
    return (time.perf_counter() - t0) / n * 1e3
N, nf = 312, 518
rng = np.random.default_rng(0)
G = rng.random((nf, N)); c = rng.random((1, N)); buf = np.empty_like(G); acc = np.empty_like(G)
def inplace():
    np.multiply(c, G, out=acc)
    np.multiply(c, G, out=buf); np.add(acc, buf, out=acc)
for rep in range(3):
    print(f"G*c {t(lambda: G * c):.3f} ms, out= {t(lambda: np.multiply(G, c, out=buf)):.3f}, two-term new {t(lambda: c * G + c * G):.3f}, two-term inplace {t(inplace):.3f}")
