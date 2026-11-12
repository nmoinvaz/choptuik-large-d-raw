#!/usr/bin/env python3
"""#558: the prediction of sigma_1's period over D 198 to 203.6 (the 12 states D 203.63 to 198.13), written on the issue before the run.
usage: python predict_558.py       (run from I558-win2; needs ../I533-win2/period_p2_533.py, ../I535-win2/period_535.py and the logs they read)
The p2 chirp (P(D) = P0 + p1 x + p2 x^2, x = D - 228, cubic trend) fitted to the 63 equilibrated states D 204.13 to 237.13 (#533's model with #535's twelve states), its period at the centre D 200.88 of the window, with the spread
of a parametric bootstrap (the fit as the truth, white noise at its residual rms, 200 trials); beside it the linear drift (p2 = 0) and the constant period of the same states. Also the periods of sigma_2..4 and the amplitudes.
Acceptance of #558: the measured period (quadratic trend + one sinusoid over the 12 new states, the method of #535) is within 0.05 of the p2 chirp's value."""
import math, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
for p in ("I535-win2", "I533-win2", "I525-win2", "I522-win2", "I521-win2", "I505-win2"):
    sys.path.insert(0, os.path.join(HERE, "..", p))
import period_p2_533 as m  # noqa: E402
import period_535 as p5  # noqa: E402
CENTRE = (198.1312 + 203.6312) / 2
if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    Do, Yo = m.collect51()
    new = p5.collect_new()
    Dn = np.array(sorted(new))
    Yn = np.array([np.mean(new[d], axis=0) for d in Dn])
    Da, Ya = np.concatenate([Dn, Do]), np.concatenate([Yn, Yo])
    print(f"{len(Da)} states D {Da[0]:.4f} to {Da[-1]:.4f}; window centre D {CENTRE:.3f}")
    F = m.Fitter(Da, 3)
    print("| series | p2 chirp: P0, p1, p2 | rms | period at the centre | bootstrap sd | linear drift (p2 = 0) | constant period |\n|---|---|---|---|---|---|---|")
    for i in (1, 2, 3, 4):
        y = Ya[:, i - 1]
        best, f0 = F.fit_free(y)
        cst = F.const(y)
        P = lambda th: th[0] + th[1] * (CENTRE - m.D0) + th[2] * (CENTRE - m.D0) ** 2
        beta, _ = m.lin(Da, y, 3, best["theta"])
        truth = m.columns(Da, 3, m.phase(Da, *best["theta"])) @ beta
        rng = np.random.default_rng(60 + i)
        vals = [P(F.fit_free(truth + rng.normal(0, math.sqrt(best["ss"] / len(Da)), len(Da)))[0]["theta"]) for _ in range(200)]
        th = best["theta"]
        print(f"| sigma_{i} | {th[0]:.4f}, {th[1]:+.5f}, {th[2]:+.6f} | {math.sqrt(best['ss'] / len(Da)):.4f} | {P(th):.3f} | {np.std(vals):.3f} | {P(f0['theta']):.3f} | {cst['theta'][0]:.3f} |", flush=True)
