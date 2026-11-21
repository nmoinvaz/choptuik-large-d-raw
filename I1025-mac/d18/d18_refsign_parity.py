"""#1025, after the sign-convention check, information: per k_c 63 state, the hybrid signs at the references 1.20 and 2.60 beside
the ends of that state's own scans and the robust changes inside them (each state's own signs, no comparison across D), and the
parity of the root count each gap then implies: (1.20, scan start), (scan end, 2.60), and (1.20, 2.60) in all.
usage: d18_refsign_parity.py REFS.jsonl D:SCAN.jsonl[+SCAN2...],...   (a D without scans: D:)"""
import sys, os, json
sys.argv, A = [sys.argv[0], "x"], sys.argv[1:]
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import d185_scan_read as rd
import d18d_read as dr
sg = lambda s: "+" if s > 0 else "-"
ref = {}
for r in map(json.loads, open(A[0])):
    ref.setdefault(r["D"], {})[round(r["lam"], 2)] = r
par = lambda a, b: "even" if a == b else "odd"
for item in A[1].split(","):
    D, fs = item.split(":"); D = float(D)
    a, b = ref[D][1.2], ref[D][2.6]
    head = f"D {D:g}: 1.20 {sg(a['sign'])}, 2.60 {sg(b['sign'])}; (1.20, 2.60) {par(a['sign'], b['sign'])}"
    if not fs:
        print(head + "; no scan"); continue
    S, rep = dr.merge([json.loads(l) for f in fs.split("+") for l in open(f)])
    rob, non = rd.changes(S)
    lo, hi = S[0], S[-1]
    print(head + f"; scan {lo['lam']:.2f} {sg(lo['sign'])} to {hi['lam']:.2f} {sg(hi['sign'])}, {len(rob)} robust changes "
          f"{[c['br'] for c in rob]}{', non-robust ' + str([c['br'] for c in non]) if non else ''}; "
          f"(1.20, {lo['lam']:.2f}) {par(a['sign'], lo['sign'])}, ({hi['lam']:.2f}, 2.60) {par(hi['sign'], b['sign'])}")
