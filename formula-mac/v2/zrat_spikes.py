# Do the Z-rat (12,12) fits that match the points stay smooth between them? Evaluate on a fine grid 3.0005-70 and
# compare with the Z-poly K=32 fit (a smooth reference that also matches the points): max |difference| by range.
import numpy as np
import common as C, forms as F
D, H, L, s, run = C.data()
g = np.r_[np.linspace(3.0005, 3.04375, 200), np.linspace(3.04375, 4, 2000), np.linspace(4, 10, 3000), np.linspace(10, 70, 12000)]
evp, ip = F.fit_zeta_poly_arb(D, H, L, s, 32, ns0=-11.0); P = evp(g); P = P[0] + P[1]
for ns in (-9.0, -11.0, -13.0):
    ev, info = F.fit_zeta_rat_arb(D, H, L, s, (12, 12), ns0=ns); Z = ev(g); Z = Z[0] + Z[1]
    zp = info['poles_zeta']; real_in = [float(z.real) for z in zp if abs(z.imag) < 1e-9 and 0 < z.real < 1]
    Dp = [2 + ((1 - ns) * (z + 1 / z) / 2 + 1 + ns) / 2 for z in real_in]
    out = []
    for a, b in [(3.0005, 3.04375), (3.04375, 4), (4, 10), (10, 70)]:
        m = (g >= a) & (g <= b); out.append(f'{a:g}-{b:g}: {np.nanmax(np.abs(Z[m] - P[m])):.1e}')
    print(f'Z-rat (12,12) ns {ns:g}: real poles in 0<zeta<1 at D = {np.round(Dp, 4)} | max |Z-rat - Z-poly32| ' + '  '.join(out))
