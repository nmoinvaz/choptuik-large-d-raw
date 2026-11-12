#!/usr/bin/env python3
"""#543 follow-up (not an acceptance): which mode each sigma is, along the ladder. ladder_543.py's single-law fits fail (equilibrated rms about 1.4 over 0.66 to 0.76 and 4.0 over 0.66 to 0.80) because the sigma index
stops naming one mode at x_last >= 0.74. This reads, from the near_null logs, each sigma's share of the norm in Delta ("delta share") and its top (block, harmonic) components, classifies the mode, and fits the smooth regime alone.
usage: python modes_543.py [--selftest]       (run from I543-win2 after the lanes; needs ../I537-win2/)
Classes: D (delta share >= 0.9: the Delta direction), H3 (delta share < 0.01 and the top component harmonic 3), H1 (the top component harmonic 1, delta share below 0.9), other.
Fits (not the acceptance of #543): ln sigma of the mode tracked as 'the H1 mode with the largest delta share, or the D mode where one exists' (the old sigma_3) against x_last over the smooth regime 0.66 to 0.72, by a + b x and a + b ln x.
--selftest: the classification of planted log lines."""
import math, os, re, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
LAY = [(0.66, HERE, "last066"), (0.68, HERE, "last068"), (0.69, HERE, "last069"), (0.70, os.path.join(HERE, "..", "I537-win2"), "base"), (0.71, HERE, "last071"), (0.72, os.path.join(HERE, "..", "I537-win2"), "last072"),
       (0.74, HERE, "last074"), (0.76, HERE, "last076"), (0.80, HERE, "last080")]
PAT = re.compile(r"^\s+sigma_(\d) ([0-9.e+-]+) \(converged to [0-9e.+-]*\); delta share ([0-9.e+-]+); blocks .*?; top (\S+ k(\d+))", re.M)


def classify(share, kh):
    if share >= 0.9:
        return "D"
    if share < 0.01 and kh == 3:
        return "H3"
    if kh == 1:
        return "H1"
    return "other"


def parse(path):
    return [(int(m.group(1)), float(m.group(2)), float(m.group(3)), int(m.group(5))) for m in PAT.finditer(open(path, encoding="utf-8").read())]


def selftest():
    ok = (classify(1.0, 1) == "D" and classify(2.9e-4, 3) == "H3" and classify(0.7, 1) == "H1" and classify(0.3, 1) == "H1" and classify(0.5, 2) == "other" and classify(0.95, 3) == "D")
    line = "  sigma_3 4.392e-26 (converged to 5e-16); delta share 7.0e-01; blocks p1 0.07, m_h 0.05, node4.p 0.03; top p1 k1 0.07, m_h k1 0.05"
    m = PAT.search(line)
    ok = ok and m and int(m.group(1)) == 3 and abs(float(m.group(2)) - 4.392e-26) < 1e-30 and abs(float(m.group(3)) - 0.7) < 1e-9 and int(m.group(5)) == 1
    print("selftest: ok" if ok else "selftest FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    print("| x_last | sigma_1 (class, delta share) | sigma_2 | sigma_3 | sigma_4 |\n|---|---|---|---|---|")
    track = {}
    for x, d, tag in LAY:
        rows = parse(os.path.join(d, f"nn_{tag}.log"))
        cells = []
        for i, s, sh, kh in rows:
            cells.append(f"{s:.3e} ({classify(sh, kh)}, {sh:.1e})")
        print(f"| {x:.2f} | " + " | ".join(cells) + " |")
        cand = [(sh, s) for i, s, sh, kh in rows if classify(sh, kh) in ("D", "H1") and sh >= 0.5]
        track[x] = max(cand)[1] if cand else float("nan")
    print("\nthe tracked mode (the sigma of the largest delta share among D and H1 modes with share >= 0.5, i.e. the old sigma_3), raw:")
    print("| x_last | sigma | ln sigma | change of ln sigma per 0.01 of x_last from the previous layout |\n|---|---|---|---|")
    prev = None
    for x, d, tag in LAY:
        v = math.log(track[x])
        per = "" if prev is None else f"{(v - prev[1]) / ((x - prev[0]) * 100):+.2f}"
        print(f"| {x:.2f} | {track[x]:.3e} | {v:.2f} | {per} |")
        prev = (x, v)
    xs = np.array([x for x, _, _ in LAY if x <= 0.72 + 1e-9])
    y = np.array([math.log(track[x]) for x in xs])
    print("\nfits of the tracked mode's raw ln sigma over the smooth regime x_last 0.66 to 0.72 (6 points), not the acceptance:")
    for form, X in (("a + b x", np.column_stack([np.ones_like(xs), xs])), ("a + b ln x", np.column_stack([np.ones_like(xs), np.log(xs)])), ("a + b x + c x^2", np.column_stack([np.ones_like(xs), xs, xs ** 2]))):
        beta = np.linalg.lstsq(X, y, rcond=None)[0]
        res = y - X @ beta
        print(f"  {form}: coefficients {', '.join(f'{b:+.3f}' for b in beta)}, rms residual {math.sqrt(np.mean(res ** 2)):.4f}")
