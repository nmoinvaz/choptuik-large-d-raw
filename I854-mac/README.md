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
