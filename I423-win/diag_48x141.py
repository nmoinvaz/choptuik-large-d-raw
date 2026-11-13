#!/usr/bin/env python3
"""#423: where does rt_sigma.py's start crash on the 48x141 state (native access violation after the header line)? Runs the steps of rt_sigma.main() one by one with prints.
usage: OPENBLAS_NUM_THREADS=2 python -X faulthandler diag_48x141.py [STATE] [LU]      (cwd = the worktree root; LU = 0 skips the LU step)
Steps: (1) RT(D, Nt, N) and RTmp, (2) the residual in arb, (3) rt.jacobian (the f64 Jacobian), (4) mps.LUdd of it. Each step prints its time and the process's working set."""
import ctypes
import ctypes.wintypes as wt
import os
import sys
import time

here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, here)
import rt_launch  # noqa: E402,F401  (supplies multidouble._dd_dot and math.fma)

sys.path.insert(0, os.path.join(os.getcwd(), "solver", "rt"))
import numpy as np  # noqa: E402
import flint  # noqa: E402
from rt_model import RT  # noqa: E402
from rt_mp import RTmp  # noqa: E402
import rt_mpsolve as mps  # noqa: E402


class PMC(ctypes.Structure):
    _fields_ = [("cb", wt.DWORD), ("PageFaultCount", wt.DWORD), ("PeakWorkingSetSize", ctypes.c_size_t), ("WorkingSetSize", ctypes.c_size_t),
                ("QuotaPeakPagedPoolUsage", ctypes.c_size_t), ("QuotaPagedPoolUsage", ctypes.c_size_t), ("QuotaPeakNonPagedPoolUsage", ctypes.c_size_t),
                ("QuotaNonPagedPoolUsage", ctypes.c_size_t), ("PagefileUsage", ctypes.c_size_t), ("PeakPagefileUsage", ctypes.c_size_t)]


def mem():
    c = PMC()
    c.cb = ctypes.sizeof(c)
    ctypes.windll.psapi.GetProcessMemoryInfo(ctypes.windll.kernel32.GetCurrentProcess(), ctypes.byref(c), c.cb)
    return f"ws {c.WorkingSetSize / 2**30:.2f} GB, peak ws {c.PeakWorkingSetSize / 2**30:.2f} GB, commit {c.PagefileUsage / 2**30:.2f} GB"


state = sys.argv[1] if len(sys.argv) > 1 else r"C:\Users\nathan\Source\choptuik-large-d-raw-stage\I145-mac\controls\nt_48x141_D40.0201_48x141.npz"
do_lu = not (len(sys.argv) > 2 and sys.argv[2] == "0")
flint.ctx.prec = 192
d = np.load(state)
D, Nt, N = float(d["D"]), int(d["Nt"]), int(d["N"])
t0 = time.time()
rt = RT(D, Nt, N, horizon=0)
rm = RTmp(D, Nt, N, prec=192, horizon=0)
print(f"(1) RT and RTmp built: L {rt.L}, {time.time() - t0:.1f} s, {mem()}", flush=True)
z = mps.from_dd(d["zh"], d["zl"])
t0 = time.time()
F = rm.residual_m(z)
print(f"(2) residual_m: max|F| {mps.amax(F):.2e}, {time.time() - t0:.1f} s, {mem()}", flush=True)
t0 = time.time()
J = rt.jacobian(mps.to_f64(z))
print(f"(3) rt.jacobian: shape {J.shape}, dtype {J.dtype}, {J.nbytes / 2**30:.2f} GB, contiguous {J.flags['C_CONTIGUOUS']}, {time.time() - t0:.1f} s, {mem()}", flush=True)
if do_lu:
    t0 = time.time()
    P = mps.LUdd(J, overwrite=True)
    print(f"(4) LUdd done in {time.time() - t0:.1f} s, {mem()}", flush=True)
print("diag done", flush=True)
