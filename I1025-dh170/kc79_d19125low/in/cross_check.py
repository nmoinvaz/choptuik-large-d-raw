"""#1025 lower_root, lane A (D 18.5, k_c 63, the Mac's state sol_l1kc63Wm1025_D18.5000.npy): two cross-machine checks against the Mac's own D 18.5 data on that state.
overlap: each lambda of lane A that the Mac's file also holds at D (1.20 is in I1025-mac/d18/d18_refsign_1025.jsonl) must have the same hybrid sign and both
points noise-robust (exit 1 otherwise); the ln|det| difference is printed and flagged above 1e-6 (information, no exit).
seam: lane A's highest lambda against the Mac's scan (I1025-mac/d18/d185_scan_1025.jsonl, 1.55 to 1.90) at its lowest lambda: equal signs = no change is needed
between them (information: an odd number of changes in the gap if they differ; the Mac's 1.55 to 1.61 are all minus).
usage: cross_check_mac.py LANE_SCAN.jsonl MAC_FILE.jsonl D {overlap|seam} | cross_check_mac.py selftest (planted equal rows pass; a planted sign flip exits 1;
a planted ln|det| shift of 1e-3 is flagged and exits 0; the seam reports equal and differing signs)"""
import sys, json
K = lambda x: round(x, 4)
def overlap(A, M, D):
    a = {K(r["lam"]): r for r in A if r["D"] == D}; m = {K(r["lam"]): r for r in M if r["D"] == D}
    ks = sorted(k for k in a if k in m)
    bad = [k for k in ks if a[k]["sign"] != m[k]["sign"] or not (a[k]["noise_robust"] and m[k]["noise_robust"])]
    flag = [k for k in ks if abs(a[k]["ln"] - m[k]["ln"]) > 1e-6]
    return ks, bad, flag, {k: a[k]["ln"] - m[k]["ln"] for k in ks}
def seam(A, M, D):
    a = max((r for r in A if r["D"] == D), key=lambda r: r["lam"]); m = min((r for r in M if r["D"] == D and r["lam"] > a["lam"] + 1e-9), key=lambda r: r["lam"])
    return a["lam"], a["sign"], m["lam"], m["sign"]
def selftest():
    mk = lambda l, s=-1.0, ln=-1896.0: dict(D=18.5, lam=l, sign=s, ln=ln, noise_robust=True)
    M = [mk(1.2, -1.0, -1896.5871419008333), mk(2.6, -1.0, -1880.07)]
    ok = overlap([mk(1.2, -1.0, -1896.5871419008333), mk(1.22)], M, 18.5)
    fl = overlap([mk(1.2, 1.0, -1896.5871419008333)], M, 18.5)
    sh = overlap([mk(1.2, -1.0, -1896.5871419008333 + 1e-3)], M, 18.5)
    s1 = seam([mk(1.52), mk(1.54, -1.0)], [mk(1.55, -1.0), mk(1.56, -1.0)], 18.5); s2 = seam([mk(1.54, 1.0)], [mk(1.55, -1.0)], 18.5)
    good = ok[0] == [1.2] and ok[1] == [] and fl[1] == [1.2] and sh[1] == [] and sh[2] == [1.2] and s1 == (1.54, -1.0, 1.55, -1.0) and s2 == (1.54, 1.0, 1.55, -1.0)
    print(f"selftest: equal {ok[1:3]}, sign flip {fl[1]}, shift {sh[2]}, seam {s1[1] == s1[3]} and {s2[1] == s2[3]} -> {'PASS' if good else 'FAIL'}"); sys.exit(0 if good else 1)
if __name__ == "__main__":
    if sys.argv[1] == "selftest":
        selftest()
    ld = lambda p: [json.loads(l) for l in open(p) if l.strip()]
    A, M, D = ld(sys.argv[1]), ld(sys.argv[2]), float(sys.argv[3])
    if sys.argv[4] == "overlap":
        ks, bad, flag, dl = overlap(A, M, D)
        print(f"cross-machine overlap at D {D}: lambda {ks}; sign or robustness differs at {bad or 'none'}; ln difference {dl}; above 1e-6 at {flag or 'none'} -> {'PASS' if ks and not bad else 'FAIL'}")
        sys.exit(0 if ks and not bad else 1)
    la, sa, lm, sm = seam(A, M, D)
    print(f"seam at D {D}: lane A's highest lambda {la:.3f} sign {'+' if sa > 0 else '-'}; the Mac's lowest above it {lm:.3f} sign {'+' if sm > 0 else '-'} -> "
          f"{'equal: an even number of changes in the gap (information)' if sa == sm else 'DIFFERENT: an odd number of changes in the gap (information)'}")
