# I1035-mac: the factored horizon segment, stage 1 (mpmath prototype): transcription checks, loop gain, sweeps, P1

Machine: the Apple M5 Mac (the coordinator's), a subagent, one process at nice 10. Issue:
https://github.com/nmoinvaz/choptuik-large-d/issues/1035

Code: `hp/factored_horizon.py` on the branch `feat/factored-horizon-proto` of choptuik-large-d (from main 82f87a33),
venv-314 (Python 3.14, mpmath 1.3.0, numpy 2.5.4). The note is `notes/FACTORED_HORIZON.md` 5.1.

Inputs (read from this repository with `git show origin/main:<path>`): `T81/conv_pin5_D73.0000_D73.000000.npz`,
`I461-win2/crawlJ/anm_pin3_D242.3642.npz`, `I603-win2/base/base_pin3_D225.1312.npz`,
`I603-win2/chain/anm_pin3_D241.9602.npz`, `T139-macm3/chain/anm_pin3_D73.7500.npz`.

Files: one `<name>.log` (stdout) and `<name>.json` (the command's record) per run; `queue.log` the start and end of
each queued run (its exit codes before 19:06 UTC read 0 whatever the run returned, a bug of the queue script).
- `selftest*.log`: the planted checks and the five controls.
- `check_*.log/json`: the transcription check at the five states, its control (`_nh`) and the exact-1/k reading.
- `ref_D242_288.json`, `ref_D73_288.json`: the reference fixed points (y, rows, gamma at 288 bits) and their logs
  (`ref_D242_288.log`, `ref_D73.log`); `ref_D73_slaved_diverges.log`: the D 73 reference from the slaved start.
- `gain_*`: sweeps from the slaved, warm and naive starts, plain and Anderson.
- `p1_*`: P1 at both states, with hp's and an exact 1/k, and with a_h moved by 1e-8/G with its control.
- `loop_*`: the power iteration of the sweep map and the forward pass's response per order.
- `power_D242.log`: the same power iteration by a scratch script before `loop` existed (the same numbers).
- `p1_D73_move.log`: stopped by hand after its first sweeps (time); nothing from it is quoted.
- The check records `check_*.json` come from the first runs of each check (the same code for the rows); the
  `check_*.log` files are the reruns of 20:07 UTC.
