# I573-win2: #507's new zero pairs at the cuts kf 22 and kf 25 (mode-count circles at D 61.0264)

Issue https://github.com/nmoinvaz/choptuik-large-d/issues/573 (moved from macm3 to win2 by the coordinator at 07:46 UTC). Machine win2 (Windows 11 desktop, Intel Core Ultra 7 265K, 20 threads, 96 GB). Code: worktree `D:\choptuik-i573` at main 80b5056 (`hp/modecount_circle.py`), the complex determinant module built there by `hp/modecount_build.sh` (`cargo build --release --offline` with `-C target-cpu=native`, after one online `cargo fetch --locked` for multidouble 4.1.0, because the offline build found no cached copy): rustc 1.96.0 (ac68faa20 2026-05-25), cargo 1.96.0 (30a34c682 2026-05-25), Python 3.12.8 (venv-t126), `modecount_cx.cp312-win_amd64.pyd` sha256 7ab672ea9a17b239eb77897aaf5ec32de00580b70c3522707785b3bec4e722c3.
States, copied to `hp/data/` from the raw clone (kf 22 and kf 25 from `I244-macm3/kf22|kf25/hp_data_after/`, kf 27 from `I280-macm3/hp_data_after/`), sha256: kf 22 7dd8e81469dbf2f7318d28ee36e4fe16226c016bff16b0803b0e8cb38f7cf6b1; kf 25 48ac56a22988ffdcb30d40cd6262b9493a327a77b4fffd0a7b61af873a0f50de; kf 27 1fd892fcd0e326276b1885f10fc42421d917590f298e585867adb3fc352e8ac1. The seed `hp/data/seeds/local/up23_D61.0264.npz` sha256 c3393ce849de0f11406a02c5227a32cbb41795d29f5d8c2856fb2093a463a948.
Every circle is one process, one thread, below-normal priority, with its own empty cache: `python modecount_circle.py data/seeds/local/up23_D61.0264.npz RE,IM,0.36 --M=48 --kf=K --n0=20 --fmax=1e-15 --data=<circle folder> --res=<circle folder>/res.jsonl`, from `hp/`, up to 18 at once (`drive_57x.py`, jobs in `jobs_stage1.json`, status in `jobs_status.jsonl`). Cap: 150 points per circle (the script has no cap option; the driver stops a process whose cache holds more than 152 determinants and writes `cap.json`). Circles of #573: the control at 2.55 + 0.25i (kf 22) and 2.75 + 0.25i (kf 25), then eight circles per cut at Re 1.85 and 2.35 with Im +0.25, -0.25, +0.75, -0.75, then stage 2. Results follow in this README.

## Results (2026-11-12 07:52:04 to 08:38:30 UTC)

