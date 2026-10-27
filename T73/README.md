# raw/T73: run output of T72 and T73 (large D, D 67.74 to 70.98)

Copied from wip/qd-mac at f75a607 (hp/data/large_d/t72 and t73) on 2026-10-27, unchanged. The runs and their
settings are in comms.txt on main (T72 18:24 UTC, T73 18:28 UTC, 2026-10-26); the code is wip/qd-horizon f41d622.

- t72/: T72, scan_hp --pin 7 and --pin 5 with --pin_from seed (the held band drifted; stopped at 67.80)
- t73/: T73, as T72 with --pin_hist full1, to the 4 h limit (pin 7 to 70.63, pin 5 to 70.98); per run the records
  (pin7.jsonl, pin5.jsonl), every attempted step (*_attempts.jsonl), the logs and the converged states (*_D<D>.npz)
