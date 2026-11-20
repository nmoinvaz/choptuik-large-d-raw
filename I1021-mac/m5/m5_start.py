"""#1021: the start of one M = 5 fixed-(A, w) solve at a located M = 3 zero: the zero (located at xi1 R1) from a
relocation's count file, and its M = 3 harmonics x3 = (-2 Im F3, 2 Re F3) from the record of the located point in
that run's cache (the last record there). Prints "A W B3 C3". --r1b takes the zero located at the second radius
(located_r1b) instead; CACHE is then that radius's cache.
    python m5_start.py COUNT.json CACHE [--r1b]"""
import json, sys
key = "located_r1b" if "--r1b" in sys.argv else "located"
c = json.load(open(sys.argv[1]))
zs = [z for z in c["zeros"] if z.get(key)]
if len(zs) != 1:
    raise SystemExit(f"{len(zs)} zeros with '{key}' in {sys.argv[1]}, not 1")
z = zs[0][key]
rec = None
for l in open(sys.argv[2]):
    r = json.loads(l)
    if (round(r["A"], 12), round(r["wf"], 12)) == (round(z["A"], 12), round(z["wf"], 12)):
        rec = r
if rec is None:
    raise SystemExit("the located point has no record in the cache")
print(f"{z['A']:.12f} {z['wf']:.12f} {-2 * rec['F3im']:.10f} {2 * rec['F3re']:.10f}")
