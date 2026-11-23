# I1025-dh610/eval_dh170_d1975: dh170's k_c 87 D 19.75 start state evaluated on this build at lambda 1.32 and 1.33, against his rows and linRe's, to tell an evaluation difference between machines from a steep ln|det|

Machine dh610 (Fedora 45, i7-12700, 20 logical CPUs, 64 GB RAM, Linux). Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1025. Written 2026-11-23 08:48:52 UTC, before any run of this folder. The k_c 87 roots are not yet physical.

## Order (coordinator t5, hc, after the step 4 result of `../reconv_d1975`, raw ae9b6924), in part
"Go on your test: dh170's start state (352107a8, record 6078a0b4) on your build at 1.32 and 1.33 (2 processes of 1 thread, nice 10, record system first), and your two readings written in the README before the run: (a) yours differs from dh170's rows by ~0.4 and matches linRe within 1e-4: the two Linux machines evaluate ln|det| differently; (b) yours matches dh170's rows within 1e-3: ln|det| is that steep along the 4e-10 move. Also record each machine's CPU model and numpy/OpenBLAS core type (numpy.show_config or threadpoolctl) in the README, beside dh170's if you can read it from his folder."

## Why
In `../reconv_d1975` (step 4) linRe, which is 4.0279e-10 (L2, Delta included) from dh170's state, gave ln|det| = -2806.0300899137 at 1.32 and -2806.9886015473 at 1.33, and dh170's own rows (his machine) for his state give -2806.4460599255 and -2806.6102602939: differences +0.416 and -0.378, about 4000 times more per unit of |dz| than between the pairs of states on one build (about 2.5e+05 per unit), and the root near lambda_1's line is 1.327228 (linRe) against his 1.325410. macm3's macOS rows differ from this build's on the same state (macm3's) by at most 8.5e-04 in ln|det|.

## The readings, as numeric rules written before the run
x = ln|det| of dh170's state on this build at 1.32 and 1.33, h = dh170's own rows (`in/ref_dh170_scan_D19.75_1025.jsonl`: -2806.4460599255, -2806.6102602939), l = linRe's rows on this build (`in/ref_linRe_D19.75_1.32.jsonl`, `_1.33.jsonl`). Both lambda must satisfy a rule (`in/eval_compare.py`, whose selftest plants each case and whose `--mutate` must fail):
- **(b) ln|det| is that steep along the 4e-10 move:** |x - h| <= 1e-3.
- **(a) the two Linux machines evaluate ln|det| differently:** |x - l| <= 1e-4 and |x - h| >= 0.1 (the observed |l - h| is 0.416 and 0.378).
- **(c) neither:** anything else (for example x between the two, or off both); the numbers are reported.
(b) does not say what makes it steep. A third possibility, which this evaluation cannot tell from a smooth steepness, is that the discrete system differs: `freeze_from` sets each segment's RK4 step count to `max(4, ceil(L g / kappa rk))` from the state, so a move of 4e-10 can change one count by one when the argument is near an integer, and the total steps (3124) can stay equal. The information step below reads that directly.

## Information step (not ordered; one extra thread, no det evaluation)
`in/freeze_compare.py` builds the system for dh170's start state, linRe, macRe and macm3's start state exactly as `d18_hybsign.py` does and compares `freeze_from`'s step counts segment by segment, with |F| at that freeze. Its controls (exit 1 if either fails): a state against itself differs in no segment; dh170's state at kappa 0.7 against kappa 0.69 differs in at least one.

