# I940-dh610: quad-double Delta from D 67.77 to 73.27 (qd_window.py)

Machine dh610 (Fedora 45, i7-12700, 20 threads), issue https://github.com/nmoinvaz/choptuik-large-d/issues/940.
Code: `hp/qd_window.py` at main 30a3a31b, worktree `choptuik-large-d-940`, run from `hp/` with the python of
`choptuik-large-d-855/.venv` (hpkernel from the 7e4cfd03 build, multidouble 4.5.0; its quad-double path is not touched by
the octo-double renormalization bug). Inputs: T73's and T75's pin-5 and pin-7 double-double states and T84-mac's D 68.5
pilot states, read from copies extracted from the raw repository's origin/main into `~/scratch940/in` (nothing is written
into T73, T75 or T84-mac); `inputs.txt` is the issue's selection command run on origin/main (69 D, 39 below 71). Outputs:
`pilot/` (the pilot's jsonl, logs, states) and `runs/` (the window's `qd_window.jsonl`, logs and `*_full.npz` and
`*_pinned.npz` states), 4 processes of 2 threads at nice 10.
