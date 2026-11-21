"""#966 diagnostic, not one of the criteria: from signs966 lines, the sign runs of Delta's c_k (the first and last runs,
cut by the ends, dropped), the angle pi/(mean run) of a conjugate pair that would give them, and with the root test at
k = N (r) the point D0 + r cos(angle) +- i r sin(angle). A rough reading, not a validated estimator."""
import math, re, sys
for l in open(sys.argv[1]):
    m = re.match(r"D0 (\S+) N (\d+) signs (\S+)  root test k \S+: (.*)", l)
    D0, sg, r = float(m.group(1)), m.group(3), float(m.group(4).split()[-1])
    runs = [len(x.group()) for x in re.finditer(r"\++|-+", sg)][1:-1]
    mr = sum(runs) / len(runs)
    th = math.pi / mr
    print(f"D0 {D0:.4f}: inner runs {runs}, mean {mr:.2f}, angle {math.degrees(th):.1f} deg; root test r {r:.3f}; "
          f"point {D0 + r * math.cos(th):.2f} +- {r * math.sin(th):.2f}i")
