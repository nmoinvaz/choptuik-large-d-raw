# I573-win2: #507's new zero pairs at the cuts kf 22 and kf 25 (mode-count circles at D 61.0264)

Issue https://github.com/nmoinvaz/choptuik-large-d/issues/573 (moved from macm3 to win2 by the coordinator at 07:46 UTC). Machine win2 (Windows 11 desktop, Intel Core Ultra 7 265K, 20 threads, 96 GB). Code: worktree `D:\choptuik-i573` at main 80b5056 (`hp/modecount_circle.py`), the complex determinant module built there by `hp/modecount_build.sh` (`cargo build --release --offline` with `-C target-cpu=native`, after one online `cargo fetch --locked` for multidouble 4.1.0, because the offline build found no cached copy): rustc 1.96.0 (ac68faa20 2026-05-25), cargo 1.96.0 (30a34c682 2026-05-25), Python 3.12.8 (venv-t126), `modecount_cx.cp312-win_amd64.pyd` sha256 7ab672ea9a17b239eb77897aaf5ec32de00580b70c3522707785b3bec4e722c3.
States, copied to `hp/data/` from the raw clone (kf 22 and kf 25 from `I244-macm3/kf22|kf25/hp_data_after/`, kf 27 from `I280-macm3/hp_data_after/`), sha256: kf 22 7dd8e81469dbf2f7318d28ee36e4fe16226c016bff16b0803b0e8cb38f7cf6b1; kf 25 48ac56a22988ffdcb30d40cd6262b9493a327a77b4fffd0a7b61af873a0f50de; kf 27 1fd892fcd0e326276b1885f10fc42421d917590f298e585867adb3fc352e8ac1. The seed `hp/data/seeds/local/up23_D61.0264.npz` sha256 c3393ce849de0f11406a02c5227a32cbb41795d29f5d8c2856fb2093a463a948.
Every circle is one process, one thread, below-normal priority, with its own empty cache: `python modecount_circle.py data/seeds/local/up23_D61.0264.npz RE,IM,0.36 --M=48 --kf=K --n0=20 --fmax=1e-15 --data=<circle folder> --res=<circle folder>/res.jsonl`, from `hp/`, up to 18 at once (`drive_57x.py`, jobs in `jobs_stage1.json`, status in `jobs_status.jsonl`). Cap: 150 points per circle (the script has no cap option; the driver stops a process whose cache holds more than 152 determinants and writes `cap.json`). Circles of #573: the control at 2.55 + 0.25i (kf 22) and 2.75 + 0.25i (kf 25), then eight circles per cut at Re 1.85 and 2.35 with Im +0.25, -0.25, +0.75, -0.75, then stage 2. Results follow in this README.

## Results (2026-11-12 07:52:04 to 08:38:30 UTC)

28 circles, one process and one thread each, below-normal priority, up to 18 at once: stage 1 (18 circles, 07:52 to 08:21) and stage 2 (10 circles of R 0.06, 08:26 to 08:38). All 28 exited 0, all resolved, none reached the 150-point cap (stage 1: 31 to 63 determinants, 12 to 29 min a circle; stage 2: 30 determinants, 12 min). A determinant takes 27 s (median, max 36 s) on one thread: 1069 determinants, about 8 h of single-thread time in 46 min of wall time. Per-circle records: `<circle>/res.jsonl`, `<circle>/stdout.log`, `jobs_status.jsonl`; the table below is `results_summary_573.txt` (`summ_57x.py`).


== I573-win2
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

**Acceptance.**

1. *The windings above and below are equal, and each zero found has a +1 circle: met.* Stage 1: kf 22 at Re 1.85: Im +0.25 and -0.25 both +1 (zero 2.0446), Im +0.75 and -0.75 both +1 (zero 2.0845 +- 0.9868i); at Re 2.35: Im +-0.25 both 0, Im +-0.75 both +1 (zero 2.0979 +- 0.9895i). kf 25: Re 1.85: Im +-0.25 both +1 (zero 2.0446), Im +-0.75 both +1 (1.9489 +- 0.9436i); Re 2.35: Im +-0.25 both +1 (2.4792 +- 0.5777i), Im +-0.75 both +1 (2.4727 +- 0.5755i). Stage 2 gave every zero found a circle of R 0.06 (one per zero, positions closer than 0.03 taken as one, the best estimate used; the conjugate partner was circled where stage 1 found it), and all ten wind +1, resolved, with positions to 1e-7 to 1e-5.
2. *The control re-finds the box's pair at that cut: met.* kf 22: the control at 2.55 + 0.25i winds +1 with the zero 2.689714 + 0.476098i (stage 2, estimate 1e-7), against #244's own circle at kf 22, 2.689664 + 0.475823i (its estimate 2.9e-3): they differ by 5e-5 and 2.8e-4. kf 25: the control at 2.75 + 0.25i winds +1 with 2.903469 + 0.242777i (1e-5), against #447's 2.90346 + 0.24278i: they differ by 1e-5 and 3e-6.
3. *The pairs found per cut, and whether 2.3966 +- 0.5476i and 1.9035 +- 0.9107i move with the cut.*

| cut | real zero | pair near 1.9 (kf 27: 1.9035 +- 0.9107i, #507, #574) | pair near 2.4 (kf 27: 2.3966 +- 0.5476i, #507) | the box's pair |
|---|---|---|---|---|
| kf 27 | (not in these columns) | 1.9035 +- 0.9107i (#574: 1.903548 + 0.910715i) | 2.3966 +- 0.5476i | #472's pair |
| kf 25 | 2.043531 | 1.948891 +- 0.943590i | 2.472506 +- 0.575722i | 2.903469 +- 0.242777i |
| kf 22 | 2.043533 | 2.086880 +- 0.989734i | none found | 2.689714 +- 0.476098i |

(With +- the conjugate was found as well: both pairs at kf 25, the pair near 1.9 at kf 22; the box's pair was circled in the upper half-plane only.) **Both pairs move with the cut.** The pair near 1.9 goes from 1.9035 + 0.9107i (kf 27) to 1.9489 + 0.9436i (kf 25), a shift of (+0.0454, +0.0329), and to 2.0869 + 0.9897i (kf 22), a further (+0.138, +0.046), the kf 22 position being #244's own 2.086881 + 0.989734i. The pair near 2.4 goes from 2.3966 + 0.5476i (kf 27) to 2.4725 + 0.5757i (kf 25), a shift of (+0.0759, +0.0281) (the position of notes/MODE_COUNT.md's 2.4725 + 0.5757i). At kf 22 no zero is found near it: the circles at 2.35 +- 0.25i (R 0.36) wind 0, and the circles at 2.35 +- 0.75i find only the 2.0869 zero, so that pair has left the region the circles cover (1.99 < Re < 2.71, |Im| up to 1.11) or merged with another, and I have not located it. The real zero 2.0435 does not move: 2.043533 at kf 22 and 2.043531 at kf 25 (2e-6). The box's pair moves too (2.9035 + 0.2428i at kf 25, 2.6897 + 0.4761i at kf 22). So the zero pairs of #507 belong to the cut, like the pairs inside the box (#472), and are not separate from it.

**Checks and notes.** The cap of 150 points is enforced by the driver, since `modecount_circle.py` has none; no circle came near it. The determinants were computed on Windows and may differ from macm3's in their last bits (libm pow); the windings and the controls are what count. The offline build of `hp/modecount_cx` needed one online `cargo fetch` (see the top). The circles use the state's `--kf=K` and the seed `up23_D61.0264.npz`, M 48, `--fmax=1e-15`, n0 20; each log line starts with the state's |F| (1.3e-19 at kf 22).
