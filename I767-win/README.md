# I767-win: #82's nodes 1.09 and 1.11 at sigma_0..7 on a second machine, K 15

Machine win (surface-laptop-4, 8 threads), issue https://github.com/nmoinvaz/choptuik-large-d/issues/767.

Scripts (written by the coordinator): `run_767.sh` (`amp_flint_par.py <wf> 15 1500 1280 --procs 3 --fit phys --mf 6:12`
at wf 1.09 and 1.11, from the worktree C:/Users/nathan/Source/choptuik-i767 at 188853c5, #82's summation order before
#246, with venv-t151's python-flint 0.9.0 and FLINT 3.6.0) and `compare_767.py` (its selftest must pass).

Criteria, written before the run (#767): each node's sigma_str (20 digits) equals win2's K 45 file
`I82-win2/sigF_w<wf>_K45_J1500_p1280.json` at n = 0..7, or the first differing n is named; the control, the 1.09 K 15
file against the 1.10 K 45 file, must differ. #295 showed K 15 J 1500 reproduces the K 45 file at these orders bit for
bit on win2, and #229 that win2 and macm3 agree bit for bit at equal --procs.
