# I854-mac: newton_od's keep_projected (the projected point as ElimO's iterate) at s0_D252, against #839's A_s1

Machine: the Apple M5 Mac (`mac`), agent mac752. Issue https://github.com/nmoinvaz/choptuik-large-d/issues/854.

Code: branch `wip/m752-854` (394e45b0, off main a4279a8d), worktree /Users/nathan/Source/choptuik-large-d-854; the
code before #854 is the wip/i839 worktree at main 4617f876 (A_s1's). Build: main 3c35f0c's hpkernel (i599/site2).
3 threads, nice 10, one job at a time (queue.sh).

## Plan and criteria (written before the queue)

**The change:** `newton_od(..., keep_projected=True)` on ElimO keeps the projected point as the iterate, at the start and at
each accepted trial, and steps from it alone (`s.so.newton_o`). Both trial tests are covered: the own test and the natural
test, where theta no longer carries the displacement. Off, the default, every call is as before. Passed through as
`planted --keep_projected 1` and `anm_run.py --od_keep_projected 1`.

**Planted test (done, hp/newton_od_toy.py):** ElimO around the toy with a pair of horizon unknowns h = 10 y, which a
stub re-seeder's projection sets from y, from the planted start (y moved, h at the root's value).

- With each test (own, natural), the default and the option converge to the root (distance 1.9e-33).
- With the option, the start it steps from and the point it returns are projected (offset 0). Its first step's h part
  is 10 times its y part, to 7.4e-20 of the step. By default the start keeps its whole offset.
- The control `--mutate=keepskip` (the re-seeder leaves points unprojected) fails, and the toy's other controls still
  fail.
- The default path's logs (both tests at verbose 2, the chord case, the why case) are byte-identical to 4617f876's
  (toylogs_*.txt).

**The default reproduces #839 A_s1's step 0:**

- `dz0`: planted --save_dz0's start and first step (eight parts each), equal bit for bit between 4617f876 and
  394e45b0 with the option off. The control compares against the option's own dz0, whose start is projected, and must
  differ.
- `step0`: off_step0 (it_max 1) prints step 0's record, the trial lines, the projection lines and the step line. It
  must equal A_s1's text without the seconds. A_s1 wrote no JSON, so its printed record is the only one. The control
  `--mutate=digit` must fail, and A_s1 against #713's old-system step 0 fails too.
- cmp_854.py does both comparisons.

**The run, keep_s1:** #713's flags (`--switch 0 --reseed_o 3 --reseed_start pred --qd 0 --seed 1`, it_max 12, tol
1e-40) plus `--keep_projected 1`, with `--Delta_ref` the truth's eight-part Delta.

- Bar: pinned max|F| below 1e-40 within 12 steps, and |Delta − truth| ≤ 1e-30.
- Otherwise: the steps with their accepted lam, beside A_s1's 9 accepted steps (I839-mac README, "Stopped").

Estimate: dz0 runs about 6 min each, off_step0 about 60 min. keep_s1 takes 1–12 h: about 7 steps of 30–60 min if lam
grows to 1, and 12 h at the step limit.

## The default against A_s1 (queue.log, 20:37–22:40 UTC)

| check | result | control | control result |
|---|---|---|---|
| dz0, 4617f876 against 394e45b0 off (cmp_dz0.log) | 16 of 16 arrays bit for bit, pass | against the option's dz0 | 7 of 16 equal (z4–z7, d3–d7 differ), FAIL as required |
| step0, A_s1 against off_step0 (cmp_step0.log) | 7 of 7 lines equal, pass | `--mutate=digit` | FAIL as required |

- off_step0 accepts lam 1/8 after refusing 1, 1/2 and 1/4, as A_s1 did: |F| 3.40e-12 → 2.97e-12, |dz| 2.20e-12 →
  1.93e-12, Delta − truth −2.7542e-13 afterwards (A_s1's table: −2.750e-13 from the log's three digits).
