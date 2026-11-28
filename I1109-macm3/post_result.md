#1109 stage 1c roots on macm3 with Rust block 12, runner t5-macm3 (MacBook Air M3), 2026-11-28 07:36 UTC. Raw: `I1109-macm3/`, raw-data commit c8ac83ce7.

**The control passes bar 1: r0's root 0.0455917190 is +1.08e-10 from mm5's refined 0.0455917189 (bar 1e-05).** w01's root is 0.0454377413 (r0 -1.5398e-04) and w10's is 0.0440586917 (r0 -1.5330e-03), both from exit 4 runs: the last det-linear point was not robust (dln > 0.1), so each is a det-linear estimate inside its final robust bracket, 7.40e-05 and 1.17e-04 wide. Root shift over Delta shift: 0.7868 (w01), 0.7838 (w10).

### Roots (by `roots_summary.py`, output `roots_summary.txt`; `--tol=1e-6 --maxev=20 --b12=rust --b12_threads=2`, D 23.0, k_c 127)

| state | bracket given | evaluations | exit | status | final robust bracket (width) | det-linear root | root - r0 | Brent end | seconds |
|---|---|---|---|---|---|---|---|---|---|
| r0 | (0.044, 0.047) | 6 | 0 | tol | [0.045591589325629484, 0.045592089325629484] (5.000e-07) | 0.04559171900836614 | +0.000000e+00 | 0.045591589325629484 | 3435 |
| w01 | (0.04, 0.05) | 8 | 4 | nonrobust | [0.04543682118453806, 0.04551080985916185] (7.399e-05) | 0.045437741323263336 | -1.539777e-04 | 0.04543682118453806 | 4067 |
| w10 | (0.035, 0.055) | 7 | 4 | nonrobust | [0.0439440084375612, 0.044061381734647125] (1.174e-04) | 0.044058691651310954 | -1.533027e-03 | 0.044061381734647125 | 3858 |

No bracket was widened (no exit 2). Evaluations (lambda, hybrid sign, float64 sign, dln, robust, seconds):

- r0: 0.044 +1 +1 6.02e-06 R 532; 0.04558004240440045 +1 +1 7.56e-04 R 583; 0.045591589325629484 +1 +1 6.55e-02 R 543; 0.045592089325629484 -1 +1 2.40e-02 R 575; 0.045847052968168205 -1 +1 3.42e-05 R 577; 0.047 -1 +1 5.81e-06 R 625
- w01: 0.04 +1 +1 2.07e-06 R 531; 0.04394636449886087 +1 +1 6.39e-06 R 543; 0.04543682118453806 +1 +1 9.66e-03 R 457; 0.045437741323263336 -1 +1 3.03e-01 NOT robust 297; 0.04551080985916185 -1 +1 1.21e-04 R 523; 0.04588650575739605 -1 +1 1.93e-05 R 540; 0.0479221690466289 -1 +1 3.49e-06 R 561; 0.05 -1 +1 2.39e-06 R 616
- w10: 0.035 +1 +1 1.34e-06 R 532; 0.0439440084375612 +1 -1 7.87e-05 R 584; 0.044058691651310954 +1 -1 5.68e-01 NOT robust 423; 0.044061381734647125 -1 -1 3.30e-03 R 544; 0.044260916043785035 -1 -1 4.41e-05 R 575; 0.05288801687512241 -1 -1 1.70e-06 R 576; 0.055 -1 -1 1.57e-06 R 625

### Bars and reading

| item | value | verdict |
|---|---|---|
| bar 1: r0 root within 1e-05 of 0.0455917189 | 0.04559171900836614, difference +1.0837e-10 | **PASS** |
| bar 2: w01 root, w01 - r0 | 0.045437741323263336, -1.539777e-04; bracket gives -1.5490e-04 to -8.0909e-05 | reported |
| reading: Delta moved -1.957e-04; root shift / Delta shift | 0.7868 (bracket 0.792 to 0.413) | for reading |
| bar 2: w10 root, w10 - r0 | 0.044058691651310954, -1.533027e-03; bracket gives -1.6477e-03 to -1.5303e-03 | reported |
| reading: Delta moved -1.956e-03; root shift / Delta shift | 0.7838 (bracket 0.842 to 0.782) | for reading |

The two ratios agree to 0.39% (det-linear roots); the brackets are wider than that, w01's most (ratio 0.413 to 0.792).

### What ran

Step 1 (`ellrs/build.sh` in `venv-macm3-1058b`, "ellrs neon accelerate"): `ell_b12rs.py selftest` exit 0, `--mutate=nolam` exit 1, `--mutate=harm` exit 1, `check` (k_c 31, D 10.5, lambda 2.87, 2 threads, controls) exit 0: 15010 of 15010 entries bit for bit, both controls 0 of 15010 (logs `selftest*.log`, `check_kc31.log`).
Step 2: three `d18_secant.py run` at once, 2 threads each (`RAYON_NUM_THREADS=2`, OpenBLAS and vecLib 1), `nice -n 10`, `caffeinate -is`, 14400 s cap each (`common/capped_run.py`), detached by `common/launch_1070.py` (a copy from the #1025 runs). Started 2026-11-28 06:27:28 UTC; r0 ended 07:24:50, w10 07:31:51, w01 07:35:21 UTC. Code: `~/Source/choptuik-ell1fast` at 693a4d79; inputs blob-checked (R0 90d3e655, d1a3a641; w01 458d9026, 3410f1e5; w10 9947a645, eb52631f; r0 `--pin` matched). Each run printed the record system at start: |F| 3.1959e-10, 3.1878e-10, 3.1673e-10 against the records' 3.1949e-10, 3.1852e-10, 3.1660e-10; steps 4179, 4179, 4182. RSS 2.8 to 3.0 GiB per process (one sample, 9 min in); load average 15 to 20 from other processes; 532 to 625 s per evaluation with the three at once.

### Failed or disagrees

- w01 and w10 ended exit 4 (nonrobust final point, dln 0.303 and 0.568 against the 0.1 limit), as the stage 1c control did with `--b12=fast`; their roots are the det-linear estimates at those points. w01's sign at its last point (hybrid -1, not robust) and w10's (hybrid +1, not robust) are not trusted; taken at face value they narrow w01's root to between 0.04543682 and 0.04543774 and w10's to between 0.04405869 and 0.04406138.
- The float64 sign disagrees with the hybrid sign for w10 at 0.0439440 and 0.0440587 (f64 -1, hybrid +1) and, for r0 and w01, at every evaluation above the root (f64 +1 up to lambda 0.047 and 0.05, hybrid -1). The hybrid sign is the one the roots use.
- r0 against mm5's stage 1c2 B (same bracket, same code path, other machine): det-linear roots differ by 1.40e-10; the final brackets' ends differ by 3.8e-8 (here [0.045591589325629484, 0.045592089325629484], mm5 [0.04559155115141893, 0.04559205115141893]).
- Nothing was pushed or posted from this Mac (SSH and gh unavailable); the `running` label and the "started" comment are not set.

### Recommended tasks

- **A third state on the same line (w03 or w05), then the root shifts against Delta.** What: re-solve k_c 127 at D 23.0 with Delta moved a fraction of R0's weak-vector step, root by `--b12=rust`. Why: the two det-linear shifts give 0.787 and 0.784 times the Delta shift, but w01's bracket allows 0.41 to 0.79. Acceptance: the third point's root shift over its Delta shift lies within 2% of 0.785, or the linear reading is withdrawn. Depends on: whatever built `sol_w01` and `sol_w10` (mm5, #1109 stage 1c).
