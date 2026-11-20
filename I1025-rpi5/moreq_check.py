"""#1025 more random Q at D 12.5 and 13: python3 moreq_check.py [--mutate=signs|logabs|nq]
Compares signtest_moreq_D<D>.log (--nq=12) with the nq=3 lines of signtest_lowD.jsonl (criteria: signtest_moreq_criteria.log of
raw I1025-mac, xfkappa). Per D and lambda: (1) the first 4 signs and logabs equal the nq=3 line's (reported: exact or the difference);
(2) all 13 signs agree; (3) the two lambda have opposite signs. Exit 0 only if all hold for both D.
--mutate=signs flips one of the first 4 signs, =logabs adds 1 to logabs, =nq drops the last sign: each must make the check fail (exit 1)."""
import json, sys
mut = next((a.split("=")[1] for a in sys.argv[1:] if a.startswith("--mutate=")), None)
here = __file__.rsplit("/", 1)[0] if "/" in __file__ else "."
base = {}
for l in open(f"{here}/signtest_lowD.jsonl"):
    r = json.loads(l)
    if "state" in r:
        base[(r["D"], round(r["lam"], 12))] = r
ok = True
for D in (12.5, 13.0):
    name = "12.5" if D == 12.5 else "13"
    lines = [json.loads(l) for l in open(f"{here}/signtest_moreq_D{name}.log") if l.startswith("{")]
    sys_ok = [r for r in lines if "system_check" in r]
    rows = [r for r in lines if "state" in r]
    print(f"D {name}: system check same={[r['same'] for r in sys_ok]}; {len(rows)} lambda lines")
    if len(rows) != 2:
        ok = False; print("  expected 2 lambda lines"); continue
    first = []
    for r in rows:
        b = base[(D, round(r["lam"], 12))]
        sg, la = list(r["signs"]), r["logabs"]
        if mut == "signs": sg[0] = -sg[0]
        if mut == "logabs": la += 1.0
        if mut == "nq": sg = sg[:-1]
        c1 = sg[:4] == b["signs"] and la == b["logabs"]
        c2 = len(sg) == 13 and len(set(sg)) == 1
        first.append(sg[0])
        print(f"  lam {r['lam']:.7f}: n signs {len(sg)}, first 4 = nq3 line {sg[:4] == b['signs']}, logabs {la!r} vs {b['logabs']!r} "
              f"(diff {la - b['logabs']:.3g}), all agree {c2}, agree flag {r['agree']}, n_below_1e_12 {r['n_below_1e_12']} (nq3 {b['n_below_1e_12']}), sec {r['sec']}")
        ok = ok and c1 and c2
    c3 = len(first) == 2 and first[0] != first[1]
    print(f"  opposite signs between the two lambda: {c3}")
    ok = ok and c3
print("check", "PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)