- off_step0's exit 1 is planted's (a) verdict after one step (max|F| 2.97e-12), as it_max 1 gives.
- The option's dz0 shares the start's first parts: its z0–z3 and d0–d2 are A_s1's bits. The projection moves only
  parts 4–7 of z, so the change from the default sits below quad-double in the start.
- Times: the dz0 runs took 745–761 s each and off_step0 5113 s, against 6 min and 60 min estimated. Another agent's
  3-thread job shares the CPU.

## keep_s1: what to expect, written 00:21 UTC before step 1's shorter trials

- From the iterate's projection zp with the step s from there, a trial at lam is, by default,
  z + lam (disp + s) with z = zp − disp, that is zp + lam s − (1 − lam) disp. With the option it is zp + lam s.
- At lam 1 the two are the same point. So keep_s1's lam-1 trials repeat A_s1's while zp does. Step 0 (lam 1/8) and
  step 1's lam-1 trial (point max|F| 7.40e17, the same ladder |R|) are A_s1's to the printed digits.
- At lam < 1 only the default carries −(1 − lam) disp. A_s1's step 8 trials fit P0 (1 − lam)^1.91 with P0 = 4.83e14,
  the unprojected iterate's own point max|F|. The prediction for the option: the shorter trials follow the lam-1
  trial's value times lam^4 (#839's |dz|^4 law), for example 4.6e16 at step 1's lam 1/2 against A_s1's 5.01e16. The gap
  should grow at later steps, where A_s1's P0 term dominates, and larger lam should be accepted there.
- Step 1's lam 1/2 (00:39 UTC): point max|F| 4.63e16, 0.0626 of the lam-1 trial's 7.40e17 (1/16 within 0.2%), against
  A_s1's 5.01e16 (0.0677). Refused, its projection failed (ladder |R| 1.05e7 → 5.21e1).
