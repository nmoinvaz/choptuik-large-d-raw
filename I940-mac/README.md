# I940-mac: the quad-double full system's Delta under the Nov 5 kernel against #940's, at five D below 71

Machine: mac (the coordinator), issue https://github.com/nmoinvaz/choptuik-large-d/issues/940.

`hp/qd_window.py --mode full` (main 09ffaa1e) on T73's pin-5 states at D 67.8, 68.0, 69.0, 70.0 and 70.5, with the
hpkernel of 2026-11-05 (venv-qds, multidouble 2.1.0), against I940-dh610's solutions of the same states with today's
kernel (multidouble 4.5.0). Both converge (|F| 2.5e-54 to 1.6e-53), and Delta differs by 1.247e-23, 1.317e-23,
7.445e-24, -1.302e-23 and -2.41e-23 (`kernel_gap.jsonl`; the Nov 5 kernel's records in `kernel_old.jsonl`). At D 68.5
the same comparison on T84-mac's states gave -1.241e-23, and the Nov 5 kernel reproduces T84-mac's record exactly.

Reading: the full system is near-singular here (notes/QUAD_DOUBLE.md 12.4), so a converged root moves along its weak
direction with the arithmetic's rounding, and Delta with it. The plan (tolerance 1e-32 against 1e-34) moves Delta by
at most about 1e-27 and the two starts by at most 8.9e-28 under one kernel, so the kernel term, about 2e-23, is the
largest of the three. `hp/export_qd.py` takes the largest measured gap as each quad-double row's kernel term.
