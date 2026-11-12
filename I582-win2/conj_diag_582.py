"""Diagnostic for the conjugate asymmetry seen by sym_582.py: recompute det at a differing lower point P, at the upper point Q matched to it
(the cached coordinates), at the exact conjugate conj(P), at P again, and at P with Re shifted by 1e-13. Same state and options as the circle runs."""
import glob, json, math, os, sys, time
HP = "D:/choptuik-i573/hp"
os.chdir(HP)
sys.path.insert(0, HP)
from modecount_common import setup
RAW = "D:/choptuik-large-d-raw"


def load(f):
    return [json.loads(l) for l in open(glob.glob(f"{RAW}/{f}/modecount_*_evals.jsonl")[0])]


L = {(r["re"], r["im"]): r for r in load("I582-win2/k27_re2.85_im-1.25")}
U = {(round(r["re"], 9), round(r["im"], 9)): r for r in load("I574-win2/k27_re2.85_im+1.25")}
best = None
for (re_, im), r in L.items():
    u = U.get((round(re_, 9), round(-im, 9)))
    if u and (best is None or abs(r["lnabs"] - u["lnabs"]) > best[0]):
        best = (abs(r["lnabs"] - u["lnabs"]), r, u)
d, r, u = best
P = (r["re"], r["im"])
Q = (u["re"], u["im"])
print(f"P (lower) {P!r}  lnabs {r['lnabs']!r} arg {r['arg']!r}")
print(f"Q (upper) {Q!r}  lnabs {u['lnabs']!r} arg {u['arg']!r}   |dQ-conj(P)| re {abs(Q[0]-P[0]):.3e} im {abs(Q[1]+P[1]):.3e}")
st = setup("data/seeds/local/up23_D61.0264.npz", M=48, threads=1, kf=27, fmax=1e-15, centre_tol=None)
tests = [("P again", P), ("conj(P) exact", (P[0], -P[1])), ("Q again", Q), ("P, Re + 1e-13", (P[0] + 1e-13, P[1])), ("P, Re + 1e-9", (P[0] + 1e-9, P[1]))]
for name, (a, b) in tests:
    t = time.time()
    la, arg, pmin, pmax = st.det(a, b)
    print(f"{name:<16} ({a!r}, {b!r}): lnabs {la!r} arg {arg!r} pmin {pmin:.6e} ({time.time()-t:.0f} s)", flush=True)
