"""#1078: the sign changes of det M(lambda) on the M' 96 state, from two --scan runs of lowD_gamma.py (a: hmax 0.05 plan, unpolished; b: hmax 0.0015, polish 4).
Lists every sign change by position (the bracket of two neighbouring scan points and its midpoint) on each plan, compares the two plans (the same change when the midpoints
are within 1e-5), and says where the roots found by the root searches fall among the changes: M' 96 5.140867320755084 (hmax 0.05, #1072), M' 128 5.140802680792423 (#1072),
M' 160 in (5.140897587455, 5.140902680792) (#1078 step 2, stopped).
usage: scan_signs.py A.jsonl B.jsonl  |  scan_signs.py selftest [--mutate=drop|shift]   (selftest exit 0 only if every planted case reads as written)"""
import json, sys
MUT = next((a.split("=", 1)[1] for a in sys.argv if a.startswith("--mutate=")), None)
args = [a for a in sys.argv[1:] if not a.startswith("--")]
TOL = 1e-5
ROOTS = {"M' 96 (hmax 0.05, #1072)": 5.140867320755084, "M' 128 (#1072)": 5.140802680792423,
         "M' 160 (lower end of its bracket)": 5.140897587455, "M' 160 (upper end of its bracket)": 5.140902680792}


def changes(rows, shift=0.0):
    rows = sorted(rows, key=lambda r: r["lam"])
    if MUT == "drop":
        rows = [r for r in rows if not (r["sign"] < 0 and r["lam"] < 5.14080)]     # control: lost points hide the changes between them
    out = []
    for a, b in zip(rows, rows[1:]):
        if a["sign"] != b["sign"]:
            out.append(dict(lo=a["lam"], hi=b["lam"], mid=0.5 * (a["lam"] + b["lam"]) + shift, frm=a["sign"], to=b["sign"]))
    return out


def compare(ca, cb):
    """pairs of changes of the two plans within TOL (midpoints), the unmatched of each"""
    pairs, used = [], set()
    for x in ca:
        j = next((j for j, y in enumerate(cb) if j not in used and abs(x["mid"] - y["mid"]) <= TOL + 1e-12), None)
        if j is not None:
            used.add(j); pairs.append((x, cb[j]))
    ua = [x for x in ca if not any(x is p[0] for p in pairs)]
    ub = [y for j, y in enumerate(cb) if j not in used]
    return pairs, ua, ub


def selftest():
    mk = lambda lams, f: [dict(lam=l, sign=f(l)) for l in lams]
    lams = [5.14060 + 1e-5 * k for k in range(41)]
    f1 = lambda l: -1.0 if 5.140667 < l < 5.140723 or l > 5.140867 else 1.0      # changes near 5.140667, 5.140723, 5.140867
    f2 = lambda l: -1.0 if 5.140667 < l < 5.140723 or l > 5.140867 else 1.0
    f3 = lambda l: -1.0 if 5.140687 < l < 5.140743 or l > 5.140887 else 1.0      # all three moved by 2e-5
    A, B, C = changes(mk(lams, f1)), changes(mk(lams, f2), shift=2e-5 if MUT == "shift" else 0.0), changes(mk(lams, f3))
    ok = True
    cases = [("three changes found", len(A) == 3, True),
             ("the same plan matches all", len(compare(A, B)[0]) == 3, True),
             ("changes moved by 2e-5 do not match", len(compare(A, C)[0]) == 0, True)]
    for name, got, want in cases:
        print(f"planted: {name}: {got}, expected {want}: {'PASS' if got == want else 'FAIL'}")
        ok &= got == want
    print("selftest:", "PASS" if ok else "FAIL")
    return ok


if args and args[0] == "selftest":
    sys.exit(0 if selftest() else 1)
res = {}
for lab, f in zip("ab", args[:2]):
    rows = [json.loads(l) for l in open(f) if l.strip()]
    rows = [r for r in rows if r.get("scan")]
    res[lab] = rows
    print(f"plan {lab} ({f}): {len(rows)} points, lambda {min(r['lam'] for r in rows):.6f} to {max(r['lam'] for r in rows):.6f}, hmax {rows[0]['hmax']}, |F| of the state {rows[0]['F']:.2e}")
    print("  signs: " + " ".join(("+" if r["sign"] > 0 else "-") for r in sorted(rows, key=lambda r: r["lam"])))
ca, cb = changes(res["a"]), changes(res["b"])
for lab, cs in (("a", ca), ("b", cb)):
    print(f"sign changes on plan {lab}: {len(cs)}")
    for c in cs:
        print(f"  ({c['lo']:.6f}, {c['hi']:.6f}) midpoint {c['mid']:.6f}: {'+' if c['frm'] > 0 else '-'} to {'+' if c['to'] > 0 else '-'}")
pairs, ua, ub = compare(ca, cb)
print(f"matched within {TOL:g}: {len(pairs)}; only on plan a: {len(ua)}; only on plan b: {len(ub)}")
for name, lam in ROOTS.items():
    where = [("a", c) for c in ca if c["lo"] <= lam <= c["hi"]] + [("b", c) for c in cb if c["lo"] <= lam <= c["hi"]]
    near = [f"plan {lab} bracket ({c['lo']:.6f}, {c['hi']:.6f})" for lab, c in where]
    print(f"root {name} {lam!r}: " + (", ".join(near) if near else "inside no sign-change bracket of either plan"))
