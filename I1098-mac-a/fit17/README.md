# I1098-mac-a/fit17: the interim ladder fit on the 17 ladder records D 250-8000, and its planted calibration on that ladder

Machine: Nathan's Mac (coordinator t5). Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1098. Run 2026-11-28 01:35:08 UTC by the clock.

- Code: main 8a45e8f6, `hp/ladder_fit.py` and `hp/ladder_pade.py` (e8f6934a: check 2 runs for every point), with main's `hp/export_delta_all.py` reading the records' err_sum.
- Input: `I1098-mac-a/ladder_records/D*/direct_s.jsonl` at raw af4bc862e (17 records; sigma = each record's err_sum).
- `run.sh` (paths shortened to this repository's; it ran from the scratchpad): `ladder_fit.py planted --ladders=X $(cat ladder_args.txt) --sigmas=1e-25 --seeds=20`, which gave F; `ladder_fit.py real <the 17 folders> --F=<that F>`; `ladder_pade.py real <the 17 folders> --Ms=1,2,3`. Every step exited 0 (`run.log`).
- Interim: three points (D 4628, 5555, 6666) are still running, so this is not the 20-point fit of record.
