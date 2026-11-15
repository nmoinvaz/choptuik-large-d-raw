# I659-mac: the large-D chain's figures at its front, D 259.74, and at the comparison frontier, D 245.64

Machine: the Mac (Apple M5, the coordinator's machine), one process at a time, nice 10. Issue:
https://github.com/nmoinvaz/choptuik-large-d/issues/659. Code: branch `wip/xf-659` at 0127c19e (`hp/chain_front.py`, the
five `hp/plot_*.py`). Raw data read from a separate worktree of this repository at d5009848.

- `top/`: the logs (every plotted number) of the five figures at the chain's front, delta_all.csv's highest chain_fit D,
  259.7436 (`I603-win2/chain_nsr/anm_pin3_D259.7436.npz`). Their SVGs are on the branch, `hp/*.svg`.
- `fits/`: the same five figures, and their logs, at the comparison frontier, the highest chain_fit row whose err is the
  fits spread, 245.6366 (`I603-win2/chain/anm_pin3_D245.6366.npz`; `--front fits`). This is the alternative proposed in
  the closing comment.
- `renders/`: Quick Look stills of some of them (the animated ones at `--frame 33` and `39`), as looked at.
- `README_wave_family.diff`: the README change the branch's `figure_front` check expects (the wave family's alt text and
  caption at D 259.74). With it, `check_numbers.py` passes 1979 of 1979 and its selftest.

What the fold does to them at 259.74, from the logs:

| quantity (wave_family) | D 200 | D 245.64 | D 259.74 |
|---|---|---|---|
| √(D−2) \|c1\| | 2.79179 | 2.77830 | 2.77417 |
| \|c1\| / \|c3\| | 15.98 | 16.34 | 16.97 |
| \|c3\| / \|c5\| | 13.76 | 14.31 | 13.98 |

- **The ratios.** |c1|/|c3| grows 2.3% from 200 to 245.64, then 3.9% in the last 14 units of D. |c3|/|c5| turns down
  there; harmonics 5–13 are held at the smooth fit while 1 and 3 are solved on the folding branch.
- **big_picture's panel 1.** At 259.74, the chain's Δ falls by 0.037 in its last 3 units of D, a visible downturn at the
  panel's right end. At 245.64 there is none.
- **The other three.** echo_harmonics, fit_steps and harmonics_held look the same at either D.
