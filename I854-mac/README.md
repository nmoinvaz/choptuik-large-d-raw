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
