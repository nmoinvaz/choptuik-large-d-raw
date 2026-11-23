# I1079-macm3/m5: M = 5 at the two certified M = 3 excited zeros of #1079, do they persist?

Machine: macm3 (Apple M3, 8 cores, 24 GB), session `choptuik-macm3-i1080`. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1080 (coordinator t5's order of 2026-11-23, after #1079). Raw base: `I1026-dh610/` of the raw-data repository at 143d4d5bcd.
Code: main 59f36abc (no tracked changes), `solver/inner_stokes/hier_nb.py` 68b287ece6, `hier.py` b4e4d887aa, `inner_nb.py` 53374669c3, `inner_np.py` 80b7edaa77 (blobs). #1026 ran fc7dee4d of wip/excited-zeros; main's `hier_nb.py` and `hier.py` differ from it only by opt-in options (`--h5/--h7/--h9`, `--polish`, `--floor_max`, `--verbose=3` output), whose defaults leave the solve unchanged; the control tests that.
Environment: venv `~/Source/venv-macm3-i1080` (Python 3.14.3, numpy 2.5.4, scipy 1.18.1, mpmath 1.3.0, numba 0.68.1, llvmlite 0.50.0; the same pins as #1026's venv; made for this task because no macm3 venv has numba), 2 processes per solve, nice 10, one BLAS thread per process (`OMP_NUM_THREADS=1` etc.; #1026 left them unset), detached under `caffeinate -is` (`launch.py`).

## Reading, fixed before the run (copied from the issue)

**Reading, fixed before the run.** A zero persists at M = 5 when both of these hold:
- its walks converge (|r₃|, |r₅| below 10⁻⁶ in each solve, #1026's bar) at ξ₁ 0.2 and 0.25, to the same (A, ω/ω∞) within 10⁻⁵;
- its M = 3 → 5 shift is smaller than its M = 1 → 3 shift. If no M = 1 partner lies within 0.3, the bar is 0.1, below half the known zero's 0.24.

It fails when a walk does not converge, or the shift is larger. Report |F₅|/|F₃| at each converged zero; the known zero's is about 0.06.

How the code reads it (`report1080.py`, selftest with seven synthetic cases, two that persist and five that fail): a walk converges when `walk1026.py`'s verdict says so (Newton step below 3e-6 in A and w/w_inf, best solve's |r_3|, |r_5| below 1e-6); the radii agree when the two zeros differ by at most 1e-5 in A and in w/w_inf; shifts are Euclidean norms in (A, w/w_inf) from the box centre (the certified M = 3 zero) to the walk's zero (best solved point plus the Newton step); the M = 1 partner is the nearest zero of orientation +1 in #995's located list (`inputs/zeros_M1.md`, 25 zeros, sum -1), and the bar is its distance to the M = 3 zero. The issue's rule has no case for two converged radii that disagree, or for a walk stopped by the iteration cap; the report counts both as a failure and says which. |F₅|/|F₃| is |F_5/F_1| over |F_3/F_1| at the best solved point.

## The M = 1 partners (from `inputs/zeros_M1.md`, before any run)

```
x1: M = 3 zero (3.446218246, 0.347606965), M = 1 partner (3.307235, 0.367124) located at xi1 0.2, shift (+0.13898, -0.01952), distance 0.14035, bar 0.14035
x2: M = 3 zero (3.526473057, 0.211497981), M = 1 partner (3.674531, 0.360326) located at xi1 0.2, 0.25, shift (-0.14806, -0.14883), distance 0.20993, bar 0.20993
```

For x1 the nearest zero of any orientation is a -1 zero at (3.495560, 0.366224), 0.053 away; orientation +1 is the rule's.

## Commands (`run1080.sh`, run from `solver/inner_stokes` of main 59f36abc)

```
W="/Users/nathan/Source/venv-macm3-i1080/bin/python -u walk1026.py"      # blob d95e6afd65c7, from I1026-dh610/ (eval1026.py b6675e38262d)
$W control 2.726475885672135 1.0156030949093042 0.1444194785 0.0110874259 --xi1 0.2  --procs 2 --maxit 25   # gate: eval1026.py exits 0 (within 1e-5 of A 2.718579189, w 0.999228404), --mutate=shift exits 1
$W x1 3.446218246366727 0.34760696521740736 0.8054175864 0.0117800438 --xi1 0.2  --procs 2 --maxit 25
$W x2 3.5264730566957154 0.21149798139121542 0.9765085452 -0.0017633195 --xi1 0.2  --procs 2 --maxit 25
$W x1 3.446218246366727 0.34760696521740736 0.8054175864 0.0117800438 --xi1 0.25 --procs 2 --maxit 25
$W x2 3.5264730566957154 0.21149798139121542 0.9765085452 -0.0017633195 --xi1 0.25 --procs 2 --maxit 25
$W control 2.726475885672135 1.0156030949093042 0.1444194785 0.0110874259 --xi1 0.25 --procs 2 --maxit 25   # route check at 0.25, not a gate (#1026's control failed its start solve there)
/Users/nathan/Source/venv-macm3-i1080/bin/python report1080.py report
```

Each solve is `hier_nb.py 5 A w --x=B3,C3[,B5,C5] --fixA --schur --procs 2 --verbose=1 --xi1=XI` (the line is the first line of each `logs/fix_*.log`). The control at ξ₁ 0.2 runs first; the zeros at 0.2 run side by side (4 processes), then the zeros and the 0.25 control side by side (6). The driver stops on a failed control gate or on a Traceback in any log, and runs the rest otherwise.

x1 and x2 are the first and second excited zeros of #1079 (orientation +1), p̂ from the box files `inputs/A_M_box_M3x1E2_h1e-12_w1e-13.json` and `inputs/A_M_box_M3x2E2_h1e-12_w1e-12.json` (raw `I1079-macm3/levers/data/`; blobs 1e6432082f72 and a1ae03915f0c); `report1080.py args NAME` prints the walk's four arguments from them (B3, C3 to 10 decimals, the convention of the control's `0.1444194785 0.0110874259`, which is the fundamental's box centre `solver/proof/data/A_M_box_M3_1e-9.json`).

## Files

| file | content |
|---|---|
| `run1080.sh`, `memlog1080.py`, `launch.py` | the driver, the memory and load sampler (every 60 s), the detached starter |
| `walk1026.py`, `eval1026.py` | #1026's walk and its control gate, unchanged (blobs above); `run1026.sh.dh610`, `common1026.sh.dh610` are dh610's driver and paths, for reference |
| `report1080.py` | the inputs and the reading of this issue (`args`, `partners`, `report`, `selftest`) |
| `inputs/` | the two box files, `zeros_M1.md` of I995-mac/m1b (blob 91635eb89d12), the stored M = 5 selection log |
| `walks/`, `logs/`, `exits_1080.txt`, `memlog_1080.log` | one JSON per walk, each solve's and walk's log, exits, the sampler |

## The extended-precision walks (the coordinator's rule, copied before the run)

From #1080's comment 7111416293, copied verbatim here at 2026-11-23 19:20 UTC, before any walk ran. The exploratory folders (`explore/`, `explore_mp/`) are not readings; the walks below are, under this rule. His message with the order: start x1's walk now (5 processes at nice 10 beside x2's start rerun) on a0441d8b, stop x1's undamped start (176daf53), x2's walk the same way after x2's start converges, and after each located end `value_mp.py pointv <A> <WF> --M=5 --v=<last v> --r1=0.2`; report each iteration's |R|, |R|/sigma and step.

> **The extended-precision M = 5 walk: rule fixed before it runs** (coordinator, 2026-11-23 19:30 UTC)
>
> **Code:** `feat/inner-mp` a0441d8b.
> - `value_mp.value_v` solves r₃ = r₅ = 0 for (B₃, C₃, B₅, C₅) at 34 and 42 digits, with step halving for M > 3.
> - `zero_mp.py A WF - OUT --M=5 --v0=...` runs Newton in (A, ω/ω∞) on R₁, by central differences, 5 values per iteration.
> - **Validation:** at the certified M = 5 fundamental zero, `value_v` converges to |r₃|, |r₅| < 3×10⁻³³ with B₃..C₅ inside Theorem A(5)'s box (Mac, 2293 s). At the first excited zero it converges from macm3's float64 stall: |r₃| 1.9×10⁻²⁸, max|Y| 1.16 (comment 7111397278).
>
> **Runs:**
> 1. **Control (dh370, 5 processes):** the walk from the fundamental's M = 3 zero, `2.726475885672135 1.0156030949093042` with v₀ = (B₃, C₃, 0, 0) = (0.1444194785, 0.0110874259, 0, 0). **It passes** when it ends "located" within 10⁻¹⁰ of Theorem A(5)'s box centre (2.71857918921174, 0.999228403206568).
> 2. **x1 (macm3, 5 processes):** from x1's M = 3 (A, ω/ω∞) with v₀ = x1fm's solved v.
> 3. **x2 (macm3):** the same, once x2's start solve converges.
>
> **Reading for each excited zero.** It persists at M = 5 when all three hold:
> - (i) its walk ends "located" (`zero_mp`'s rule);
> - (ii) the located point also gives |R₁| < 10³ σ at r₁ 0.2 (`value_mp.py pointv --r1=0.2` with the walk's last v), so it does not depend on the radius;
> - (iii) its M = 3 → 5 shift is smaller than its M = 1 → 3 shift (0.140 for x1, 0.210 for x2).
>
> It fails when the walk diverges or stalls without being located, or the shift is larger. |F₅|/|F₃| is reported at each located zero (the fundamental's is about 0.06). A reading counts only if the control passes.

How the code applies it (`run_walk_mp.sh`, `walk_report.py`): "located" is `zero_mp.py`'s own rule (exit 0: the last |R| under 1e3 sigma_mp, or the next step under 1e-13 with |R| what that step removes); (ii) is `value_mp.py pointv` at the located walk's last (A, w/w_inf) and last v with `--r1=0.2`, then |R_1| against 1e3 sigma; (iii) is the Euclidean norm in (A, w/w_inf) from the box centre to the walk's last point (`walk_report.py shift`), against 0.14035 (x1) and 0.20993 (x2). The located point is the last row's (A, w/w_inf), the centre of the last iteration, not the point after its unapplied step. The control is the coordinator's, on dh370; I do not run it, and no reading of mine counts until it passes.

Commands, from `solver/inner_stokes` of the worktree `~/Source/choptuik-large-d-1080mp2` at a0441d8b (no tracked changes), venv `~/Source/venv-macm3-1058b`, nice 10, detached under `caffeinate -is`:
```
python3 zero_mp.py selftest ; python3 zero_mp.py selftest --mutate=sign        (the first lands, the second must fail)
python3 zero_mp.py 3.446218246366727 0.347606965217407 - m5/walk_x1.jsonl --M=5 --v0=<x1fm's solved v, full digits> --procs=5 --iters=8
python3 value_mp.py pointv <A> <WF> --M=5 --v=<last v> --r1=0.2          (only after a located end)
```
x1's undamped start on 176daf53 was stopped at 19:19 UTC after 63 CPU minutes with no result, by the order above. Its log is `explore_mp/logs/pointv_x1.log` (the command only).

Files: `run_walk_mp.sh`, `walk_report.py`, `walk_x1.jsonl` (one row per iteration), `logs/walk_x1.log`, `logs/walk_x1_table.md`, `logs/pointv_r0.2_x1.log`, `exits_walk.txt`, `memlog_walk.log`.

**x1's walk, iteration 0 and the stop (2026-11-23).** Started 19:20:58 UTC. Row 0 landed at 23:47:09 UTC (`walk_x1.jsonl`, `logs/walk_x1_table.md`): |R_1| 3.540e5, sigma 5.17e-18, |R_1|/sigma 6.85e22, valued 5 of 5, orientation -1, step (dA, dw) = (-0.09815, -0.09679), norm 0.1378; the five points took 3.12, 3.80, 2.85, 4.44 and 3.58 h (17.8 CPU-h in all). By the coordinator's order ("report it and stop it there") the walk was then stopped with TERM at 23:47 UTC (`zero_mp` exit 143, no `pointv`, line in `exits_walk.txt`; `wait_row_stop` in the scratchpad did it). That is not a reading: the walk did not end, diverge or stall, and iteration 1 was not run.

## Results

Run: 2026-11-23 17:34:10 to 2026-11-23 17:35:09 UTC under `caffeinate -is` (59 s wall; the control's walk wall 48 s); the machine was awake throughout. The sampler wrote 1 line (the run is shorter than its 60 s interval): load 1.18, 14.5 GB free or inactive at the start; the peak resident memory of the solves was not recorded. No Traceback in any log. `logs/report.md` is the driver's first report, `logs/report_final.md` the same with the start-solve table.

- **Control, xi1 0.2: PASS.** Zero (2.718579192, 0.999228404), stored (2.718579189, 0.999228404), difference (+3.06e-09, +2.30e-10)  [r_1 -6.32e-03+1.14e-04i, |r_3| 1.1e-10, |r_5| 5.2e-10, 7 solves]. #1026's control: 3.1e-9 and 3.2e-10 from the stored zero. The gate's mutation (`--mutate=shift`) exits 1 as it must.
- **Control, xi1 0.25 (not a gate): the start solve fails**, |r_3| 8.3e3, the value #1026 had there, so the route is not validated at 0.25.
- **x1 and x2: the start solve does not converge at xi1 0.2 or 0.25, so no walk starts** (each walk's first solve, at the M = 3 zero with its M = 3 harmonics, level 3 stays at |r_3| from 1.9e5 to 1.0e6). Both FAIL by the rule.

| zero | xi1 | converged (A, w/w_inf) | \|r1\| | \|r3\| | \|r5\| | solves | Newton step | M3 -> 5 shift (dA, dw), norm | \|F5\|/\|F3\| |
|---|---|---|---|---|---|---|---|---|---|
| x1 | 0.2 | not converged | | | | | | | |
| x1 | 0.25 | not converged | | | | | | | |
| x2 | 0.2 | not converged | | | | | | | |
| x2 | 0.25 | not converged | | | | | | | |

Start solve of each walk (A, w/w_inf and the harmonics at the M = 3 zero; F_nu/F_1 from the solve; the walk goes on only when |r_3|, |r_5| are under 1e-6)

| walk | xi1 | \|r1\| | \|r3\| | \|r5\| | \|F3\| | \|F5\| | \|F5\|/\|F3\| | walk |
|---|---|---|---|---|---|---|---|---|
| control | 0.2 | 1.21e+02 | 2.7e-08 | 3.8e-10 | 0.0539 | 0.0030 | 0.0556 | converged, 7 solves |
| control | 0.25 | 4.53e+07 | 8.3e+03 | 1.2e-10 | 0.0520 | 0.0028 | 0.0548 | start solve not converged |
| x1 | 0.2 | 7.88e+07 | 2.1e+05 | 1.9e-06 | 0.2525 | 0.0839 | 0.3321 | start solve not converged |
| x1 | 0.25 | 6.66e+06 | 1.9e+05 | 1.0e-05 | 0.2553 | 0.0851 | 0.3333 | start solve not converged |
| x2 | 0.2 | 1.81e+06 | 3.3e+05 | 2.4e+03 | 0.3290 | 0.1775 | 0.5395 | start solve not converged |
| x2 | 0.25 | 4.03e+07 | 1.0e+06 | 1.2e+05 | 0.3263 | 0.2114 | 0.6479 | start solve not converged |

x1: M = 3 zero (3.446218246, 0.347606965); M = 1 partner (+1) (3.307235, 0.367124) located at xi1 0.2, M1 -> 3 shift (+0.13898, -0.01952), distance 0.14035; bar 0.14035
    VERDICT x1: FAILS (xi1 0.2: no converged walk (the start solve did not converge: |r_3| 2.1e+05 |r_5| 1.9e-06 not under 1e-06); xi1 0.25: no converged walk (the start solve did not converge: |r_3| 1.9e+05 |r_5| 1.0e-05 not under 1e-06))
x2: M = 3 zero (3.526473057, 0.211497981); M = 1 partner (+1) (3.674531, 0.360326) located at xi1 0.2, 0.25, M1 -> 3 shift (-0.14806, -0.14883), distance 0.20993; bar 0.20993
    VERDICT x2: FAILS (xi1 0.2: no converged walk (the start solve did not converge: |r_3| 3.3e+05 |r_5| 2.4e+03 not under 1e-06); xi1 0.25: no converged walk (the start solve did not converge: |r_3| 1.0e+06 |r_5| 1.2e+05 not under 1e-06))

