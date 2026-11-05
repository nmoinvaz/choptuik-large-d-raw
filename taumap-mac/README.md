# taumap-mac: mapped tau grid at low D, solves against the uniform references and per-call timings

Machine: the Mac, a coordinator subagent

Task: step 5 of notes/LOW_D_SPEEDUP.md in the code repository (branch feat/tau-map, wip/tau-map), the section
"Step 5, the test: procedure and criteria". Scripts: hp/tau_map_solve.py (solve, time), hp/tau_map_study.py,
hp/tau_map_check.py.

- `runs.jsonl`: one record per mapped solve (map, plans, per-call seconds, |F|, Delta, difference from the reference).
- `points.jsonl`: lowD_dd.solve_point's records of the same solves.
- `timing.jsonl`: one newton_mixed call per state on its own plan.
- `states/`: the converged mapped states (meta tau_map = [s0, L, mutate]).
- `study_*.json`: tau_map_study.py on the reference states.
- `logs/`: the runs' logs. `PROGRESS.md`: dated progress lines.
