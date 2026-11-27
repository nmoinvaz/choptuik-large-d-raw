# I1098-mac-a/fit15: the ladder fit on the 15 ladder records D 250-4000, and its planted calibration on that ladder

Coordinator (t5), Mac, 2026-11-27 14:19 UTC. Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1098.

- Code: `hp/ladder_fit.py` and `hp/ladder_pade.py` of `wip/twenty-digits` at b85787c0, run beside main's
  `hp/export_delta_all.py` (cb8a7428, the reader that knows the records' err_sum) on main's `hp` path
  (`track_c.py` fd5af03c and `dd_fits_mp.py` 42783ae0, equal on both). The branch's own export_delta_all.py
  (282ef87a) predates err_sum and takes the residual bound (about 1e-30) as sigma, under which no fit is accepted.
- Input: `I1098-mac-a/ladder_records/D*/direct_s.jsonl` at raw 217fbc392 (15 records; sigma = each record's err_sum).
- `real15.json`: `ladder_fit.py real <the 15 folders> --F=3` (exit 0). The value and h, s are F-independent; E there is
  at F = 3.
- `planted15.log` / `.json`: `ladder_fit.py planted --ladders=X $(cat ladder_args.txt) --sigmas=1e-25 --seeds=20`
  (the real D list and sigma ratios err_sum/1e-25), exit 0: F = 1.59.
