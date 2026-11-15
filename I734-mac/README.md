# I734-mac: #491's sigma table (crawlJ near_null runs at D 239.54-241.89), and the ks of the D 40-61 node law's runs

Machine: the coordinator's Mac (Apple M5), agent xfkappa. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/734.

## The sigma table (`sigma/`)

`hp/near_null.py` at the four crawlJ bases, made by the coordinator's session on this Mac on 2026-11-10 21:16-21:43
PST (2026-11-11 05:16-05:43 UTC) and quoted in #491's second comment. Found in that session's scratchpad
(`.../11bcbd25-9376-453b-88d5-a7c6ad0172dd/scratchpad/nn/`), copied here unchanged (sha-256 equal, modification times
kept). The code is near_null.py's first version, a9b08854 (2026-11-11 05:07 UTC): its JSON has the keys state, D,
pivots and vectors, without the plan and step entries later versions add, and its check is the exact Jacobian at 140
digits. The kernel was the hpkernel installed in the Mac's venv then (its build of 2026-11-08), not recorded in the
files. The same session's D 237.13 and 242.36 runs are in `I488-mac/`.

| D | state | sigma_1 | sigma_2 | sigma_3 (mostly Delta) | sigma_4 | ||J v_1|| / sigma_1 | LU, check (s) |
|---|---|---|---|---|---|---|---|
| 239.5375 | I461-win2/crawlJ/anm_pin3_D239.5375.npz | 3.525e-26 | 3.496e-26 | 1.190e-24 | 1.906e-24 | 0.999189 | 306, 331 |
| 240.5141 | I461-win2/crawlJ/anm_pin3_D240.5141.npz | 1.423e-26 | 1.445e-26 | 2.944e-25 | 8.619e-25 | 0.999943 | 307, 330 |
| 241.1244 | I461-win2/crawlJ/anm_pin3_D241.1244.npz | 8.093e-27 | 8.188e-27 | 1.410e-25 | 4.464e-25 | 0.999821 | 347, 488 |
| 241.8874 | I461-win2/crawlJ/anm_pin3_D241.8874.npz | 4.005e-27 | 3.963e-27 | 8.223e-26 | 1.303e-25 | 0.999610 | 348, 484 |

Every check passes (exit 0). A rerun would be cheap: about 11-14 min per base on this Mac at 2 threads (the LU and
the 140-digit check as above), so under an hour for the four, with today's kernel.

## The ks of the D 40-61 node law's runs (`ks.log`, `ks_vs_res.csv`)

`hp/ks_vs_res.py` (choptuik-large-d wip/xf-734 84591784). The node law is notes/BEYOND_LIGHT_CONE.md section 5's 15
runs of `solver/beyond_lc/hp_node_test.py` at D 40.02, 50.01 and 60.00 (last node 0.6-0.8). Their records carry no ks;
the script's default, 160 since its only commit (46d03ba0), is the one they ran at, since the documented command
passes none. Their inputs and the other 18 double-double scan states of hp/data/states at D 40-61 were solved at the
ks of their meta, 100. Re s is hp/horizon_radius.py's, from each state's a_h block.

| runs | ks | Re s | 1.9 Re s | ks / Re s | flagged |
|---|---|---|---|---|---|
| 15 node runs (D 40.02, 50.01, 60.00) | 160 | 21.13, 26.23, 31.30 | 40.1, 49.8, 59.5 | 7.57, 6.10, 5.11 | none |
| 21 scan states, D 40.02-60.00 | 100 | 21.13-31.30 | 40.1-59.5 | 4.73-3.19 | none |

No run has ks < 1.9 Re s; the smallest ratio is 3.19 (up13_D60.0020). Control `--mutate=ks` (every ks taken as 40)
flags all 36 and exits 1 (`ks_mutate.log`). `check_numbers.log`: `check_numbers.py --selftest` at 84591784, 2019 of
2019, selftest 2019 of 2019.
