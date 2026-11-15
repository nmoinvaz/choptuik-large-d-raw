"""compare the rebuilt lam_gauge.csv with the stored one: bars 1 and 2 of #814"""
import csv, sys, collections
rd = lambda f: list(csv.DictReader(l for l in open(f) if not l.startswith("#")))
old, new = rd(sys.argv[1]), rd(sys.argv[2])
da = {"raw:" + r["state"]: r for r in csv.DictReader(open(sys.argv[3])) if r["state"].strip()}
O = {r["state"]: r for r in old}; N = {r["state"]: r for r in new}
lost = [s for s in O if s not in N]
moved = [s for s in O if s in N and any(O[s][c] != N[s][c] for c in ("lam_g", "Delta", "mu", "D", "D_str"))]
print("stored rows", len(old), "| rebuilt rows", len(new), "| stored states missing from the rebuild:", len(lost),
      "| with lam_g, Delta, mu, D changed:", len(moved))
nm = [s for s in da if s not in N]
noerr = [s for s in da if s in N and (N[s]["Delta_err"], N[s]["Delta_err_kind"]) != (da[s]["err"], da[s]["err_kind"])]
print("states delta_all.csv names:", len(da), "| missing from the rebuild:", len(nm), "| present with a different err pair:", len(noerr))
new_states = [s for s in N if s not in O]
print("new rows:", len(new_states), collections.Counter(s.rsplit("/", 1)[0] for s in new_states).most_common(5))
diff = collections.Counter()
for s in O:
    if s in N:
        for c in O[s]:
            if O[s][c] != N[s][c]:
                diff[c] += 1
print("changed cells on common rows by column:", dict(diff))
rc = collections.Counter((O[s]["role"], N[s]["role"]) for s in O if s in N and O[s]["role"] != N[s]["role"])
print("role changes:", dict(rc))
bbn = [r for r in new if r["role"] == "backbone"]
print("backbone D", len(bbn), "| frontier", bbn[-1]["D"], bbn[-1]["lam_g"][:12], bbn[-1]["state"])
ok = not lost and not moved and not nm and not noerr
print("bars 1 and 2:", "PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)
