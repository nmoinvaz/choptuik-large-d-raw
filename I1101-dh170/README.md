# I1101-dh170: the root of R2's state (kappa 0.35) on the Rust block 12, with state B's root as the control

Machine `dh170` (Fedora, i7-7700, 4 cores / 8 threads, 31 GiB), account claude-me2. Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1101 (depends on #1025, #1102). Coordinator t5. Written 2026-11-27 07:22 UTC by the clock, before any build or run of this folder (the worktree, the pins, the reading script and its planted selftest came first; the order is quoted at the end).

## Bars (t5's, fixed before any run; each can fail)
1. **Gates** (a failed gate stops the task): `ell_b12rs.py selftest` exit 0; `--mutate=nolam` exit 1; `--mutate=harm` exit 1; the k_c 31 `check` (`--threads=2 --controls=1`) exit 0, prints "15010 of 15010 entries bit for bit", and both controls FAIL. The build prints `ellrs <isa> <products>`.
2. **Control: R0's state (state B) on this scanner**, `d18_secant.py scan --b12=rust --b12_threads=1`, lambda 0.045 and 0.050, one process each (a failure stops the task: R2's root would not compare with B's):
   - hybrid signs + at 0.045, then - at 0.050, both points robust (noise signs equal the hybrid sign, dln <= 0.1);
   - each ln|det| within 1e-4 of dh370's: -3902.5303054577 (0.045) and -3901.1035170558 (0.050);
   - the det-linear root of the two points within 1e-5 of 0.045967998.
3. **R2's root** (when `I1101-win2/R2/` is on the raw origin; its state and record blobs are pinned in "R2 pins" below before the scan starts): scan at lambda 0.045, 0.050, 0.060, 0.070.
   - delta = root(R2) - 0.045967998, the det-linear root of the 0.045/0.050 pair if it brackets (signs differ, both robust), so the estimator's bias cancels as it did for the scatter; otherwise the first bracketing pair, said so with the estimator's bias not cancelling.
   - E_root = delta x 16/15, the root's step error at kappa 0.7, k_c 127 if that error is proportional to kappa^4. The root's solve scatter is 1.75e-4 (`I1101-dh370/`).
   - **|E_root| >= 3e-3** (17x the scatter, more than half the 127 to 135 root step): the step error is real; thresholds must be extrapolated in kappa as well as k_c, and the k_c-only zeros are withdrawn.
   - **|E_root| <= 1e-3**: the step error does not drive the late k_c steps, and #1103's inference fails.
   - **between**: mixed, reported as measured.
   - If no pair brackets: report and wait (nothing widened, no extra lambda).
   - For information: #1103's estimate is E_root about +0.02 (its 0.016 at k_c 135 scaled by (135/127)^4), so a root near 0.065, which the 0.060/0.070 pair brackets.
4. **Reading rules.** A root is read only from robust points. `results_1101.py` prints the table, the bars' verdicts and the det-linear root; `read_lower.py` (89309d3c) is run on the same files for its estimator range, which is the spread over interpolation choices, not an enclosure. The scatter, the bias of a two-point det-linear root and a rigorous enclosure are different things: every quoted root here is a det-linear estimate from two points, and any +- is named.

## Pins (by blob, `git hash-object --no-filters`; the drivers refuse any other)
| what | where | blob |
|---|---|---|
| code | worktree `~/Source/choptuik-large-d-1102` at `d4b6b6ce` of `wip/ell1-rust-b12` (clean), `solver/matter/` | |
| scanner | `d18_secant.py` (`--b12=rust`, `--b12_threads`) | 9706e506 |
| Rust block 12 driver | `ell_b12rs.py` | a1fff74f |
| crate | `ellrs/build.sh`, `Cargo.toml`, `Cargo.lock` | e6254c9b, 5bae423e, 2147ed9a |
| python | `~/Source/choptuik-large-d-1058b/.venv` (3.14.10, multidouble avx2), not modified; ellrs goes to `~/Source/ellrs-site-1102` (PYTHONPATH) | |
| state B (R0's re-solve) | raw `I1101-win2/R0/sol_l1kc127k070w2_D23.0000.npy`, copy in `in/` | 90d3e655 |
| record of B | `l1kc127k070w2.jsonl` (|F| 3.1949266444e-10, 4179 steps, Delta 1.1743225027439044) | d1a3a641 |
| k_c 31 gate | raw `I1102-mac/in/` state `sol_l1kc31r1025_D10.5000.npy`, record `l1kc31r1025.jsonl`, D 10.5, lambda 2.87 | f07a8984, e5a87ec5 |
| reader | `read_lower.py`, its change finder `d185_scan_read.py` (from `I1101-dh370/in/`) | 89309d3c, 7c9d400f |
| reading script | `results_1101.py` (this folder; selftest exit 0, `--mutate=shift`, `signs`, `e16` exit 1 each, `selftests/`) | |
| dh370's records | `I1101-dh370/scan_B/scan_D23.0_p0.jsonl` (copy `in/dh370_scan_B_D23.0_p0.jsonl`; ddm block 12; the control's reference) | 6acc3345 |

## Commands (OPENBLAS, OMP, MKL, VECLIB, RAYON threads = 1 throughout; every run a systemd user unit under `systemd-inhibit`; steps and exits in `steps.txt`)
1. `run_gates.sh` (unit `i1101g`): `VIRTUAL_ENV=~/Source/choptuik-large-d-1058b/.venv PATH=$VIRTUAL_ENV/bin:$PATH ellrs/build.sh ~/Source/ellrs-site-1102` from `solver/matter`; then, with `PYTHONPATH=~/Source/ellrs-site-1102`, `ell_b12rs.py selftest`, `selftest --mutate=nolam`, `selftest --mutate=harm`, and `ell_b12rs.py check in/l1kc31r1025.jsonl in/sol_l1kc31r1025_D10.5000.npy 10.5 2.87 --threads=2 --controls=1`.
2. `run_scan.sh ctl in/sol_l1kc127k070w2_D23.0000.npy in/l1kc127k070w2.jsonl 90d3e655 d1a3a641 0.045,0.050` (unit `i1101c`): the `d18_secant.py` selftest (0 1 1 1: `half`, `norobust`, `nosigncheck`) and `read_lower.py` selftest (0 1 1: `shift`, `round2`), then two processes, `PYTHONPATH=SITE nice -n 10 python -u d18_secant.py scan RECORD STATE 23.0 LAM OUT --b12=rust --b12_threads=1 --pin=STATEBLOB,RECORDBLOB`, then `read_lower.py` and `results_1101.py control`.
3. `run_scan.sh r2 <R2 state> <R2 record> <state blob> <record blob> 0.045,0.050,0.060,0.070` (unit `i1101r2`), then `results_1101.py r2`.
Threads: 3 beside `i1088a-d622x` (6 threads, python at nice 19, which has priority and which I never touch), up to 6 when it ends; the control uses 2, R2's scan 4 only after d622x has ended (cap 10 h from 23:51 UTC, so by 09:51 at the latest). Nice 10 as ordered; d622x's python runs at nice 19, and 2 + 6 threads fill the 8 logical CPUs, so no contention is expected, but a nice-10 process would win one if it came (reported to t5).

## Predictions (mine, registered before any run; information, not pass rules)
| item | prediction |
|---|---|
| build | exit 0 at the first try 85% (crates.io reachable from the shell 92%); 1 to 5 min |
| gates | selftest 0 and the two mutations 1: 92%; k_c 31 "15010 of 15010": 90%; both controls FAIL: 95% |
| control, signs and robustness | + then -, both robust: 90% |
| control, ln\|det\| | within 1e-4 of dh370's at both points: 85%; within 1e-9 (the same bits): 55% (the float64 blocks are the same code and the Rust block 12 is DDEll's bit for bit; a different CPU's libm or BLAS kernel could move them) |
| control, root | within 1e-5 of 0.045967998: 88%; within 1e-8: 55% |
| control wall | 2400 to 4800 s per point (block 12 about 2700 s on one thread from dh370's 678 s on four, plus 840 s of float64 blocks, 50 s of logdet), the two in parallel: done 1.0 to 1.4 h after the start |
| R2, which pair brackets | 0.045/0.050: 30%; 0.050/0.060: 20%; 0.060/0.070: 30%; none: 20% |
| R2, E_root | >= 3e-3: 40%; <= 1e-3: 30%; between: 30% (#1103's inference from residual sizes against the solve scatter; no direct prior) |
| R2 wall | 4 processes at once on a free machine, 3000 to 4800 s per point |

## Status
- 2026-11-27 07:22 UTC: folder, pins, bars, scripts and the reading script's planted selftest written before any build or evaluation. `run_gates.sh` starts next.

## Order, verbatim

### t5's hc (the task section; 27 Nov 07:16 UTC by t5's message)

> Issue #1101 in nmoinvaz/choptuik-large-d, comment 7212323177 (read it and comment 7211909730 first; they are the
> record). Machine dh170, account claude-me2. Your auto-memory has your handover (dh170-handover-2026-11-27.md):
> the raw clone, its push script, read_lower and the yield rule.
> 
> In short:
> 1. Worktree ~/Source/choptuik-large-d-1102 at d4b6b6ce of wip/ell1-rust-b12; build ellrs into ~/Source/ellrs-site-1102
>    with ~/Source/choptuik-large-d-1058b/.venv's bin/ first on PATH; gates: selftest 0, nolam 1, harm 1, k_c 31 check
>    "15010 of 15010" with both controls failing (dh370's I1102-dh370/README.md has every command).
> 2. Control: d18_secant.py scan --b12=rust --b12_threads=1 on R0's state (I1101-win2/R0/, blobs 90d3e655, d1a3a641) at
>    lambda 0.045 and 0.050, one process each: signs + then -, robust, ln|det| within 1e-4 of dh370's, det-linear root
>    within 1e-5 of 0.045967998.
> 3. When I1101-win2/R2/ appears on the raw origin (about 11:30 UTC): pin R2's blobs and scan at lambda 0.045, 0.050,
>    0.060, 0.070; report delta, E_root and the bar verdict.
> Threads: 3 beside D 622's check (i1088a-d622x has priority, never touch it), up to 6 when it ends; 1 thread per
> process, nice 10, systemd user units. Raw folder I1101-dh170/, README with the bars first, records at the end. No
> code changes. A failed gate or control stops the task and is reported. Report to me at each step's end; post on
> #1101 at each milestone.

### #1101 comment 7212323177

> **dh170: the root scan of R2's state, on the Rust block 12, with a control first** (t5, 2026-11-27 07:16 UTC by the
> clock). This carries out comment 7211909730 on dh170.
> 
> **Code.** A new worktree `~/Source/choptuik-large-d-1102` at d4b6b6ce of `wip/ell1-rust-b12` (`git fetch origin`, then
> `git worktree add --detach`). `d18_secant.py` blob 9706e506 (`--b12=rust`), `ell_b12rs.py` a1fff74f. Python
> `~/Source/choptuik-large-d-1058b/.venv`. ellrs's block 12 is DDEll's bit for bit (#1102: k_c 31 and k_c 127 on dh370).
> Raw folder `I1101-dh170/`, README with these bars first.
> 
> **Threads.** 3 beside D 622's check (`i1088a-d622x`, 6 threads; it has priority), up to 6 once it ends. 1 thread per
> process (OMP, OPENBLAS, MKL, VECLIB, RAYON = 1), `--b12_threads=1`, nice 10, systemd user units.
> 
> 1. **Build and gates**, as dh370 did (`I1102-dh370/README.md`): `ellrs/build.sh ~/Source/ellrs-site-1102` with the
>    venv's `bin/` first on PATH; it prints `ellrs <isa> <products>`. Then `ell_b12rs.py selftest` exit 0, `--mutate=nolam`
>    exit 1, `--mutate=harm` exit 1, and the k_c 31 check (raw `I1102-mac/in/`, state f07a8984, record e5a87ec5, D 10.5,
>    λ 2.87, `--threads=2 --controls=1`): exit 0, "15010 of 15010", both controls fail. A failed gate stops the task.
> 2. **Control: state B on this scanner.** `d18_secant.py scan --b12=rust --b12_threads=1` on R0's state (raw
>    `I1101-win2/R0/`, state 90d3e655, record d1a3a641, `--pin` both) at λ 0.045 and 0.050, one process per λ. Bars:
>    signs + then −, both robust; each ln|det| within 1e-4 of dh370's (−3902.5303054577, −3901.1035170558); the det-linear
>    root within 1e-5 of 0.045967998. A failure stops the task: R2's root would then not compare with B's.
> 3. **R2's root.** When win2 pushes `I1101-win2/R2/` (its waiter pushes at `r2.done`, expected about 11:30 UTC): pin
>    R2's state and record blobs, then scan at λ 0.045, 0.050, 0.060 and 0.070. Reading and bars from comment 7211909730:
>    δ = root(R2) − 0.045967998 from the bracketing pair, E_root = δ × 16/15. |E_root| ≥ 3e-3: the step error is real;
>    ≤ 1e-3: #1103's inference fails; between: mixed. If no pair brackets, report and wait.
> 
> **Estimate.** Build and gates 10 min; the control about 1.5 h (by about 09:00); R2's scan about 3 h after R2 lands.
> 

### #1101 comment 7211909730

> **Follow-on amended before R2 ends: the root of R2's state** (t5, 2026-11-27 06:51 UTC by the clock).
> 
> #1103's residual split (raw 97c0b8da3, `I1103-mac/split/`) infers that from k_c ≈ 120 on, the RK4 step that
> `freeze_from` ties to k_c moves the root λ₁ more than the k_c truncation does:
> 
> - the RK residual of one step change (×1.07) falls by 0.70 → 0.78 per rung, which is (k/(k+8))⁴;
> - the truncation residual in harmonics 0–10 falls by about 0.35 per rung;
> - the late root steps fall by 0.80–0.85, close to the RK rate.
> 
> That is an inference from residual sizes, not a measured root. R2 (κ 0.35, twice R0's steps) measures it directly
> once its state has a root:
> 
> 1. **Scan.** When R2 ends and its state is pushed: `d18_secant.py scan` (92b9bf53, blob eb1396ad) on R2's state at
>    λ 0.045, 0.050, 0.060 and 0.070, with the pins, reader and robustness test of `I1101-dh370/`.
> 2. **Reading.** δ = root(R2) − root(B), with root(B) = 0.045967998 (`I1101-dh370/`, R0's state). Take R2's det-linear
>    root from its bracketing pair; use the 0.045/0.050 pair if it brackets, so the estimator's bias cancels as it
>    did for the scatter. E_root = δ × 16/15 is the root's step error at κ 0.7, k_c 127, if that error is ∝ κ⁴.
> 3. **Bars, written before the scan.** The root's solve scatter is 1.75e-4 (`I1101-dh370/`).
>    - |E_root| ≥ 3e-3 (17× the scatter, and more than half the 127 → 135 root step): the step error is real. The
>      thresholds must then be extrapolated in κ as well as k_c, and the k_c-only zeros are withdrawn.
>    - |E_root| ≤ 1e-3: the step error does not drive the late k_c steps, and #1103's inference fails.
>    - Between: mixed, reported as measured.
> 4. **#1103's estimate, for information:** E_root ≈ +0.02, from its 0.016 at k_c 135 scaled by (135/127)⁴. The
>    root would then sit near 0.065, which the 0.060/0.070 pair brackets.
> 
> R2's own bars for Δ stand as amended on 01:46 UTC. The scan runs on whichever machine is free when R2 ends.
> 

## Control result (27 Nov 07:25:17 to 07:50:46 UTC = 1529 s; unit `i1101c`; 2 processes, 1 thread each, nice 10; `results_ctl.md`, `read_lower_ctl.txt`, `scan_ctl/`, `scan_ctl_p0.raw`, `scan_ctl_p1.raw`)
Both processes printed the pin check and `D 23.0 k_c 127: |F| 3.1911792672e-10 (record 3.1949266444e-10), steps 4179 (record 4179): the record system`, then `block 12 by ellrs (avx2, products dgemm, 1 threads)`, and exited 0; peak RSS 4.51 GiB (4733032 kB) and 4.51 GiB (4734076 kB). The selftests before the scan: `d18_secant.py` exit 0 and its mutations `half`, `norobust`, `nosigncheck` exit 1 each; `read_lower.py` exit 0 and `shift`, `round2` exit 1 each; `results_1101.py` selftest exit 0 and `shift`, `signs`, `e16` exit 1 each (`selftests/`).

| bar | wanted | result | |
|---|---|---|---|
| signs | + at 0.045, then - at 0.050 | +, - | PASS |
| robust | both points | both (noise signs equal the hybrid sign; dln 1.54e-05 and 2.50e-06) | PASS |
| ln\|det\| at 0.045 | within 1e-4 of -3902.5303054577 | -3902.5303054577 (difference +4.1e-12 from the rounded reference; equal to dh370's double) | PASS |
| ln\|det\| at 0.050 | within 1e-4 of -3901.1035170558 | -3901.1035170558 (difference -4.8e-11 from the rounded reference; equal to dh370's double) | PASS |
| det-linear root | within 1e-5 of 0.045967998 | 0.045967998 (difference -9.2e-11) | PASS |
| on the Rust block 12 | `b12` field `rust` | `rust` at both points | PASS |
**The control passes every bar** (`results_1101.py control` exit 0). Beyond the bars: all numeric fields of both records (`sign`, `ln`, `noise`, `noise_ln`, `dln`, `f64_sign`, `f64_ln`) equal dh370's records of state B (ddm block 12, machine dh370) bit for bit, so the Rust block 12 on one thread here gives the stored Python block's bits on another machine of the same instruction set (avx2). `read_lower.py`: one robust change (0.045, 0.050), + to -, det-linear 0.045968, range [0.045968, 0.045968] (two points: the range is of the interpolation choices, not an enclosure). The float64 sign differs from the hybrid sign at 0.045, as in dh370's.

| prediction | result |
|---|---|
| build exit 0 at the first try (85%), 1 to 5 min | right: 47 s |
| selftest 0, mutations 1 1 (92%); k_c 31 15010 of 15010 (90%); both controls FAIL (95%) | right |
| control: + then -, both robust (90%) | right |
| control: ln\|det\| within 1e-4 (85%); within 1e-9, the same bits (55%) | right, and more: every numeric field is bit for bit dh370's |
| control: root within 1e-5 (88%); within 1e-8 (55%) | right: -9.2e-11 |
| control wall 2400 to 4800 s per point | WRONG, faster: 1521 s and 1515 s per point (float64 blocks 413 s, Rust block 12 1074 s, logdet 34 s and 28 s on one thread), the two in parallel 1529 s in all (dh370's ddm points took 6818 s and 6678 s, 4.5 times as long) |
## Status
- 2026-11-27 07:55 UTC: gates and control done; R2's scan waits for `I1101-win2/R2/` on the raw origin (expected about 11:30 UTC). Each point costs about 1520 s on one thread, so R2's four points take about 26 min when run in parallel.

## R2 pins (written 2026-11-27 10:21 UTC by the clock, before R2's scan starts)
`I1101-win2/R2/` reached the raw origin at 10:20:42 UTC (commit 1c02fde6c, "R2 (kappa 0.35) ended"). Copies in `in/` (names `sol_l1kc127k035w2_D23.0000.npy`, `l1kc127k035w2.jsonl`; the `in/R2_*` files are the same bytes with the raw names kept). The driver refuses any other blob.
| what | blob |
|---|---|
| R2 state `sol_l1kc127k035w2_D23.0000.npy` | **25ba3a91** |
| R2 record `l1kc127k035w2.jsonl` (kappa 0.35, u0 0.04, Ks 30, k_c 127, |F| 3.1242366894e-10, F_start 2.158e-09, **8351 steps**, Delta 1.1743229234047416, psi-constraint 1.463841e-03, 30786 s) | **9111bfca** |
| win2's syscheck of it (`R2_syscheck_kc127.txt`, exit 0, "ACCEPTED: the record class's |F| with a step count that comes back") | 6a2ad865 |
Facts from the record, not read into: steps 8351 are in the 8358 +- 2% window; Delta_R2 - Delta_source (1.174322923415951) = -1.1e-11 and Delta_R2 - Delta_R0 (1.1743225027439044) = +4.2e-7.
Command: `run_scan.sh r2 in/sol_l1kc127k035w2_D23.0000.npy in/l1kc127k035w2.jsonl 25ba3a91 9111bfca 0.045,0.050,0.060,0.070` (unit `i1101r2`): 4 processes, 1 thread each, nice 10, `--b12=rust --b12_threads=1`, the bars above unchanged. It runs beside none of step 1c's jobs (all ended); expected about 26 to 30 minutes (control points took 1521 s and 1515 s).
Prediction registered above (R2, which pair brackets: 0.045/0.050 30%, 0.050/0.060 20%, 0.060/0.070 30%, none 20%; E_root >= 3e-3 40%, <= 1e-3 30%, between 30%). Add: `|F|` of the state reproduces the record (record system) 95%; all four points robust 75%.

## R2 result (27 Nov 10:21:28 to 12:12:18 UTC = 6650 s; unit `i1101r2`; 4 processes, 1 thread each, nice 10; `results_r2.md`, `read_lower_r2.txt`, `scan_r2/`, `scan_r2_p0.raw` to `scan_r2_p3.raw`; written 2026-11-27 12:15 UTC by the clock)
All four processes printed the pin check, `D 23.0 k_c 127: |F| 3.1258555149e-10 (record 3.1242366894e-10), steps 8351 (record 8351): the record system` and `block 12 by ellrs (avx2, products dgemm, 1 threads)`, and exited 0; peak RSS 4.51 to 4.64 GiB (4733404 to 4863912 kB). The selftests ran in the control's step; `results_1101.py r2` exit 2 (no pair brackets).

| lambda | hybrid sign | noise signs | robust | dln | float64 sign | ln\|det\| | seconds (float64 blocks, Rust block 12, logdet) |
|---|---|---|---|---|---|---|---|
| 0.045 | + | + + | True | 1.35e-05 | - | -4211.9503431400 | 6625 (1741, 4865, 19) |
| 0.050 | + | + + | True | 1.35e-05 | + | -4212.5955870798 | 6600 (1752, 4823, 25) |
| 0.060 | + | + + | True | 1.37e-05 | - | -4213.9037243145 | 6493 (1782, 4648, 63) |
| 0.070 | + | + + | True | 1.38e-05 | - | -4215.2427588991 | 6534 (1748, 4751, 36) |

**No pair brackets: report and wait** (`results_1101.py r2` exit 2; nothing widened, no extra lambda). Hybrid sign is + at all four points, all noise-robust; `read_lower.py`: 0 robust changes in 0.045 to 0.070, endpoint signs + and +, no `ln|det|` local minimum without a sign change, no repeated point. The float64 sign differs from the hybrid sign at 0.045, 0.060 and 0.070, as it did at 0.045 in the control. Bars not applied: delta, E_root and the verdict are not formed.

What the four points do and do not say (mine, outside the bars):
- `ln|det|` falls smoothly with lambda, by 129, 131 and 134 per unit lambda over the three intervals, with no dip. In the control `ln|det|` changed by +1.4268 between 0.045 and 0.050 (its root lies 9.7e-4 above 0.045 and 4.0e-3 below 0.050, and ln(0.00403/0.00097) = 1.43). A root 3e-3 above 0.070 would steepen the 0.060 to 0.070 slope by about 150 per unit lambda (-ln(0.013/0.003)/0.01 is -147); it steepens by 3. A root within about 3e-3 of 0.070, or of 0.045, would show as a dip; none does.
- Assuming the control's orientation (the sign is + below the root and - above it) and a single sign change: the root lies above 0.070, delta > +0.024032, E_root > +0.0256, which is above #1103's estimate of +0.02. This is an assumption, not a reading under the bars: the orientation of the hybrid sign across two different states is not established, and an even number of roots in the window would also give four equal signs.
- With the other orientation the root lies below 0.045: delta < -0.000968, |E_root| > 1.03e-03, so the bar's "<= 1e-3" case fails either way for a single sign change, but 3e-3 is not decided there.

| prediction | result |
|---|---|
| R2, which pair brackets: none (20%; 0.045/0.050 30%, 0.050/0.060 20%, 0.060/0.070 30%) | none: the registered 20% outcome happened; the three pairs (30%, 20%, 30%) did not bracket |
| R2, E_root >= 3e-3 (40%), <= 1e-3 (30%), between (30%) | not formed: no pair brackets |
| R2 reproduces its record's system, `|F|` and steps (95%) | right: all four processes print `|F| 3.1258555149e-10 (record 3.1242366894e-10), steps 8351 (record 8351): the record system` |
| all four points robust (75%) | right: noise signs equal the hybrid sign at all four, dln 1.35e-05 to 1.38e-05 |
| R2 wall 3000 to 4800 s per point on a free machine; the pins section said 26 to 30 min in all | WRONG, slower: 6493 to 6625 s per point, 6650 s in all (1 h 51 min), 4.3 to 4.4 times the control's 1521 s per point at the same k_c. The machine was not free: step 1d (#1105) started two re-solves of 2 threads each at 10:33:42 UTC, 12 min after this scan, and they ran to 11:42 and 11:47 UTC; a root run of step 1d ran beside the scan to its end. The cause of the 4.3 times is not separated by these runs (4 processes against the control's 2 is the other difference) |

## Status
- 2026-11-27 12:15 UTC: R2's scan done (6650 s): hybrid sign + at 0.045, 0.050, 0.060, 0.070, all robust; no pair brackets: reported to t5, waiting for t5's order (nothing widened).

## R2 widened scan (t5's order, comment 7218045186, 27 Nov 12:16 UTC by t5's clock; this section written 2026-11-27 12:20 UTC by the clock, before the scan starts)
**Bars and reading (t5's, fixed before the run; each can fail).** R2's state, the same pins and scanner, Rust block, 1 thread each: lambda 0.085, 0.100, 0.130 (above) and 0.035 (below), 4 processes, nice 10.
- The first robust sign change found gives the bracket. Then `d18_secant.py run` on it at tol 5e-5, and delta = root - 0.045968, E_root = delta x 16/15, read against this issue's bars (|E_root| >= 3e-3 real, <= 1e-3 refutes #1103's inference, between mixed).
- No robust change in [0.035, 0.130]: reported as measured, and then the next points are 0.025 and 0.17 (not started by me; I report and wait).
- For information (t5): R2's Delta equals the source's to 1.1e-11, so a root shift of order 0.02 would sit in the step error of the mode matrix's own integration (its blocks are integrated with the state's step map), not in the state.
- My additions, written before the run: "the first robust change" is read over the eight points of `scan_r2/` (0.045, 0.050, 0.060, 0.070) and `scan_r2w/` (0.035, 0.085, 0.100, 0.130) together, neighbouring points only, both ends noise-robust with dln <= 0.1, and where there are several the lowest-lambda one gives the bracket and the others are listed (t5 decides what follows). The secant record is read only if its status is `tol`, both ends robust with opposite signs, and its bracket lies inside the scan's pair; root = `lam_lin`. The secant evaluates its two ends again (about two points of cost); it runs on 1 thread as the scan does. No other lambda is run.
- The control's orientation (+ below the root) is not assumed by the reading; it only sorts my predictions.

**Pins.**
| what | where | blob |
|---|---|---|
| R2 state and record | unchanged (R2 pins above): `in/sol_l1kc127k035w2_D23.0000.npy`, `in/l1kc127k035w2.jsonl` | 25ba3a91, 9111bfca |
| scanner, block 12 driver, worktree | `d18_secant.py`, `ell_b12rs.py`, `~/Source/choptuik-large-d-1102` at d4b6b6ce (unchanged) | 9706e506, a1fff74f |
| reader | `read_lower.py`, `d185_scan_read.py` (unchanged) | 89309d3c, 7c9d400f |
| reading script | `results_1101.py` with the new mode `r2w` (the version before is `selftests/results_1101_before_r2w.py`; `r2` and `control` unchanged) | 0ee6b8bf |
| driver | `run_scan_w.sh` (the scan, then the secant if a bracket is found) | 4a762140 |
Sequence: the unit `i1101r2w` runs `run_scan_w.sh`: pins, wait for step 1d's four roots of #1105 to end (`DONE_c150`, `DONE_c165w`, `DONE_r150`, `DONE_r165w`; a `STOP_` counts as ended) and refuse to start if one of the four was refused (`HOLD_r2w.txt`), the `results_1101.py` selftest (0) and its mutations `shift`, `signs`, `e16`, `last` (1 each; `selftests/selftest_results_w*.txt`), the scan (4 processes), `read_lower.py` on `scan_r2all/` (the eight points), `results_1101.py r2w scan_r2 scan_r2w` (exit 2 none, 3 a bracket), then if 3 the secant `d18_secant.py run RECORD STATE 23.0 LO HI secant_r2w.jsonl --tol=5e-5 --maxev=20 --b12=rust --b12_threads=1 --pin=25ba3a91,9111bfca`, then `results_1101.py r2w ... --secant=secant_r2w.jsonl` (exit 0 formed, 4 not read). Steps and exits in `steps.txt`.

| item | prediction (mine, registered before the run; information, not pass rules) |
|---|---|
| first robust change in [0.035, 0.130] | none: 45%; (0.100, 0.130): 25%; (0.085, 0.100): 12%; (0.070, 0.085): 8%; (0.035, 0.045): 7%; two or more changes: 8% (inside the above, counted by the lowest) |
| a pole fit, for information | ln\|det\| = a + b lambda + ln\|lambda0 - lambda\| on the four R2 points (1 degree of freedom) has its best fits at lambda0 near 0.12 (rms 8e-4 in ln) and near 0.00 (1.5e-3); every far root fits to 1e-2. It does not locate a root |
| given a change: the bar | |E_root| >= 3e-3 (real): 97%, because a root above 0.070 has E_root > 0.0256 and one in (0.035, 0.045) has |E_root| between 1.0e-3 and 1.2e-2 |
| all four new points robust | 80% |
| wall | scan: 4 processes alone, 1800 to 3000 s per point (the control's 1521 s was 2 processes); secant: 2 end points and 3 to 6 interior points of 1500 to 2500 s each, 2 to 4 h in all |

## Status
- 2026-11-27 12:20 UTC: widened scan prepared and pinned; waits for step 1d's roots (c150, r150, r165w, c165w running; c165's first run and r165's were refused, same-signed ends, and both were rerun on 2.138 to 2.172).

### Order for the widened scan, verbatim (t5, 27 Nov 12:16 UTC by t5's clock)

#### t5's hc

> t5: R2's scan accepted as read (no bracket, nothing formed, as written), and your extra figures are useful. On priority: my wording was loose; your reading was reasonable, and the 4.3x is noted. Order (#1101, my newest comment there is the record): widen R2's scan at lambda 0.085, 0.100, 0.130 and 0.035, same pins and scanner, Rust block, 1 thread each, 4 processes, nice 10. Start them as soon as step 1d's four roots end; until then 1d's roots go first. Then the secant (d18_secant.py run, tol 5e-5) on the first robust change, then delta, E_root and the bar verdict. No change in [0.035, 0.130] means report as measured. The widened 2.138-2.172 bracket for r165 is accepted.

#### #1101 comment 7218045186

> **R2's root: the scan widened** (t5, 2026-11-27 12:16 by the clock)
> 
> dh170's scan of R2's state (comment 7218031107, raw a32353d04) read + at λ 0.045, 0.050, 0.060 and 0.070, all robust,
> with ln|det| falling smoothly. So no pair brackets, and δ is not formed, as written. The orientation of the sign
> across two states is not established: macm3's two k_c 143 states at D 23.125 changed sign in opposite senses (#1025,
> comment 7216553513). So the root lies above 0.070 (the control's orientation: δ > +0.024) or below 0.045.
> 
> **Extension, written before it runs.** On R2's state, the same pins and scanner, Rust block, 1 thread each: λ 0.085,
> 0.100, 0.130 (above) and 0.035 (below), 4 processes, nice 10.
> - The first robust sign change found gives the bracket. Then `d18_secant.py run` on it at tol 5e-5, and δ =
>   root − 0.045968, E_root = δ × 16/15, read against this issue's bars (≥ 3e-3 real, ≤ 1e-3 refutes).
> - No robust change in [0.035, 0.130]: reported as measured, and then the next points are 0.025 and 0.17.
> - For information: R2's Δ equals the source's to 1.1e-11. So a root shift of order 0.02 would sit in the step error of
>   the mode matrix's own integration (its blocks are integrated with the state's step map), not in the state.
> 


# Test K: is the step error in the mode matrix alone? (state B with --kappa_mm=0.35)

Written 2026-11-27 15:56 UTC by the clock, before any run of Test K (bars, reading rule, pins, driver, reader with its planted selftest and predictions first; t5's order is quoted at the end). Folder `I1101-dh170/`; files `run_scan_k.sh`, `results_1101k.py`, `scan_k/`, `scan_k_p*.raw`, `ctl_k31/`, `secant_k.jsonl`, `steps_check_k.txt`, `read_lower_k.txt`, `results_k.md`, `results_k_secant.md`. Issue #1101; coordinator t5. t5's order (the hc after step 1e, and comment 7222591656): beside R2's secant, scan state B with `--kappa_mm=0.35 --b12=rust --b12_threads=1` at lambda 0.085, 0.100, 0.115, 0.130, 4 processes, nice 10; check the `kappa_mm 0.35 ... steps` line (about 8351); then `run` at tol 5e-5 on the robust change and compare with R2's secant root.

## Bars (t5's, fixed before the run; each can fail)
r2 is the root of R2's own secant (`secant_r2w.jsonl`, d18_secant.py run, tol 5e-5, the det-linear root `lam_lin`).
- **|root - r2| <= 3e-3** (the path scatter between two states at k_c 143 was 2.2e-3): the state's kappa does not matter, the step error is the mode matrix's; then #1104 uses `--kappa_mm` on the stored states, without re-solves.
- **|root - r2| >= 1e-2**: the state's kappa matters too.
- **Between**: reported as measured.
- The step-count line: about 8351 (R2's record steps at kappa 0.35).

**Reading rule (mine, stated before the run):** a root is read only from a `d18_secant.py run` ending with status `tol`, both bracket ends robust with opposite hybrid signs, inside the scan's bracket (the same rule for R2's record). The difference is read on the ranges [a - d, b - c] of the final brackets [a, b] (Test K) and [c, d] (R2): the whole range inside +-3e-3 reads as the first bar, the whole range at 1e-2 or more in size as the second, anything else (a range that straddles a bar included) as between. `lam_lin`'s difference is printed beside it. The step-count line must be 8351 +- 2% (mine; the scans are killed otherwise and the cause is looked for). The scan's bracket is the first robust change (lowest lambda, the others listed). If no pair brackets in 0.085-0.130: reported as measured, nothing widened by me (t5's order names no further points). `--ends` hands the scan's two end records to `run` (bit-identical evaluations: R2's secant re-evaluated 0.100 to the same ln|det|, -4219.6804690495), which saves two evaluations; this is my choice beyond the order. Estimator values at the width of the final bracket, not rigorous enclosures.

## Pins (by blob; the driver refuses any other)
| what | where | blob |
|---|---|---|
| scanner with `--kappa_mm` | worktree `~/Source/choptuik-large-d-1101k` at `wip/ell1-kappa-mm` f56f91d2 (d4b6b6ce plus 16 lines of `d18_secant.py`), `solver/matter/d18_secant.py` | 2f3ee874 |
| Rust block 12 | `ell_b12rs.py` (unchanged from d4b6b6ce), ellrs in `~/Source/ellrs-site-1102` (avx2 matrixmultiply), venv `~/Source/choptuik-large-d-1058b/.venv` | a1fff74f |
| state B (R0's re-solve at kappa 0.7, k_c 127, D 23.0) | raw `I1101-win2/R0/sol_l1kc127k070w2_D23.0000.npy`, copy in `in/` (the control's) | 90d3e655 |
| record of state B | `I1101-win2/R0/l1kc127k070w2.jsonl`, copy in `in/` | d1a3a641 |
| k_c 31 controls | `in/sol_l1kc31r1025_D10.5000.npy`, `in/l1kc31r1025.jsonl` (the gate's) | f07a8984, e5a87ec5 |
| reader of the scans | `read_lower.py`, `d185_scan_read.py` (the control's) | 89309d3c, 7c9d400f |
| reader of Test K | `results_1101k.py` (selftest exit 0, `--mutate=ref`, `--mutate=bar`, `--mutate=last` exit 1; `selftests/selftest_results_1101k*.txt`) | c31a27c3 |
| driver | `run_scan_k.sh` | bf5c1c83 |

## Commands (unit `i1101k` runs `run_scan_k.sh`; steps in `steps.txt`, tag `[k]`)
1. `d18_secant.py selftest` (exit 0) and its mutations `half`, `norobust`, `nosigncheck` (exit 1 each) in the new worktree; `results_1101k.py selftest` and its mutations.
2. The k_c 31 controls (t5's test on this machine and build): `d18_secant.py scan in/l1kc31r1025.jsonl in/sol_l1kc31r1025_D10.5000.npy 10.5 2.87 OUT --b12=rust --b12_threads=1` plain, with `--kappa_mm=0.7` (the record's kappa: ln|det| and sign bit for bit equal to the plain scan) and with `--kappa_mm=0.35` (ln|det| moves by more than 1e-3; t5 saw +0.695 on its lambda). Three processes, 1 thread each, nice 10.
3. The scan: `d18_secant.py scan in/l1kc127k070w2.jsonl in/sol_l1kc127k070w2_D23.0000.npy 23.0 L scan_k/scan_D23.0_p<i>.jsonl --b12=rust --b12_threads=1 --kappa_mm=0.35 --pin=90d3e655,d1a3a641` for L in 0.085, 0.100, 0.115, 0.130, one process each, 1 thread, nice 10, `PYTHONPATH=SITE`. Its raw output must print `kappa_mm 0.35: ... 8351 +- 2% steps` and the record system (|F| and steps equal to the record's).
4. `read_lower.py scan_k 0.085 0.130` and `results_1101k.py scan scan_k`.
5. `d18_secant.py run RECORD STATE 23.0 LO HI secant_k.jsonl --tol=5e-5 --maxev=20 --b12=rust --b12_threads=1 --kappa_mm=0.35 --ends=scan_kall.jsonl --pin=90d3e655,d1a3a641` on the first robust change; then `results_1101k.py scan scan_k --secant=secant_k.jsonl --r2=secant_r2w.jsonl` (needs R2's secant to have ended with status `tol`).

## Predictions (mine, registered before the run; information, not pass rules)
| item | prediction |
|---|---|
| the `kappa_mm 0.35` step count within 2% of 8351 | 90% |
| k_c 31 control: kappa_mm 0.7 bit for bit equal to plain | 90% (t5 saw it); kappa_mm 0.35 moves ln\|det\| by more than 1e-3: 97% |
| the scan has a robust change in 0.085-0.130 | 65% (no change 35%; R2's own bracket (0.100, 0.130) with det-linear 0.129367 and estimator range 0.1025-0.1294 puts state B's root near R2's if t5's reading holds, which can sit just above 0.130) |
| given a root: \|root - r2\| <= 3e-3 (whole range) | 40%; between 3e-3 and 1e-2 or straddling: 30%; 1e-2 or more: 30% (state B's kappa 0.7 solve and R2's kappa 0.35 solve are different discrete solutions, and the determinant amplifies state differences exponentially, so the 2.2e-3 scatter between two k_c 143 states is the scale to compare with) |
| scan wall per point (4 processes beside R2's secant, 5 busy threads on 4 cores) | 4400 to 6000 s: 60% |
| secant wall (about 9 evaluations, no end evaluations) | 4 to 6 h: 60% |

## Status
- 2026-11-27 15:56 UTC: bars, reading rule, pins, driver, reader (planted selftest, three mutations) written before any run of Test K. Not started.
- 2026-11-27 15:56:57 UTC: unit `i1101k` started (`run_scan_k.sh`, bf5c1c83). Selftests 0/1/1/1 and 0 with both reader mutations failing; k_c 31 controls (15:57:43): plain and `--kappa_mm=0.7` ln|det| -430.2952244423991 bit for bit equal, `--kappa_mm=0.35` -429.60035787499453 (shift +0.6949, as t5's +0.695); the four scans started 15:57:43 UTC (nice 10, 1 thread each, beside R2's secant: 5 busy threads), all four print `kappa_mm 0.35: ... 8351 steps (the record's kappa 0.7: 4179)` and the record system (|F| 3.1912e-10 against the record's 3.1949e-10, 4179 steps) at 15:58 UTC, `steps_check_k.txt` PASS.

## Order, verbatim

> t5: step 1e accepted: re-solves agree 4-8x better with each other than with the stored states, and the offset is flat at D 15-15.5 then rises. #1105's u0 question is answered and the offsets are recorded. Its next steps wait, because #1101 matters more now. New order, #1101 Test K (my newest #1101 comment is the record), beside R2's secant: a worktree of wip/ell1-kappa-mm at f56f91d2 (d18_secant.py blob 2f3ee874; the same ellrs SITE ~/Source/ellrs-site-1102 works, ell_b12rs.py is unchanged). Scan state B (I1101-win2/R0/, blobs 90d3e655 and d1a3a641) with --kappa_mm=0.35 --b12=rust --b12_threads=1 at lambda 0.085, 0.100, 0.115, 0.130, 4 processes, nice 10. Check the 'kappa_mm 0.35 ... steps' line, which should be about 8351. Then 'run' at tol 5e-5 on the robust change, and compare with R2's secant root against the bars: within 3e-3 means the mode matrix alone; 1e-2 or more means the state matters too.

## Test K scan result (15:57:43 to about 17:31 UTC; unit `i1101k`; 4 processes, 1 thread each, nice 10, `--kappa_mm=0.35 --b12=rust --b12_threads=1`; `results_k.md`, `read_lower_k.txt`, `scan_k/`, `scan_k_p0.raw` to `scan_k_p3.raw`; written 2026-11-27 17:34 UTC by the clock)
All four processes printed the pin check, `kappa_mm 0.35: ... 8351 steps (the record's kappa 0.7: 4179)`, the record system (`|F| 3.1911792672e-10 (record 3.1949266444e-10), steps 4179 (record 4179)`) and `block 12 by ellrs (avx2, products dgemm, 1 threads)`, and exited 0.

| lambda | hybrid sign | noise signs | robust | dln | float64 sign | ln\|det\| | seconds (float64 blocks, Rust block 12, logdet) |
|---|---|---|---|---|---|---|---|
| 0.085 | - | - - | True | 1.16e-05 | + | -4220.2872608844 | 5369 (1741, 3604, 24) |
| 0.100 | - | - - | True | 1.20e-05 | + | -4221.2864886242 | 4991 (1517, 3418, 56) |
| 0.115 | - | - - | True | 1.94e-05 | + | -4222.6749825989 | 5599 (1652, 3926, 20) |
| 0.130 | - | - - | True | 2.45e-05 | + | -4224.2162780980 | 5226 (1599, 3594, 33) |

**No robust change in 0.085-0.130: report and wait** (`results_1101k.py scan` exit 2; `read_lower.py`: 0 robust changes, endpoint signs - and -, no ln|det| local minimum, float64 alone has the opposite sign (+) at all four, which the earlier scans showed too). Nothing widened by me, no secant: the reading rule needs a robust change. The bars are not applied (no root).

What the four points do and do not say (mine, outside the bars; the estimators are values at the scanned lambdas, not enclosures):
- `ln|det|` falls smoothly, by 67, 93 and 103 per unit lambda over the three intervals, with no dip.
- Assuming the orientation (sign + below the root, - above it: measured at state B's own root, + at 0.045 and - at 0.050 in the control, and at R2's bracket, + at 0.100 and - at 0.130; assumed for K) and a single sign change: state B's root with the mode matrix at kappa 0.35 lies **below 0.085**. R2's secant (`secant_r2w.jsonl`, as of 2026-11-27 17:34 UTC) has + at 0.1 and - at 0.129367 (its third evaluation, the interior point), so r2 lies in (0.1, 0.129367) and **|root - r2| > 0.015**, above the 1e-2 bar: the state's kappa matters too. This is an inference from signs under the stated assumptions, not a measured root; the scan below 0.085 would measure it.
- Against t5's R1 (kappa 0.5 state and steps, root 0.09500769, comment 7223316450): if the step error were the mode matrix's alone, the root would depend on the mode matrix's steps only, and with the root rising monotonically as they are refined (0.046 at 0.7, 0.09500769 at 0.5) the 0.35 root on state B would be at or above R1's. It lies below 0.085 < 0.09500769 under the assumptions above. In shifts from state B's own root 0.045967998: R2's is more than 0.054, Test K's is less than 0.039 (and negative if K's root lies below 0.045967998).
- Alternatives not excluded by four minus signs: an even number of sign changes inside the scanned range (spacing 0.015 would miss two close ones), or the root above 0.130 with the opposite orientation.

R2's ln|det| and K's at the lambdas both have (K's mode matrix on kappa 0.35 steps, R2's solved at kappa 0.35):

| lambda | K: sign, ln\|det\| | R2: sign, ln\|det\| | K - R2 in ln\|det\| |
|---|---|---|---|
| 0.100 | - -4221.286489 | + -4219.680469 | -1.6060 |
| 0.130 | - -4224.216278 | - -4223.517447 | -0.6988 |

| prediction | result |
|---|---|
| the `kappa_mm 0.35` step count within 2% of 8351 (90%) | right: 8351 on all four (`steps_check_k.txt` PASS), with the record system reproduced (|F| 3.1912e-10 against 3.1949e-10, 4179 steps) |
| k_c 31 control: 0.7 bit for bit equal to plain (90%); 0.35 moves ln\|det\| by more than 1e-3 (97%) | right: -430.2952244423991 for both, and +0.6949 at 0.35 |
| the scan has a robust change in 0.085-0.130 (65%; no change 35%) | WRONG: no change; the registered 35% outcome happened (all four hybrid signs -, all robust) |
| given a root: within 3e-3 of r2 (40%), between (30%), 1e-2 or more (30%) | not formed: no root. The inference below (outside the bars) puts the difference above 1e-2 if its assumptions hold |
| scan wall per point 4400 to 6000 s (60%) | right: 4991 to 5599 s (5 busy threads on 4 cores, as registered) |
| secant wall 4 to 6 h (60%) | not run (no bracket) |

## Status after the scan
- 2026-11-27 17:34 UTC: Test K's scan done (about 5300 s per point, 17:31 UTC): hybrid sign - at 0.085, 0.100, 0.115, 0.130, all robust; no robust change, so no secant: reported to t5, waiting for t5's order (nothing widened). R2's secant is still running (bracket (0.1, 0.129367)).

# Test K extension: state B with --kappa_mm=0.35 at lambda 0.040, 0.055, 0.070 and 0.150

Written 2026-11-27 17:35 UTC by the clock, before any run of the extension (reading rule, pins, driver, predictions first; t5's order is quoted at the end). Files `run_scan_k2.sh`, `scan_k/scan_D23.0_p4..p7.jsonl` (beside p0..p3), `scan_k2_p4..p7.raw`, `steps_check_k2.txt`, `read_lower_k2.txt`, `results_k2.md`, `secant_k.jsonl`, `secant_k.log`, `results_k2_secant.md`. Issue #1101; coordinator t5. The first four points (0.085 to 0.130) were all hybrid -, robust, no change (comment 7224555330).

## What t5 ordered
The same state B with `--kappa_mm=0.35`, Rust block, at lambda 0.070, 0.055, 0.040 (below) and 0.150 (above, in case the orientation flipped), 4 processes beside R2's secant (which keeps its thread: 5 busy threads on 4 cores, as in the first scan). Then `run` at tol 5e-5 on the first robust change, and report the eight signs and the root against R2's bracket (0.100, 0.130). t5: "If the root is below 0.085, the bar reads 'the state's kappa matters' (more than 1e-2 from R2)."

## Reading rule (unchanged from Test K; the same reader blob c31a27c3 reads all eight points)
- The bracket is the first robust change among the eight points (lowest lambda; the others are listed). A change needs both points noise-robust and robust (dln <= 0.1) with opposite hybrid signs.
- The root is read only from a `run` ending `tol`, both ends robust and of opposite signs, inside the scan's pair; the difference from R2's secant root is read on the ranges [a - d, b - c] of the final brackets (the bars 3e-3 and 1e-2 are t5's, fixed in the first section; R2's own secant must have ended with status `tol`, else its robust bracket bounds the difference outside the rule).
- Step count: each new scan must print `kappa_mm 0.35: ... 8351 +- 2% steps` and the record system (the scans are killed otherwise).
- No robust change in [0.040, 0.150]: reported as measured, nothing widened by me. If R2's secant ends first, its record is read as it stands.
- The k_c 31 controls are not repeated (same pinned worktree and blobs as the first scan, whose controls passed).

## Pins (as the first scan, plus the driver)
| what | blob |
|---|---|
| worktree `~/Source/choptuik-large-d-1101k` at f56f91d2, `d18_secant.py` | 2f3ee874 |
| `ell_b12rs.py`, ellrs in `~/Source/ellrs-site-1102`, venv `~/Source/choptuik-large-d-1058b/.venv` | a1fff74f |
| state B and its record (`in/`) | 90d3e655, d1a3a641 |
| `read_lower.py`, `d185_scan_read.py`, `results_1101k.py` | 89309d3c, 7c9d400f, c31a27c3 |
| driver `run_scan_k2.sh` (unit `i1101k2`) | 969cf894 |

## Predictions (mine, registered before the run; information, not pass rules)
| item | prediction |
|---|---|
| the `kappa_mm 0.35` step count within 2% of 8351 at all four | 90% |
| the first robust change is in (0.070, 0.085) | 30%; in (0.055, 0.070) 25%; in (0.040, 0.055) 20% |
| no robust change in 0.040-0.150 | 15% (a change at (0.130, 0.150) 4%; two changes, or a non-robust end that blocks the pair, 6%) |
| sign at 0.040 is + | 80% (state B's own root, kappa 0.7, is 0.045968 with + below it) |
| given a root: reads as the state's kappa matters (1e-2 or more from R2) | 90% (R2 is above 0.100, K below 0.085 if the orientation holds); between 3e-3 and 1e-2 or straddling: 8%; within 3e-3: 2% |
| scan wall per point (5 busy threads on 4 cores, as the first scan) | 4400 to 6200 s: 70% (first scan 4991 to 5599 s) |
| secant wall (about 8 evaluations with the two end records, 1 thread, R2's secant beside it) | 3 to 6 h: 60% |

## Status
- 2026-11-27 17:35 UTC: bars, reading rule, pins, driver and predictions written before any run of the extension. Not started.
- 2026-11-27 17:35:53 UTC: unit `i1101k2` started (`run_scan_k2.sh`, 969cf894). Selftests 0/1/1/1 and 0 with both reader mutations failing; the four scans (lambda 0.040, 0.055, 0.070, 0.150; files p4..p7; nice 10, 1 thread each, beside R2's secant) started 17:35:53 UTC; at 17:36:13 all four print `kappa_mm 0.35: ... 8351 steps (the record's kappa 0.7: 4179)` and the record system (|F| 3.1912e-10 against 3.1949e-10, 4179 steps), `steps_check_k2.txt` PASS.

## Order, verbatim

> t5: Test K's scan read (all - at 0.085-0.130, nothing formed, as written). Extend it now, 4 processes (R2's secant keeps its thread): the same state B with --kappa_mm=0.35, Rust block, at lambda 0.070, 0.055, 0.040 (below) and 0.150 (above, in case the orientation flipped). Then run the secant (tol 5e-5) on the first robust change, and report the eight signs and the root against R2's bracket (0.100, 0.130). If the root is below 0.085, the bar reads 'the state's kappa matters' (more than 1e-2 from R2).

## Test K extension: t5's second order (17:4x UTC 27 Nov): no secant
> t5: Test K's reading is accepted: the state's kappa matters (my newest #1101 comment). Let the extension's four scan points finish for the record, but do NOT run its secant (a mode matrix at kappa 0.35 about a kappa 0.7 state is not a valid root). R2's secant runs on. Report the four signs when they land.

- The four scans (lambda 0.040, 0.055, 0.070, 0.150; unit `i1101k2`, started 17:35:53) run on. The driver `run_scan_k2.sh` would start `run` on the first robust change after them, so its main process (pid 2307228, waiting for the scans) was frozen with SIGSTOP at 17:44:45 UTC; the scans are its children and run on (checked by `ps`: four python processes in state R). Killing the driver would end the unit and, with the systemd default `KillMode=control-group`, the scans; hence the freeze.
- After the four scans ended, `run_k2_read.sh` (the driver's read-only stages: record-system lines into `steps.txt`, `read_lower.py scan_k 0.040 0.150` into `read_lower_k2.txt`, `results_1101k.py scan scan_k` into `results_k2.md`; no secant) is run by hand, and then the frozen driver's unit is stopped. The reading rule and the predictions of the section above stand for the signs; the secant predictions ("given a root", "secant wall") are void: no secant, no root, so the bars are not applied to this extension.

### Order of the last steps (t5's third message, 17:4x UTC 27 Nov: "once the four scans have ended and written their records, end the stopped driver (kill -9 its pid, or systemctl --user stop the unit), so no stopped process is left. Then do the read-only reading. Note it in the README.")
1. When all four scans have exited (four `[k2] lambda ... exit` lines in `steps.txt`), a watcher checks that no scan process of p4..p7 is left, then runs `systemctl --user stop i1101k2.service` (ends the frozen driver pid 2307228 and its `systemd-inhibit` wrapper; the scans have ended, so `KillMode=control-group` kills nothing else) and checks with `ps` that no process of `run_scan_k2.sh` is left.
2. Then `run_k2_read.sh` (now blob 399f0746; its header comment changed to say the unit is stopped before it) runs the read-only stages. The times of both steps are in `steps.txt` (tags `k2s` and `k2r`) and in the status line below.

## Test K extension result (scans 17:35:53 to 19:10:33 UTC; unit `i1101k2`; lambda 0.040, 0.055, 0.070, 0.150, files p4..p7; 4 processes, 1 thread each, nice 10, `--kappa_mm=0.35 --b12=rust --b12_threads=1`; `results_k2.md`, `read_lower_k2.txt`, `scan_k2_p4.raw` to `scan_k2_p7.raw`; written 2026-11-27 19:11 UTC by the clock)
All four processes printed the pin check, `kappa_mm 0.35: ... 8351 steps (the record's kappa 0.7: 4179)`, the record system (`|F| 3.1911792672e-10 (record 3.1949266444e-10), steps 4179 (record 4179)`) and `block 12 by ellrs (avx2, products dgemm, 1 threads)`, and exited 0 at 19:05:30 (lambda 0.040), 19:08:34 (lambda 0.055), 19:08:43 (lambda 0.070), 19:10:33 (lambda 0.150) UTC.

| lambda | scan | hybrid sign | noise signs | robust | dln | float64 sign | ln\|det\| | seconds (float64 blocks, Rust block 12, logdet) |
|---|---|---|---|---|---|---|---|---|
| 0.040 | extension | + | + + | True | 3.21e-05 | + | -4213.8355983987 | 5354 (1633, 3662, 59) |
| 0.055 | extension | + | + + | True | 4.30e-05 | + | -4216.2320148322 | 5542 (1590, 3919, 33) |
| 0.070 | extension | + | + + | True | 1.43e-04 | + | -4219.7620966375 | 5552 (1632, 3890, 30) |
| 0.085 | first | - | - - | True | 1.16e-05 | + | -4220.2872608844 | 5369 (1741, 3604, 24) |
| 0.100 | first | - | - - | True | 1.20e-05 | + | -4221.2864886242 | 4991 (1517, 3418, 56) |
| 0.115 | first | - | - - | True | 1.94e-05 | + | -4222.6749825989 | 5599 (1652, 3926, 20) |
| 0.130 | first | - | - - | True | 2.45e-05 | + | -4224.2162780980 | 5226 (1599, 3594, 33) |
| 0.150 | extension | - | - - | True | 3.07e-05 | - | -4226.4083914770 | 5657 (1802, 3835, 19) |

**The eight signs: + + + - - - - - (0.040 to 0.150). One robust change, (0.070, 0.085), + to -** (`results_1101k.py scan` exit 3, `read_lower.py`: 1 robust change, 0 non-robust points, endpoint signs + at 0.040 and - at 0.150, no ln|det| local minimum; det-linear 0.079425, estimator range [0.070915, 0.079425] at the width of the pair). The orientation did not flip (nothing above 0.130 changes). Float64 alone has the opposite sign at 0.085 to 0.130 (the earlier scans showed that too).

**No secant** (t5's order, 17:45 UTC: "a mode matrix at kappa 0.35 about a kappa 0.7 state is not a valid root"), so no root of K is read and the bars are not applied. The brackets alone (estimators at the scanned lambdas, not enclosures; arithmetic by `append_k2_result.py`):

|  | root's bracket | shift from state B's own root 0.045968 (bracket ends) | source |
|---|---|---|---|
| state B, kappa 0.7 (R0, control) | 0.045967998 | 0 | dh370, control passed (`results_ctl.md`) |
| K: state B, mode matrix at kappa 0.35 | (0.07, 0.085), det-linear 0.079425 | +0.0240 .. +0.0390 | this scan (`read_lower_k2.txt`), no secant |
| R2: kappa 0.35 re-solve | (0.114683, 0.129367) after 4 evaluations | +0.0687 .. +0.0834 | R2's secant, still running |
| R1: kappa 0.5 re-solve (t5, macm3) | 0.09500769 | +0.0490 | t5's comment 7223316450 |

- K's bracket (0.070, 0.085) against R2's (0.114683, 0.129367): root(K) - root(R2) lies in [-0.0594, -0.0297], the whole range above 1e-2 in size, as t5 wrote for a root below 0.085 ("the state's kappa matters"). Outside the reading rule (no secant record), the same range as the reading rule would take it.
- The mode matrix's part of R2's shift: K moved by +0.024 to +0.039 from state B's own root, R2 by +0.069 to +0.083: the ratio is 0.29 to 0.57 from the brackets. The rest, +0.030 to +0.059, is the state's.

| prediction | result |
|---|---|
| the `kappa_mm 0.35` step count within 2% of 8351 at all four (90%) | right: 8351 on all four (`steps_check_k2.txt` PASS), the record system reproduced (|F| 3.1912e-10 against 3.1949e-10, 4179 steps) |
| the first robust change is in (0.070, 0.085): 30%; (0.055, 0.070): 25%; (0.040, 0.055): 20% | (0.070, 0.085) happened: the most likely of the three buckets, 30%; its hybrid sign pattern is + + + - - - - - |
| no robust change in 0.040-0.150 (15%) | right: one change |
| the sign at 0.040 is + (80%) | right |
| given a root: reads as the state's kappa matters (90%) | void: no secant (t5's order). By the brackets alone the range is [-0.0594, -0.0297], whole range above 1e-2 in size: the same reading, outside the reading rule |
| scan wall per point 4400 to 6200 s (70%) | right: 5354 to 5657 s (5 busy threads on 4 cores, as registered) |
| secant wall 3 to 6 h (60%) | void: not run |

## Status after the extension
- 19:10:33 UTC: the four scans ended (exit 0 each, last at lambda 0.150); 19:10:36 UTC: `systemctl --user stop i1101k2.service` ended the frozen driver and its `systemd-inhibit` (no scan was running; `ps`: 0 processes of `run_scan_k2.sh` left, unit inactive; steps.txt tag `k2s`); 19:10:36 UTC: `run_k2_read.sh` (399f0746) read the eight points, exit 3 (a bracket), no secant (tag `k2r`). Reported to t5; R2's secant runs on (4 evaluations, bracket (0.114683, 0.129367)).

## R2 widened scan and secant result (scan 12:46:59 to 14:01:09 UTC, secant 14:01:09 UTC 27 Nov to 00:42:36 UTC 28 Nov; unit `i1101r2w`, `run_scan_w.sh`; 1 thread per process, nice 10, `--b12=rust --b12_threads=1`; `results_r2w.md`, `results_r2w_secant.md`, `read_lower_r2w.txt`, `secant_r2w.jsonl`, `secant_r2w.log`, `scan_r2/`, `scan_r2w/`, `scan_r2all/`; written 2026-11-28 00:45 UTC by the clock)
All processes printed the pin check and the record system, and exited 0. The scan read the eight points (the four of `scan_r2/` and the four of `scan_r2w/`) with `read_lower.py`: 1 robust change, (0.100, 0.130), + to -, no non-robust point, no ln|det| local minimum; the secant ran on it (`--pin=25ba3a91,9111bfca`).

| lambda | from | hybrid sign | noise signs | robust | dln | float64 sign | ln\|det\| | seconds (float64 blocks, Rust block 12, logdet) |
|---|---|---|---|---|---|---|---|---|
| 0.035 | widened scan | + | + + | True | 1.33e-05 | - | -4210.6738318039 | 4423 (1285, 3118, 20) |
| 0.045 | first scan | + | + + | True | 1.35e-05 | - | -4211.9503431400 | 6625 (1741, 4865, 19) |
| 0.050 | first scan | + | + + | True | 1.35e-05 | + | -4212.5955870798 | 6600 (1752, 4823, 25) |
| 0.060 | first scan | + | + + | True | 1.37e-05 | - | -4213.9037243145 | 6493 (1782, 4648, 63) |
| 0.070 | first scan | + | + + | True | 1.38e-05 | - | -4215.2427588991 | 6534 (1748, 4751, 36) |
| 0.085 | widened scan | + | + + | True | 1.39e-05 | - | -4217.3438843690 | 4411 (1262, 3121, 29) |
| 0.100 | widened scan | + | + + | True | 1.35e-05 | - | -4219.6804690495 | 4410 (1265, 3114, 31) |
| 0.130 | widened scan | - | - - | True | 2.03e-05 | - | -4223.5174465975 | 4418 (1275, 3114, 29) |

**The secant** (`d18_secant.py run` 0.1 0.13, tol 5e-5, `maxev 20`; status `tol`, exit 0, 10 evaluations, 38487 s; both bracket ends robust with opposite hybrid signs, inside the scan's pair; the reading rule of the section above is met):

| # | lambda | role | hybrid sign | noise signs | dln | ln\|det\| | seconds | x the first (2351 s, alone) | ended about (UTC, start 14:01:09 + cumulative seconds) |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 0.1000000000 | end | + | + + | 1.35e-05 | -4219.6804690495 | 2351 | 1.00 | 14:40 |
| 2 | 0.1300000000 | end | - | - - | 2.03e-05 | -4223.5174465975 | 3954 | 1.68 | 15:46 |
| 3 | 0.1293668891 | interior | - | - - | 2.09e-05 | -4223.4978332022 | 4819 | 2.05 | 17:06 |
| 4 | 0.1146834446 | interior | + | + + | 3.65e-05 | -4223.1071772153 | 4597 | 1.96 | 18:23 |
| 5 | 0.1234412471 | interior | - | - - | 3.41e-05 | -4223.5351830764 | 3933 | 1.67 | 19:28 |
| 6 | 0.1190623458 | interior | - | - - | 1.25e-04 | -4224.5431816817 | 4024 | 1.71 | 20:35 |
| 7 | 0.1172068478 | interior | + | + + | 2.25e-04 | -4225.0237888553 | 4441 | 1.89 | 21:49 |
| 8 | 0.1179158498 | interior | - | - - | 1.59e-03 | -4227.0200769929 | 3797 | 1.62 | 22:53 |
| 9 | 0.1178310580 | interior | - | - - | 2.33e-02 | -4229.7102288258 | 3291 | 1.40 | 23:47 |
| 10 | 0.1178060580 | interior | + | + + | 7.74e-03 | -4228.5899539305 | 3267 | 1.39 | 00:42 |

**Root and bar.** Final bracket (0.117806058, 0.117831058), width 2.50e-05, signs + and -, both ends robust (dln 7.74e-03 at the + end, 2.33e-02 at the - end, under 0.1); det-linear root (`lam_lin`) **0.117824909**.
- delta = root - 0.045968 = **+0.071857** (the bracket gives +0.071838 to +0.071863).
- E_root = delta x 16/15 = **+0.076647** (bracket +0.076627 to +0.076654).
- Bar (t5's): |E_root| >= 3e-3 is real, <= 1e-3 refutes #1103's inference, between is mixed. **|E_root| >= 3e-3: the step error is real** (`results_1101.py r2w --secant` exit 0, `results_r2w_secant.md`). The estimator values are at the width of the final bracket, not rigorous enclosures.

**The three roots and Test K side by side** (arithmetic on the numbers above and on the scan pair of `read_lower_k2.txt`; not a fit):

|  | kappa of the state (and of the mode matrix) | steps | root | shift from state B's own root 0.045968 |
|---|---|---|---|---|
| state B (R0, control) | 0.7 | 4179 | 0.045967998 | 0 |
| R1 (t5, macm3) | 0.5 | 5847 | 0.09500769 | +0.04904 |
| R2 (this secant) | 0.35 | 8351 | 0.117824909 (bracket 0.117806 to 0.117831) | +0.07186 |
| Test K: state B, mode matrix at 0.35 (scan pair only, no secant) | 0.7 state, 0.35 mode matrix | 4179 (state), 8351 (mode matrix) | in (0.07, 0.085) | +0.0240 .. +0.0390 |

- Shift per added step: 2.94e-05 from 4179 to 5847 steps, 9.11e-06 from 5847 to 8351 steps. The shift grows with the refinement and by less than the steps do; three points, so no extrapolation is made here.
- Test K's scan pair puts the mode matrix's part of R2's shift at 0.33 to 0.54; the state's part is the rest, 0.46 to 0.67. This uses K's pair, not a K root (no secant, t5's order).

**Load and the priority rule.** The first evaluation took 2351 s alone. Evaluations 2, 3, 4, 5, 6, 7, 8 took more than 1.5 times that (3526 s), up to 4819 s (the third). What ran beside R2's secant, by the clock: Test K's four scans 15:57 to 17:31 UTC, its extension's four scans 17:35 to 19:10, the #1104 re-solve (3 threads, nice 10) from 19:37, the #1104 kappa 0.7 re-root (1 thread, nice 19) 19:39 to 22:40. Evaluation 2 (about 14:41 to 15:46) ran before them, and I did not record here what else was busy then. I did not throttle: the extra jobs ran at nice 19 or were the registered 4 to 5 busy threads, and 4600 s beside five busy threads was the time I had registered for the loaded case (#1104 README, Resources). Evaluations 9 and 10 ran with only the re-solve (3 threads) beside R2 and took 3291 and 3267 s (1.39 times the first).

| prediction | result |
|---|---|
| no robust change in [0.035, 0.130]: 45%; (0.100, 0.130): 25%; (0.085, 0.100): 12%; (0.070, 0.085): 8%; (0.035, 0.045): 7% | (0.100, 0.130) happened (the 25% case, the second most likely): + at 0.035 to 0.100, - at 0.130, all eight robust; the secant root 0.117825 is inside it |
| pole fit (for information): best fit at lambda0 near 0.12, rms 8e-4 in ln | the root is 0.1178, near the first of the two registered fits (it does not locate a root, as registered) |
| given a change: |E_root| >= 3e-3 (97%) | right: E_root = +0.07665, 26 times the bar |
| all four new points robust (80%) | right: 0.035, 0.085, 0.100, 0.130 all robust (dln 1.33e-05 to 2.03e-05) |
| scan wall: 1800 to 3000 s per point | WRONG: 4410 to 4423 s per point (4450 s for the four, 12:46:59 to 14:01:09 UTC); the cause was not looked for |
| secant wall: 2 end points and 3 to 6 interior points of 1500 to 2500 s each, 2 to 4 h in all | WRONG: 2 ends and 8 interior points (10 evaluations), 2351 to 4819 s each, 38487 s = 10.7 h in all |

## Status after R2's secant
- 00:42:36 UTC 28 Nov: R2's secant ended (status `tol`, exit 0, 10 evaluations, 38487 s): root 0.117824909, delta +0.071857, E_root +0.076647, the step error is real; reported to t5 by hc (00:4x UTC). #1101 is not closed and keeps its `running` label (t5 decides).

# R3: the kappa 0.25 point (R1's state re-solved at kappa 0.25 on mm5; the root on dh170)

Written 2026-11-28 00:58 UTC by the clock, before any R3 run (bars, reading rule, memory rule, pins, driver and predictions first; t5's order is quoted at the end). Machine dh170 (i7-7700, 4 physical cores, 31 GB; Linux), issue https://github.com/nmoinvaz/choptuik-large-d/issues/1101, coordinator t5. t5's order: the hc of 28 Nov about 00:50 UTC and comment 7231154979 ("R3 also on mm5"). Files of this section: `run_scan_r3.sh`, `results_r3.py`, `scan_admit.sh`, `selftests/dryrun_r3.sh`, `pins_r3.txt`, `in/sol_l1kc127k025mm5_D23.0000.npy`, `in/l1kc127k025mm5.jsonl`, `scan_r3/`, `scan_r3_p*.raw`, `read_lower_r3.txt`, `results_r3.md`, `secant_r3.jsonl`, `secant_r3.log`, `results_r3_secant.md`, `DONE_r3.txt` / `STOP_r3.txt`; steps and exits in `steps.txt`, tag `[r3]`.

## What R3 is
mm5 re-solves R1's state (raw `I1101-macm3/in/`: `sol_l1kc127k050m3_D23.0000.npy` 0124dbd2, `l1kc127k050m3.jsonl` 944a8179) at kappa 0.25 (`ell_refine.py l1kc127k050m3 127 l1kc127k025mm5 127 1 23.0 2.0992182200 --kappa 0.25 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma`, 6 threads, nice 10, cap 43200 s; worktree at 48c36355). Its state and record go to `I1101-mm5/` (expected about 03:00 to 06:00 UTC 28 Nov). This is the fourth consistent point (kappa 0.7, 0.5, 0.35, 0.25) and the test of t5's single power: through R0 (0.045968), R1 (0.09500769) and R2 (0.117824909) the power p = 2.39 gives the root 0.1272 at kappa 0.25 (and 0.1348 at kappa 0). macm3 started its own R3 at 17:48 UTC 27 Nov and has been unreachable since about 20:00; if it returns, the two are a reproducibility check (t5).

## Bars and reading (t5's, fixed before the run; each can fail)
1. **The state** (mm5's re-solve): |F| <= 5e-10 and steps 11700 +- 2% (11466 to 11934). Otherwise the state is not scanned, the driver writes `STOP_r3.txt`, and I report (no cause looked for without t5's order).
2. **The scan:** on the Rust block 12 (`d18_secant.py scan --b12=rust --b12_threads=1`), 1 thread per process, nice 10, at lambda 0.115, 0.125, 0.135, 0.145, beside #1104's re-solve; widen to 0.105 and 0.155 if no robust change; nothing further.
3. **The root:** `d18_secant.py run` at tol 5e-5 on the robust change. Reading: **the root against 0.1272; within 2e-3 the model stands** (the root scatter is about 1e-3 at this size), **otherwise a second term is needed** (t5: then a fourth kappa point is next).

**Reading rule (mine, stated before the run).** A root is read only from a `d18_secant.py run` ending with status `tol`, both bracket ends robust (noise signs equal the hybrid sign, dln <= 0.1) with opposite hybrid signs, and inside the scan's pair; root = `lam_lin` (the det-linear root inside the final bracket). "Stands" needs `lam_lin` and the whole final bracket inside [0.1252, 0.1292]; "a second term is needed" needs `lam_lin` and the whole bracket outside it; a bracket that reaches the edge of the band is "reported as measured". With several robust changes the lowest-lambda one gets the secant and the others are listed. The estimator values are at the width of the final bracket, not rigorous enclosures. R2's root 0.117824909 and R1's 0.09500769 are taken as measured (t5's comments).

## Memory rule (new; the machine would run out of memory otherwise)
One scanner process (`d18_secant.py scan` or `run`) held 4733032 kB (Test K) and 4862620 kB (R2's secant) at peak; the machine has 32735432 kB, about 4 GiB of other use, and the #1104 re-solve holds up to 2.7 GB. So at most **4 scanner processes at once while `ell_refine.py` runs, 5 otherwise**, counted over the whole machine (`scan_admit.sh`, `bg_admit`, one flock so two drivers cannot both see a free slot). R3's four scans beside the re-solve are 4. If #1104's kappa 0.5 scan (4 processes) and R3's scan are due together, the second waits for free slots, and I tell t5. Nothing else of my runs changes: the #1104 driver gets the same rule before it can start (its pin below is updated then).

## Pins (by blob, `git hash-object --no-filters`; the driver refuses any other)
| what | where | blob |
|---|---|---|
| R3 state and record | raw `I1101-mm5/`, copied to `in/`; blobs written to `pins_r3.txt` and `steps.txt` when both land (unchanged for 2 min) | at landing |
| scanner worktree | `~/Source/choptuik-large-d-1102` at d4b6b6ce, `solver/matter/d18_secant.py` (as R2) | 9706e506 |
| block 12 driver, ellrs, venv | `ell_b12rs.py` in the worktree; ellrs in `~/Source/ellrs-site-1102`; `~/Source/choptuik-large-d-1058b/.venv` | a1fff74f |
| scan readers | `in/read_lower.py`, `in/d185_scan_read.py` (the #1101 copies) | 89309d3c, 7c9d400f |
| reader of R3 (selftest exit 0; mutations `tol`, `pred`, `last`, `sign` exit 1; `selftests/selftest_results_r3*.txt`) | `results_r3.py` | 50c83985 |
| admission library | `scan_admit.sh` | e61f8891 |
| driver | `run_scan_r3.sh` (unit `i1101r3`), dry-run test `selftests/dryrun_r3.sh` with a fake scanner (planted roots 0.1272, 0.1075, 0.3; a bad \|F\| and a bad step count stop it) | c060c215, b3e41c15 |

The scanner is the one of R2 (9706e506 at d4b6b6ce); the kappa_mm worktree's d18_secant.py (2f3ee874) differs from it only by the `--kappa_mm` option, which these runs do not use (`git diff d4b6b6ce f56f91d2 -- solver/matter/d18_secant.py`: the `kappa_mm` function and its two calls). `--ends` takes the two end records from the scan, which saves two evaluations of the secant.

## Driver (`run_scan_r3.sh`, unit `i1101r3`, started now; it waits for the files)
1. Static pins, the `results_r3.py` selftest and mutations (0 1 1 1 1), the `d18_secant.py` selftest and mutations (0 1 1 1).
2. Waits: a `git fetch` of the raw push worktree every 5 min (the worktree is only fetched, never checked out here), until `sol_l1kc127k025mm5_D23.0000.npy` and `l1kc127k025mm5.jsonl` are each present once under `I1101-mm5/` of `origin/main` with unchanged blobs for 2 min; copies them to `in/`; writes the blobs to `pins_r3.txt`; checks the record: |F| <= 5e-10, steps in [11466, 11934], kappa 0.25, k_c 127, D 23, l 1.
3. Scan: four processes (`scan_r3/scan_D23.0_p0..3.jsonl`, `scan_r3_p*.raw`); each prints the record system (|F| and steps equal to the record's), else the group is killed (`STOP`); then `read_lower.py` and `results_r3.py scan` (exit 0 a bracket, 2 none); on 2, the two widened points (p4, p5) and the reading again; none again: `DONE_r3.txt` "no robust change in 0.105 .. 0.155" and no secant.
4. Secant on the first robust change at tol 5e-5, `--maxev=20`, `--ends=scan_r3_all.jsonl`, `--pin` the two blobs; then `results_r3.py read` into `results_r3_secant.md` (exit 0 formed, 4 the record is not read).

## Predictions (mine, registered before the run; information, not pass rules)
| item | prediction |
|---|---|
| R3's state and record land on `I1101-mm5/` by 06:00 UTC 28 Nov | 55% (t5: about 03:00 to 06:00) |
| mm5's re-solve passes its bars (\|F\| <= 5e-10, steps 11700 +- 2%) | 85% |
| the four points show one robust change | 80% (in (0.125, 0.135): 55%; (0.115, 0.125): 20%; (0.135, 0.145): 5%); none, widening needed: 20% |
| the root within 2e-3 of 0.1272 (the single power stands) | 35%; below 0.1252: 45% (with two terms of the kappa series the local order falls toward the leading one, so the error at 0.25 is larger than the single power gives); above 0.1292: 20% |
| scan wall per point (4 processes beside the re-solve's 3 threads) | 5500 to 9000 s: 60% (R2's 8351-step points took 4410 s; 11700 steps is 1.4 times as many) |
| secant | 6 to 10 evaluations: 60%; wall 8 to 16 h: 55% |

## Status
- 2026-11-28 00:58 UTC: bars, rule, pins, driver and predictions written before any R3 run; the driver passed its dry run on a fake scanner (root 0.1272 stands; root 0.1075 found by the widened points; root 0.3 no change in six points, no secant; |F| 7e-10 and 12000 steps both stop). The unit `i1101r3` starts next.

## Order, verbatim

### t5's hc (28 Nov)

> t5: R2's write-up accepted, and the scorecard is fine; #1101 stays open (R3 is the next test). Order: arm a waiter now for R3's state from mm5 (raw I1101-mm5/: sol_l1kc127k025mm5_D23.0000.npy and l1kc127k025mm5.jsonl; expected about 03:00-06:00 UTC). When both land, pin their blobs and scan on the Rust block at lambda 0.115, 0.125, 0.135, 0.145, 1 thread each, nice 10, beside #1104's re-solve, then the secant at tol 5e-5 on the robust change; widen to 0.105 and 0.155 if none. Bars and reading: my #1101 comment 7231154979 (root against 0.1272, within 2e-3). README section first.

### Comment 7231154979 (t5, 2026-11-28 00:44 by the clock)

> **R3 also on mm5** (t5, 2026-11-28 00:44 by the clock)
>
> macm3, which started R3 (κ 0.25 from R1's state) at 17:48 UTC, has been unreachable since about 20:00. R3 is the test of the single-power model above (prediction 0.1272), so it runs again on mm5's 6 free threads. If macm3 returns with its own R3, the two are a reproducibility check of the same system on two machines.
>
> - **Run (mm5):** a worktree of the l = 1 code at 48c36355 (`ell_refine.py` 631e5801, `dss_ell.py` 5d28c19e, as R0–R2), R1's state and record (raw `I1101-macm3/in/`: `sol_l1kc127k050m3_D23.0000.npy` 0124dbd2, `l1kc127k050m3.jsonl` 944a8179), blob-checked: `ell_refine.py l1kc127k050m3 127 l1kc127k025mm5 127 1 23.0 2.0992182200 --kappa 0.25 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma`, 6 threads, nice 10, cap 43200 s.
> - **Bars:** |F| ≤ 5e-10 and steps 11700 ± 2%. Its state and record are pushed to `I1101-mm5/`. The root scan runs on dh170 (Rust block) at λ 0.115, 0.125, 0.135, 0.145, with the secant at tol 5e-5.
> - **Reading:** the root against 0.1272 (the single power p = 2.39). Within 2e-3, the model stands (the root scatter is about 1e-3 at this size); otherwise a second term is needed.
