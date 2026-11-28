#!/usr/bin/env python3
"""#1109 stage 1c on macm3: the three roots' records (r0, w01, w10 .jsonl; .exit; .out): robust bracket, status, root, bar 1, root - root(r0).
Run from this folder: python3 roots_summary.py [DIR]   (writes nothing; redirect to roots_summary.txt).
       python3 roots_summary.py --selftest             (planted records: bar 1 must pass at +5e-6, fail at +2e-5 and at -2e-5, and
                                                        give no verdict when r0 has no root record)"""
import json, os, sys, tempfile

REF = 0.0455917189     # mm5's refined root of R0 (#1109 comment 7233613794, stage 1c2 B, --b12=rust)
BAR1 = 1e-5
NAMES = ("r0", "w01", "w10")
DELTA = {"w01": -1.957e-4, "w10": -1.956e-3}   # Delta shift of each state along R0's weak vector (the order's numbers, for reading only)


def load(d, n):
    p = os.path.join(d, f"{n}.jsonl")
    rs = [json.loads(l) for l in open(p) if l.strip()] if os.path.exists(p) else []
    ev = [e for e in rs if e.get("kind") != "root"]
    fin = [e for e in rs if e.get("kind") == "root"]
    ex = os.path.join(d, f"{n}.exit")
    rc = int(open(ex).read().strip()) if os.path.exists(ex) else None
    return ev, fin, rc


def report(d, out=print):
    roots = {}
    for n in NAMES:
        ev, fin, rc = load(d, n)
        pos = [e["lam"] for e in ev if e["sign"] > 0 and e.get("robust")]
        neg = [e["lam"] for e in ev if e["sign"] < 0 and e.get("robust")]
        br = f"robust bracket [{max(pos)!r}, {min(neg)!r}] width {min(neg) - max(pos):.4e}" if pos and neg else "no robust sign change yet"
        tail = (f"status {fin[-1]['status']} ({fin[-1].get('why')}), lam_lin {fin[-1]['lam_lin']!r}, {fin[-1]['sec']} s" if fin
                else "no root record")
        out(f"{n}: exit {rc}; {len(ev)} evaluations; {br}; {tail}")
        for e in sorted(ev, key=lambda e: e["lam"]):
            dln = f"{e['dln']:.2e}" if e.get("dln") is not None else "-"
            out(f"     {e['lam']!r:24} hybrid {int(e['sign']):+d} f64 {int(e['f64_sign']):+d} dln {dln:>9} robust {e['robust']} {e.get('sec')} s")
        roots[n] = fin[-1]["lam_lin"] if fin else None
    ok = None
    if roots["r0"] is not None:
        dd = roots["r0"] - REF
        ok = abs(dd) <= BAR1
        out(f"bar 1: r0 lam_lin - {REF} = {dd:+.4e}; |d| <= {BAR1:g}: {'PASS' if ok else 'FAIL'}")
        for n in ("w01", "w10"):
            if roots[n] is not None:
                sh = roots[n] - roots["r0"]
                ev, fin, _ = load(d, n)
                lo, hi = fin[-1]["bracket"]
                out(f"{n}: lam_lin {roots[n]!r}; {n} - r0 = {sh:+.6e}; final bracket [{lo!r}, {hi!r}] gives {n} - r0 in "
                    f"[{lo - roots['r0']:+.4e}, {hi - roots['r0']:+.4e}]; Delta moved {DELTA[n]:+.3e} along R0's weak vector, "
                    f"root shift / Delta shift = {sh / DELTA[n]:.4f} (bracket {(lo - roots['r0']) / DELTA[n]:.3f} to {(hi - roots['r0']) / DELTA[n]:.3f})")
    return ok


def selftest():
    def planted(d, r0root):
        for n, lo, hi in (("r0", 0.0440, 0.0470), ("w01", 0.0400, 0.0500), ("w10", 0.0350, 0.0550)):
            with open(os.path.join(d, f"{n}.jsonl"), "w") as f:
                f.write(json.dumps({"kind": "eval", "lam": lo, "sign": 1.0, "f64_sign": 1.0, "dln": 1e-6, "robust": True, "sec": 1}) + "\n")
                f.write(json.dumps({"kind": "eval", "lam": hi, "sign": -1.0, "f64_sign": -1.0, "dln": 1e-6, "robust": True, "sec": 1}) + "\n")
                if r0root is not None or n != "r0":
                    f.write(json.dumps({"kind": "root", "status": "tol", "why": "planted", "lam_lin": r0root if n == "r0" else 0.04, "sec": 2,
                                        "bracket": [lo, hi]}) + "\n")
            open(os.path.join(d, f"{n}.exit"), "w").write("0\n")
    res = []
    for r0root, want in ((REF + 5e-6, True), (REF + 2e-5, False), (REF - 2e-5, False), (None, None)):
        with tempfile.TemporaryDirectory() as d:
            planted(d, r0root)
            res.append((r0root, want, report(d, out=lambda s: None)))
    good = all(w == g for _, w, g in res)
    for r0root, want, got in res:
        print(f"planted r0 root {r0root!r}: bar 1 expected {want}, read {got}")
    print("selftest:", "PASS" if good else "FAIL")
    return 0 if good else 1


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    report(sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.abspath(__file__)))
