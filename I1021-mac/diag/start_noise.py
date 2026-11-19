"""#1021: noise_3 at the start radius of each continuation-valued point of the Mac cache, recomputed from its
replayed seed with argcount 068913b4's own start (nested.inner at the start radius, _refine3, _floor3); --full N
instead runs f_M3 on the first N rows and compares the record with the cache's, bit for bit.
    python start_noise.py CODE CACHE SEEDS OUT.jsonl [--full N] [--from I --to J]"""
import json, sys, time
import numpy as np
code, cache, seeds, out = sys.argv[1:5]
sys.path.insert(0, code + "/solver/inner_stokes")
import argcount as ac
opt = dict(zip(sys.argv[5::2], sys.argv[6::2]))
recs = {}
for line in open(cache):
    r = json.loads(line)
    recs[(r["A"], r["wf"])] = r
rows = [json.loads(l) for l in open(seeds)]
rows = [s for s in rows if (recs[(s["A"], s["wf"])].get("fix") or {}).get("ok")]
I = ac._probe_inner_np()
import nested
if "--full" in opt:
    for s in rows[:int(opt["--full"])]:
        t = time.time()
        r = ac.f_M3(((s["A"], s["wf"]), tuple(s["seed"]), 0.17, True))
        c = recs[(s["A"], s["wf"])]
        same = [r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[7]] == [c["re"], c["im"], c["info"], c["F3re"], c["F3im"], c["ymax"], c["sig"], c["fix"]]
        print(f"line {s['line']} ({s['A']}, {s['wf']}): f_M3 again, {time.time() - t:.0f} s, record bit for bit: {same}", flush=True)
    sys.exit(0)
lo, hi = int(opt.get("--from", 0)), int(opt.get("--to", len(rows)))
with open(out, "a") as fh:
    for s in rows[lo:hi]:
        t, c = time.time(), recs[(s["A"], s["wf"])]
        rs = c["fix"]["trail"][0]
        F3s, _, _ = nested.inner(s["A"], s["wf"], complex(*s["seed"]), rs)
        v = np.array([-2 * F3s.imag, 2 * F3s.real])
        v, r, J = ac._refine3(I, s["A"], s["wf"], v, rs)
        n = float(ac._floor3(I, s["A"], s["wf"], v, rs)[2:].max())
        row = dict(line=s["line"], A=s["A"], wf=s["wf"], start=rs, r3=float(np.abs(r[2:]).max()), noise3=n,
                   accepted=bool(np.abs(r[2:]).max() <= 3 * n), sec=round(time.time() - t, 1))
        fh.write(json.dumps(row) + "\n")
        fh.flush()
