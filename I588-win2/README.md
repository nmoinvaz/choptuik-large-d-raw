# I588-win2: ulp replicas of the twelve R 0.06 circles, an empirical error bar for their zero positions

Issue https://github.com/nmoinvaz/choptuik-large-d/issues/588 (assigned by the coordinator at 11:37 UTC, 2026-11-12, moved from win3). Machine win2 (Windows 11 desktop, Intel Core Ultra 7 265K, 20 threads, 96 GB), 9 threads of it. Code: worktree `D:\choptuik-i573` at main 80b5056 (`hp/modecount_circle.py` `circle()`, `hp/modecount_common.py` `setup`), the same build as `I574-win2/README.md` (`modecount_cx.cp312-win_amd64.pyd` sha256 7ab672ea9a17b239eb77897aaf5ec32de00580b70c3522707785b3bec4e722c3, Python 3.12.8 in venv-t126).
States (`hp/data/modecount_state_D61.0264_M48_kf<K>.npz`) sha256: kf 22 7dd8e81469dbf2f7318d28ee36e4fe16226c016bff16b0803b0e8cb38f7cf6b1; kf 25 48ac56a22988ffdcb30d40cd6262b9493a327a77b4fffd0a7b61af873a0f50de; kf 27 1fd892fcd0e326276b1885f10fc42421d917590f298e585867adb3fc352e8ac1; seed `up23_D61.0264.npz` sha256 c3393ce849de0f11406a02c5227a32cbb41795d29f5d8c2856fb2093a463a948. Every determinant is `setup(..., M=48, threads=1, kf=K, fmax=1e-15).det(re, im)`, one thread per process.
The issue text says the twelve circles are at kf 27 (#507, #573, #574). The twelve R 0.06 circles run on win2 are #573's ten (kf 22: four, kf 25: six), #574's one and #585's one (kf 27), each at its own cut and state (`circles_588.json`); #507's ran on macm3.
Pre-registered before any evaluation of this task: `predictions_588.json` (the design, the derivation of the expected spread, seven criteria Q1 to Q7 and the controls) and `circles_588.json`, committed to the raw-data repository before the run. Results follow in this README.

## Results (2026-11-12 11:42:05 to 14:05:18 UTC)

**Summary.** The position of a zero from an R 0.06 circle scatters under single-ulp moves of its arguments by **2e-8 to 1e-7 at kf 22, 1e-6 to 7e-6 at kf 25 and 1.6e-5 to 2.5e-5 at kf 27**, the spread growing by a factor of about 3 per kf step. At kf 22 and kf 25 the circle's own n0/2-against-n0 estimate has the size of the spread (ratio 0.4 to 1.9, no zero flagged); at kf 27 it does for A (1.3) and is 6.9 times too small for B, which is the one flagged zero. The 12 controls reproduce the stored zeros bit for bit, and all 120 shifted replicas resolve with winding +1. Three of the seven predictions failed (Q1, Q3, Q4), all because I took the arithmetic noise as the same at every cut; Q2 holds with values close to the analytic estimate. The predictions were fixed and committed before any evaluation (`predictions_588.json`, raw 05ef0e3e).

132 replica runs (12 circles × 11), 3960 determinants, 9 worker processes of one thread each, 8593 s (`replicas_588.py`, `replicas_588.log`, `replicas_588.jsonl`, `replicas_588_evals.jsonl`); 18.6 s a determinant (median, 12.6 to 29.9 s), 20.9 h of single-thread time. The table is `results_588.txt` (`analyze_588.py`, whose `--selftest` recovers a known scatter and fails a control moved by an ulp, and whose `--mutate=control` makes Q5 fail); the per-cut table is `results_588_percut.txt` (`percut_588.py`).

**What the spread is.** s = sqrt(Σ|z_r − z̄|² / (N − 1)) over the 10 shifted replicas of one circle, in the complex plane: the sample std of the recovered position when every argument det M is asked at is moved by 1 to 3 ulp, a sample std over 10 replicas (relative uncertainty about 24%), the rounding-noise error bar of the double-double evaluation at that cut. It is not a bound, and it does not include the truncation or state errors of the cut itself, nor the dependence on kf or M. "Own estimate" is the stored circle's own n0/2-against-n0 power-sum difference.

**Per cut** (`results_588_percut.txt`):

| kf | zeros | replica spread s, range | s, geometric mean | s / own estimate, range | flagged | median (replicas' own estimate / s) | spread of s in the ensemble (std of ln s) |
|---|---|---|---|---|---|---|---|
| 22 | 4 | 1.8e-08 to 9.6e-08 | 5.95e-08 | 0.6 to 0.8 | 0 | 0.84 | 0.69 |
| 25 | 6 | 1.1e-06 to 7.4e-06 | 2.82e-06 | 0.4 to 1.9 | 0 | 0.80 | 0.60 |
| 27 | 2 | 1.6e-05 to 2.5e-05 | 1.97e-05 | 1.3 to 6.9 | 1 | 0.96 | 0.23 |

**Per zero** (`results_588.txt`):

| circle | kf | stored zero | own estimate | replicas used | replica spread s | s / estimate | flag (s > 3 x est) | replicas' own estimate (median) | stored zero from the replica mean | control bit equal |
|---|---|---|---|---|---|---|---|---|---|---|
| k22_z_re2.0446_im-0.0003 | 22 | 2.043533-0.000000i | 2.3e-08 | 10 of 10 | 1.80e-08 | 0.8 | no | 1.2e-08 | 2.94e-08 | yes |
| k22_z_re2.0845_im+0.9868 | 22 | 2.086880+0.989734i | 1.4e-07 | 10 of 10 | 8.56e-08 | 0.6 | no | 4.9e-08 | 4.96e-08 | yes |
| k22_z_re2.0845_im-0.9868 | 22 | 2.086880-0.989734i | 1.4e-07 | 10 of 10 | 9.58e-08 | 0.7 | no | 9.7e-08 | 4.68e-08 | yes |
| k22_z_re2.6897_im+0.4761 | 22 | 2.689714+0.476098i | 1.2e-07 | 10 of 10 | 8.48e-08 | 0.7 | no | 1.1e-07 | 6.38e-08 | yes |
| k25_z_re1.9489_im+0.9436 | 25 | 1.948891+0.943589i | 2.6e-06 | 10 of 10 | 2.01e-06 | 0.8 | no | 1.3e-06 | 2.43e-06 | yes |
| k25_z_re1.9489_im-0.9436 | 25 | 1.948893-0.943590i | 5.2e-06 | 10 of 10 | 2.22e-06 | 0.4 | no | 1.6e-06 | 2.11e-06 | yes |
| k25_z_re2.0446_im+0.0003 | 25 | 2.043531-0.000001i | 2.6e-06 | 10 of 10 | 1.10e-06 | 0.4 | no | 9.5e-07 | 1.93e-06 | yes |
| k25_z_re2.4727_im+0.5755 | 25 | 2.472506+0.575722i | 6.2e-06 | 10 of 10 | 3.27e-06 | 0.5 | no | 4.0e-06 | 3.43e-06 | yes |
| k25_z_re2.4727_im-0.5755 | 25 | 2.472511-0.575721i | 2.2e-06 | 10 of 10 | 4.22e-06 | 1.9 | no | 3.1e-06 | 4.29e-06 | yes |
| k25_z_re2.9040_im+0.2433 | 25 | 2.903469+0.242777i | 1.1e-05 | 10 of 10 | 7.37e-06 | 0.7 | no | 6.4e-06 | 5.51e-06 | yes |
| k27_z_re1.9028_im+0.9160 | 27 | 1.903548+0.910715i | 1.2e-05 | 10 of 10 | 1.57e-05 | 1.3 | no | 1.5e-05 | 2.16e-06 | yes |
| k27_z_re2.3966_im+0.5477 | 27 | 2.396581+0.547584i | 3.6e-06 | 10 of 10 | 2.48e-05 | 6.9 | **FLAG** | 2.4e-05 | 3.43e-05 | yes |

| prediction | verdict |
|---|---|
| Q1: all twelve s between 7e-6 and 7e-5 | **fails**: only the kf 25 zero at 2.904 (7.4e-6) and the two kf 27 zeros are in; the others are lower, down to 1.8e-8 |
| Q2: A in 8e-6 to 3.2e-5, B in 1.4e-5 to 5.6e-5 | holds: A 1.57e-5, B 2.48e-5 (the analytic R \|ε\| / √n0 from #585's noise gives 1.6e-5 and 2.7e-5) |
| **Q3: 8 to 11 zeros flagged** | **fails**: 1 (B) |
| **Q4: kf 22 median s / estimate above 100** | **fails**: 0.7 |
| Q5: control bit for bit, 12 of 12 | holds |
| Q6: at least 118 of 120 shifted replicas resolve with winding +1, at least 9 of 10 for each circle | holds: 120 of 120 |
| Q7: stored zero within 3 s of the replica mean for at least 11 of 12 | holds: 12 of 12 (offsets 2e-8 to 3.4e-5 against s) |

**What this says, and what it does not.**

- The cause of the three failures is my assumption (H_noise) that the arithmetic noise of det M is the same at every cut. #585 measured it only at kf 27. The data say the opposite: the spread of a W = 1 circle is R |ε| / √n0, so |ε|, the noise per determinant, is about 4e-6 at kf 22, 2e-4 at kf 25 and 1.5e-3 at kf 27 (from the geometric means of s), rising by 3.6 times a kf step from 22 to 25 and by 2.6 from 25 to 27. Three cuts do not tell the law; the source of the growth (the matrix's conditioning, the number of frozen harmonics) is untested.
- A circle's own estimate is a single draw of the same noise. The median of the replicas' own estimates is 0.8 to 0.96 of s at each cut (the table above), so on average it is the right size, but one draw varies: B's stored estimate, 3.6e-6, is 7 times below the 2.4e-5 that its replicas typically report. Where a bar matters, a replica spread (10 replicas, 30 determinants each) is the measured one; the stored estimate alone can be low by that factor at kf 27.
- These are the noise of the double-double determinant. They say nothing of the exact determinant (#584, #594), which moves only 3e-5 rad per ulp, and the bars apply to the double-double circles of #573, #574 and #585 only.
- The twelve circles are the ones run on win2 (kf 22, 25 and 27), not the kf 27 circles of #507 (macm3's); the coordinator confirmed this at 11:43.

**Notes.** Scripts: `replicas_588.py`, `analyze_588.py`, `percut_588.py`, with `circles_588.json`, `predictions_588.json`, `run_start.txt`. The determinants were computed on Windows (libm `pow` differs from macm3's). The control replica is evaluated freshly, not read from the cache.
