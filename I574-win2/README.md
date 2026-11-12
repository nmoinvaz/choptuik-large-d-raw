# I574-win2: the strips 1.0 < |Im lambda| <= 2.0 above #507's columns at kf 27 (mode-count circles at D 61.0264)

Issue https://github.com/nmoinvaz/choptuik-large-d/issues/574 (moved from macm3 to win2 by the coordinator at 07:46 UTC). Machine win2 (Windows 11 desktop, Intel Core Ultra 7 265K, 20 threads, 96 GB). Code: worktree `D:\choptuik-i573` at main 80b5056 (`hp/modecount_circle.py`), the complex determinant module built there by `hp/modecount_build.sh` (`cargo build --release --offline` with `-C target-cpu=native`, after one online `cargo fetch --locked` for multidouble 4.1.0, because the offline build found no cached copy): rustc 1.96.0 (ac68faa20 2026-05-25), cargo 1.96.0 (30a34c682 2026-05-25), Python 3.12.8 (venv-t126), `modecount_cx.cp312-win_amd64.pyd` sha256 7ab672ea9a17b239eb77897aaf5ec32de00580b70c3522707785b3bec4e722c3.
States, copied to `hp/data/` from the raw clone (kf 22 and kf 25 from `I244-macm3/kf22|kf25/hp_data_after/`, kf 27 from `I280-macm3/hp_data_after/`), sha256: kf 22 7dd8e81469dbf2f7318d28ee36e4fe16226c016bff16b0803b0e8cb38f7cf6b1; kf 25 48ac56a22988ffdcb30d40cd6262b9493a327a77b4fffd0a7b61af873a0f50de; kf 27 1fd892fcd0e326276b1885f10fc42421d917590f298e585867adb3fc352e8ac1. The seed `hp/data/seeds/local/up23_D61.0264.npz` sha256 c3393ce849de0f11406a02c5227a32cbb41795d29f5d8c2856fb2093a463a948.
Every circle is one process, one thread, below-normal priority, with its own empty cache: `python modecount_circle.py data/seeds/local/up23_D61.0264.npz RE,IM,0.36 --M=48 --kf=27 --n0=20 --fmax=1e-15 --data=<circle folder> --res=<circle folder>/res.jsonl`, from `hp/`, up to 18 at once together with #573's circles (`drive_57x.py`, jobs in `jobs_stage1.json`, status in `jobs_status.jsonl`). Cap: 150 points per circle (the driver stops a process whose cache holds more than 152 determinants and writes `cap.json`). Circles of #574: twelve of R 0.36 at Re 1.85, 2.35, 2.85, 3.35, 3.85, 4.35 and Im +1.25, +1.75; then the mirror (Im -> -Im) of every circle that winds nonzero, plus the mirror controls 2.35 - 1.25i and 3.35 - 1.25i, then small circles (R 0.06) on every zero found. Results follow in this README.

## Results (2026-11-12 08:07:34 to 08:42:00 UTC)

16 circles, one process and one thread each, below-normal priority, started by `drive_57x.py` together with #573's (at most 18 at once across both). Stage 1 is the twelve circles of R 0.36 at Re 1.85, 2.35, 2.85, 3.35, 3.85, 4.35 and Im +1.25, +1.75 (08:07 to 08:24, 9.0 to 16.8 min a circle, 22 to 48 determinants). Then came the R 0.06 circle on the zero found, the mirror of the one circle that winds nonzero, and two mirror controls at 2.35 - 1.25i and 3.35 - 1.25i (R 0.36, 08:26 to 08:42, 11.3 to 15.8 min, 27 to 30 determinants for the controls and the zero, 48 for the mirror). All 16 exited 0, all resolved, none reached the 150-point cap (`jobs_status.jsonl`). A determinant takes 25.2 s on one thread (median, 11 to 30 s): 463 determinants, 3.1 h of single-thread time. The coordinator moved #574 to win3 at 08:35 and cancelled the move at 08:37, after all twelve stage-1 circles had finished here; the four later circles were already running and finished. The table is `results_summary_574.txt` (`summ_57x.py`). The estimates in brackets are each circle's own range, not bounds.

