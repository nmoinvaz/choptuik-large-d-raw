# I778-mac: #742's natural-test attempt N rebuilt to Newton step 1, its simplified correction and weak directions

Machine: the Mac (Apple M5, the coordinator's machine), one process at a time, 4 threads, nice 10. Issue:
https://github.com/nmoinvaz/choptuik-large-d/issues/778, with the pre-registration in its comments. Code: `hp/crawl_probe.py`
on branch `wip/xf-778` at 1bc0433c, which made these runs. 4107b92b after it only reorders probe's printing.
Build: venv-314's installed hpkernel (pre-#523, rounded projector), the one #742 ran on and #752 rebuilt on.
Inputs: `I742-win/L/anm_pin13_D117.0000.npz` and `I742-win/logs/N.log`.

## Files

- `run_778.sh`: everything, in order (`bash run_778.sh RAW OUT` from the checkout's `hp/`). `exits.txt`: each start and exit.
- `anm.log`, `R/`: `crawl_probe.py anm --stop 1 --attempts 1` on #742's FLAGS with N's `--h_max 1.0 --a0 1.0
  --od_accept natural`. It saved `R/crawl_iter_D118.0000_s1.npz`, the iterate at Newton step 1, and the prediction.
- `logcmp_base.log`, `logcmp_step0.log`, `logcmp_step1.log`: the rebuilt log against N.log. `logcmp_control.log`: `--mutate digit`.
- `probe.log`, `probe/`: `probe --arms none --theta 1 --weak 4` at the iterate.
- `weak.log`, `weak.jsonl`: `weak --iter ... --lams 0,1 --w 4`.

## Results

| criterion | result | verdict |
|---|---|---|
| R1, the saved iterate against newton_od's records | max\|F\| 8.472e-20, \|dz\| 2.4510e-09, equal (PinnedO.newton_o call 1 of 3) | passes |
| R2, logcmp against N.log | base polish 5 of 5 lines, series and step 0 11 of 11, step 1 3 of 3; `--mutate digit` 10 of 11, FAIL | passes, and the control fails |
| R3, θ at λ = 1 as the corrector projects the trial | 9.612e-01 (N's step-1 ratio 9.612e-01); the step formed again is bit for bit the stored one | passes |
| T, the simplified correction's share in the four weakest directions at the iterate's projection | 1.0000 (σ 9.809e-25, 9.790e-25, 6.764e-26, 3.030e-26); the self-check gives 1 to 6.7e-16 | above 0.9 |
| W, the four directions | at the iterate's projection and at the λ = 1 trial: p1's harmonic 11 (directions 0 and 1) and harmonic 13 (directions 2 and 3), cos/sin pairs, Δ components 3e-8 to 1.2e-6 | the same pairs as #752's own-test crawl |

The iterate's own step lies 0.998 in the harmonic-13 pair (components +0.025, +0.023, −0.462, −0.886), with p1's harmonic 13 at 2.2e-9. The λ = 1 trial's own step lies 0.9997 there (−0.007, 0.000, −0.224, −0.975), with harmonic 13 at 1.2e-9.

At the trial σ is 1.168e-24, 1.157e-24, 1.543e-25 and 6.899e-26. The harmonic-13 pair's σ is 3e-26 to 1.5e-25 here, against #752's 4.9e-28 at the root and the own-test trial. That fits #752's finding that these σ shrink with the distance to the root: this iterate is 2.45e-9 from its step's end, the own-test crawl's 1.68e-15.