## Inputs (copies in `in/`; `in_blobs.txt` lists their `git hash-object --no-filters` blobs; the lane refuses any other blob)
| item | blob |
|---|---|
| dh170's k_c 87 D 19.75 state `sol_l1kc87dh170d1975_D19.7500.npy` (raw I1025-dh170/kc87_d1975) | 352107a8 |
| dh170's record `l1kc87dh170d1975.jsonl` (|F| 3.987605893965491e-10, 3124 steps) | 6078a0b4 |
| `d18_hybsign.py` (xfkappa's, unmodified) | e089207a |
| dh170's rows `ref_dh170_scan_D19.75_1025.jsonl` (1.30 to 1.33, his machine) | 0336f50f |
| linRe's rows at 1.32 and 1.33 (this build, `../reconv_d1975/scan/lin`) | b1d3f64a, 99d9b463 |
| linRe, macRe, macm3's start state and their records (`../reconv_d1975/in`) | 4988a55c / 6735329b, a81f02dc / 19f8e9ce, 5825f5d0 / 84f75a48 |
| `eval_compare.py`, `freeze_compare.py` (mine) | 2dbbccc2, 92c0dbfe |
Worktree `~/Source/choptuik-large-d-1025f` at 505d8399 (clean), python `~/Source/venv-i1058/bin/python`.

## Commands (`lane_eval.sh` via `start_eval.sh` = systemd user unit i1025ac under `systemd-inhibit` with the alert-only memory log)
- Pre-run: pins, worktree, `eval_compare.py selftest` exit 0 and `--mutate` exit 1, MemAvailable at least 3 x 2.5 GB + 4 GB (the k_c 87 processes peaked at 2.2 GB).
- Two processes of 1 thread (OPENBLAS/OMP/MKL = 1), nice 10, cap 28800 s each by exact pid: `d18_hybsign.py in/l1kc87dh170d1975.jsonl in/sol_l1kc87dh170d1975_D19.7500.npy 19.75 LAM run/eval_D19.75_pN.jsonl` for LAM 1.32 (p0) and 1.33 (p1), each printing the record system first (I read the first lines of both logs a minute in; a "NOT the record system" stops the work and is reported).
- Information: `freeze_compare.py in` as a third process of 1 thread at nice 10, into `run/freeze_compare.txt`.
- After: `eval_compare.py` into `eval_compare.txt`.

## The two machines (the coordinator's request)
This machine (`machine_dh610.txt`, from `machine_info.sh`; threadpoolctl is not installed, so numpy.show_config() and OPENBLAS_VERBOSE=2 give the core type):
```
date: 2026-11-23 08:47:21 UTC; host: dh610-fedora; kernel: 7.3.3-300.fc45.x86_64
Architecture:                            x86_64
CPU(s):                                  20
Model name:                              12th Gen Intel(R) Core(TM) i7-12700
Thread(s) per core:                      2
Core(s) per socket:                      12
CPU(s) scaling MHz:                      73%
L2 cache:                                12 MiB (9 instances)
L3 cache:                                25 MiB (1 instance)
SIMD flags: avx2 avx_vnni fma 
python: Python 3.14.10 (main, Nov 11 2026, 00:18:44) [Clang 23.1.3 ]
mpmath       1.3.0
multidouble  5.1.0
numpy        2.5.4
python-flint 0.9.0
scipy        1.18.1
--- OPENBLAS_VERBOSE=2: import numpy, import scipy.linalg
Core: Haswell
Core: Haswell
Core: Haswell
--- numpy.show_config(), the BLAS/LAPACK part
      "name": "scipy-openblas",
      "found": true,
      "version": "0.3.34.106.0",
      "openblas configuration": "OpenBLAS 0.3.34.106.0  USE64BITINT DYNAMIC_ARCH NO_AFFINITY Haswell MAX_THREADS=64",
      "name": "scipy-openblas",
      "found": true,
      "version": "0.3.34.106.0",
      "openblas configuration": "OpenBLAS 0.3.34.106.0  USE64BITINT DYNAMIC_ARCH NO_AFFINITY Haswell MAX_THREADS=64",
  "SIMD Extensions": {
    "baseline": [
    "found": [
    "not found": [
--- scipy.__config__
      "name": "gcc",
      "version": "14.2.1",
      "name": "cython",
      "version": "3.2.9",
      "name": "gcc",
      "version": "14.2.1",
      "name": "gcc",
      "version": "14.2.1",
      "version": "0.19.0",
      "name": "scipy-openblas",
--- multidouble isa
multidouble ? isa avx2
```
dh170's machine, as far as his folder says (`../../I1025-dh170/kc87_d1975/README.md`, `../../I1058-dh170/README.md`): Fedora 45, i7-7700, 8 logical CPUs, 31 GiB RAM; python `~/Source/choptuik-large-d-1058b/.venv` (3.14.10, multidouble 5.1.0, avx2). His folder does not record numpy's or scipy's version or OpenBLAS's core type (no `pip list`, `show_config` or `Core:` line in it). His venv was made by uv from `requirements.txt`, whose pins at 7ca74dd5 are numpy 2.5.4 and scipy 1.18.1, the versions of this venv; that is my reading of the pins, not a line of his. An i7-7700 has AVX2 and FMA and no AVX-512 (from the CPU generation, not from his folder), so I expect OpenBLAS's DYNAMIC_ARCH to pick the Haswell core on both machines, as it does here. **I could not read his OpenBLAS core type: `OPENBLAS_VERBOSE=2 ~/Source/choptuik-large-d-1058b/.venv/bin/python -c "import numpy"` and `... -c "import numpy; numpy.show_config()"` on his machine would give it.**

## Acceptance (fixed before the run)
- Both d18 processes exit 0 and print "the record system" (a "NOT the record system" or a non-zero exit stops the work and is reported); the printed |F| is shown beside his record's 3.9876058940e-10.
- The reading is (a), (b) or (c) by the rules above, with the numbers of both lambda; hybrid signs, noise signs and float64 signs are printed as the reader prints them.

## Predictions, registered before the run (information)
- Both processes exit 0 and print the record system (95%); the printed |F| equals 3.9876058940e-10 to 8 digits (85%; the k_c 87 check on this machine gave that value to 10 digits); each point takes 1900 to 2200 s (65%; six processes took 2114 to 2128 s).
- Reading: **(b) 60%, (a) 10%, (c) 30%.** I put (a) low because both machines should run the same OpenBLAS wheel (0.3.34.106.0), the same multidouble 5.1.0 avx2 and single-threaded Haswell kernels, which gives the same float64 bits; macOS (ARM) against this build, with different kernels, differs by at most 8.5e-04. Hybrid signs -, + at 1.32, 1.33 (90%); the two-point det-linear root within 1e-4 of dh170's 1.325410 (60%, the same event as (b) in practice).
- Freeze comparison (information): dh170's start state against linRe differs in at least one segment (70%); linRe against macRe (85%); dh170's start against macm3's start (90%); the two controls pass (95%). If (b) holds and dh170's state against linRe differs in a segment, the steepness is a change of the discrete system, not a smooth derivative.

## Status
- 2026-11-23 08:48:52 UTC: folder, inputs, selftests, machine information and lane prepared before any run.
