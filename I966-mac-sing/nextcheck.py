"""#966 next bases: does Re of the pair stay at 262.08? Reading fixed in the README before any new base landed:
at each base, the nearest stable pole of locate off the axis (D_im > 0.05) within 0.05 of P1 = 262.0810 +- 0.9729i in
D_re and D_im, and the root test within 5% of |D0 - P1|. Exit 0 when every base given passes, 1 otherwise.
--mutate=move moves P1 by 0.1 in D_re, which must give exit 1.
    python nextcheck.py LOCATE.json [LOCATE.json ...] [--mutate=move]"""
import json, sys
P1 = complex(262.0810 + (0.1 if "--mutate=move" in sys.argv else 0.0), 0.9729)
ok_all, n = True, 0
for f in [a for a in sys.argv[1:] if a.endswith(".json")]:
    for r in json.load(open(f)):
        n += 1
        p = next((q for q in r["pade"] if q["D_im"] > 0.05), None)
        d = abs(P1 - r["D0"])
        near = p is not None and abs(p["D_re"] - P1.real) <= 0.05 and abs(p["D_im"] - P1.imag) <= 0.05
        root = abs(r["root_radius"] / d - 1) <= 0.05
        ok_all &= near and root
        print(f"D0 {r['D0']:.4f}: nearest stable pole off the axis "
              + (f"{p['D_re']:.4f} +- {p['D_im']:.4f}i (n {p['n']})" if p else "none")
              + f" -> {'at P1' if near else 'NOT at P1'}; root test {r['root_radius']:.4f}, |D0 - P1| {d:.4f}, "
              f"{r['root_radius'] / d - 1:+.2%} -> {'match' if root else 'NO match'}")
print(f"{n} bases: {'PASS, Re stays at 262.08' if ok_all and n else 'FAIL'}"
      + (" (--mutate=move)" if "--mutate=move" in sys.argv else ""))
sys.exit(0 if ok_all and n else 1)
