#!/usr/bin/env python3
"""#1025 winb: planted cases of read_ddB_1025.py (Amendment 3's reading) on row A's hybrid record (D 17.5) and a copy of it with every sign flipped
(row B's orientation). dd records are planted det records (5 agreeing variants, noise signs equal) at root -/+ 0.02."""
import copy, json, os, subprocess, sys, tempfile
HERE = os.path.dirname(os.path.abspath(__file__)).replace("\\", "/")
HJ = HERE + "/I1025-win/p4_highD/ell_p4_hybrid_1025_w_highD.jsonl"
hyb = [json.loads(l) for l in open(HJ) if l.strip() and abs(json.loads(l)["D"] - 17.5) < 1e-9][-1]
root, tmp = hyb["lam"], tempfile.mkdtemp()
def dd(lam, sg, bad=False):
    r = dict(D=17.5, kc=63, lam=lam, dd=[dict(sign=sg, ln=-1930.0, sec=30.0) for _ in range(5)], noise=[dict(eps=e, signs=[sg, sg]) for e in (1e-24, 1e-20, 1e-16)], f64_sign=1.0)
    if bad:
        r["dd"][0]["sign"] = -sg
    fn = f"{tmp}/dd_{lam:.6f}_{sg:+.0f}{'b' if bad else ''}.jsonl"
    open(fn, "w").write(json.dumps(r) + "\n")
    return fn
flip = copy.deepcopy(hyb); flip["evals"] = {k: dict(v, sign=-v["sign"]) for k, v in hyb["evals"].items()}
FJ = tmp + "/hyb_flipped.jsonl"; open(FJ, "w").write(json.dumps(flip) + "\n")
lo, hi = (lambda s, b=False: dd(root - 0.02, s, b)), (lambda s, b=False: dd(root + 0.02, s, b))
cases = [("usual hybrid, dd -/+", lo(-1), hi(1), HJ, "ROOT PASSES"), ("usual hybrid, dd +/-", lo(1), hi(-1), HJ, "DD DISAGREES"),
         ("usual hybrid, dd +/+", lo(1), hi(1), HJ, "NO ROOT BETWEEN THEM"), ("flipped hybrid (row B's orientation), dd +/-", lo(1), hi(-1), FJ, "ROOT PASSES"),
         ("flipped hybrid, dd -/+", lo(-1), hi(1), FJ, "DD DISAGREES"), ("usual hybrid, 5 variants disagree at the upper point", lo(-1), hi(1, True), HJ, "NEITHER READING APPLIES")]
bad = 0
for n, a, b, h, want in cases:
    o = subprocess.run([sys.executable, HERE + "/read_ddB_1025.py", a, b, repr(root), h], capture_output=True, text=True)
    last = (o.stdout.strip().splitlines() or [o.stderr[-200:]])[-1]
    ok = last.startswith("DDREAD: " + want)
    bad += not ok
    print(f"{n}: {last[:130]} [{'ok' if ok else 'WRONG, wanted ' + want}]")
print("selftest", "FAILED" if bad else "passed")
sys.exit(bad)
