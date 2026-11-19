# I997-win2: Delta's Taylor series in D at D 3.15, M 160 (#997 step a, discovery candidate 6)

Machine win2 (runner win2b), 9 threads, venv-i962 (`C:\Users\nathan\Source\venv-i962`), code `D:\choptuik-i962\hp` at origin/main 459180e6 (Python only, the installed hpkernel unchanged).
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/997 (the coordinator's command is in its comment 6996854170).

Command, run from `hp/` with RAW = `D:/choptuik-large-d-raw-743` (the raw-data worktree that has `I927-mac/inputs/`):

    python anm_lowd.py RAW RAW/I997-win2/series --state I927-mac/inputs/lowDhm_x0.000625-0.9_D3.1500_M160.npz --N 20 --checks "" --target 3.14 --threads 9 \
        --save_series RAW/I997-win2/series/series_D3.15_M160_N20.npz

Glue: `run997a.sh` chains that command and logs its start and exit in `exits_997.txt`; the run's stdout is `series/run.log`, its records `series/anm_lowd.jsonl`, the series `series/series_D3.15_M160_N20.npz`.
