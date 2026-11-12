# I574-win3: mode-count circles in the strips 1.0 < |Im lambda| <= 2.0 at kf 27

Machine: win3 (NATHAN-PC, Windows 11 Pro, i7-12700, 20 logical processors, 64 GB). Issue:
https://github.com/nmoinvaz/choptuik-large-d/issues/574 (moved here from macm3 and win2).

Code: choptuik-large-d at main 80b50568, worktree C:\Users\nathan\Source\choptuik-i574, `hp/modecount_build.sh`
(`modecount_build.log`), rustc 1.99.1, Python 3.14.10. State: `modecount_state_D61.0264_M48_kf27.npz` from
`I280-macm3/hp_data_after/`, copied into `hp/data/`, sha256
`1fd892fcd0e326276b1885f10fc42421d917590f298e585867adb3fc352e8ac1`.

Each circle is one folder `c<RE><IM>i_R<R>/` run by `drive_574.py` (one process, one thread, below-normal priority, its
own empty cache). The driver enforces the cap of 150 points by killing a process whose cache holds more than 152
determinants (`cap.json`). `control_cap_dir/` and `control_cap.log` are its control, a cap of 25.

## Cancelled

The coordinator cancelled #574 for win3 at 08:55 UTC (win2 had finished its circles). Stage 1 had run from 08:50 to
about 08:55 UTC: four circles (Re 1.85, 2.35, 2.85 and 3.35 at Im +1.25) were started and stopped before any finished.
Their caches and logs are kept as they were, with no record in any `circles.jsonl`, so they hold no winding. The
cap control (`control_cap.log`, `control_cap_dir/`) passed: a cap of 25 stopped a circle at 28 determinants and wrote
`cap.json`; one thread took 16.8 s per determinant (15.95 to 18.08).
