import sys, json, time
sys.path.insert(0, "/home/nathan/Source/cl-995/solver/inner_stokes")
import numpy as np
import nested
RAW = "/home/nathan/Source/choptuik-large-d-raw/I1020-dh610"
Z = {"control": (2.726475885672135, 1.0156030949093042), "minus": (2.59859992115029, 0.22175721241675567),
     "plus": (2.844769136217688, 0.2179638045394524), "newzero": (2.338793487291773, 0.09623779643756343)}
pts = []
for r in ("0.2", "0.25", "0.3", "0.35"):
    for f in (f"{RAW}/m3/points_M3_r{r}.jsonl", f"{RAW}/inputs1013/points_M3_r{r}.jsonl"):
        try:
            pts += [json.loads(l) for l in open(f)]
        except FileNotFoundError:
            pass
for name, (A, wf) in Z.items():
    cand = [p for p in pts if np.isfinite(p.get("F3re", np.nan)) and isinstance(p["info"], float) and p["info"] < 1e-8]
    p = min(cand, key=lambda p: (p["A"] - A) ** 2 + (p["wf"] - wf) ** 2)
    F3 = complex(p["F3re"], p["F3im"])
    for r1 in (0.2, 0.25):
        t = time.time()
        F3n, R, r3 = nested.inner(A, wf, F3, r1)
        print(f"{name} A {A:.6f} wf {wf:.6f} xi1 {r1}: seed from ({p['A']:.4f},{p['wf']:.4f}) F3n {F3n:.10f}  x3 ({-2*F3n.imag:.10f}, {2*F3n.real:.10f})  |r_1| {abs(R):.3e}  |r_3| {r3:.2e}  [{time.time()-t:.0f} s]", flush=True)