- Step 1 accepted lam 1/4 (01:03 UTC), as A_s1 did: |F| 2.97e-12 → 2.23e-12, |dz| 1.93e-12 → 1.45e-12.
- Step 2 (02:18 UTC): lam 1 at 2.34e17 (A_s1's), lam 1/2 at 1.46e16 (1/16 of it; A_s1 2.39e16), refused; lam 1/4
  accepted, as A_s1 did: |F| 2.23e-12 → 1.67e-12, |dz| 1.45e-12 → 1.08e-12.

### Two further predictions, written 02:25 UTC before step 3

1. **When lam reaches 1.** The projections so far succeeded at moves lam·|dz| up to 4.82e-13 (step 1, lam 1/4) and
   failed from 5.5e-13 (step 0, lam 1/4, point max|F| 4.93e15). With the option a trial's point max|F| is
   C (lam |dz|)^4 alone, so keep_s1 should accept the largest lam with lam·|dz| below about 5e-13. That gives lam 1/2 at
   step 3 (|dz| 1.08e-12, borderline) and lam 1 by step 4 or 5, where A_s1 took 1/2 and then 1/4.
2. **Where it goes.** In every step so far dDelta is −|dz| to the printed digits and |F| falls to (1 − lam)|F|. So the
   steps walk to Delta − truth = −2.203e-12 whatever lam is. The option changes how fast, not where, and the Delta bar
   (1e-30) is expected to fail. The open part is what a lam-1 step does to |F|: a quadratic fall, or a slow one if the
   smallest pivot keeps falling with |dz| (A_s1: 4.1e-3 |dz|^0.98).
- Step 3 accepted lam 1/2 (03:03 UTC), as A_s1 did: |F| 1.67e-12 → 8.36e-13, |dz| 1.08e-12 → 5.42e-13. Its lam-1 trial
  was A_s1's (7.41e16).

### Prediction 1 corrected (03:05 UTC, before step 4)

Prediction 1 is wrong as written, for a reason that was in A_s1's log. The projection moves only m_h and a_h, so two
trials with the same bulk part project to the same point. keep_s1's projected iterates are therefore A_s1's while the
accepted lam agree, and its lam-1 trials are A_s1's points. A_s1's projection failed at every lam-1 trial through
step 8: 4.63e15, 2.90e14, 9.16e13, 2.90e13 and 1.81e12 at steps 4–8. Meanwhile A_s1's accepted step 8 trial
(lam 1/64, near 4.6e14 by the P0 fit) projected. So whether a projection succeeds is not a threshold on point max|F|.

The corrected prediction: keep_s1 repeats A_s1 at step 4 (lam 1 refused at 4.63e15, lam 1/2 accepted). It can first
depart at step 5, where A_s1 refused lam 1/2 at 1.59e15 and keep_s1's lam 1/2 should come at about 1.8e13 (2.90e14/16).
It reaches lam 1 only if a lam-1 projection succeeds at some smaller |dz| than A_s1 reached (7.6e-14). Without lam-1
steps, |F| falls at most by (1 − lam) per step, so the bar (1e-40 within 12 steps) is not expected to be met.
- Step 4 accepted lam 1/2 (03:43 UTC), as the corrected prediction says and as A_s1 did: lam 1 refused at 4.63e15,
  |F| 8.36e-13 → 4.18e-13, |dz| 5.42e-13 → 2.71e-13.
- Step 5 (04:29 UTC), the first possible departure: lam 1 refused at 2.90e14 (A_s1's). lam 1/2 came at 1.81e13, as
  predicted (2.90e14/16), 88 times below A_s1's 1.59e15, and its projection failed all the same (u0 quad-double
  |R| 1.07e13 → 2.59e9, ladder FAILED). So the trial's point max|F| does not decide the projection: A_s1's accepted
  trials projected from up to about 4.6e14 (step 8, lam 1/64), and keep_s1's lam 1/2 fails from 1.81e13.
- Step 5 accepted lam 1/4 (04:56 UTC), as A_s1 did: |F| 4.18e-13 → 3.13e-13, |dz| 2.71e-13 → 2.03e-13. No departure.
- Step 6 (06:42 UTC), the departure, in the other direction. lam 1 refused at 9.16e13 (A_s1's). keep_s1's lam 1/2,
  1/4 and 1/8 came at 5.73e12, 3.58e11 and 2.24e10, each the lam-1 trial's times lam^4. Each projection failed (u0
  quad-double |R| 3.39e12 → 8.14e8, 2.11e11 → 4.72e7, 1.29e10 → 5.24e6, ladders FAILED). A_s1 accepted lam 1/4 here,
  whose trial carried −(3/4) disp and a higher point max|F| (its lam 1/2 was 8.77e14).
- Every projection path starts from the trial's own horizon data: the u0 rung, its quad-double polish, the re-seed's
  polish from the point's own data (qd_start pred), and the ladder's first rung. The two variants' trials at one lam
  have the same bulk and differ only in −(1 − lam) disp_h. So at step 6 the default's horizon data, mixed toward the
  unprojected iterate's, projected, while keep_s1's (zp_h + lam s_h) did not, even at lam 1/8. What decides the
  projection is where the trial's horizon data start, not the trial's point max|F|.
- Step 6 accepted lam 1/16 (06:59 UTC): |F| 3.13e-13 → 2.94e-13, |dz| 2.03e-13 → 1.91e-13. The run was then stopped
  by its PIDs (queue.log), the log saved first as keep_s1_at_stop.log (exit 143).

## Stopped after step 6 (the coordinator's word, 03:04 UTC)

**The answer.** keep_projected works as designed but does not remove the crawl. At lam 1 both variants evaluate
zp + s, so the full-step trials are A_s1's, and their projection fails at every step. Only the shorter trials change.
They lose the displacement term, since all 15 refused trials lie on one curve, 5.36e64 · move^4 within 0.3%. Yet they
project less often: at step 6 keep_s1 refused lam 1/4 and 1/8 and took 1/16, where A_s1 took 1/4. The bar is not met.
After 7 steps max|F| is 2.94e-13, and Delta − truth is −2.01e-12, heading to −2.203e-12.

### The steps against A_s1 (side_854.log; the checks pass, the controls side_854_digit.log and side_854_power.log fail)

| step | \|F\| before | \|dz\| before | A_s1 lam | keep_s1 lam | lam-1 trial, both | A_s1's refused shorter trials | keep_s1's refused shorter trials (ratio to lam-1 × lam^4) |
|---|---|---|---|---|---|---|---|
| 0 | 3.40e-12 | 2.20e-12 | 1/8 | 1/8 | 1.26e18 | 1/2: 7.89e16, 1/4: 4.93e15 | 1/2: 7.89e16 (1.002), 1/4: 4.93e15 (1.002) |
| 1 | 2.97e-12 | 1.93e-12 | 1/4 | 1/4 | 7.40e17 | 1/2: 5.01e16 | 1/2: 4.63e16 (1.001) |
| 2 | 2.23e-12 | 1.45e-12 | 1/4 | 1/4 | 2.34e17 | 1/2: 2.39e16 | 1/2: 1.46e16 (0.998) |
| 3 | 1.67e-12 | 1.08e-12 | 1/2 | 1/2 | 7.41e16 | none | none |
| 4 | 8.36e-13 | 5.42e-13 | 1/2 | 1/2 | 4.63e15 | none | none |
| 5 | 4.18e-13 | 2.71e-13 | 1/4 | 1/4 | 2.90e14 | 1/2: 1.59e15 | 1/2: 1.81e13 (0.999) |
| 6 | 3.13e-13 | 2.03e-13 | 1/4 | 1/16 | 9.16e13 | 1/2: 8.77e14 | 1/2: 5.73e12 (1.001), 1/4: 3.58e11 (1.001), 1/8: 2.24e10 (1.002) |

Delta − truth before each step (table_keep_s1.log, summed from the log's three-digit dDelta): 0, −2.750e-13,
−7.575e-13, −1.120e-12, −1.660e-12, −1.931e-12, −1.999e-12, and −2.011e-12 after step 6 (A_s1: −2.050e-12 after its
step 6, −2.127e-12 after step 8). The trial law over all 15 refused trials of keep_s1 (table_keep_s1.log): point
max|F| = 5.214e64 |dz|^3.9990, or 5.3589e64 move^4 within 0.19% for the lam-1 trials and 0.3% for the shorter ones.
A_s1's lam-1 trials gave 5.3587e64 (#839).

### The algebra

From the projected iterate zp, with s the step there, a trial at lam is zp + lam s − (1 − lam) disp by default
(the iterate z = zp − disp, the direction disp + s) and zp + lam s with the option. At lam 1 the two are one point.
The projection moves only m_h and a_h, so two trials with one bulk part project to one point. While the accepted lam
agree, the projected iterates and the lam-1 trials agree, and the logs show it: the lam-1 lines are A_s1's at all 7
steps, the |R| of their failed projections included.

### Step 5 against the prediction

Step 5 did not depart. Its lam 1/2 came at the predicted 1.81e13 (2.90e14/16), 88 times below A_s1's refused 1.59e15,
and its projection failed all the same. The departure came at step 6, towards shorter steps.

### The reading

The crawl is the failure of the full step's projection, not the choice of iterate. No lam-1 trial has projected in
16 steps of the two runs, from point max|F| 1.26e18 down to 1.81e12. Without a lam-1 step, |F| falls at most by
(1 − lam) per step. It does fall exactly so: |F_new| = (1 − lam)|F| at every step. The projection's success is not
set by the trial's point max|F| either. Every projection path starts from the trial's own horizon data (the u0
rung, its quad-double polish, the re-seed's polish from the point's own data, and the ladder's first rung), and the
polish stops when its first Newton step after six block steps rises past 1e12 times the best (polish_q with
take_all). At step 6 the default's trials, whose horizon data are mixed toward the unprojected iterate's, projected
at lam 1/4. keep_s1's, zp_h + lam s_h, failed at lam 1/8 from point max|F| 2.2e10. So where the horizon data start
decides. #850 and #852 (the coordinator's note) put plain Newton's quadratic region at D 240 near 1e-81 relative in
Delta, against this start's 1e-12.

The pivots, paired with their own point: the step line prints the accepted point's pivots (octo_corrector.newton_od
prints st after z, st = zk, stt). Paired with that point's own |dz|, the smallest pivot is 0.0102–0.0108 |dz| at all
16 accepted points of both runs, 0.0105 within the printed pivots' two digits (pivot_pair.log, with its selftest and
control). The smallest LU pivot thus falls in proportion to |dz|, and so to |F| (|F| = 1.54 |dz| at every point).

### Discrepancies

- #839's table and fit paired each step's printed pivot with the |dz| the step started from: pivot/|dz| 0.0053–0.0104,
  fit 4.1e-3 |dz|^0.98 (I839-mac README, "Stopped"). The pivot belongs to the accepted point. With that point's own
  |dz| the ratio is 0.0102–0.0108 (above). table_839.py pairs them the same way and was used here unchanged
  (table_keep_s1.log); pivot_pair.py gives the corrected pairing.
- Prediction 1 (lam 1 by step 4 or 5) was wrong. It was corrected before step 4 from A_s1's log ("Prediction 1
  corrected").
- table_keep_s1.log exits 1, as A_s1's did: its Delta check needs planted's JSON, which a stopped run does not write.
  off_step0.log's exit 1 is planted's (a) verdict after one step.
- Times: keep_s1's steps took 44–123 min (step 6: 7388 s), and the dz0 runs 12.5 min each, against 30–60 min and
  6 min estimated. Another agent's 3-thread jobs shared the CPU.

### Recommended task: project the full step's point from other horizon starts

- **What:** at step 0 of the D 252.6 planted test, take the lam-1 trial's bulk zp0_b + s0_b from I854-mac/dz0_keep.npz
  (z the projected start, d its step, eight parts each). Project it with planted's settings (Reseeder with qd,
  qd_start pred, od 3; ElimO switch 0; 3 threads) from these horizon starts:
  - (a) zp0_h + s0_h, the logged trial, as the control;
  - (b) zp0_h, the start's own consistent data, without the tangent step;
  - (c) the lam-1/8 trial's projected data, extrapolated linearly in lam to 1;
  - (d) a chain lam 1/4, 1/2, 1, each starting from the previous projection's data;
  - (e) start (a) with polish_q's rise_max 1e40 and it_max 64.

  For each converged projection, take newton_o at the projected point: its pinned max|F| and |dz|.
