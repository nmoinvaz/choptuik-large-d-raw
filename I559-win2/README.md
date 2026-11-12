# I559-win2: the last-node ladder to 0.98 at D 242.36

Machine win2 (Windows 11 desktop, Intel Core Ultra 7 265K, 20 threads, 96 GB), issue https://github.com/nmoinvaz/choptuik-large-d/issues/559 (follows from #554).
Start: crawlJ's state `I461-win2/crawlJ/anm_pin3_D242.3642.npz`, nodes 0.3, 0.4, 0.5, 0.6, 0.7. #554's commands (`I554-win2/lane_554.sh`): `renode_o.py ... --nodes 0.3,0.4,0.5,0.6,<x>` for x = 0.94, 0.96, 0.98, then `near_null.py --k=4` and `near_null_eq.py --plant=7` on each; the control `--mutate sign` once (at 0.96). One lane of 2 threads (`lane_559.sh`, `layout_lib.sh`).
`renode_o.py` and `near_null.py` from `D:\choptuik-i446g/hp` at main 14dc386, `near_null_eq.py` from `D:\choptuik-i505/hp` at 0cce81e. Exit codes in `exits.txt`. Results follow in this README.
