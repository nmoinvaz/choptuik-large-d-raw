# I766-win: M 64 checks of the dM-neighbours errs at D 7.0 and 8.2

Machine win (surface-laptop-4), issue https://github.com/nmoinvaz/choptuik-large-d/issues/766.

`run_766.sh` (written by the coordinator) runs relayout.py at M 64 from T79's M 48 states `T79-win/down_D7.0000.npz` and
`down_D8.2000.npz`, as T79 did at D 4, 5, 6 and 8 (kc 60, ks 100, no freeze projector below D 35.35), then
`compare_766.py`. Criteria, written before the run (#766): |Delta(64) - Delta(48)| within the rows' errs in
hp/data/delta_all.csv, 3.0e-14 at D 7.0 (dM neighbours) and 9.5e-21 at D 8.2 (one-sided). A difference above its err
means #764's rule underestimates there, and is reported.
