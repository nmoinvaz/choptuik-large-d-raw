"""#1025 D 18 (A), information: the scan's sign changes, an estimate in each bracket (det linear in lambda between the two
grid points, det = sign exp(ln - ln_ref)), delta = lambda - lambda_0(D) at the brackets' ends and the estimates, float64
against the hybrid, and the hionly control against the full dd M.
usage: d18_scan_place.py SCAN.jsonl ROOT.jsonl DDM.jsonl D WT_MATTER"""
import sys, json
import numpy as np

scan, rootf, ddmf, D, wt = sys.argv[1], sys.argv[2], sys.argv[3], float(sys.argv[4]), sys.argv[5]
sys.path.insert(0, wt)
import ell_delta

Ds, L0 = ell_delta.lam0_table()
l0, l0e = ell_delta.lam0_at(D, Ds, L0)
print(f"lambda_0({D:g}) = {l0:.10f} (interpolation error {l0e:.1e}, ell_delta.lam0_at)")
S = sorted((json.loads(l) for l in open(scan)), key=lambda r: r["lam"])
ref = max(r["ln"] for r in S)
print(f"scan: {len(S)} points, {S[0]['lam']:.2f} to {S[-1]['lam']:.2f}; not noise-robust: "
      f"{[r['lam'] for r in S if not r['noise_robust']] or 'none'}")
ch = [(a, b) for a, b in zip(S, S[1:]) if a["sign"] != b["sign"]]
print(f"hybrid sign changes: {len(ch)}")
for a, b in ch:
    fa, fb = a["sign"] * np.exp(a["ln"] - ref), b["sign"] * np.exp(b["ln"] - ref)
    est = a["lam"] + (b["lam"] - a["lam"]) * fa / (fa - fb)
    print(f"  bracket ({a['lam']:.2f}, {b['lam']:.2f}): delta ({a['lam'] - l0:+.6f}, {b['lam'] - l0:+.6f}); "
          f"det-linear estimate {est:.6f}, delta {est - l0:+.6f}")
R = json.loads(open(rootf).readlines()[-1])
inb = [(a["lam"], b["lam"]) for a, b in ch if a["lam"] < R["lam"] < b["lam"]]
print(f"bisected root (information only) {R['lam']:.10f}, delta {R['lam'] - l0:+.6f}, inside {inb or 'no bracket'}")
fc = [(a["lam"], b["lam"]) for a, b in zip(S, S[1:]) if a["f64_sign"] != b["f64_sign"]]
dis = [r["lam"] for r in S if r["f64_sign"] != r["sign"]]
print(f"float64 sign changes: {len(fc)} in {fc}; float64 differs from the hybrid at {len(dis)} of {len(S)} points: {dis}")
M = {}
for l in open(ddmf):
    r = json.loads(l)
    M[(r["lam"], r["mutate"])] = r
for lam in sorted({k[0] for k in M}):
    f, h = M.get((lam, None)), M.get((lam, "hionly"))
    if not (f and h):
        continue
    fl, hl = [v["ln"] for v in f["dd"]], [v["ln"] for v in h["dd"]]
    print(f"lam {lam}: full dd signs {sorted(set(v['sign'] for v in f['dd']))} ln {np.mean(fl):.10f} spread "
          f"{max(fl) - min(fl):.1e}; hionly signs {sorted(set(v['sign'] for v in h['dd']))} ln {np.mean(hl):.10f} spread "
          f"{max(hl) - min(hl):.1e}; hionly - full {np.mean(hl) - np.mean(fl):+.4f}")
