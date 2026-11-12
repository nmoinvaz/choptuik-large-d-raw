"""#468: the check of --save_base's first real run (anm_run.py, de63a118), the coordinator's 031232Z message.

    cd choptuik-i513/hp && python.exe ..\..\choptuik-large-d-raw\I468-win\check_base.py RAW BASE.npz POLISH.log
        [--threads 1] [--held_exact 0|1] [--stored_plan 0|1] [--mutate qd|dd|shift]

The saved eight-part base must (1) load, (2) have the exact sum of its eight parts' last entry (Delta) equal to the
polish log's last `converged, Delta HI LO` within the log's digits (1e-20), and (3) have its pinned max|F| on reload
(PinnedO at the state's own held values, as octo_corrector.py does) within a factor 2 of the polish's last |F|.
--held_exact 0 takes the held values from the state's first two parts, as anm_run.py does without --held_o 1, 1 from
all eight parts. --stored_plan 1 evaluates on the plan stored in the base's meta, as anm_run.py's reload does
(--keep_plan 1); 0 plans again at the state (plan_tol 1e-32), which anm_run.py's comment (#461) says leaves a state ~5e-36
off its own equations. The log's HI is a double printed to 17 decimals, so it is read as float(HI); LO is its second part
(v1 of this script read HI as a decimal, off by up to 5e-18). --mutate qd keeps the first four parts, dd the first two
(check 3 must fail), shift adds 1e-15 to Delta's first part (check 2 must fail). Exits 1 when a check fails."""
import os
import re
import sys

sys.path.insert(0, os.getcwd())
import numpy as np  # noqa: E402
import mpmath as mp  # noqa: E402
from octo_corrector import _delta, load_o, omax, pinned_o  # noqa: E402

args = [a for a in sys.argv[1:] if not a.startswith("--")]
opt = dict(zip(sys.argv[1:], sys.argv[2:]))
raw, base, log = args[0], args[1], args[2]
threads = int(opt.get("--threads", 1))
held_exact = bool(int(opt.get("--held_exact", 0)))
stored_plan = bool(int(opt.get("--stored_plan", 0)))
mutate = opt.get("--mutate", "")
z8, meta = load_o(os.path.join(raw, base))
z8 = [np.array(p, dtype=float) for p in z8]
if mutate == "qd":
    for q in range(4, 8):
        z8[q][:] = 0.0
elif mutate == "dd":
    for q in range(2, 8):
        z8[q][:] = 0.0
elif mutate == "shift":
    z8[0][-1] += 1e-15
print(f"loaded {base}: D {meta['D_str'][:12]}, {len(z8)} parts of {len(z8[0])} entries; mutate '{mutate}', held_exact {int(held_exact)}, stored_plan {int(stored_plan)}", flush=True)
mp.mp.dps = 60
D_sum = _delta(z8)
rows = [re.search(r"on (\d+): \|F\| (\S+) converged, Delta (\d\.\d+) ([+-]\d\.\d+e[+-]\d+)", ln) for ln in open(log, encoding="utf-8", errors="replace")]
last = [m for m in rows if m][-1]
F_log = float(last.group(2))
D_log = mp.mpf(float(last.group(3))) + mp.mpf(last.group(4))
dD = abs(D_sum - D_log)
print(f"Delta, exact sum of the eight parts {mp.nstr(D_sum, 40)}", flush=True)
print(f"Delta, log's float(hi) + lo        {last.group(3)} {last.group(4)}   difference {mp.nstr(dD, 4)} (1e-20 allowed)", flush=True)
s, sp, sq, so = pinned_o(meta, tuple(np.ascontiguousarray(p) for p in z8), threads=threads, held_exact=held_exact)
if stored_plan:
    s.set_segs(meta["segs"])
    print(f"plan: the base's stored plan ({sum(len(sg) - 1 for sg in meta['segs'])} steps)", flush=True)
F = omax(so.residual_o(tuple(np.ascontiguousarray(p) for p in z8)))
ratio = F / F_log
print(f"pinned max|F| on reload {F:.3e}, the polish's last |F| {F_log:.3e}, ratio {ratio:.3g} (0.5 to 2 allowed)", flush=True)
ok2, ok3 = bool(dD < 1e-20), bool(0.5 <= ratio <= 2.0)
print(f"check 2 (Delta within the log's digits): {'PASS' if ok2 else 'FAIL'}; check 3 (reload |F| within a factor 2): {'PASS' if ok3 else 'FAIL'}", flush=True)
sys.exit(0 if ok2 and ok3 else 1)
