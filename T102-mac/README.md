# T102-mac: replica of T99's pilot (a), sigma_0..22 (K 45) at wf 1.00, J 1250, 1280 bits: the cross-machine control of the sigma_22 campaign

Machine: mac (Apple M5, 4 physical cores, 32 GB), checkout ~/Source/choptuik-t83 (9e669de, amp_flint_par.py identical to main's), venv ~/Source/choptuik-large-d/.venv.
Comms entry: 2026-11-02 22:57 UTC cloud to mac
Command: nice -n 10 python -u amp_flint_par.py 1.0 45 1250 1280 --procs 2 --fit phys --mf 6:12 --fit-step 1
Started 2026-11-02 22:58 UTC.

Done 2026-11-03 12:50 UTC, 49936 s (832.3 min) on the script clock. sigma_err_fit.py exit 0, err22 1.297e-31. 23 of 23 sigma strings equal to T99-win2 scan45J1250.
