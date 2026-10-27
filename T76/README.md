# T76: the stall detector's runs (hp/stall_margin.py), D 40-73

Machine: mac

- states.jsonl, kappa_states.jsonl, smoke*.jsonl: converged states, D 40-67.74 (hp/data/states, seeds, large_d/up70_*)
- seeds.jsonl, seeds.log: T48's attempted steps (hp/data/large_d/up70_attempts.jsonl) in D_from 62.0-62.2, 64.0-64.2,
  67.60-67.76, each seed rebuilt with --predictor lagrange_dd from the 4 saved states before it
- kappa_pinned.jsonl: T73's last states (raw/T73) with --pin 7 / --pin 5 and the full system, --qdh 1
