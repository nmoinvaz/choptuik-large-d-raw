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
