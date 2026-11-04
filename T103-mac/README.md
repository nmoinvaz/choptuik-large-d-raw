# T103-mac: replica of T99's pilot (b), sigma_0..22 (K 45) at wf 1.00, J 1500, 1280 bits: the cross-machine control of the sigma_22 campaign

Machine: mac (Apple M5, 4 physical cores, 32 GB), checkout ~/Source/choptuik-t83 (9e669de, amp_flint_par.py identical to main's), venv ~/Source/choptuik-large-d/.venv.
Comms entry: 2026-11-03 13:40 UTC cloud to mac
Command: nice -n 10 python -u amp_flint_par.py 1.0 45 1500 1280 --procs 2 --fit phys --mf 6:12 --fit-step 1
Started 2026-11-03 13:42 UTC.

Stopped 2026-11-04 00:40 UTC by the runner under the cloud 23:18 rule (used swap over 16 GB, 16884 MB), last line "k 41" at 37410 s (order 42 under way), run clock about 10 h 58 min. No JSON written. A hp release build in choptuik-anm (not the runner's) pushed swap from 11.6 to 16.9 GB in 5 minutes. A stopped replica is recorded, not replaced.

Relaunch 2026-11-04 01:18 UTC from scratch per the cloud 2026-11-04 01:18 entry. The first start (2026-11-03 13:42 UTC) was stopped at k 41 (37410 s) on the 16 GB swap rule, its log is w1.0000_stopped_k41.log. The relaunch writes w1.0000.log and the JSON.
