"""#1021: one point through f_M3 of the argcount at CODE, alone, seeded with the known zero's F_3 (what argcount's
count passes with an empty cache), logging noise_3 at every _floor3 call (each start, each march step, the final
one) and each _refine3 end; BOUNDS (JSON) go to f_M3 as args[4], and SIGALRM at BOUND_S + 60 s is a backstop.
    python onepoint_cap.py CODE A WF R1 BOUNDS BOUND_S"""
import json, signal, sys, time, traceback
import numpy as np
code = sys.argv[1]
sys.path.insert(0, code + "/solver/inner_stokes")
import argcount as ac
p = (float(sys.argv[2]), float(sys.argv[3]))
r1run, bounds, bound = float(sys.argv[4]), json.loads(sys.argv[5]), int(sys.argv[6])
z = (2.7264758856 / 2j) * (0.0532 + 0.0041j)
seed = (float(z.real), float(z.imag))
print(f"point A {p[0]!r} wf {p[1]!r} seed {seed!r}; xi1 {r1run}, bounds {bounds}", flush=True)
T0 = time.time()
fl, ref = ac._floor3, ac._refine3


def floor3(I_, A, wf, v, rr, *a, **k):
    out = fl(I_, A, wf, v, rr, *a, **k)
    print(f"{time.time() - T0:8.1f} s  noise3 at xi1 {rr}: {float(np.max(out[2:])):.4g}  max|v| {np.abs(v).max():.4g}", flush=True)
    return out


def refine3(I_, A, wf, v, rr, **k):
    out = ref(I_, A, wf, v, rr, **k)
    print(f"{time.time() - T0:8.1f} s  _refine3 at xi1 {rr}: |r3| {np.abs(out[1][2:]).max():.4g}", flush=True)
    return out


ac._floor3, ac._refine3 = floor3, refine3


def alarm(*_):
    print(f"{time.time() - T0:8.1f} s  BOUND {bound} s reached; stack:", flush=True)
    traceback.print_stack()
    sys.exit(3)


signal.signal(signal.SIGALRM, alarm)
signal.alarm(bound + 60)
res = ac.f_M3((p, seed, r1run, True, bounds))
print(f"{time.time() - T0:8.1f} s  f_M3 returned: {res[:7]}  fix {res[7] if len(res) > 7 else None}", flush=True)
