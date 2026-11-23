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

## Results

(none yet)
