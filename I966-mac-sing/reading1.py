"""#966 reading (1), fixed in the README at 2026-11-21 14:49:34 UTC: over the next three new bases after 262.3756, the
real stable Pade pole's Re (locate's real stable pole nearest the base, D_im <= 0.05) lies within 0.01 of its mean.
    python reading1.py LOCATE_D*.json ... [--mutate=shift]
Only bases with D0 > 262.3756 count, the first three in order of D. Exit 0 when three bases meet it, 1 when three
bases do not (or a base has no real stable pole), 3 while fewer than three have landed. --mutate=shift adds 0.02 to
the first counted base's Re, which must give exit 1 once three bases have landed."""
import json, statistics, sys
shift = "--mutate=shift" in sys.argv
R = sorted((json.load(open(f))[0] for f in sys.argv[1:] if f.endswith(".json")), key=lambda r: r["D0"])
R = [r for r in R if r["D0"] > 262.3756 + 1e-6][:3]
xs = []
for i, r in enumerate(R):
    q = min((p for p in r["pade"] if p["D_im"] <= 0.05), key=lambda p: abs(p["D_re"] - r["D0"]), default=None)
    x = None if q is None else q["D_re"] + (0.02 if shift and i == 0 else 0.0)
    xs.append(x)
    print(f"D0 {r['D0']:.4f}: real stable pole " + (f"{x:.4f} (n {q['n']})" if q else "none"))
if len(R) < 3:
    print(f"{len(R)} of 3 bases landed: reading (1) pending" + (" (--mutate=shift)" if shift else ""))
    sys.exit(3)
if any(x is None for x in xs):
    print("a base has no real stable pole: reading (1) NOT met" + (" (--mutate=shift)" if shift else ""))
    sys.exit(1)
m = statistics.mean(xs); dev = max(abs(x - m) for x in xs)
ok = dev <= 0.01
print(f"mean {m:.4f}, largest |Re - mean| {dev:.4f} (bound 0.01): reading (1) {'MET: a real singularity near D ' + format(m, '.3f') + ' is read, type unknown' if ok else 'NOT met'}"
      + (" (--mutate=shift)" if shift else ""))
sys.exit(0 if ok else 1)
