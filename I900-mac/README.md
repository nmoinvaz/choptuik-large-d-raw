# I900-mac: the cross term of a start off the root is linear in the offset (D 240.1244)

Machine: mac (Apple M5), agent xfchecks. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/900

Code: wip/xf-900 (main 1dee59e4, #884's 6118a8be, and ea36b6c0, `truth_restep.py blend`), on main 3c35f0c's hpkernel,
from the choptuik-large-d-900 worktree. One process at nice 10, 3 kernel threads, OPENBLAS_NUM_THREADS=1 (`run.sh`).
Runs in `queue.sh` order, after I884-mac's queue.

The starts are z_s = u2 + s (truth − u2), with u2 #874's I874-mac/anm_pin3_D240.1244_u2.npz and the truth
I603-win2/chain/anm_pin3_D240.1244.npz, made in eight parts by `truth_restep.py blend` (`blend_s<s>.log`) for s = 1/2,
1/4 and 1. Each is saved with the truth's meta and plan and read with the truth's held values (#884), so all three are
in the truth's system. At s = 1 the blend equals the truth (max|z − B| 0.0 in `blend_s1.log`).

From each start, one `step_spread.py` run steps the unperturbed state and seeds 1 and 3 at rel 1e-85 on the Δ block
(`dl_D240_s<s>.json`), as #857 did. `cross.py` reads the odd part L and the even part n of the two seeds' returns,
as `I857-mac/tables.py` does, and c = L − 1 of the stored truth from #857's runs (+8.324447e-02).

Deferred, before any step_spread run: the coordinator stopped the queue on 2026-11-16 at 04:03 UTC, pending a
math review of the wall's cause (label blocked). The three blends and their logs are made; the code is on
wip/xf-900 (ea36b6c0), and `queue.sh` is ready to run as written. `cross.py --selftest` passes.

## Criteria (posted on the issue before the runs)

| # | criterion | fails when |
| --- | --- | --- |
| C1 | `cross.py --selftest` passes (planted L − 1 linear in s passes; a part in s² of a tenth of c fails; an s = 1 off the truth's L by 1e-9 fails), and `cross.py --mutate swap` (s = 1/2 read as 1/4 and the reverse) FAILS | the check misreads a planted case or the control passes |
| C2 | the planted s = 1: `--ref` passes (the truth's dΔ −4.3765436014297066e-58), and L equals the truth's L from #857 to 1e-12 of it | the blend or its system differs from the truth's |
| C3 | the prediction: (L − 1) / (s c) within 1% of 1 for s = 1/2 and s = 1/4 | either is off by more than 1% |
| C4 | reported: n at each s, and the fit L − 1 = c1 s + c2 s² through s = 1/2 and 1, with its value at 1/4 | (reported) |
