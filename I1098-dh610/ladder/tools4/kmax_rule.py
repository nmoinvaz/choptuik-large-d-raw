"""#1098's kmax rule for D >= 2231 (recipe v2 amendment, 2026-11-26): the tail runs to kmax 23 and is extended to h25 when
h23's release took a step (its pending dDelta was above --ddelta) or the fall from h19 to h21 is slow, r = |c21/c19| >
0.05, c_k being harmonic k's change of Delta over its accepted outer steps. Reads a tail's release_ls.jsonl (json only)
and prints c19, c21, r, h23's steps and pending, and the verdict; exit 0 when kmax 23 suffices, 2 when h25 is needed,
1 when the log does not have h19, h21 and h23's release yet.

    python3 kmax_rule.py TAIL/release_ls.jsonl [--k 23] [--rmax 0.05]
"""
import json
import sys
from decimal import Decimal, getcontext


def main():
    a = sys.argv[1:]
    opt = dict(zip(a[1::2], a[2::2]))
    k, rmax = int(opt.get("--k", "23")), float(opt.get("--rmax", "0.05"))
    getcontext().prec = 60
    recs = [json.loads(line) for line in open(a[0]) if line.strip()]
    prev, ch, steps, pend = None, {}, {}, {}
    for r in recs:
        h = r["harm"]
        if r.get("accepted") and "Delta" in r:
            d = Decimal(r["Delta"])
            if prev is not None:
                ch[h] = ch.get(h, Decimal(0)) + d - prev
            prev = d
            steps[h] = steps.get(h, 0) + 1
        if r.get("done"):
            pend[h] = r.get("dDelta_full")
    k1, k2 = k - 4, k - 2
    if k1 not in ch or k2 not in ch or k not in pend:
        print(f"not yet: changes for h{sorted(ch)}, releases for h{sorted(pend)}")
        return 1
    r = abs(ch[k2] / ch[k1])
    st = steps.get(k, 0)
    ext = st > 0 or r > Decimal(str(rmax))
    rem = float(abs(ch[k2]) * r / (1 - r)) if r < 1 else float("inf")
    print(f"c{k1} {float(ch[k1]):+.3e}, c{k2} {float(ch[k2]):+.3e}, r {float(r):.3g} (bar {rmax}), the geometric "
          f"remainder past h{k2} {rem:.2e} (err_tail's, information); h{k}: {st} steps, "
          f"pending {pend[k]:+.2e}: " + (f"extend to h{k + 2}" if ext else f"kmax {k} suffices"))
    return 2 if ext else 0


if __name__ == "__main__":
    sys.exit(main())
