# I1110-dh170: a chord state's root against R2's LM root at k_c 127, D 23.0

Machine dh170 (i7-7700, 4 physical cores, 31 GB; Linux). Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1110 (coordinator t5; depends on #1101, Task B closing, comment 7231427295; R0-R2's order, comment 7231148229). Written 2026-11-28 01:19 UTC by the clock, before any run of this task (bars, commands, resources, pins and predictions first; t5's order of 28 Nov 01:15 UTC is quoted at the end).

## Question
At k_c 55, D 16 two converged states of one system can have roots at least 3.4e-3 apart: "chord-all" (U40 re-solved by chord steps on K35's exact 5124-step map) differs from the LM state K35 by 1.95e-10 at equal |F| (1.889e-10), yet its root was bracketed in (2.24160, 2.24560) against K35's 2.24897; the change comes from the 6.8e-12 strong-band part of the difference (p, m, psi at the inner nodes, harmonics 5-31). So the kappa order could not be read there. At k_c 127, D 23.0 the order p = 2.39 was read from three roots (R0 0.045968, R1 0.09500769, R2 0.117824909) and has not been tested against this scatter. This task runs the same control at k_c 127: R0's state (kappa 0.7, 4179 steps) re-solved by chord steps on R2's own step map (kappa 0.35, 8351 steps), keeping its weak and null coordinates, and its root against R2's LM root 0.117824909.

## Bars (#1110's, copied; each can fail)
1. **The chord state is on R2's map:** its `.map.json` has 8351 steps (R2's record's count, exactly) and |F| <= 5e-10 (R2: 3.12e-10). If the count differs, stop and report; the coordinator then adds a map taken from R2's own steps.
2. **Control that must fail:** the same `chord` with `kappa=0.34` must give a count other than 8351. If it gives 8351, the count cannot tell maps apart, and bar 1 means nothing.
3. **Report** delta = root(chord) - 0.117824909 and the state difference |z_chord - z_R2| by band.
   - |delta| <= 2e-3 (under 1/10 of R1 - R2 = 0.0229): the scatter does not hide R0-R2's order, and #1104 may use it.
   - |delta| >= 7e-3 (about 1/3 of it): the order from R0-R2 is not readable either; #1104's kappa step waits for the double-double and ladder-free roots of #1111.
   - Between: mixed; reported as such.
Also from t5's order: jac exits 3 (not the record system) -> stop and report; if (0.10, 0.13) does not bracket, widen once to (0.05, 0.16) and say so; the R3 scan (#1101) keeps priority over this task's root.

**Reading rule (mine, stated before the run).** The root is read from `i1101_weakdir.py root` ending with status `tol` (tol 1e-6), both bracket ends robust (dln <= 0.1) with opposite hybrid signs; root = `lam_lin` of its final record; delta = root - 0.117824909 (R2's det-linear root, `I1101-dh170/secant_r2w.jsonl`). The verdict is read on the final bracket: delta's range [a - 0.117824909, b - 0.117824909] entirely inside [-2e-3, 2e-3]: "<= 2e-3"; entirely at |delta| >= 7e-3: ">= 7e-3"; any other: "between, mixed". If the root step stops at its cap (timeout) before status `tol`, I report the robust bracket of the evaluations so far and read its range by the same rule, saying that no root was formed; a range that straddles a bar reads "between (not decided)". The estimator values are at the width of the bracket, not enclosures. The state difference by band is `coords` of `i1101_weakdir.py` on R0's SVD (the bands are R0's: null s/s_max < 1e-11, weak [1e-11, 1e-5), strong >= 1e-5), base R2's state, so it is the part of z_chord - z_R2 in each of R0's bands.

## Code and inputs (pins by blob, `git hash-object --no-filters`)
| what | where | blob |
|---|---|---|
| code | worktree `~/Source/choptuik-1110` at `origin/wip/i1101-weakdir` db7f9c60, `solver/matter/i1101_weakdir.py` (`jac`, `svd`, `chord`, `root`, `coords`) | 8709abbd |
| the scanner library the `root` step imports | `solver/matter/d18_secant.py` of the same worktree (`D18_DIR`; its default `~/Source/choptuik-kmm` does not exist here); `RealEval` takes `b12` ddm or fast (no Rust in this version) | eb1396ad |
| venv | `~/Source/choptuik-large-d-1058b/.venv` (Python 3.14.10, numpy 2.5.4, scipy 1.18.1; the system python3 has no numpy) | |
| R0's state, kappa 0.7, 4179 steps | `in/sol_l1kc127k070w2_D23.0000.npy` (copy of `I1101-dh170/in/`) | 90d3e655 |
| R0's record (\|F\| 3.1949e-10, kappa 0.7, u0 0.04, Ks 30) | `in/l1kc127k070w2.jsonl` | d1a3a641 |
| R2's state (LM, kappa 0.35, 8351 steps; for the state difference only) | `in/R2_sol_l1kc127k035w2_D23.0000.npy` | 25ba3a91 |

## Commands (cwd `~/Source/choptuik-1110/solver/matter`, venv python; each step its own `systemd-run --user` unit under `systemd-inhibit`, `nice -n 10`, `OPENBLAS_NUM_THREADS=OMP_NUM_THREADS=MKL_NUM_THREADS=RAYON_NUM_THREADS=2`, under `timeout`; output into this folder; `R0REC` = `in/l1kc127k070w2.jsonl`, `R0STATE` = `in/sol_l1kc127k070w2_D23.0000.npy`)
| unit | timeout | command |
|---|---|---|
| `i1110-jac` | 7200 s | `i1101_weakdir.py jac R0REC R0STATE 23.0 jac_r0.npz --pin=90d3e655,d1a3a641` (exit 3: not the record system: stop and report) |
| `i1110-svd` | 3600 s | `i1101_weakdir.py svd jac_r0.npz svd_r0.npz` |
| `i1110-chord` | 3600 s | `i1101_weakdir.py chord svd_r0.npz R0REC R0STATE 23.0 kappa=0.35 sol_chord035_D23.0000.npy` (bar 1) |
| `i1110-ctl` | 3600 s | `i1101_weakdir.py chord svd_r0.npz R0REC R0STATE 23.0 kappa=0.34 sol_chord034_D23.0000.npy` (bar 2, the control) |
| `i1110-coords` | 3600 s | `i1101_weakdir.py coords svd_r0.npz in/R2_sol_l1kc127k035w2_D23.0000.npy chord035=sol_chord035_D23.0000.npy` (bar 3's state difference; not in t5's list) |
| `i1110-root` | 14400 s | `i1101_weakdir.py root sol_chord035_D23.0000.npy 0.10 0.13 root_chord035.jsonl --tol=1e-6 --b12=fast` with `D18_DIR` the worktree's `solver/matter`; widened once to (0.05, 0.16), file `root_chord035_wide.jsonl`, if (0.10, 0.13) does not bracket |
`jac_r0.npz` (0.6 GB) and `svd_r0.npz` (2 GB) stay on the machine; everything else is pushed. Steps, exits and times are in `steps.txt` (tag `[1110]`).

## Resources
t5: 2 threads of the 5 free, beside the #1104 re-solve (3 threads, nice 10) and the waiting R3 driver (unit `i1101r3`). **The R3 scan keeps priority** when mm5's R3 lands: if both would run, R3's scan takes its 4 threads and this task's root waits (before it starts: it does not start while R3's scan processes run or its priority file `/tmp/dh170_prio_r3` exists; once running, it is stopped with SIGSTOP while R3's scan processes run and continued after; a stopped process keeps its memory). The root step counts as a scanner process of the memory rule of #1101/#1104 (`scan_admit.sh`: at most 4 scanner processes while `ell_refine.py` runs, 5 otherwise; one process holds 4.7 to 4.9 GB): its command line carries the marker argument `--note="d18_secant.py scan root1110"`, which the admission count matches. The steps before the root (J 0.6 GB, SVD 2 GB) are not counted.

## Predictions (mine, registered before the run; information, not pass rules)
| item | prediction |
|---|---|
| jac reproduces the record system (exit 0) | 90% |
| jac wall (2 threads, beside the re-solve) | 20 to 90 min: 60%; over its cap of 7200 s: 7% |
| bar 1: the kappa=0.35 chord state has exactly 8351 steps | 95% (the Test K line `kappa_mm 0.35: 8351 steps` is the same `freeze_from(z, 0.35)`) |
| bar 1: \|F\| <= 5e-10 | 60% (chord on the strong band only, R0's weak coordinates kept; K35's chord-all reached 1.889e-10) |
| bar 2: the kappa=0.34 control gives a count other than 8351 | 97% |
| (0.10, 0.13) brackets the chord state's root | 40%; widening needed: 55%; no bracket in (0.05, 0.16) either: 5% |
| delta: \|delta\| <= 2e-3: 25%; between: 20%; >= 7e-3: 55% | the chord state keeps R0's weak and null coordinates, which the kappa change moves in the LM re-solves, and the k_c 55 control moved the root by 3.4e-3 to 7.4e-3 for a 1.95e-10 state difference; the R0 to R2 difference is far larger |
| the root step reaches status `tol` within its cap of 14400 s | 25%: an evaluation took 2351 s (R2, Rust block 12, alone) and 3300 to 4800 s beside other jobs; the `fast` block 12 may be slower, and 10 to 20 evaluations are needed for tol 1e-6 |

## Status
- 2026-11-28 01:19 UTC: README, bars, commands, reading rule, resources and predictions written before any run; inputs copied and blob-checked (90d3e655, d1a3a641, 25ba3a91); worktree `~/Source/choptuik-1110` at db7f9c60; imports of `i1101_weakdir`'s dependencies and `d18_secant` checked in the venv. The driver and the reader are written next, and pushed with their blobs before the first unit starts.

## Order, verbatim (t5, 28 Nov 01:15 UTC)

> t5 (01:15 UTC): a second task beside your #1101/#1104 waiters, issue #1110 (read its body; it is the record). Keep every waiter you have; this runs on 2 threads of the 5 free.
>
> 1. Worktree: git -C ~/Source/choptuik-large-d fetch origin wip/i1101-weakdir && git -C ~/Source/choptuik-large-d worktree add --detach ~/Source/choptuik-1110 origin/wip/i1101-weakdir (must be at db7f9c60). Venv: the one your #1101 runs use (choptuik-large-d-1058b/.venv). Work from ~/Source/choptuik-1110/solver/matter.
> 2. Raw folder I1110-dh170/ in a separate worktree of your raw clone, README first (first line "# I1110-dh170: a chord state's root against R2's LM root at k_c 127, D 23.0", machine, issue URL, the bars of #1110 copied, the commands). Push it before any run.
> 3. Inputs: copy I1101-dh170/in/sol_l1kc127k070w2_D23.0000.npy (blob 90d3e655) and l1kc127k070w2.jsonl (d1a3a641) into I1110-dh170/in/, blob-check them with git hash-object --no-filters.
> 4. Each step as its own systemd-run --user unit (names i1110-jac, i1110-svd, i1110-chord, i1110-ctl, i1110-root), nice -n 10, OPENBLAS_NUM_THREADS=2 OMP_NUM_THREADS=2 MKL_NUM_THREADS=2 RAYON_NUM_THREADS=2, each under timeout (jac 7200 s, svd 3600, chord 3600, ctl 3600, root 14400), output into I1110-dh170/:
>    python3 i1101_weakdir.py jac REC STATE 23.0 jac_r0.npz --pin=90d3e655,d1a3a641
>    python3 i1101_weakdir.py svd jac_r0.npz svd_r0.npz
>    python3 i1101_weakdir.py chord svd_r0.npz REC STATE 23.0 kappa=0.35 sol_chord035_D23.0000.npy
>    python3 i1101_weakdir.py chord svd_r0.npz REC STATE 23.0 kappa=0.34 sol_chord034_D23.0000.npy   (the control)
>    python3 i1101_weakdir.py root sol_chord035_D23.0000.npy 0.10 0.13 root_chord035.jsonl --tol=1e-6 --b12=fast
>    jac_r0.npz and svd_r0.npz (0.6 and 2 GB) stay on the machine; push everything else.
> 5. Stops: jac exits 3 (not the record system) -> stop and report. Bar 1: the kappa=0.35 chord state's .map.json must have exactly 8351 steps and |F| <= 5e-10; otherwise stop and report before the root. Bar 2: the kappa=0.34 control must give a count other than 8351; if it gives 8351, stop and report. If (0.10, 0.13) does not bracket, widen once to (0.05, 0.16) and say so.
> 6. Report: delta = root(chord) - 0.117824909 and the verdict against #1110's bars (<= 2e-3, >= 7e-3, between), steps, |F|, seconds. Post the table on #1110 and #1101 (numbers from a script or the files; times from date -u), push, then report to me with hc_t5.sh.
> Your R3 scan keeps priority when mm5's R3 lands: if both would run, the R3 scan takes its 4 threads and #1110's root waits.

### Issue #1110's body (the record; acceptance as copied in the bars above)

> **Question.** At k_c 55, D 16 two converged states of one system can have roots ≥ 3.4e-3 apart. "chord-all" was U40 re-solved by chord steps on K35's exact 5124-step map. It differs from the LM state K35 by 1.95e-10 at equal |F| (1.889e-10). Yet its root was bracketed in (2.24160, 2.24560), against K35's 2.24897. The change comes from the 6.8e-12 strong-band part of the difference: p, m and ψ at the inner nodes, harmonics 5–31. So the κ order could not be read there. At k_c 127, D 23.0 the order p = 2.39 was read from three roots, R0 0.045968, R1 0.09500769 and R2 0.117824909. It has not been tested against this kind of scatter. This task runs the same control at k_c 127.
>
> **Code.** `wip/i1101-weakdir` at db7f9c60 (`i1101_weakdir.py`: `jac`, `svd`, `chord`, `root`), venv-1025dd, from `solver/matter`. The block-12 choice is `--b12=fast` as in #1101's task B.
>
> **Estimate.** J by complex step at k_c 127: about 15 min; SVD a few minutes; chord steps under 10 min; the root 10–20 evaluations of 3–5 min. About 2 h on 2 threads. J (about 8350 unknowns) needs about 0.6 GB and the SVD about 2 GB.
