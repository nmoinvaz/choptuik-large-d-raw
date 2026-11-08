# I177-win2: Python 3.14 crash test on win2 (access violations 0xc0000005)

Machine: win2 (Windows 11 desktop, Intel Core Ultra 7 265K, 20 threads, ASRock Z890I Nova WiFi).
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/177

Runs beside #82 (I82-win2/) on the 3.12 venv; #82 is not touched. The crash test is #146's repeat-and-compare loop of the
amplitude copy `amp_flint_par.py 1.10 15 750 640 --procs 1 --fit phys --mf 6:12` on a Python 3.14 venv, hashed with
`I140-win2/compare.py` against fd6b5ef2f90d4f559a1a1ab68a7e85fe7c9b8538cc7e50ac41d2fb5510eb47d8 (#161).

Contents are added as the task proceeds (install record, `pip freeze`, rounds, crash records).
