"""A runner's check for #907 (not in run907.sh): abs(F) of one state with the RK steps frozen from another state, the
same S.residual the walk and width use. usage: python frz907.py RAWROOT CODE_SOLVER_MATTER"""
import sys

import numpy as np

raw, code = sys.argv[1], sys.argv[2]
sys.path.insert(0, code)
from sigdss_solver import make  # noqa: E402

D, EPS, KC = 10.5, 3.33333333333, 15
st = {
    "892end": raw + "/I892-rpi5/walk_up_10.5.npy",
    "897end": raw + "/I897-winb/walk2_up_10.5.npy",
    "907end": raw + "/I907-winb/walk3_up_10.5.npy",
    "jac1": raw + "/I907-winb/jac1_up_10.5.npy",
}
z = {k: np.asarray(np.load(v), float) for k, v in st.items()}
print("state (Delta):", {k: round(float(v[-1]), 9) for k, v in z.items()})
for frozen in ("892end", "897end", "907end"):
    S = make(D, EPS, z[frozen], kc=KC)
    row = {k: float(np.linalg.norm(S.residual(z[k][None, :])[0])) for k in z}
    print("steps frozen from %-6s: abs(F) at " % frozen + ", ".join("%s %.4e" % (k, v) for k, v in row.items()))
