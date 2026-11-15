# I812-macm3: #749's box at D 61.03 (M 48): the conjugate lenses at kf 39-45, then kf 47, the uncut system

Machine macm3 (M3 Mac, 6 threads), issue https://github.com/nmoinvaz/choptuik-large-d/issues/812.

Scripts (written by the coordinator): `common.sh` and `job.sh` (#789's, with the folder changed), `run_812_lens.sh`
(the four conjugate lenses, two at a time at 3 threads) and `run_812_kf47.sh` (kf 47's control and four R 0.36
circles, five single-thread processes). The same worktree and build as #749 and #789 (choptuik-large-d-749 at
bd7df22f, venv-macm3-314). The lenses run on the cuts' saved states in that worktree's hp/data.

Criteria (#812): each lens winds +1 with 0 mismatches, and its zero lies within its estimate of the conjugate of
#789's upper lens zero. At kf 47 the control winds +1, every circle has 0 mismatches, windings are up to 6, and the
count comes with its basis. The control's log header must show kfreeze 47; if it does not, report before the circles.
