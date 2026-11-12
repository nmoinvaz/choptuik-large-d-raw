# I562-mac: the held-offset homotopy of #562's main arm (probes, controls, traces)

Machine mac (the shared Apple M5 Mac, 4 threads at nice 10), issue https://github.com/nmoinvaz/choptuik-large-d/issues/562 (the main arm, subagent).
Code: `hp/held_homotopy.py` on branch `wip/i562-subagent` of the code repository (commits named per file below).
Inputs: `I562-win2/renode_0975_D242.3642.npz` (the 0.3, 0.4, 0.5, 0.6, 0.975 start) and `I461-win2/crawlJ/anm_pin3_D242.3642.npz` (crawlJ's 0.7 state).

| file | what | code | exit |
|---|---|---|---|
| `probe_real_v1_float_offset.*` | first probe of the real start; its chord ladder below h = 1e-16 is wrong (the offset was formed with the float 1 - t, which is 1 there) | f118357 | 0 |
| `probe_real.*` | the probe of the real start, offset fixed: t = 0 check, tangent, weak basis, Delta's linear response by rows, chord ladder h = 1e-0..1e-46; `probe_real_setup.npz` holds a, b (= r0), tau0, V, sigma, h0 | ae2afa7 | 0 |
| `fd_tau.log` | finite differences of the residual along tau0 (h = 1e-40, 1e-50, 1e-60) against -b = J tau0; the f64 V rows are not accurate enough to show sigma (stopped before its Jacobian part) | scratch script | stopped |
| `mut_sign.*` | control `--mutate sign`: the t = 0 check must fail | 4d37ece | 1 (as it must) |
| `test_planted_2rungs.*` | code test: the planted trace (eps 2.5e-17), two rungs | 4d37ece | pending |
