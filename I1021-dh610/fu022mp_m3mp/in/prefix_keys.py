"""#1013 recount4, criterion 4 read independently of argcount_samebits.py: (a) recount3's cache is recount4's first lines
byte for byte; (b) every key of recount3 that has a later record in recount4, with what each record is (valued3, the
10 sigma guard, the fu variant). Exit 0 when (a) holds and every later record of an old key is an accepted fu row for a
point that recount3 had without a usable value (not valued3, or guard-blocked), or an argcount --retry record
for a point that recount3 had not valued3 (the first form of this script left that case out). --mutate=edit changes one digit of an
old line in memory, which must fail (a)."""
import json, sys
old = open(sys.argv[1]).read().splitlines(); new = open(sys.argv[2]).read().splitlines()
if "--mutate=edit" in sys.argv:
    new = list(new); new[100] = new[100].replace("1", "2", 1)
pre = new[:len(old)] == old
key = lambda r: (round(r["A"], 12), round(r["wf"], 12))
v3 = lambda r: (isinstance(r.get("info"), float) and r["info"] < 1e-8) or bool((r.get("fix") or {}).get("ok"))
guard = lambda r: abs(complex(r["re"], r["im"])) < 10 * r.get("sig", 0.0) or r.get("ymax", 0.0) > 100
O = {}
for l in old:
    r = json.loads(l); O[key(r)] = r
bad = 0
for i, l in enumerate(new[len(old):], len(old) + 1):
    r = json.loads(l); k = key(r)
    if k in O:
        o = O[k]
        okk = ("fu" in r and (not v3(o) or guard(o))) or ("fu" not in r and not v3(o))   # an accepted fu row, or
        # argcount --retry computing again a point that had no value (its first form left this case out)
        bad += not okk
        print(f"line {i}: old key {k}: old record valued3 {v3(o)}, guard-blocked {guard(o)} "
              f"(|R|/sigma {abs(complex(o['re'], o['im'])) / o['sig'] if o.get('sig') else float('nan'):.3g}); new record {'fu ' + str(r['fu']) if 'fu' in r else 'argcount --retry, valued3 ' + str(v3(r))}, "
              f"|R|/sigma {abs(complex(r['re'], r['im'])) / r['sig'] if r.get('sig') else float('nan'):.3g}: {'expected' if okk else 'UNEXPECTED'}")
print(f"(a) recount3's {len(old)} lines are recount4's first lines: {pre}; later records of old keys not expected: {bad}")
print("criterion 4 read as prefix and keys:", "PASS" if pre and not bad else "FAIL")
sys.exit(0 if pre and not bad else 1)
