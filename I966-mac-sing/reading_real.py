"""#966: is the real pole near 265.078 on the chain's path? Reading fixed 2026-11-21 18:05:25 UTC (#966 comment
7066990195): two bases in a row with D0 > 263.5 and the root test within 5% of 265.078 - D0 confirm it; the root test
more than 5% above 265.078 - D0 at two bases in a row means it is not there.
    python reading_real.py LOCATE_D*.json ... [--mutate=scale]
Exit 0 confirmed, 1 not there, 3 pending. --mutate=scale multiplies each root test by 1.2, which must read 'not there'
once two bases past 263.5 exist."""
import json, sys
scale = 1.2 if "--mutate=scale" in sys.argv else 1.0
R = sorted((json.load(open(f))[0] for f in sys.argv[1:] if f.endswith(".json")), key=lambda r: r["D0"])
seq = []
for r in R:
    d = 265.078 - r["D0"]; rt = r["root_radius"] * scale; e = rt / d - 1
    past = r["D0"] > 263.5
    tag = ("within 5%" if abs(e) <= 0.05 else "above by more than 5%" if e > 0.05 else "below by more than 5%") if past else "before 263.5, not read"
    print(f"D0 {r['D0']:.4f}: root test {rt:.4f}, 265.078 - D0 {d:.4f}, {e:+.2%}: {tag}")
    if past:
        seq.append("in" if abs(e) <= 0.05 else "above" if e > 0.05 else "below")
code, v = 3, "pending"
for a, b in zip(seq, seq[1:]):
    if a == b == "in":
        code, v = 0, "CONFIRMED: the real pole is on the chain's path"; break
    if a == b == "above":
        code, v = 1, "NOT THERE: the root test stays more than 5% above 265.078 - D0"; break
print(f"reading: {v}" + (" (--mutate=scale)" if scale != 1.0 else ""))
sys.exit(code)
