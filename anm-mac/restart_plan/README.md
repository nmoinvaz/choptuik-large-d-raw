# anm-mac/restart_plan: restarting the large-D chain from a stored state

Machine: the Mac. hp/anm_run.py from D 128.56 (one step to 129.06), then restarts from the saved state.

- `step.log`, `restart*.log`, `v2/`: restarts with the base polish started from the state's first two parts: the first
  quad-double |F| is 3.89e-13 whether the plan and held values are stored or recomputed.
- `v3/`: with the polish started from all four parts (main fece0ba): 1.97e-32 at 129.06, and 1.29e-35 from T114's
  stored 135.06 state, where the old restart had failed (T113-win/chain_from135*).