| circle | state | evals so far | winding | points | resolved | max step | zeros inside (estimate) |
|---|---|---|---|---|---|---|---|
| k27_mctl_re2.35_im-1.25 | done | 27 | +0.0000 | 25 | yes | 0.376 |  |
| k27_mctl_re3.35_im-1.25 | done | 28 | +0.0000 | 26 | yes | 0.392 |  |
| k27_mirror_re1.85_im-1.25 | done | 48 | +1.0000 | 46 | yes | 0.389 | 1.902782 -0.916030i (2e-02) |
| k27_re1.85_im+1.25 | done | 48 | +1.0000 | 46 | yes | 0.389 | 1.902797 +0.916032i (2e-02) |
| k27_re1.85_im+1.75 | done | 27 | +0.0000 | 25 | yes | 0.351 |  |
| k27_re2.35_im+1.25 | done | 27 | +0.0000 | 25 | yes | 0.376 |  |
| k27_re2.35_im+1.75 | done | 26 | +0.0000 | 24 | yes | 0.361 |  |
| k27_re2.85_im+1.25 | done | 26 | +0.0000 | 24 | yes | 0.371 |  |
| k27_re2.85_im+1.75 | done | 26 | +0.0000 | 24 | yes | 0.365 |  |
| k27_re3.35_im+1.25 | done | 28 | +0.0000 | 26 | yes | 0.393 |  |
| k27_re3.35_im+1.75 | done | 22 | +0.0000 | 20 | yes | 0.194 |  |
| k27_re3.85_im+1.25 | done | 27 | +0.0000 | 25 | yes | 0.390 |  |
| k27_re3.85_im+1.75 | done | 22 | +0.0000 | 20 | yes | 0.125 |  |
| k27_re4.35_im+1.25 | done | 29 | +0.0000 | 27 | yes | 0.387 |  |
| k27_re4.35_im+1.75 | done | 22 | +0.0000 | 20 | yes | 0.059 |  |
| k27_z_re1.9028_im+0.9160 | done | 30 | +1.0000 | 28 | yes | 0.357 | 1.903548 +0.910715i (1e-05) |

**Coverage.** The twelve circles leave no point of the rectangle 1.6 <= Re <= 4.6, 1.0 <= Im <= 2.0 farther than 0.3536 (= 0.5/sqrt(2)) from a centre, against R 0.36 (`coverage_57x.py`, a 0.001 grid; its `--selftest` shows a dropped circle or R 0.35 leaving points uncovered). So every zero of that rectangle lies in at least one circle.

**Acceptance.**

- *The windings above and below are equal: met for the circles that were run in both half-planes, and not run for the rest.* Eleven of the twelve upper circles wind 0, the twelfth (1.85 + 1.25i) winds +1. Its mirror at 1.85 - 1.25i winds +1 and holds 1.902782 - 0.916030i (2e-2), the conjugate of the upper 1.902797 + 0.916032i (2e-2). The two mirror controls, at 2.35 - 1.25i and 3.35 - 1.25i, wind 0 as their upper twins do. The other nine lower circles (Im -1.25 at Re 2.85, 3.85, 4.35 and the whole Im -1.75 row) were not run: the lower strip -2.0 <= Im <= -1.0 is empty by the conjugate symmetry of the zero set, which these three mirror circles and #573's conjugate pairs (to 5e-6) support, and not by circles.
- *Each zero found has a +1 circle: met.* The circle of R 0.06 on 1.902797 + 0.916032i winds +1 and puts the zero at 1.903548 + 0.910715i (1e-5), against #507's 1.903566 + 0.910707i (5.5e-6): 2e-5 and 8e-6 apart.
- *1.9035 +- 0.9107i is found again by any circle that overlaps it: met.* Exactly one stage-1 circle contains it, the one at 1.85 + 1.25i (0.343 from the centre, R 0.36), and it finds it. The next nearest centres, 2.35 + 1.25i (0.56) and 1.85 + 1.75i (0.84), are farther than R and wind 0.

**So the rectangle 1.6 < Re < 4.6, 1.0 < Im <= 2.0 at kf 27 (D 61.0264, M 48) holds exactly one zero, 1.903548 + 0.910715i, and by the conjugate symmetry the strip 1.0 < |Im| <= 2.0 holds that zero and its conjugate.** The highest |Im| of any zero found at kf 27 stays 0.91. The determinants were computed on Windows and may differ from macm3's in their last bits (libm `pow`).

**Recommended tasks (the coordinator decides).** *The lower strip by circles.* What: the nine lower circles of R 0.36 not run (Im -1.25 at Re 2.85, 3.85, 4.35 and Im -1.75 at all six Re), with `drive_57x.py`. Why: the acceptance's "above and below" is met on three mirror circles only. Acceptance: all nine wind 0 and resolve, with no cap hit. Cost: about 2 h of single-thread time (the upper twins took 22 to 29 determinants of 25 s each). Depends on #574.