- **Why:** the crawl of #839 and #854 is the failure of the full step's projection. Every failed projection stops at
  the polish's first Newton step after the block steps, and step 6 of #854 showed that the start's horizon data
  decide.
- **Acceptance:**
  - (a) reproduces the logged failure (u0 quad-double |R| 7.48e17 → 1.83e14, ladder FAILED), or the task stops.
  - The lam-1/8 trial projects from its own data, as in the runs (the second control).
  - For each of (b)–(e), report converged or not and the |R| reached.
  - A start passes when its projection converges and the projected point's pinned max|F| and |dz| fall below the
    start's 3.40e-12 and 2.20e-12, since the own test then accepts the full step. Otherwise its numbers are reported
    against those.
- **Cost:** about 8 projections at 13–27 min each and 2–3 newton_o calls at 3 threads, about 3–4 h. A script of about
  100 lines.
- **Depends on:** #854 (raw I854-mac, dz0_keep.npz).

### Files

keep_s1.log and keep_s1_at_stop.log (the run, stopped after step 6), side_854.py with side_854*.log (the table and
its checks), pivot_pair.py with pivot_pair.log, table_keep_s1.log (table_839.py on keep_s1), cmp_854.py with
cmp_dz0.log and cmp_step0.log, the dz0 runs (dz0_old, dz0_off, dz0_keep: .log and .npz), off_step0 (.log, .json,
.npz), queue.sh and queue.log, run.sh, and the toy's logs (toy.log, toy_keepskip.log, toylogs_*.txt, toy_logs.py).
