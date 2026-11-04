"""Shared helpers for agent B: state loading, harmonic coordinates, Chebyshev fits in 1/n."""
import glob, json
import numpy as np
R = '/Users/nathan/Source/choptuik-large-d-raw/'
H = '/Users/nathan/Source/choptuik-large-d/hp/data/states/'
M = 32
NODES = [0.3, 0.4, 0.5, 0.6, 0.7]
# z layout: p1, c0 | node (p, m, a, c) x5 | m_h, a_h | Delta; parities from hp/src/model.rs and solver/spec.py
FIELDS = [('ctr', 'p1', 'odd'), ('ctr', 'c0', 'even')]
for i, x in enumerate(NODES):
    FIELDS += [(f'n{x}', 'p', 'odd'), (f'n{x}', 'm', 'odd'), (f'n{x}', 'a', 'even'), (f'n{x}', 'c', 'even')]
FIELDS += [('hor', 'm_h', 'odd'), ('hor', 'a_h', 'even')]
L = 4 * M * 6 + 1
th = np.pi * np.arange(M) / M


def basis(par):
    cols, lab = [], []
    if par == 'odd':
        for k in range(1, M, 2):
            cols.append(np.cos(k * th)); lab.append(('c', k))
            cols.append(np.sin(k * th)); lab.append(('s', k))
    else:
        cols.append(np.ones(M)); lab.append(('c', 0))
        for k in range(2, M, 2):
            cols.append(np.cos(k * th)); lab.append(('c', k))
            cols.append(np.sin(k * th)); lab.append(('s', k))
        cols.append(np.cos(M * th)); lab.append(('c', M))
    return np.array(cols).T, lab


B_ODD, LAB_ODD = basis('odd')
B_EVEN, LAB_EVEN = basis('even')
# full transform: h = T z, z = Tinv h (Delta kept as the last coordinate)
Tinv = np.zeros((L, L)); LABELS = []
for f, (blk, name, par) in enumerate(FIELDS):
    Bm, lab = (B_ODD, LAB_ODD) if par == 'odd' else (B_EVEN, LAB_EVEN)
    Tinv[f * M:(f + 1) * M, f * M:(f + 1) * M] = Bm
    LABELS += [(blk, name, cs, k) for cs, k in lab]
Tinv[-1, -1] = 1.0; LABELS.append(('Delta', 'Delta', '', 0))
T = np.linalg.inv(Tinv)


def load(p):
    d = np.load(p); m = json.loads(str(d['meta']))
    parts = [d['zh'], d['zl']] + ([d['z2'], d['z3']] if 'z2' in d else [np.zeros(L), np.zeros(L)])
    return float(m['D']), parts, m


def zf(parts):
    """float64 value of a four-part state, summed low parts first"""
    return ((parts[3] + parts[2]) + parts[1]) + parts[0]


def train_files(dmin=35.0, dmax=61.1, t12_every=1, t13_every=1):
    fs = sorted(glob.glob(H + 'up*_D*.npz')) + sorted(glob.glob(R + 'T12-win/scratch/t12/up*_D*.npz'))[::t12_every] \
        + sorted(glob.glob(R + 'T13-win/scratch/t13/up*_D*.npz'))[::t13_every]
    out = []
    for p in fs:
        D, parts, m = load(p)
        if dmin <= D <= dmax and m['M'] == 32 and list(m['nodes']) == NODES:
            out.append((D, p))
    out.sort()
    return out


TRUTH = {67.742203: '/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/43f19197-40d3-4ad8-aa26-db5322fa8689/scratchpad/agentB/g_zero67_newton_state.npz',  # qd-converged here from T73/t73/full1_D67.7422.npz
         68.5: R + 'T84-mac/pin5_D68.5000_full.npz',
         69.5: R + 'T84-mac/pin5_D69.5000_full.npz', 70.5: R + 'T84-mac/pin5_D70.5000_full.npz',
         71.0: R + 'T84-mac/pin7_D71.0000_full.npz', 71.5: R + 'T84-mac/pin7_D71.5000_full.npz',
         72.8: R + 'T81/conv_pin7_D72.8000_D72.800000.npz', 73.0: R + 'T81/conv_pin5_D73.0000_D73.000000.npz'}


class Cheb:
    """least squares Chebyshev fit in x = 1/(D-2), mapped to [-1, 1] over [xa, xb]"""
    def __init__(self, Ds, Y, deg, xa=None, xb=None, w=None):
        x = 1.0 / (np.asarray(Ds) - 2)
        self.xa = x.min() if xa is None else xa; self.xb = x.max() if xb is None else xb
        V = np.polynomial.chebyshev.chebvander(self.t(x), deg)
        if w is not None:
            V = V * w[:, None]; Y = Y * w[:, None]
        self.C, *_ = np.linalg.lstsq(V, Y, rcond=None)
        self.deg = deg

    def t(self, x):
        return 2 * (x - self.xa) / (self.xb - self.xa) - 1

    def __call__(self, D):
        x = 1.0 / (np.atleast_1d(np.asarray(D, dtype=float)) - 2)
        return np.polynomial.chebyshev.chebvander(self.t(x), self.deg) @ self.C
