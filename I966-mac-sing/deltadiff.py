"""#966: the relative difference of Delta's c_k between two jets at one base, k = 1..N, and the meta 'state' of each."""
import json, sys
sys.path.insert(0, sys.argv[1])
import mpmath as mp
import numpy as np
from jet_singularity import load_jet, row_series
mp.mp.dps = 60
Za, ma = load_jet(sys.argv[2]); Zb, mb = load_jet(sys.argv[3])
ca, _ = row_series(Za, "delta"); cb, _ = row_series(Zb, "delta")
rel = [float(abs(x - y) / abs(y)) for x, y in zip(ca, cb)]
print("states:", ma.get("state"), "|", mb.get("state"))
print("rel diff of Delta's c_k, k 1..N:", " ".join(f"{r:.1e}" for r in rel))
print(f"max over k {max(rel):.2e} at k {int(np.argmax(rel)) + 1}")
