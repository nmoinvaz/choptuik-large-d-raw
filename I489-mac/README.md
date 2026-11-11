# I489-mac: crawlJ's D 242.3642 state re-noded to layouts ending at x = 0.8, their base polish and weakest directions

Machine: mac (Apple M5), a subagent of the coordinator, 2 threads under nice 10.
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/489 (depends on #488 and #461).

Code: choptuik-large-d main a9b0885 plus `hp/renode_o.py` and `anm_run.py --save_base` (branch `wip/i489-subagent`,
84e4d7f), interpreter venv-314 (Python 3.14, its installed `hpkernel` built 2026-11-08).

Source state: `I461-win2/crawlJ/anm_pin3_D242.3642.npz` (nodes 0.3-0.7, eight parts, crawlJ's plan of 21 steps).

## Re-node, layout 1 (0.3, 0.4, 0.5, 0.6, 0.7, 0.8)

`renode_o.py RAW I461-win2/crawlJ/anm_pin3_D242.3642.npz I489-mac/renode_L1_<last>_D242.3642.npz --nodes
0.3,0.4,0.5,0.6,0.7,0.8 --last <last>`, logs `renode_L1_<last>.log`. The four old segments keep crawlJ's plan, and the
new one (0.7 to 0.8) is planned at 1e-32 (6 steps). The stored state's pinned max|F| on its own layout, with the held
offset at its own coefficients as the base polish forms it, is 7.99e-38, all in the held rows (crawlJ's polish of
crawlI's base started at 8.14e-38 for the same reason).

| start (`--last`) | node 0.8 from | its block's rows before, after | pinned max\|F\| of the start | largest block |
|---|---|---|---|---|
| f64 | `driver.renode`, beyond="horizon", summed in f64 | 6.12e-09 (not refined) | 6.12e-09 | 0.7 to 0.8 and horizon |
| horizon | the horizon series at u0 0.2, in eight parts | 6.12e-09, 0 | 1.62e-34 | horizon p, harmonics 1 and 3 |
| integrate | the Taylor steps from 0.7, in eight parts | 6.12e-09, 0 | 1.59e-34 | horizon p, harmonics 1 and 3 |

The horizon series and the Taylor steps differ at 0.8 by 4.4e-36 (p, m), 1.9e-36 (c) and 3e-39 (a). The control
(`--mutate sign`, `renode_L1_ctl_sign.*`) leaves the rows at 1.22e-08 and its check fails (exit 1), as it must.
The polish starts from the horizon start (`run_polish.sh`, `polish_L1.log`, `polish_L1/`).

Results follow as the runs finish.
