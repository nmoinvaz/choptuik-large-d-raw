import numpy as np, time
def t(f, n=20):
    f(); t0 = time.perf_counter()
    for _ in range(n): f()
    return (time.perf_counter() - t0) / n * 1e3
for N, nf, no in ((96, 158, 32), (168, 278, 56), (312, 518, 104)):
    B = nf + 1
    Dm = np.random.rand(N, N); fc = np.random.rand(B, N) + 1j * np.random.rand(B, N); fr = np.random.rand(nf, N)
    Bo = np.random.rand(no, N); So = np.random.rand(N, no); cr = np.random.rand(nf, no)
    mask = np.random.rand(N // 2 + 1)
    print(f"N {N} nf {nf}: complex@real {t(lambda: fc @ Dm):.3f} ms, split re/im {t(lambda: fc.real @ Dm + 1j * (fc.imag @ Dm)):.3f}, "
          f"real@real {t(lambda: fr @ Dm):.3f}, rfft/irfft {t(lambda: np.fft.irfft(np.fft.rfft(fr, axis=-1) * mask, n=N, axis=-1)):.3f}, "
          f"coef->grid {t(lambda: cr @ Bo):.3f}, grid->coef {t(lambda: fr @ So):.3f}, "
          f"cplx elem mul {t(lambda: fc * fc):.3f}, real elem mul {t(lambda: fr * fr):.3f}")
