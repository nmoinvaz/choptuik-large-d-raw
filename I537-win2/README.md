# I537-win2: which exponential is the wall, one node moved at D 242.36

Machine win2 (Windows 11 desktop, Intel Core Ultra 7 265K, 20 threads, 96 GB), issue https://github.com/nmoinvaz/choptuik-large-d/issues/537 (depends on #489 and #502).
Start: crawlJ's state `I461-win2/crawlJ/anm_pin3_D242.3642.npz` (layout 0.3, 0.4, 0.5, 0.6, 0.7). Two lanes of 2 threads each, Python only, venv-t126.
Lane A (`lane_a.sh`): `renode_o.py` to first node 0.35 (nodes 0.35,0.4,0.5,0.6,0.7), then `near_null.py --k=4` and `near_null_eq.py --plant=7` on that start, then both on crawlJ's own state (the baseline).
Lane B (`lane_b.sh`): `renode_o.py` to last node 0.72 (nodes 0.3,0.4,0.5,0.6,0.72), its control `--mutate sign`, then `near_null.py` and `near_null_eq.py` on that start, and the control `near_null.py --mutate=sigma`.
`renode_o.py` and `near_null.py` from `D:\choptuik-i446g/hp` at main 14dc386, `near_null_eq.py` from `D:\choptuik-i505/hp` at 0cce81e. Exit codes in `exits.txt`. Results follow in this README.
