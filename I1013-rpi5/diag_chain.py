"""#1013 step 4 diagnosis: does M = 3's inner solve (argcount.f_M3, xi1 0.2) converge along a continuation from the known zero out to A 3.6?
    python3 diag_chain.py WF A_END STEP OUT.jsonl [R1 (default 0.2)]
Each point is seeded with the previous converged point's tuned F_3 (the first with the known zero's formula, as argcount does), and the chain
stops after 3 points in a row with |r_3| >= 1e-8. One record per point: A, wf, r3 (or the exception text), tuned F_3, max |Y|, sigma, |R|, valid
(= argcount's rule: |r_3| < 1e-8, max |Y| <= 100, |R| >= 10 sigma), seconds. Run with the venv python from anywhere."""
import json, sys, time, math
sys.path.insert(0, "/home/nathan/Source/cl-995/solver/inner_stokes")
import argcount
wf, aend, step, out = float(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3]), sys.argv[4]
A0 = 2.7264758856
F3 = ((A0 / 2j) * (0.0532 + 0.0041j)); F3 = (F3.real, F3.imag)
A, bad = A0, 0
r1 = float(sys.argv[5]) if len(sys.argv) > 5 else 0.2
fh = open(out, "a")
while A <= aend + 1e-9:
    t = time.time()
    r = argcount.f_M3((((A, wf)), F3, r1))
    dt = time.time() - t
    Rv = complex(r[0], r[1])
    ok3 = isinstance(r[2], float) and r[2] < 1e-8
    valid = ok3 and r[5] <= 100 and abs(Rv) >= 10 * r[6]
    rec = dict(A=A, wf=wf, r3=r[2], F3re=r[3], F3im=r[4], ymax=r[5], sig=r[6], absR=(abs(Rv) if ok3 else None), valid=bool(valid), sec=round(dt, 1))
    fh.write(json.dumps(rec) + "\n"); fh.flush(); print(rec, flush=True)
    if ok3:
        F3, bad = (r[3], r[4]), 0       # seed the next point with this one's tuned F_3
    else:
        bad += 1
        if bad >= 3: print("3 failures in a row: stop"); break
    A += step
