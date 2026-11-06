# qd2start-mac: second starts for the full system in quad-double at D 71.0, 71.5, 72.8 and 73.0

Machine: the Mac (Apple M5), coordinator session, 2026-11-05.

hp/data/delta_qd.csv has one converged full-system solution at these four D. The second starts from the double-double
pinned states stalled (T84-mac/qd_fullleg_pin5.log at 71.0 and 71.5, T81/conv_pin5_D72.8000 and conv_pin7_D73.0000).
These runs start from the other pin's state polished in quad-double in its own pinned system (T84-mac's
`*_pinned5_dz.npz` and `*_pinned7_dz.npz`, copied here so the converged states land in this folder), whose
full-system residual is 1e-30 to 5e-32, and converge the full system (kfreeze 13) with T84-mac/qd_fullleg.py
unchanged, each with its own Taylor plan.

    cd ../choptuik-large-d-raw/qd2start-mac
    PYTHONPATH=../../choptuik-large-d/hp python3 ../T84-mac/qd_fullleg.py second.jsonl pin5_D71.0000_pinned5_dz.npz \
        pin5_D71.5000_pinned5_dz.npz pin5_D72.8000_pinned5_dz.npz pin7_D73.0000_pinned7_dz.npz --threads 2

Kernel: main's hp (multidouble 3.2.0, choptuik-large-d main at the commit named in the post).
