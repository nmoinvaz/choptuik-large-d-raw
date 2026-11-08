"""I70 job 3 pre-check (macm3): modecount_cx under the running interpreter. One determinant of the D 61 M 32 kf 13 seed state at lambda = 0.3, compared bit for bit with
I160-macm3's cache record of the same point (made on Python 3.13 with the modecount_cx built then).
    python3 smoke_cx.py            (from the repository root)
Exit 0: lnabs, arg, pmin and pmax equal the record. Exit 1: they differ. A control that must differ: lambda = 0.3000001."""
import json, os, sys
sys.path.insert(0, "hp")
from modecount_common import setup
st = setup("hp/data/seeds/local/up23_D61.0264.npz", M=32, kf=13, fmax=1e-15)
ref = None
for ln in open("../choptuik-large-d-raw/I160-macm3/data/modecount_D61.0264_M32_kf13_evals.jsonl"):
    r = json.loads(ln)
    if r["re"] == 0.3 and r["im"] == 0.0:
        ref = r
la, arg, pmin, pmax = st.det(0.3, 0.0)
print(f"python {sys.version.split()[0]}  lnabs {la!r}  arg {arg!r}  pmin {pmin!r}  pmax {pmax!r}")
print(f"record  lnabs {ref['lnabs']!r}  arg {ref['arg']!r}  pmin {ref['pmin']!r}  pmax {ref['pmax']!r}")
same = (la, arg, pmin, pmax) == (ref["lnabs"], ref["arg"], ref["pmin"], ref["pmax"])
la2, arg2, pmin2, pmax2 = st.det(0.3000001, 0.0)
ctl = (la2, arg2) != (ref["lnabs"], ref["arg"])
print("bit-identical to the record:", same, "| control (lambda 0.3000001) differs:", ctl)
sys.exit(0 if same and ctl else 1)
