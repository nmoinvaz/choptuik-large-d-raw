"""#1021: per cache, the points whose F3 seed differs between the replay without 'fix' (the code that ran) and with it
(6da7da7b), with |dF3| between the two seeds and from each seed to the point's own tuned F3.
    python compare.py W NAME:CACHE [NAME:CACHE ...]   (exit 1 when the control z16 does not differ)"""
import json, sys
W = sys.argv[1]
ctrl_ok = None
for arg in sys.argv[2:]:
    name, cache = arg.split(":", 1)
    a = [json.loads(l) for l in open(f"{W}/{name}.jsonl")]
    b = [json.loads(l) for l in open(f"{W}/{name}_keepfix.jsonl")]
    assert [(x["line"], x["A"], x["wf"]) for x in a] == [(x["line"], x["A"], x["wf"]) for x in b]
    L = [json.loads(l) for l in open(cache)]
    diff = [(x, y) for x, y in zip(a, b) if x["seed"] != y["seed"]]
    print(f"{name}: {len(a)} seeds, {len(diff)} differ")
    for x, y in diff[:12]:
        r = L[x["line"]]
        s0, s1 = complex(*x["seed"]), complex(*y["seed"])
        F = complex(r["F3re"], r["F3im"])
        val = (isinstance(r.get("info"), float) and r["info"] < 1e-8) or bool((r.get("fix") or {}).get("ok"))
        print(f"  line {x['line'] + 1} ({x['A']}, {x['wf']}): seed {s0:.4f} -> {s1:.4f} (|d| {abs(s1 - s0):.3g}); "
              f"own F3 {F:.4f} ({'valued' if val else 'no value'}), |F3 - seed| {abs(F - s0):.3g} as run, "
              f"{abs(F - s1):.3g} with fix")
    if name == "control_z16":
        ctrl_ok = len(diff) > 0
print("control z16: " + ("the seeds differ, as they must" if ctrl_ok else "FAIL: no difference"))
sys.exit(0 if ctrl_ok else 1)
