"""The split extrapolation: z_i = w_i + V c_i, V the r leading right singular vectors of a trial fit's residual
(the directions the stored solves leave unconverged); w extrapolated at high degree, c at low degree."""
import numpy as np
from b_lib import Cheb


def unit_weights(Ds):
    w = np.ones(len(Ds))
    for c in np.unique(np.floor(Ds)):
        m = np.floor(Ds) == c; w[m] = 1 / np.sqrt(m.sum())
    return w


def noise_dirs(Ds, Z, r, K0=12, w=None):
    f = Cheb(Ds, Z, K0, w=w); R = Z - f(Ds)
    U, S, Vt = np.linalg.svd(R, full_matrices=False)
    return Vt[:r].T, S


class Split:
    """fit: Ks for w (clean part), Kc for c (junk coordinates; Kc = -1 holds the newest state's c, -2 the mean over
    the newest cluster)"""
    def __init__(self, Ds, Z, r, Ks, Kc, K0=12, w=None, V=None):
        self.V = noise_dirs(Ds, Z, r, K0, w)[0] if V is None else V
        C = Z @ self.V
        W = Z - C @ self.V.T
        self.fw = Cheb(Ds, W, Ks, w=w)
        self.Kc = Kc
        if Kc >= 0:
            self.fc = Cheb(Ds, C, Kc, w=w)
        else:
            o = np.argsort(Ds)
            self.c_hold = C[o[-1]] if Kc == -1 else C[Ds > Ds.max() - 0.5].mean(0)
        self.res_w = np.abs(W - self.fw(Ds)).max()

    def __call__(self, D):
        w = self.fw(D)[0]
        c = self.fc(D)[0] if self.Kc >= 0 else self.c_hold
        return w + self.V @ c, w, c
