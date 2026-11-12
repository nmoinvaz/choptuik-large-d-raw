#!/usr/bin/env python3
"""#564 side test on the new states only: does the antiphase structure (no oscillation in the sum, equal and opposite oscillations in the two series) hold in #558's twelve states, which the structure was not found on?
usage: python structure_564.py   (run from I564-win2 after eval_564.py)
For each pair, at the registered M1 period law (predictions_564.json, fitted to the 63 states), over the twelve new states: the oscillation amplitude found in the sum (a quadratic trend + cos phi, sin phi fitted to ln sigma_a + ln sigma_b)
and in the difference (a linear trend + cos phi, sin phi fitted to ln sigma_b - ln sigma_a), and the amplitudes of the two series separately (each with a quadratic trend). Equal opposite oscillations give an amplitude in the sum near 0
and in the difference twice the series'. The linear-in-u parts and the quadratic trends are free here; the period law is not refitted."""
import json, math, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
for p in ("I558-win2", "I557-win2", "I535-win2", "I533-win2", "I525-win2", "I522-win2", "I521-win2", "I505-win2"):
    sys.path.insert(0, os.path.join(HERE, "..", p))
import period_558 as p8  # noqa: E402
import period_p2_533 as m  # noqa: E402
pred = json.load(open(os.path.join(HERE, "predictions_564.json")))
new = p8.collect_new()
D = np.array(sorted(new, reverse=True))
Y = np.array([np.mean(new[d], axis=0) for d in D])
u = (D - 228.0) / 10.0


def amp(y, th, deg):
    ph = m.phase(D, *th)
    X = np.column_stack([u ** k for k in range(deg + 1)] + [np.cos(ph), np.sin(ph)])
    b, *_ = np.linalg.lstsq(X, y, rcond=None)
    e = y - X @ b
    return math.hypot(b[deg + 1], b[deg + 2]), math.sqrt(np.mean(e ** 2)), b


for pair, (ia, ib) in (("12", (0, 1)), ("34", (2, 3))):
    th = pred["models"]["M1"][pair]["theta"]
    ys, yd = Y[:, ia] + Y[:, ib], Y[:, ib] - Y[:, ia]
    A_s, r_s, _ = amp(ys, th, 2)
    A_d, r_d, b = amp(yd, th, 1)
    A_a, r_a, ba = amp(Y[:, ia], th, 2)
    A_b, r_b, bb = amp(Y[:, ib], th, 2)
    sa, sb = np.sign(ba[3]) , np.sign(bb[3])
    print(f"pair sigma_{ia + 1} + sigma_{ib + 1}: amplitude in the sum {A_s:.4f} (rms {r_s:.4f}); in the difference {A_d:.4f} (rms {r_d:.4f}); in sigma_{ia + 1} {A_a:.4f} (rms {r_a:.4f}), in sigma_{ib + 1} {A_b:.4f} (rms {r_b:.4f}); ratio sum / difference {A_s / A_d:.3f}; cos coefficients of the two series {ba[3]:+.4f}, {bb[3]:+.4f}")
