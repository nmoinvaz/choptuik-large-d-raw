"""#1021: checks of a merged M = 3 points file (argcount_merge.py's OUT) against its sources, before a recount reads it.
SPEC (json) lists the sources in merge order: name, file, the 1-based line ranges with the code that wrote them and
the noise cap that code enforced on every continuation radius (null: none, then the start noise must come from a
replay row of diag/start_noise.py, keyed by its 0-based line), the start_noise files, and for a constructed part the
original file and line of each of its records ("origin"). For the last record of every point of OUT:
  - its source is the first source, in merge order, that holds its line byte for byte (the base for prefix lines);
  - a continuation-valued record passes the cap when its final noise3 <= CAP (1e7) and its start noise3 <= CAP, by
    the code's own cap or by a replay row; a record with neither is unchecked, and fails;
  - a point whose value comes from one source while another holds it without value is listed with both files;
  - points valued in two sources with different records are counted, with the largest |dF3| and |dR|/|R|.
--mutate=noise raises the final noise3 of the first listed cross-source record to 2 CAP: the check must then fail.
    python merge_check.py OUT SPEC [--cap 1e7] [--mutate=noise]       exit 1 on a failed or unchecked record"""
import json, sys

out, spec = sys.argv[1], json.load(open(sys.argv[2]))
opt = dict(zip(sys.argv[3::2], sys.argv[4::2]))
CAP = float(opt.get("--cap", 1e7))
mutate = "--mutate=noise" in sys.argv
pre = len(open(spec["prefix"]).read().splitlines())


def valued(r):
    return (isinstance(r.get("info"), float) and r["info"] < 1e-8) or bool((r.get("fix") or {}).get("ok"))


src = []                                                 # per source: line text -> 1-based line, last record per point
for s in spec["sources"]:
    L = open(s["file"]).read().splitlines()
    first = 1 if s.get("base") else pre + 1
    s["at"] = {}
    for n in range(first, len(L) + 1):
        s["at"].setdefault(L[n - 1], n)
    s["last"] = {}
    for n in range(first, len(L) + 1):
        r = json.loads(L[n - 1])
        s["last"][(r["A"], r["wf"])] = (n, r)
    s["noise"] = {}
    for f in s.get("start_noise", []):
        for l in open(f):
            q = json.loads(l)
            s["noise"][q["line"]] = q
    src.append(s)


def code_of(s, n):
    for lo, hi, code, cap in s["ranges"]:
        if lo <= n <= hi:
            return code, cap
    return None, None


final = {}
for l in open(out).read().splitlines():
    r = json.loads(l)
    final[(r["A"], r["wf"])] = (l, r)
where = {}
for k, (l, r) in final.items():
    for s in src:
        if l in s["at"]:
            where[k] = (s, s["at"][l])
            break
cross = []
for k, (l, r) in final.items():
    if not valued(r) or k not in where:
        continue
    s0, n0 = where[k]
    others = [(s["name"], n) for s in src if s is not s0 and k in s["last"] and not valued(s["last"][k][1])
              for n in [s["last"][k][0]]]
    if others:
        cross.append((k, s0, n0, others))
if mutate and cross:
    k = cross[0][0]
    l, r = final[k]
    final[k] = (l, dict(r, fix=dict(r["fix"], noise3=2 * CAP)))
    print(f"mutate=noise: final noise3 of {k} set to {2 * CAP:g}")
unattributed = [k for k in final if k not in where]
bad, unchecked, by = [], [], {}
mx_end, mx_start = 0.0, 0.0
for k, (l, r) in final.items():
    if not (r.get("fix") or {}).get("ok") or k not in where:
        continue
    s, n = where[k]
    code, cap = code_of(s, n)
    e = r["fix"].get("noise3", float("nan"))
    mx_end = max(mx_end, e)
    if not e <= CAP:
        bad.append((k, s["name"], n, f"final noise3 {e:.3g}"))
    q = s["noise"].get(n - 1)
    if cap is not None and cap <= CAP:
        how = f"in-run cap {cap:g} ({code})"
    elif q is not None and (q["A"], q["wf"]) == k:
        how = "replayed start"
        mx_start = max(mx_start, q["noise3"])
        if not (q["noise3"] <= CAP and q["accepted"]):
            bad.append((k, s["name"], n, f"start noise3 {q['noise3']:.3g}, accepted {q['accepted']}"))
    else:
        how = "unchecked"
        unchecked.append((k, s["name"], n, code))
    by.setdefault((s["name"], how), 0)
    by[(s["name"], how)] += 1
print(f"{out.split('/')[-1]}: {len(final)} points, {sum(valued(r) for _, r in final.values())} valued; "
      f"{len(unattributed)} records not found in any source")
for (name, how), c in sorted(by.items()):
    print(f"  {name}: {c} continuation-valued records, start noise by {how}")
print(f"  largest final noise3 {mx_end:.3g}, largest replayed start noise3 {mx_start:.3g}, cap {CAP:g}")
print(f"points valued in one source and without value in another: {len(cross)}")
for k, s0, n0, others in sorted(cross, key=lambda x: x[0]):
    org = s0.get("origin", {}).get(str(n0))
    r = final[k][1]
    print(f"  ({k[0]}, {k[1]}): value from {'/'.join(s0['file'].split('/')[-3:])} line {n0}"
          + (f" (= {org})" if org else "") + f", code {code_of(s0, n0)[0]}, noise3 {(r.get('fix') or {}).get('noise3', 0):.3g}"
          + f"; without value in " + ", ".join(f"{nm} line {n}" for nm, n in others))
two = []
for k in final:
    vs = [(s["name"], s["last"][k][1]) for s in src if k in s["last"] and valued(s["last"][k][1])]
    if len(vs) > 1 and any(json.dumps(v[1], sort_keys=True) != json.dumps(vs[0][1], sort_keys=True) for v in vs[1:]):
        F = [complex(v[1]["F3re"], v[1]["F3im"]) for v in vs]
        R = [complex(v[1]["re"], v[1]["im"]) for v in vs]
        two.append((k, [v[0] for v in vs], max(abs(f - F[0]) for f in F), max(abs(x - R[0]) / abs(R[0]) for x in R)))
print(f"points valued in two or more sources with different records: {len(two)}"
      + (f"; largest |dF3| {max(t[2] for t in two):.3g}, largest |dR|/|R| {max(t[3] for t in two):.3g}" if two else ""))
for k, names, dF, dR in sorted(two, key=lambda t: -t[3])[:6]:
    print(f"  ({k[0]}, {k[1]}): {', '.join(names)}; |dF3| {dF:.3g}, |dR|/|R| {dR:.3g}")
for k, name, n, why in bad:
    print(f"  CAP FAIL ({k[0]}, {k[1]}) {name} line {n}: {why}")
for k, name, n, code in unchecked[:12]:
    print(f"  UNCHECKED ({k[0]}, {k[1]}) {name} line {n} ({code}): no in-run cap and no replay row")
ok = not bad and not unchecked and not unattributed
print(f"merge check: {'PASS' if ok else 'FAIL'}")
sys.exit(0 if ok else 1)
