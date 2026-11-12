# I574-win2: the strips 1.0 < |Im lambda| <= 2.0 above #507's columns at kf 27 (mode-count circles at D 61.0264)

Issue https://github.com/nmoinvaz/choptuik-large-d/issues/574 (moved from macm3 to win2 by the coordinator at 07:46 UTC). Machine win2 (Windows 11 desktop, Intel Core Ultra 7 265K, 20 threads, 96 GB). Code: worktree `D:\choptuik-i573` at main 80b5056 (`hp/modecount_circle.py`), the complex determinant module built there by `hp/modecount_build.sh` (`cargo build --release --offline` with `-C target-cpu=native`, after one online `cargo fetch --locked` for multidouble 4.1.0, because the offline build found no cached copy): rustc 1.96.0 (ac68faa20 2026-05-25), cargo 1.96.0 (30a34c682 2026-05-25), Python 3.12.8 (venv-t126), `modecount_cx.cp312-win_amd64.pyd` sha256 7ab672ea9a17b239eb77897aaf5ec32de00580b70c3522707785b3bec4e722c3.
States, copied to `hp/data/` from the raw clone (kf 22 and kf 25 from `I244-macm3/kf22|kf25/hp_data_after/`, kf 27 from `I280-macm3/hp_data_after/`), sha256: kf 22 7dd8e81469dbf2f7318d28ee36e4fe16226c016bff16b0803b0e8cb38f7cf6b1; kf 25 48ac56a22988ffdcb30d40cd6262b9493a327a77b4fffd0a7b61af873a0f50de; kf 27 1fd892fcd0e326276b1885f10fc42421d917590f298e585867adb3fc352e8ac1. The seed `hp/data/seeds/local/up23_D61.0264.npz` sha256 c3393ce849de0f11406a02c5227a32cbb41795d29f5d8c2856fb2093a463a948.
Every circle is one process, one thread, below-normal priority, with its own empty cache: `python modecount_circle.py data/seeds/local/up23_D61.0264.npz RE,IM,0.36 --M=48 --kf=27 --n0=20 --fmax=1e-15 --data=<circle folder> --res=<circle folder>/res.jsonl`, from `hp/`, up to 18 at once together with #573's circles (`drive_57x.py`, jobs in `jobs_stage1.json`, status in `jobs_status.jsonl`). Cap: 150 points per circle (the driver stops a process whose cache holds more than 152 determinants and writes `cap.json`). Circles of #574: twelve of R 0.36 at Re 1.85, 2.35, 2.85, 3.35, 3.85, 4.35 and Im +1.25, +1.75; then the mirror (Im -> -Im) of every circle that winds nonzero, plus the mirror controls 2.35 - 1.25i and 3.35 - 1.25i, then small circles (R 0.06) on every zero found. Results follow in this README.

## Results (2026-11-12 08:07:34 to 08:42:00 UTC)

16 circles, one process and one thread each, below-normal priority, run together with #573's: stage 1 (twelve circles, 08:07 to 08:21) and the mirrors and the small circle (four circles, 08:26 to 08:42). All 16 exited 0, all resolved, none reached the 150-point cap (stage 1: 22 to 48 determinants, 9 to 17 min a circle). A determinant takes 25 s (median, max 30 s) on one thread. Note: the coordinator moved #574 to win3 at 08:35, after the twelve circles had finished here; the four circles of stage 2 and the mirrors were already running and were left to finish. The table is `results_summary_574.txt` (`summ_57x.py`).


== I574-win2
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

**Acceptance.**

- *The windings above and below are equal: met.* Eleven of the twelve circles wind 0 (all except Re 1.85, Im +1.25). The mirror of the one that winds +1, at 1.85 - 1.25i, winds +1 and contains 1.902782 - 0.916030i, the conjugate of the upper zero 1.902797 + 0.916032i. The two mirror controls, 2.35 - 1.25i and 3.35 - 1.25i, wind 0 as their upper twins do.
- *Each zero found has a +1 circle: met.* The circle of R 0.06 on 1.902797 + 0.916032i winds +1 and puts the zero at 1.903548 + 0.910715i (estimate 1e-5).
- *1.9035 +- 0.9107i is found again by any circle that overlaps it: met.* The only stage-1 circle that contains it (distance 0.34 < R 0.36 from 1.85 + 1.25i) finds it; the circle at 2.35 + 1.25i is 0.56 away and does not overlap it. The position, 1.903548 + 0.910715i, is #507's 1.9035 + 0.9107i to 1e-5.

**So the strips 1.6 < Re < 4.6, 1.0 < |Im| <= 2.0 at kf 27, covered by twelve circles of R 0.36 at Re 1.85, 2.35, 2.85, 3.35, 3.85, 4.35 and Im +1.25, +1.75, hold no zero other than 1.9035 +- 0.9107i** (at stage 1; the circles overlap their neighbours, and the union leaves small gaps at their corners that I have not counted). The highest zero found stays at |Im| 0.91 (the pair 1.9035 +- 0.9107i). The determinants were computed on Windows and may differ from macm3's in their last bits.
