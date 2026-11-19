"""#1013 step 4 diagnosis: how much does R_1 (M = 3, xi1 0.2, nested.inner called directly: argcount withholds R above its |r_3| bar) move between inner solves?
    python3 diag_scatter.py A wf BASE_CHAIN.jsonl BASE_A NSEED SEED0 OUT.jsonl
The solve starts from the tuned F_3 of the chain record at BASE_A (a converged point) times (1 + 1e-3 u), u uniform in (-1, 1) separately
for Re and Im, one random.Random(SEED0 + k) per solve; k = -1 is the unperturbed base. Each record: r3, tuned F_3, R, |R|, phase."""
import json, sys, random, cmath
sys.path.insert(0, "/home/nathan/Source/cl-995/solver/inner_stokes")
import nested
A, wf, chain, base_a, n, seed0, out = float(sys.argv[1]), float(sys.argv[2]), sys.argv[3], float(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6]), sys.argv[7]
rec = [json.loads(l) for l in open(chain)]
b = min(rec, key=lambda r: abs(r["A"] - base_a))
assert abs(b["A"] - base_a) < 1e-3 and b["r3"] < 1e-8, b
fh = open(out, "a")
for k in ([-1] if seed0 == 0 else []) + list(range(seed0, seed0 + n)):
    rng = random.Random(k)
    f = (b["F3re"], b["F3im"]) if k < 0 else (b["F3re"] * (1 + 1e-3 * (2 * rng.random() - 1)), b["F3im"] * (1 + 1e-3 * (2 * rng.random() - 1)))
    F3n, R, r3 = nested.inner(A, wf, complex(*f), 0.2); r = [R.real, R.imag, float(r3), F3n.real, F3n.imag, float("nan"), float("nan")]
    R = complex(r[0], r[1])
    d = dict(k=k, A=A, wf=wf, start_F3=f, r3=r[2], F3re=r[3], F3im=r[4], Rre=R.real, Rim=R.imag, absR=abs(R), phase=cmath.phase(R) if R == R else None, ymax=r[5], sig=r[6])
    fh.write(json.dumps(d, default=float) + "\n"); fh.flush(); print(d, flush=True)
