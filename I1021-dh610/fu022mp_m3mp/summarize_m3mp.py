#!/usr/bin/env python3
"""#1076 fu022mp_m3mp (dh610) summarize_m3mp.py COUNT.json LEAVES.jsonl CACHE.jsonl [LOG] | selftest PASS3_COUNT PASS2_COUNT [--mutate]
Prints what the coordinator asked for: the unresolved count, the zeros (leaf_sum, the located points at xi1 0.17 and 0.2), the boxes, and the extended-precision rows of the cache (fu = "mp": valued or not) with the per-point seconds that argcount --m3mp prints
into the log ("point A .. wf ..: extended precision, |R|/sigma_mp .., valued|NOT valued, N s"). Rows after the first 3605 lines of the pass 3 cache are this run's. No number is typed by hand.
selftest: the pass 3 count file of macm3 (raw I1021-macm3/fu022mp/m3/count_M3_fu022mp_pass3_r0.17.json) must read as the pass 3 comment says (17 unresolved, leaf_sum 2, 2 zeros, 533 leaves, 174 splits, 3465 points) and the pass 2 file (17, leaf_sum 1,
518 leaves, 169 splits, 3345 points) must not; --mutate reads pass 2 where pass 3 is wanted, which must make the selftest exit 1."""
import sys, json, re, statistics

BASE = 3605


def counts(c):
    return dict(unresolved=len(c["unresolved"]), leaf_sum=c["leaf_sum"], zeros=len(c["zeros"]), nleaves=c["nleaves"], splits=c["splits"], npoints=c["npoints"])


def selftest(p3, p2, mutate):
    a = json.load(open(p2 if mutate else p3)); b = json.load(open(p2))
    want3 = dict(unresolved=17, leaf_sum=2, zeros=2, nleaves=533, splits=174, npoints=3465)
    want2 = dict(unresolved=17, leaf_sum=1, zeros=1, nleaves=518, splits=169, npoints=3345)
    bad = 0
    for name, got, want in (("pass 3 file reads as the pass 3 comment" + (" (mutated: pass 2 file given)" if mutate else ""), counts(a), want3), ("pass 2 file reads as the pass 2 comment", counts(b), want2)):
        ok = got == want
        bad += not ok
        print(f"  {name}: {got}: {'ok' if ok else 'WRONG, wanted ' + str(want)}")
    print("selftest" + (" --mutate" if mutate else ""), "FAIL" if bad else "PASS")
    return 1 if bad else 0


if __name__ == "__main__":
    if sys.argv[1] == "selftest":
        sys.exit(selftest(sys.argv[2], sys.argv[3], "--mutate" in sys.argv))
    cf, lf, pf = sys.argv[1:4]
    log = sys.argv[4] if len(sys.argv) > 4 else None
    c = json.load(open(cf))
    print(f"count file: {cf}")
    print(f"unresolved leaves {len(c['unresolved'])}, leaves {c['nleaves']}, splits {c['splits']}, points {c['npoints']}, leaf_sum {c['leaf_sum']}, boundary winding {c['boundary_winding']}, argcount seconds {c['sec']:.0f}, zeros {len(c['zeros'])}")
    print("unresolved cells (A0, A1, wf0, wf1):")
    for u in c["unresolved"]:
        print("   " + ", ".join(f"{x:.8g}" for x in u))
    print("zeros:")
    for z in c["zeros"]:
        l, l2 = z.get("located"), z.get("located_r1b")
        f = lambda q: "none" if not q else f"A {q['A']:.6f}, wf {q['wf']:.6f} (|F| {q['absF']:.4g}, floor {q['floor']:.4g}, sign {q['sign']:+d})"
        print(f"   cell A {z['cell'][0]:.6f} to {z['cell'][1]:.6f}, wf {z['cell'][2]:.8f} to {z['cell'][3]:.8f}, W {z['W']}; xi1 0.17: {f(l)}; xi1 0.2: {f(l2)}")
    print("| box A | box wf | boundary winding | leaf_sum | unresolved |")
    print("|---|---|---|---|---|")
    for b in c["boxes"]:
        (a0, a1), (w0, w1) = b["box"]
        print(f"| {a0:.6f} to {a1:.6f} | {w0:.5f} to {w1:.5f} | {b['boundary_winding']:.3g} | {b['leaf_sum']} | {b['unresolved']} |")
    L = [json.loads(l) for l in open(lf)]
    print(f"leaves file: {len(L)} leaves, ok False in {sum(1 for l in L if not l['ok'])}, depth up to {max(l['depth'] for l in L)}")
    R = [json.loads(l) for l in open(pf)]
    new = R[BASE:]
    mp = [r for r in new if r.get("fu") == "mp"]
    plain = [r for r in new if "fu" not in r]
    ok64 = lambda r: (isinstance(r.get("info"), float) and r["info"] < 1e-8) or bool((r.get("fix") or {}).get("ok"))
    print(f"cache: {len(R)} lines; after the first {BASE}: {len(new)} rows: {len(mp)} fu mp rows ({sum(1 for r in mp if r.get('valued'))} valued, {sum(1 for r in mp if not r.get('valued'))} not valued), {len(plain)} argcount rows (tuned in float64: {sum(1 for r in plain if ok64(r))})")
    if log:
        T = [(float(m[0]), float(m[1]), m[2], m[3], int(m[4])) for m in re.findall(r"point A ([\d.]+) wf ([\d.]+): extended precision, \|R\|/sigma_mp (\S+), (valued|NOT valued), (\d+) s", open(log).read())]
        if T:
            s = [t[4] for t in T]
            print(f"log: {len(T)} extended-precision points, {sum(1 for t in T if t[3] == 'valued')} valued, {sum(1 for t in T if t[3] != 'valued')} NOT valued; seconds per point (one worker each): min {min(s)}, median {statistics.median(s):.0f}, max {max(s)}, sum {sum(s)}")
            for t in T:
                print(f"   A {t[0]:.7f} wf {t[1]:.8f}: |R|/sigma_mp {t[2]}, {t[3]}, {t[4]} s")
        else:
            print("log: no extended-precision point line yet")
