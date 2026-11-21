# I1025-win2/d17p5: the full double-double M at D 17.5, k_c 63: dd determinant signs at 1.9072222575778963 and 1.9472222575778963 around winb's hybrid root 1.9272222575778963

Machine win2 (desktop-pc, Windows 11, Core Ultra 7 265K, 20 threads, 95 GB), the win2 build session. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1025. Task: the coordinator's hc of 2026-11-21 (read 06:25 UTC): two more dd M points, now, in parallel with win2's D 18 points (`I1025-win2/d18/`). winb's D 17.5 k_c 63 hybrid root is 1.9272222575778963 (#1025 comment 7058583901, raw `I1025-win/p4_highD` 79767369; its verdict there: FAIL on the edge rule and on the float64 signtest, signs [-1, +1, -1, -1] at lambda -/+ 0.02 with 56 singular values below 1e-12). The float64 signtest cannot judge it past D 17, so the dd M is asked to.

## Setup (written 2026-11-21 06:26 UTC, before any run)

| | |
|---|---|
| code, python | as the D 18 points: worktree `D:/choptuik-i1025d` at `origin/wip/ell1-highD` 48c36355, `solver/matter`; `C:\Users\nathan\Source\venv-md510`'s python; `OPENBLAS_NUM_THREADS=OMP_NUM_THREADS=MKL_NUM_THREADS=20`; BelowNormal |
| state | winb's `I1025-win/out/sol_l1kc63Fw1025_D17.5000.npy`, blob **d85f7b71c2c1...** (git's id in raw main `origin/main` 79767369, taken by `git show`, no pull) into `solver/matter/data/`; k_c 63, Ks 30, u0 0.04, kappa 0.7, rk 1 (ell_ddm._setup's settings) |
| command | the same call as the D 18 points: `ell_ddm.py det data/sol_l1kc63Fw1025_D17.5000.npy 17.5 63 LAM --noise 1e-24,1e-20,1e-16 --out .../ell_ddm_d17p5_win2_{lo,hi}.jsonl` (5 exact variants; noise on the dd propagator entries, 2 seeds) at LAM = **1.9072222575778963** (lower, the root minus 0.02) and **1.9472222575778963** (upper, the root plus 0.02): two processes in parallel with each other and with the D 18 points, 20 BLAS threads each, caps 10800 s each by the exact root pid (command line checked for `ell_ddm.py`), by `run_d17p5.sh`; own alert-only watches into this folder |
| rule for a sign | xfkappa's, as for D 18: a dd sign counts if its 5 variants agree and 1e-24 relative noise leaves it unchanged (both seeds) |
| seconds | the seconds per point carry the load of the other processes on win2 (the D 18 points and win2b's 4-thread root), not a clean machine |

## Reading fixed before the run (the coordinator's)

**dd minus at the lower point and plus at the upper point means the root passes its sign check** (the hybrid grid read -, +, + going up). **The same sign at both means no root between them.** Plus at the lower and minus at the upper is not one of the two readings (a change in the opposite direction): reported as such. A point whose sign does not count (variants split, or 1e-24 noise flips it) is reported as such and neither reading is applied. A cap that fires, a Traceback or a missing line is a result; no tolerance is changed. I post these two with the D 18 points on #1025.

## Result (written 2026-11-21 08:34 UTC)

**Reading: dd minus at the lower point and plus at the upper point: the root passes its sign check.** Both points exited 0 (`det_1.9072222575778963`: 7581 s, root pid 34956; `det_1.9472222575778963`: 7611 s, root pid 34780; 06:26:27 to 08:33:18 UTC; caps 10800 s not reached; no Traceback). Each sign counts under xfkappa's rule (5 variants agree, 1e-24 noise unchanged for both seeds).

| lambda | dd signs, 5 variants | noise 1e-24 / 1e-20 / 1e-16 (2 seeds each) | counts | dd ln\|det\| (spread over variants) | float64 sign, ln\|det\| | dd M build s, s per LU, wall s |
|---|---|---|---|---|---|---|
| 1.9072222575778963 (lower, root - 0.02) | **-1 x5** | -, -, - | yes | -1938.1412652068 (4.8e-12) | -1, -1937.9398860305 | 2948, 275.5, 7581 |
| 1.9472222575778963 (upper, root + 0.02; the log prints it as 1.9472222575778964, the same double) | **+1 x5** | +, +, + | yes | -1936.1790235786 (9.1e-13) | +1, -1937.0380407749 | 2974, 275.3, 7611 |

The float64 signs agree with the dd ones at both points here (they did not at D 18's upper outer point). The dd sign pattern -, + brackets winb's hybrid root 1.9272222575778963 (which its float64 signtest could not judge: signs [-1, +1, -1, -1] at -/+0.02, 56 singular values below 1e-12), so the hybrid root passes the dd sign check in the sense of the pre-registered reading; it does not give the root's value (that would take a dd root search).

Seconds: M build 2948 and 2974 s, 275 s per LU, wall about 2 h 6 min each, with five det processes running together on win2 (the D 18 points and these two; about 1.4 to 1.7 cores each) and win2b's 4-thread root: slower than the D 18 points' 1545 s, 147 to 162 s per LU, which ran with fewer neighbours for part of their time. Memory (`mem.log`, `commit.log` here): commit at most 55.3 GB, minimum available 50.6 GB, `alerts.log` never written.

Files: `det_1.9072222575778963.log`, `det_1.9472222575778963.log`, `ell_ddm_d17p5_win2_lo.jsonl`, `ell_ddm_d17p5_win2_hi.jsonl`, `d17p5_win2_read.md`, `summary_d17p5.txt`, `exits_d17p5.txt`, `mem.log`, `commit.log`, `run_d17p5.sh`, `read_d17p5_win2.py`, `lib_d17p5.sh`, the watch scripts.
