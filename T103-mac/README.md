# T103-mac: replica of T99's pilot (b), sigma_0..22 (K 45) at wf 1.00, J 1500, 1280 bits: the cross-machine control of the sigma_22 campaign

Machine: mac (Apple M5, 4 physical cores, 32 GB), checkout ~/Source/choptuik-t83 (9e669de, amp_flint_par.py identical to main's), venv ~/Source/choptuik-large-d/.venv.
Comms entry: 2026-11-03 13:40 UTC cloud to mac
Command: nice -n 10 python -u amp_flint_par.py 1.0 45 1500 1280 --procs 2 --fit phys --mf 6:12 --fit-step 1
Started 2026-11-03 13:42 UTC.
