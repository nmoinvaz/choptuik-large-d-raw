"""#966: locate's stable Pade poles of Delta's series with a limit of 6 instead of locate_one's 4 (coordinator,
2026-11-21, from D 263.0929 on, once the 4-pole limit was reached). The same jet_singularity.stable_poles(c, r_max=50)
that locate_one calls, at its DPS; only the slice changes. Information beside the 4-pole list; the readings are unchanged.
    python locate6.py CODE JET.npz [--json OUT]"""
import json, sys
sys.path.insert(0, sys.argv[1])
import mpmath as mp
import jet_singularity as js
mp.mp.dps = js.DPS
Z, m = js.load_jet(sys.argv[2])
c, _ = js.row_series(Z, "delta")
sp = js.stable_poles(c, r_max=50)
D0 = m["D"]
rows = [dict(D_re=D0 + d["s"].real, D_im=d["s"].imag, abs=d["abs"], n=d["n"], spread=d["spread"]) for d in sp[:6]]
print(f"D0 {D0:.4f}: {len(sp)} stable poles in all; the first {len(rows)} (limit 6): "
      + "; ".join(f"{r['D_re']:.4f} +- {r['D_im']:.4f}i (|s| {r['abs']:.3f}, n {r['n']})" for r in rows))
if "--json" in sys.argv:
    json.dump(dict(D0=D0, n_all=len(sp), pade6=rows), open(sys.argv[sys.argv.index("--json") + 1], "w"), indent=1)
