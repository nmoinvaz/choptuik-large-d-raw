"""#903: p_min at each base of the fixed-order chain (its log's `step N: D x, pivots a..b` lines) against #603's chain at the
same D, ln p_603 interpolated linearly in D between #603's bases (I603-win2 chain, chain_nat, chain_ns, chain_nsr logs).
    python3 compare_903.py RAW CHAIN.log"""
import math
import re
import sys

raw, log = sys.argv[1], sys.argv[2]
pat = re.compile(r"^step (\d+): D ([0-9.]+), pivots ([0-9.e+-]+)\.\.")
ref = {}
for f in ("chain", "chain_nat", "chain_ns", "chain_nsr"):
    for line in open(f"{raw}/I603-win2/{f}.log"):
        m = pat.match(line)
        if m:
            ref[float(m.group(2))] = float(m.group(3))
xs = sorted(ref)


def p603(D):
    if D < xs[0] or D > xs[-1]:
        return None
    for a, b in zip(xs, xs[1:]):
        if a <= D <= b:
            t = (D - a) / (b - a) if b > a else 0.0
            return math.exp((1 - t) * math.log(ref[a]) + t * math.log(ref[b]))
    return ref[xs[-1]]


print(f"#603 reference: {len(xs)} bases, D {xs[0]:.5f}..{xs[-1]:.5f}")
print("step  D              p_min (fixed)  p_min (#603, interp.)  ln(p_fixed/p_603)")
for line in open(log):
    m = pat.match(line)
    if m:
        D, p = float(m.group(2)), float(m.group(3))
        q = p603(D)
        print(f"{int(m.group(1)):>4}  {D:<13.6f}  {p:.1e}        {q:.2e}                {math.log(p / q):+.2f}" if q else
              f"{int(m.group(1)):>4}  {D:<13.6f}  {p:.1e}        -")
