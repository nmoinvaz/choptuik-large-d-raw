"""#1013: the winding of the unresolved leaves' union in each cell whose boundary winding is an integer, from the
union's own boundary. Read-only from a cache, with argcount's Multiplier and Counter (the code at CODE). A point that
is not in the cache stops the run, so nothing is computed.
    python union_winding.py CODE CACHE LEAVES COUNT [--mutate=conj]
For each box of COUNT with an integer boundary winding and unresolved leaves inside:
  - W(cell) from the cell's own boundary, which must equal COUNT's boundary winding (the control that this reads the
    same values and edges as the count);
  - the union U of the unresolved leaves, which must be a rectangle;
  - W(U) from U's boundary, which must be resolved and equal W(cell) minus the sum of the resolved leaves' W.
Exit 0 when every such box passes, 1 otherwise. --mutate=conj conjugates every value (Multiplier's mutate), so every
winding flips and W(cell) differs from COUNT's: exit 1."""
import json
import sys

code, cache, leaves_f, count_f = sys.argv[1:5]
conj = "--mutate=conj" in sys.argv
sys.path.insert(0, code + "/solver/inner_stokes")
import argcount as ac  # noqa: E402

F = ac.Multiplier(3, cache, 1, r1=0.18, m3fix=True, retry=False, mutate="conj" if conj else None)


def raw(pts):
    miss = [p for p in pts if ac.Multiplier.key(p) not in F.vals]
    if miss:
        raise SystemExit(f"{len(miss)} points not in the cache, e.g. {miss[:3]}: nothing is computed here")


F.raw = raw
C = ac.Counter(F, 0.5, 1e-5)                         # count()'s dphi and hmin
K = json.load(open(count_f))
L = [json.loads(line) for line in open(leaves_f)]
e = 1e-9
ok_all, n = True, 0
for b in K["boxes"]:
    (a0, a1), (w0, w1) = b["box"]
    wb = b["boundary_winding"]
    if wb is None or wb != wb or abs(wb - round(wb)) > 0.1 or not b["unresolved"]:
        continue
    n += 1
    inside = [x for x in L if a0 - e <= x["a0"] and x["a1"] <= a1 + e and w0 - e <= x["w0"] and x["w1"] <= w1 + e]
    res, un = [x for x in inside if x["ok"]], [x for x in inside if not x["ok"]]
    Wc, wcraw, _, _, okc = C.cell(a0, a1, w0, w1)
    U = (min(x["a0"] for x in un), max(x["a1"] for x in un), min(x["w0"] for x in un), max(x["w1"] for x in un))
    rect = abs((U[1] - U[0]) * (U[3] - U[2]) - sum((x["a1"] - x["a0"]) * (x["w1"] - x["w0"]) for x in un)) < 1e-12
    Wu, wuraw, tv, mn, oku = C.cell(*U)
    want = round(wb) - sum(x["W"] for x in res)
    ok = okc and Wc == round(wb) and rect and oku and abs(wuraw - round(wuraw)) < 0.1 and Wu == want
    ok_all &= ok
    print(f"cell A {a0:.4f}-{a1:.4f} w {w0:.4f}-{w1:.4f}: count's winding {wb:.6g}, from its boundary {wcraw:.6g}"
          f" ({'resolved' if okc else 'unresolved'}); {len(res)} resolved leaves, sum {sum(x['W'] for x in res)}; "
          f"{len(un)} unresolved leaves, union A {U[0]:.7f}-{U[1]:.7f} w {U[2]:.8f}-{U[3]:.8f} "
          f"({'a rectangle' if rect else 'not a rectangle'}): W(U) {wuraw:.6g} "
          f"({'resolved' if oku else 'unresolved'}), min |R| on it {mn:.3g}, wanted {want}: {'PASS' if ok else 'FAIL'}")
print(f"{n} cells; union winding check{' (--mutate=conj)' if conj else ''}: {'PASS' if ok_all and n else 'FAIL'}")
sys.exit(0 if ok_all and n else 1)
