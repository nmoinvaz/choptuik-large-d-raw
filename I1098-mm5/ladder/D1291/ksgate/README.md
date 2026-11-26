# I1098-mm5/ladder/D1291/ksgate: the od ks gate on D 1291's jump state at ks 2354 (#1098)

Coordinator's order (t5, 2026-11-26 18:1x UTC): the jumps' ks+200 |dF| (qd) sat at 1.2e-45 and 1.8e-45 at ks 1954 and 2154 and read an exact 0.0 at ks 2354: the qd check's own floor. `hp/ks_gate.py` (raw/main f398e829, "the Moebius horizon's truncation gated in octo-double")
measures the octo-double residual's largest change from ks to ks + 200 instead. Run in a separate worktree `~/Source/choptuik-fastmul6c` at f398e829 so the running D 432 / D 519 / D 1291 jobs' worktree (478e9d86) is untouched; kernel `~/Source/fastmul6-site`, HP_EXACT_RECIP=1 HP_EXACT_DMAT=1 HP_HORIZON_RELAXED=1.

- State: `../jump/jump_s_D1291.0000.npz` as left by the ks 2354 jump (copy, git blob e5afeb050e179bd5015d3c8c5432d931ddadd97c; meta D 1291, M 32, kc 220, ks 2354, Moebius a 8).
- Bar, written before the run (the order): **od change at ks 2354 (to 2554) at most 1e-70** => D 1291's rls stage (running at ks 2354) goes on as is. If it exceeds 1e-70, stop D 1291 and tell the coordinator.
- Run: `python3 hp/ks_gate.py <state> --bar 1e-70 --step 200 --tries 1 --threads 2` (2 threads, nice 10), then the same on the state with its ks set to 2554 (`variant_state.py ks=2554`) for the change at 2554 (to 2754).

## Results (2026-11-26 18:13 UTC; `ksgate_2354.log`, `ksgate_2554.log`)

| gate | octo-double residual change | bar 1e-70 | wall |
|---|---|---|---|
| ks 2354 -> 2554 (the jump's own ks) | **5.29e-71** | met (a factor 1.9 below) | about 1 min, 2 threads (18:11:36 start) |
| ks 2554 -> 2754 (the state with its ks set to 2554 by `variant_state.py`, blob 77d3e9e1830153bd30348226cc5e421ea0f3c8dd) | **7.44e-74** | met | about 1 min (18:12:33 start) |

The change falls by a factor of 711 (5.29e-71 / 7.44e-74, by script) per 200 of ks. The qd check had read 1.2e-45, 1.8e-45 and 0.0 at ks 1954, 2154 and 2354 (`../run.log`): its own floor, as the coordinator said.
**D 1291's rls stage goes on at ks 2354, as is** (the 1.5n + 420 rule: ceil(1.5 (1291 - 2)) + 420 = 1934 + 420 = 2354). Not tested: that the od change bounds Delta's truncation (gain at kfree 31 is about 1.5e47 at D 300; a change of 5.29e-71 in F gives at most about 1e-23 by that gain, which was not computed for D 1291).
