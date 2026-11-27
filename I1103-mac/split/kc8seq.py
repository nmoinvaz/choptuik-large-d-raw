"""|dF| of the k_c + 8 embedding (tail of products past k_c), RK x1.07 and N + 25% for each state of a k_c sequence"""
import sys, os, re, json, numpy as np
sys.path.insert(0, "/Users/nathan/Source/choptuik-1103/solver/matter")
import i1103_split as T
out = []
for path in sys.argv[2:]:
    m = re.search(r"kc(\d+)[^_]*_D([0-9.]+)\.npy$", os.path.basename(path)); kc, D = int(m.group(1)), float(m.group(2))
    z = np.load(path); S = T.make(kc, D, z); base = S.freeze_from(z, 0.7); F0 = S.residual(z[None])[0]
    r = dict(state=os.path.basename(path), D=D, kc=kc, F=float(np.linalg.norm(F0)), steps=int(sum(base.values())))
    for dk in (8, 16):
        S8 = T.make(kc + dk, D, z); z8 = S8.regrid_from(z, S); S8.steps_map = dict(base)
        F8 = S8.residual(z8[None])[0]; back = T.restrict(F8, S8, S)
        r[f"dF_kc+{dk}"] = float(np.linalg.norm(back - F0)); r[f"dF_kc+{dk}_blocks"] = T.per_block(S, back - F0)
        r[f"F_new_kc+{dk}"] = float(max(0.0, np.linalg.norm(F8) ** 2 - np.linalg.norm(back) ** 2) ** 0.5)
    S2 = T.make(kc, D, z); S2.steps_map = {k: int(np.ceil(v * 1.07)) for k, v in base.items()}
    r["dF_rk107"] = float(np.linalg.norm(S2.residual(z[None])[0] - F0))
    print(f"{r['state']}: kc {kc} D {D} |F| {r['F']:.2e} steps {r['steps']} | kc+8: |dF| {r['dF_kc+8']:.3e} new {r['F_new_kc+8']:.3e}"
          f" block0 {r['dF_kc+8_blocks'][0]:.1e} block1 {r['dF_kc+8_blocks'][1]:.1e} | kc+16: |dF| {r['dF_kc+16']:.3e} | rk x1.07 {r['dF_rk107']:.2e}", flush=True)
    out.append(r)
json.dump(out, open(sys.argv[1], "w"))
