"""#1064 (c'): the order arm at D 237.7132, ks 307 against ks 395 (I966-mac-sing README, amendment of 2026-11-21).
    python order_compare.py LOC_K307.json LOC_K395.json [--mutate=move]
Every stable pole of each jet (locate's, up to four, folded to Im >= 0) is listed. Each K 307 pole is paired with the
nearest K 395 pole within 0.05 |s| (locate's clustering tolerance); unpaired poles are "not seen in both" and get no
reading. A paired move (max |dRe|, |dIm|) above 0.01 reads "truncation", else "neither at this resolution". Poles
within 0.1 of P2 258.361 +- 2.269i, P1 262.081 +- 0.973i and the real 265.078 are named. --mutate=move adds 0.02 to
the K 395 pole nearest P2, which must read "truncation" for P2 when P2 is seen."""
import json, sys
mut = "--mutate=move" in sys.argv
A, B = (json.load(open(f))[0] for f in sys.argv[1:3])
NAMES = {"P2": complex(258.361, 2.269), "P1": complex(262.081, 0.973), "real 265.078": complex(265.078, 0.0)}
z = lambda p: complex(p["D_re"], p["D_im"])
def name(p):
    return next((k for k, v in NAMES.items() if abs(z(p) - v) <= 0.1), "")
pa, pb = list(A["pade"]), [dict(p) for p in B["pade"]]
if mut and pb:
    k = min(range(len(pb)), key=lambda i: abs(z(pb[i]) - NAMES["P2"]))
    pb[k]["D_re"] += 0.02
for lab, r, ps in (("K 307", A, pa), ("K 395", B, pb)):
    print(f"{lab}: D0 {r['D0']:.4f}, root test {r['root_radius']:.4f}; stable poles: "
          + ("; ".join(f"{p['D_re']:.4f} +- {p['D_im']:.4f}i (|s| {p['abs']:.3f}, n {p['n']}, spread {p['spread']:.1e}"
                       + (f", {name(p)}" if name(p) else "") + ")" for p in ps) or "none"))
used = set()
for p in pa:
    tol = 0.05 * p["abs"]
    cand = [(abs(z(q) - z(p)), i) for i, q in enumerate(pb) if i not in used and abs(z(q) - z(p)) <= tol]
    if not cand:
        print(f"  {p['D_re']:.4f} +- {p['D_im']:.4f}i{' (' + name(p) + ')' if name(p) else ''}: not seen at K 395, no reading")
        continue
    _, i = min(cand); used.add(i); q = pb[i]
    mv = max(abs(p["D_re"] - q["D_re"]), abs(p["D_im"] - q["D_im"]))
    print(f"  {p['D_re']:.4f} +- {p['D_im']:.4f}i -> {q['D_re']:.4f} +- {q['D_im']:.4f}i{' (' + name(p) + ')' if name(p) else ''}: "
          f"move {mv:.4f}: {'truncation' if mv > 0.01 else 'neither at this resolution'}" + (" (--mutate=move)" if mut else ""))
for i, q in enumerate(pb):
    if i not in used:
        print(f"  {q['D_re']:.4f} +- {q['D_im']:.4f}i{' (' + name(q) + ')' if name(q) else ''}: not seen at K 307, no reading")
for k in NAMES:
    if not any(name(p) == k for p in pa) or not any(name(q) == k for q in pb):
        print(f"  {k}: not seen in both, no reading")
sys.exit(0)
