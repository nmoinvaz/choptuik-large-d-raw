# I271-mac: gamma_dd.py --M48 resampled in double-double and iterated to the floor, its four M 48 points rerun

Machine: mac (Apple M5, 10 cores, shared with other sessions; one process at a time, 1 thread, nice 10, caffeinate).
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/271 (from #266's recommended task 1).
Code: `hp/gamma_dd.py` and `hp/series_truncation.py` on the branch wip/i271 of the main repository, commit 408b4d6
(2e72818 is #271's change, the double-double resampling `resample_hi` and Newton to the floor `solve_hi`; 408b4d6 adds
#267's series gate, which these runs also exercise). The runner is `scripts/run.sh`; every exit is in
`logs/exits.txt`.

## The change

`gamma_dd.py --M48` resampled the M 32 state in f64 (lo dropped) and stopped Newton at max(10 |F_32|, 1e-27). At D 50
that left the M 48 state one Newton step short along p1's harmonics 13 and 11 (#266): Delta(48) - Delta(32) = +1.2e-11.
Now the state is resampled at 40 digits (`rv2_resolve.resample_dd`, p1 projected onto the cut in double-double), and
Newton runs to tol 1e-40, so it stops where the line search finds no step that lowers |F|. The record holds the Newton
step's Delta component at the solution (`est`, a fresh LU there), and the floor check wants |est| <= 1e-15 (exit 1
otherwise). `--mutate=old_rule` restores the old resampling and stopping rule.

## Pass and fail criteria (written before the runs)

References: #266's quad-double solutions (`I266-mac/states/qd.jsonl`, `I266-mac/lam.jsonl` at 7b04cb4).
D 50.0075: Delta_qd(48) = 1.84163113320226444156341815006, lam_qd(48) = 2.051843756433439434 (lam_fine).
D 58.006: Delta_qd(48) = 1.81537990111591269548046122778, lam_qd(48) = 2.045529761477880408.

(a) **D 50, the new path** (`gamma_dd.py --polish=4 --M48`, as gamma_batch runs it). Passes when the floor check
passes, |Delta(48) - Delta_qd(48)| <= 1e-20 and |lam(48) - lam_qd(48)| <= 1e-14 (the M 48 root's resolution at D 50,
#266). R2's double-double state is itself 9.3e-20 from the quad-double solution, so a Delta difference in
(1e-20, 1e-18] is reported as at the double-double floor and not within 1e-20, and one above 1e-18 fails (#266's task 1
asked |Delta_diff| <= 1e-18 and |lam_diff| <= 2e-14).

(b) **The control** (`--mutate=old_rule`, D 50). It must reproduce Delta(48) - Delta(32) = +1.2e-11 (within 5% of
#266's 1.198e-11 and 1.200e-11), the floor check must fire (est about -1.2e-11, floor ABOVE) and the exit must be 1.
If it does not, the check is not shown to be able to fail, and the result says so.

(c) **D 20, 30 and 40** have no quad-double reference. Each passes when the floor check passes and |F(48)| <= 1e-20;
Delta(48) - Delta(32) and lam(48) - lam(32) are reported against the old records (lam at find_lam's xtol, 1e-14). The
M 32 part of each record (unchanged code) must reproduce the old record's lam bit for bit.

(d) **series_truncation.py --Mhi=48 at D 50** (the same solve, shared code). Passes when |Delta_diff| <= 1e-18 and
its floor check passes.

(e) **D 58** (if time allows): the new path against the D 58 reference, |Delta(48) - Delta_qd(48)| as in (a) and
|lam(48) - lam_qd(48)| <= 5e-13 (the M 48 root's resolution at D 58, #266).

## Results

(filled in after the runs)
