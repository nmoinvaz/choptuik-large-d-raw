"""#1078 check 3: of the K smallest scaled float64 pivots of a mode_scale.py --small=K row, how many lie below 1e-15 (and 1e-12, 1e-9), and in which blocks.

    python3 small_count.py modescale_small200.jsonl [--mutate=thr]     |     python3 small_count.py selftest
Blocks as small_map.where: p1, c0, 'node a' (field p, m, a, c), m_h, a_h; a node's fields are grouped per node. If every one of the K pivots is below a threshold the count is censored
(at least K). selftest: planted pivots (known blocks, known counts per threshold) must read as written; --mutate=thr (the threshold read as 1e-12 for the 1e-15 count) must exit 1."""
import json
import sys
from collections import Counter

sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
import small_map as SM  # noqa: E402

MUT = next((a.split("=", 1)[1] for a in sys.argv if a.startswith("--mutate=")), None)
THR = (1e-15, 1e-12, 1e-9)


def count(small, M, K=21):
    out = {}
    for t in THR:
        tt = 1e-12 if (MUT == "thr" and t == 1e-15) else t
        sel = [(i, v) for i, v in small if abs(v) < tt]
        blocks = Counter()
        for i, _ in sel:
            blk, f, j = SM.where(i, M, K)
            blocks[blk + (f"/{f}" if f else "")] += 1
        out[t] = (len(sel), len(sel) == len(small), blocks, (min((SM.where(i, M, K)[2] for i, _ in sel), default=None), max((SM.where(i, M, K)[2] for i, _ in sel), default=None)))
    return out


def selftest():
    M = 96
    a_h = 8352
    planted = [[a_h + 10, 3e-19], [a_h + 11, 5e-17], [8256 + 3, 4e-14], [192 + 5, 2e-10], [192 + 384 * 4 + 96 + 7, 8e-8]]
    c = count(planted, M)
    ok = (c[1e-15][0] == 2 and c[1e-12][0] == 3 and c[1e-9][0] == 4 and not c[1e-15][1]
          and dict(c[1e-15][2]) == {"horizon data a_h": 2} and dict(c[1e-9][2]) == {"horizon data a_h": 2, "horizon data m_h": 1, "node 0/p": 1})
    all_below = count([[a_h + 1, 1e-18], [a_h + 2, 2e-18]], M)
    ok2 = all_below[1e-15][1] is True
    print(f"selftest{' --mutate=thr' if MUT else ''}: planted counts {[c[t][0] for t in THR]} (want [2, 3, 4]): {'PASS' if ok else 'FAIL'}; censored when all are below: {'PASS' if ok2 else 'FAIL'}")
    return 0 if ok and ok2 else 1


if __name__ == "__main__":
    if sys.argv[1:2] == ["selftest"]:
        sys.exit(selftest())
    for line in open(sys.argv[1]):
        r = json.loads(line)
        K = r["n"] // (4 * r["M"]) - 1                      # nodes: n = 4 M (K + 1)
        c = count(r["small"], r["M"], K)
        Ks = len(r["small"])
        print(f"lambda {r['lam']}, n {r['n']}: the {Ks} smallest scaled float64 pivots span (K = {K} nodes) {min(abs(v) for _, v in r['small']):.3e} .. {max(abs(v) for _, v in r['small']):.3e} (scaled pmin {r['pmin']:.3e}, pmax {r['pmax']:.3e})")
        for t in THR:
            n, cens, blocks, jr = c[t]
            print(f"  below {t:g}: {n}{' (censored: all ' + str(Ks) + ' are below, so at least ' + str(Ks) if cens else ''}{')' if cens else ''}; by block {dict(blocks)}; grid points j {jr[0]} .. {jr[1]}")
