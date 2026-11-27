"""#1102: ellrs's block 12 of a state at lambda, saved (dump) or compared bit for bit with a saved one (compare): a later
build against one already checked against DDEll.
usage: rs_dump.py MATTER_DIR dump|compare STUB STATE D LAM NPZ [THREADS]"""
import sys, time
sys.path.insert(0, sys.argv[1])
import numpy as np
from ell_fastm import load_system
import ell_b12rs, ellrs
import ddnp as dd
mode, stub, st, D, lam, f = sys.argv[2], sys.argv[3], sys.argv[4], float(sys.argv[5]), float(sys.argv[6]), sys.argv[7]
T = int(sys.argv[8]) if len(sys.argv) > 8 else 0
S, z, rec, same, msg = load_system(stub, st, D)
print(msg, flush=True)
R = ell_b12rs.RsB12(S, threads=T)
t0 = time.time()
Tr, V = R.block12(z, lam)
print(f"k_c {S.kc} lambda {lam}: ellrs ({ellrs.isa()}, products {R.R.gemm}, {R.R.threads} threads) {time.time() - t0:.1f} s", flush=True)
if mode == "dump":
    np.savez(f, th=Tr.h, tl=Tr.l, vh=V.h, vl=V.l)
    sys.exit(0)
o = np.load(f)
c = ell_b12rs.compare(Tr, dd.R(o["th"], o["tl"]))
cv = ell_b12rs.compare(V, dd.R(o["vh"], o["vl"]))
ok = c["same"] == c["n"] and cv["same"] == cv["n"]
print(f"against {f}: tangents {c['same']} of {c['n']}, end values {cv['same']} of {cv['n']} bit for bit: {'PASS' if ok else 'FAIL'}", flush=True)
sys.exit(0 if ok else 1)