28 circles, one process and one thread each, below-normal priority, started by `drive_57x.py` (at most 18 at once across #573 and #574). Stage 1 is 18 circles of R 0.36 (07:52 to 08:21, 15.5 to 28.8 min a circle, 31 to 63 determinants), stage 2 is 10 circles of R 0.06 on the zeros stage 1 found (08:26 to 08:38, 12 min a circle, 30 determinants). All 28 exited 0, all resolved, none reached the 150-point cap (`jobs_status.jsonl` has every start and exit). A determinant takes 27.0 s on one thread (median, 17 to 36 s): 1069 determinants, 8.1 h of single-thread time in 46 min of wall time. The table is `results_summary_573.txt` (`summ_57x.py`), the per-circle records are `<circle>/res.jsonl` and `stdout.log`. The estimates in brackets are each circle's own range of the zero position, not bounds.

| circle | state | evals so far | winding | points | resolved | max step | zeros inside (estimate) |
|---|---|---|---|---|---|---|---|
| k22_ctl_re2.55_im+0.25 | done | 32 | +1.0000 | 30 | yes | 0.390 | 2.689693 +0.476118i (2e-03) |
| k22_re1.85_im+0.25 | done | 37 | +1.0000 | 35 | yes | 0.346 | 2.044645 -0.000320i (8e-03) |
| k22_re1.85_im+0.75 | done | 44 | +1.0000 | 42 | yes | 0.365 | 2.084515 +0.986767i (1e-02) |
| k22_re1.85_im-0.25 | done | 37 | +1.0000 | 35 | yes | 0.346 | 2.044645 +0.000320i (8e-03) |
| k22_re1.85_im-0.75 | done | 44 | +1.0000 | 42 | yes | 0.365 | 2.084515 -0.986767i (1e-02) |
| k22_re2.35_im+0.25 | done | 42 | +0.0000 | 40 | yes | 0.363 |  |
| k22_re2.35_im+0.75 | done | 63 | +1.0000 | 61 | yes | 0.372 | 2.097907 +0.989522i (3e-02) |
| k22_re2.35_im-0.25 | done | 42 | +0.0000 | 40 | yes | 0.363 |  |
| k22_re2.35_im-0.75 | done | 63 | +1.0000 | 61 | yes | 0.372 | 2.097907 -0.989522i (3e-02) |
| k22_z_re2.0446_im-0.0003 | done | 30 | +1.0000 | 28 | yes | 0.362 | 2.043533 -0.000000i (2e-08) |
| k22_z_re2.0845_im+0.9868 | done | 30 | +1.0000 | 28 | yes | 0.373 | 2.086880 +0.989734i (1e-07) |
| k22_z_re2.0845_im-0.9868 | done | 30 | +1.0000 | 28 | yes | 0.373 | 2.086880 -0.989734i (1e-07) |
| k22_z_re2.6897_im+0.4761 | done | 30 | +1.0000 | 28 | yes | 0.354 | 2.689714 +0.476098i (1e-07) |
| k25_ctl_re2.75_im+0.25 | done | 43 | +1.0000 | 41 | yes | 0.392 | 2.904046 +0.243263i (9e-03) |
| k25_re1.85_im+0.25 | done | 37 | +1.0000 | 35 | yes | 0.349 | 2.044650 -0.000316i (8e-03) |
| k25_re1.85_im+0.75 | done | 32 | +1.0000 | 30 | yes | 0.390 | 1.948889 +0.943595i (3e-05) |
| k25_re1.85_im-0.25 | done | 37 | +1.0000 | 35 | yes | 0.349 | 2.044639 +0.000325i (8e-03) |
| k25_re1.85_im-0.75 | done | 32 | +1.0000 | 30 | yes | 0.390 | 1.948894 -0.943595i (4e-05) |
| k25_re2.35_im+0.25 | done | 61 | +1.0000 | 59 | yes | 0.370 | 2.479188 +0.577672i (1e-02) |
| k25_re2.35_im+0.75 | done | 31 | +1.0000 | 29 | yes | 0.383 | 2.472722 +0.575472i (6e-03) |
| k25_re2.35_im-0.25 | done | 61 | +1.0000 | 59 | yes | 0.370 | 2.479201 -0.577669i (1e-02) |
| k25_re2.35_im-0.75 | done | 31 | +1.0000 | 29 | yes | 0.383 | 2.472716 -0.575477i (6e-03) |
| k25_z_re1.9489_im+0.9436 | done | 30 | +1.0000 | 28 | yes | 0.357 | 1.948891 +0.943589i (3e-06) |
| k25_z_re1.9489_im-0.9436 | done | 30 | +1.0000 | 28 | yes | 0.357 | 1.948893 -0.943590i (5e-06) |
| k25_z_re2.0446_im+0.0003 | done | 30 | +1.0000 | 28 | yes | 0.362 | 2.043531 -0.000001i (3e-06) |
| k25_z_re2.4727_im+0.5755 | done | 30 | +1.0000 | 28 | yes | 0.356 | 2.472506 +0.575722i (6e-06) |
| k25_z_re2.4727_im-0.5755 | done | 30 | +1.0000 | 28 | yes | 0.355 | 2.472511 -0.575721i (2e-06) |
| k25_z_re2.9040_im+0.2433 | done | 30 | +1.0000 | 28 | yes | 0.351 | 2.903469 +0.242777i (1e-05) |

**Coverage.** The four stage-1 circles of R 0.36 at Re 1.85, 2.35 and Im +-0.25, +-0.75 leave no point of the rectangle 1.6 <= Re <= 2.6, |Im| <= 1.0 farther than 0.3536 (= 0.5/sqrt(2)) from a centre, against R 0.36 (a 0.001 grid, `coverage_57x.py`, whose `--selftest` shows a dropped circle or R 0.35 leaving points uncovered), so every zero of the rectangle lies in at least one circle, at each cut.

**Zeros of the rectangle** (the conjugate of each complex zero was circled too and agrees to 5e-6; the exception is the kf 22 zero at 2.69, outside the rectangle, circled in the upper half-plane only):

| cut | real zero | pair near 1.9 | pair near 2.4 |
|---|---|---|---|
| kf 22 | 2.043533 (2e-8) | 2.086880 +- 0.989734i (1e-7) | outside: the zero is at 2.689714 + 0.476098i (1e-7), Re above 2.6 |
| kf 25 | 2.043531 - 0.000001i (3e-6) | 1.948891 +- 0.943590i (5e-6) | 2.472506 + 0.575722i, 2.472511 - 0.575721i (6e-6, 2e-6) |

(The kf 22 state is #244's, whose kf 22 equals kf 21: `plow_odd(M, 22)` and `plow_odd(M, 21)` project on the same odd harmonics, per #244's closing summary.)

**Acceptance.**

1. *The windings above and below are equal, and each zero found has a +1 circle: met.* Every stage-1 circle and its mirror agree: kf 22 at Re 1.85, Im +-0.25 both +1 (the real zero), Im +-0.75 both +1 (2.0869 +- 0.9897i); at Re 2.35, Im +-0.25 both 0, Im +-0.75 both +1 (the same pair, 0.356 from the centre); kf 25 at Re 1.85, Im +-0.25 both +1 (real), Im +-0.75 both +1 (1.9489 +- 0.9436i); at Re 2.35, Im +-0.25 both +1 and Im +-0.75 both +1 (2.4725 +- 0.5757i, 0.352 from the first centres). Each of the ten zeros that stage 1 located got a circle of R 0.06 (positions of one cut closer than 0.03 taken as one zero), all ten wind +1 and resolve, with the positions above (2e-8 to 1e-5).
2. *The control re-finds the box's pair at that cut: met.* At kf 22 the control at 2.55 + 0.25i winds +1 and its zero, 2.689714 + 0.476098i (R 0.06 circle, 1e-7), is #244's zero 3, 2.689664 + 0.475823i (its estimate 2.9e-3): 5e-5 and 2.8e-4 apart, inside that estimate. At kf 25 the control at 2.75 + 0.25i winds +1 and its zero, 2.903469 + 0.242777i (1e-5), is #447's box pair, 2.903462 + 0.242781i (4.3e-6): 7e-6 and 4e-6 apart.
3. *The pairs per cut, and whether 2.3966 +- 0.5476i and 1.9035 +- 0.9107i move with the cut: yes, both move.* They are #244's zeros 2 and 3, and the positions at kf 22 and 25 here agree with #244's own (zero 2: 1e-6 and 0 at kf 22, 0 at kf 25; zero 3: 5e-5 and 2.8e-4 at kf 22, inside #244's estimate of 2.9e-3, and 2e-6 and 5e-6 at kf 25):

| zero | kf 22 (= kf 21) | kf 23 (#244) | kf 25 | kf 27 (#507) |
|---|---|---|---|---|
| pair near 1.9 | 2.086880 +- 0.989734i | 2.0073 + 0.9727i | 1.948891 +- 0.943590i | 1.903566 + 0.910707i, 1.9035 +- 0.9107i (#574: 1.903548 + 0.910715i) |
| pair near 2.4 | 2.689714 + 0.476098i (upper half only) | 2.5584 + 0.5825i | 2.472506 + 0.575722i, its conjugate | 2.396619 + 0.547672i, 2.3966 +- 0.5476i |

Re falls with kf at each, 2.0869, 2.0073, 1.9489, 1.9035 and 2.6897, 2.5584, 2.4725, 2.3966. Im of the first falls too (0.9897, 0.9727, 0.9436, 0.9107), and Im of the second is 0.4761, 0.5825, 0.5757, 0.5476. So neither pair is a cut-independent zero. The pair near 2.4 is at 2.69 at kf 22, outside the column 1.6 < Re < 2.6, which is why the kf 22 stage 1 of the column finds only the real zero and 2.0869 +- 0.9897i. Its conjugate at kf 22 was not circled here (nor in #244). The real zero moves little: 2.043533 and 2.043531 - 0.000001i here, 2.043532 and 2.043535 + 0.000004i in #244 (kf 22 and 25).

**Discrepancy.** At kf 25 the real zero here, 2.043531 - 0.000001i (3e-6), and #244's, 2.043535 + 0.000004i (9.5e-7), are 4e-6 apart in Re and 5e-6 in Im, a little more than the two estimates added (4e-6). Not explained; both are under #244's stop rule of 1e-5.

**Notes.** The cap of 150 points is enforced by the driver (`modecount_circle.py` has none); no circle came near it. The determinants were computed on Windows and may differ from macm3's in their last bits (libm `pow`), which the windings and the controls do not depend on. The circle log header carries the state's |F|: 1.3e-19 at kf 22 (#244 gives 1.3e-19 at both cuts). The offline build of `hp/modecount_cx` needed one online `cargo fetch --locked` (see the top). All four rows of stage 1 (Im +0.25, +0.75, -0.25, -0.75) were run, so the lower half of the rectangle is covered by circles, and the three conjugate pairs of R 0.06 circles agree to 5e-6 (kf 22 exactly at 6 digits).
