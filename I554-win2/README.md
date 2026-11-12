# I554-win2: the last-node ladder above 0.80, where the weakest equilibrated sigma peaks

Machine win2 (Windows 11 desktop, Intel Core Ultra 7 265K, 20 threads, 96 GB), issue https://github.com/nmoinvaz/choptuik-large-d/issues/554 (follows from #543).
Start: crawlJ's state `I461-win2/crawlJ/anm_pin3_D242.3642.npz`, nodes 0.3, 0.4, 0.5, 0.6, 0.7. `renode_o.py ... --nodes 0.3,0.4,0.5,0.6,<x>` (`--last horizon`) for x = 0.82, 0.84, 0.86, 0.88, 0.90, 0.92, then `near_null.py --k=4` and `near_null_eq.py --plant=7` on each, beside #543's 0.80 and #537's 0.70. One lane of 2 threads (`lane_554.sh`, `layout_lib.sh`).
`renode_o.py` and `near_null.py` from `D:\choptuik-i446g/hp` at main 14dc386, `near_null_eq.py` from `D:\choptuik-i505/hp` at 0cce81e. Exit codes in `exits.txt`. Results follow in this README.
