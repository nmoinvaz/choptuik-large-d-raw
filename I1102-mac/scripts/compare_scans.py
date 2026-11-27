"""#1102 check 2: d18_secant scan records with --b12=rust against the default's, lambda by lambda: the hybrid sign, ln|det|
(the difference, 0 when equal to the last bit), the noise members' signs and ln|det|, and the float64 ones.
usage: compare_scans.py RUST.jsonl DDM.jsonl  (exit 0 when every sign agrees and every ln|det| is equal)"""
import json, sys
ld = lambda f: {r["lam"]: r for r in (json.loads(l) for l in open(f) if l.strip())}
a, b = ld(sys.argv[1]), ld(sys.argv[2])
ok = set(a) == set(b) and len(a) > 0
for lam in sorted(a):
    if lam not in b:
        print(f"lambda {lam!r}: no default record"); ok = False; continue
    x, y = a[lam], b[lam]
    same = (x["sign"] == y["sign"] and x["ln"] == y["ln"] and x["noise"] == y["noise"] and x["noise_ln"] == y["noise_ln"]
            and x["f64_sign"] == y["f64_sign"] and x["f64_ln"] == y["f64_ln"])
    ok &= x["sign"] == y["sign"] and x["ln"] == y["ln"]
    print(f"lambda {lam!r}: sign {x['sign']:+.0f} / {y['sign']:+.0f}, ln|det| {x['ln']!r} / {y['ln']!r} (difference "
          f"{x['ln'] - y['ln']:.1e}), noise {x['noise']} / {y['noise']}, robust {x['robust']} / {y['robust']}; every field "
          f"{'equal' if same else 'NOT equal'}; seconds {x['sec']} {x['sec_parts']} / {y['sec']} {y['sec_parts']}")
print(f"check 2: {'PASS' if ok else 'FAIL'}")
sys.exit(0 if ok else 1)
