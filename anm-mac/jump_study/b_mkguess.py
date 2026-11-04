"""Save the split guesses (r = 4, Ks = 12; Kc = -1 hold, chosen by the holdout; Kc = 3 for comparison) at the truth Ds."""
import numpy as np
from b_lib import *
from b_split import Split, unit_weights
d = np.load('train36.npz'); Ds, Hc = d['Ds'], d['Hc']; Z = Hc @ Tinv.T; w = unit_weights(Ds)
for Kc in (-1, 3):
    sp = Split(Ds, Z, 4, 12, Kc, w=w)
    for Dt in (67.742203, 68.5, 69.5):
        g = sp(Dt)[0]
        np.savez(f'g_split_kc{Kc}_D{Dt:.4f}.npz', g=g)
        print(Kc, Dt, 'saved; Delta', repr(g[-1]))
