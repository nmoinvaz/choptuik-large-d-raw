# I141-mac: why the D = 30 background does not converge at M = 64, probe logs and the M = 64 setups

Machine: mac (Apple M5, 10 cores, 32 GB, macOS 27.0.1), shared with another mode-count session.
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/141
Code: branch wip/i141 of the code repository, commit 71b0e79 (worktree from main 87f2fb0). The files are
hp/modecount_common.py and hp/modecount_probe.py.
Versions: Python 3.14.7, numpy 2.5.4, mpmath 1.3.0; hpkernel 0.1.0 (isa neon, the build of 2026-11-08 16:24 PST, which
has no M 40). hp/modecount_cx comes from the main checkout's build of 2026-11-08 16:26 PST, put on PYTHONPATH
(/Users/nathan/Source/choptuik-large-d/hp/modecount_cx/build). The kernel's numerics are unchanged since both builds,
because main only added M 40 to the size lists after them.

All runs are from the worktree root with /Users/nathan/venv-314/bin/python, nice 10, caffeinate -i for the long ones,
1 thread each and at most 2 processes. Inputs from this repository were extracted with `git show origin/main:<path>`
(inputs/SOURCES.txt). The diagnostic scripts that are not in the code repository are in scripts/.

## The cause

The residual is in block 0, the centre series minus node 0, and it is a divergent series. Every other block starts at
1e-16, and the horizon block at 1.6e-11, the same as the M 32 to 48 resample. The series takes one d/dtau per order, so
its radius of convergence in x falls as M rises. At the first node x = 0.3 it diverges from M = 64 on, so |F| is the
truncated sum. It grows with kc: 1.1e4 at kc 300, 3.4e5 at 414 and 7.5e7 at 600 (probe/D30_from_M48_M64_kc300.log,
probe/D30_from_M48.log, probe/D30_from_M48_M64_kc600.log).

| D 30, no cut, at x = 0.3 | radius | ratio of terms per order | initial \|F\| on the state's nodes |
|---|---|---|---|
| M 32 (own state) | 0.435 | 0.690 | 3.3e-12 |
| M 48 (converged, October) | 0.324 | 0.927 | 9.0e-18 |
| M 64 from M 48 / from M 32 | 0.278 / 0.276 | 1.080 / 1.086 | 3.4e5 / 2.1e5 |
| M 80 from M 48 / from M 32 | 0.225 / 0.225 | 1.334 / 1.333 | 1.7e43 / 7.4e42 |

## The fix

modecount_common.fit_nodes acts on a resampled layout. It adds a node at half the first node while the centre series'
truncation estimate (series_tail) exceeds 1e-15. It raises ks by 1.5 while the horizon series' estimate does and the
series converges. setup refuses any layout whose series do not converge to 1e-15. Every layout counted so far passes
unchanged (probe/gate_states.log). The closest is D 30, M 48 without the cut, at 4.8e-16.

A first version added a node at 0.85 for the horizon (commit 1067b39; files *_outer085* and *_outer_rule*). At D 61,
M 64 that node left det M nearly singular: pivots 1e-23 to 1.8e3, hpkernel's and modecount_cx's ln|det| 2.2 apart,
and no sign change across lambda_phys. The same state with the node removed gives pivots 2.6e-14 to 4.9e6, ln|det|
4e-8 apart, and the sign change (probe/det_D61_M64_kf23_droplast.log). So the horizon side now raises ks.

## Results

| setup at M 64, fmax 1e-15 | layout | \|F\| start | \|F\| end | Delta | wall |
|---|---|---|---|---|---|
| D 30, no cut, from hp/data/modecount_state_D30.0688_M48.npz | nodes 0.15, 0.3 ... 0.7; ks 100 | 1.6e-11 | 2.5e-26 | 1.9642678762596676292 | 821 s |
| D 61, kf 23, from inputs/D61.0264_M48_kf23.npz | nodes 0.3 ... 0.7; ks 191 | 1.0e-6 | 8.5e-21 | 1.8071984300027739188 | 1595 s |
| D 61, kf 23, first rule (superseded) | nodes 0.3 ... 0.7, 0.85; ks 127 | 1.3e-11 | 4.4e-28 | 1.8071984300028238656 | 408 s |

At D 61 the 1.0e-6 start on the state's nodes is the horizon block. It is the 1.3e-11 mismatch at 0.85, grown by the
mass mode by (0.85/0.7)^58 = 8e4 on the way in to 0.7.

Delta against M (probe/delta_D61.txt and the logs):

| D 30, no cut | Delta | from M 32 |
|---|---|---|
| M 32 | 1.9642678762596676204 | 0 |
| M 48, nodes 0.3 ... (October; the count with the extra pair) | 1.9642678762610813887 | +1.41e-12 |
| M 48, node 0.15 added (scripts/m48_inner.py, \|F\| 2.4e-26) | 1.9642678762596676281 | +7.7e-18 |
| M 64, node 0.15 added (setup) | 1.9642678762596676292 | +8.7e-18 |

| D 61, kf 23 | Delta | from M 32 |
|---|---|---|
| M 32 (seed) | 1.8071984300028414779 | 0 |
| M 48 | 1.8071984300028344913 | -7.0e-15 |
| M 64, node 0.85 (\|F\| 4.4e-28) | 1.8071984300028238656 | -1.8e-14 |
| M 64, ks 191 (\|F\| 8.5e-21) | 1.8071984300027739188 | -6.8e-14 |

Determinant checks, det M at real lambda on both sides of lambda_phys (probe/det_*.log):

| state | pivots | ln\|det\| hpkernel vs cx | sign change |
|---|---|---|---|
| D 30, M 64, node 0.15 | 1.4e-7 ... 161 | equal | yes (2.06 / 2.10) |
| D 61, M 48 kf 23 (control) | 5.7e-14 ... 7.5e6 | 2e-6 apart | yes (2.03 / 2.06) |
| D 61, M 64 kf 23, node 0.85 | 1e-23 ... 1.8e3 | 2.2 apart | no |
| the same with node 0.85 removed | 2.6e-14 ... 4.9e6 | 4e-8 apart | yes |
| D 61, M 64 kf 23, ks 191 (final) | 1.9e-14 ... 4.9e6 | 1.4e-5 and 6.0e-5 apart | yes (2.03 / 2.06) |

## Files

| file | what | exit |
|---|---|---|
| probe/control_expect.log | `hp/modecount_probe.py hp/data/states/up6_D30.0688.npz --M=48 --expect=48:1.632e-11` (planted control) | 0 |
| probe/control_expect_mutated.log | the same with `--expect=48:1.632e-9` (must fail) | 1 |
| probe/selftest.log, .json | `hp/modecount_probe.py --selftest` (5/5) | 0 |
| probe/selftest_mutate_nofit.log | `hp/modecount_probe.py --selftest --mutate=nofit` (3/5, must fail) | 1 |
| probe/D30_from_M48.log, .json | `hp/modecount_probe.py hp/data/modecount_state_D30.0688_M48.npz --M=48,64,80` | 0 |
| probe/D30_from_M32.log, .json | `hp/modecount_probe.py hp/data/states/up6_D30.0688.npz --M=32,48,64,80` | 0 |
| probe/D30_from_M48_M64_kc300.log, _kc600.log | the M 48 probe at `--M=64 --kc=300` and `--kc=600` (code 5452132) | 0 |
| probe/setup_D30_M64_nofit.log, .json | `... modecount_state_D30.0688_M48.npz --M=64 --setup --nofit` (setup must refuse) | 1 |
| probe/setup_D30_M64.log, .json | `... modecount_state_D30.0688_M48.npz --M=64 --setup` (code 1067b39; the same layout now) | 0 |
| probe/setup_D61_M64_kf23.log, .json; D61_kf23_from_M48.json | `... inputs/D61.0264_M48_kf23.npz --M=48,64 --kf=23 --setup` | 0 |
| probe/*_outer085*, D61_kf23_from_M48_outer_rule.* | the same under the first rule (commit 1067b39), superseded | 0 |
| probe/gate_states.log | scripts/gate_states.py: both truncations of every counted state at its own M | 0 |
| probe/det_smoke_*.log | scripts/det_smoke.py STATE M kf 2.03,2.06 (or 2.06,2.10 at D 30), after setup | 0 |
| probe/det_D61_M64_kf23_droplast.log | scripts/det_layout.py on the node-0.85 state with the node removed | 0 |
| probe/det_D61_M48_kf23_addouter.log | scripts/det_layout.py add_outer at M 48, stopped in Newton (steps damped to 0.002) | killed |
| probe/control_D30_M48_inner015.log | scripts/m48_inner.py: M 32 to 48 at D 30, no cut, node 0.15 added, re-converged | 0 |
| probe/statediff_october_vs_I68B.log | scripts/statediff.py: October's M 48 state against #68's re-converged control B | 0 |
| probe/delta_D61.txt | Delta at D 61 by M and layout | 0 |
| states/modecount_state_D30.0688_M64.npz | setup's D 30 M 64 state (\|F\| 2.5e-26, nodes 0.15 ... 0.7) | |
| states/modecount_state_D61.0264_M64_kf23.npz | setup's D 61 M 64 kf 23 state (\|F\| 8.5e-21, ks 191) | |
| states/modecount_state_D61.0264_M64_kf23_outer085.npz | first rule, node 0.85 (\|F\| 4.4e-28; det M nearly singular) | |
| states/modecount_state_D30.0688_M48_inner015.npz | D 30 M 48 no cut, node 0.15 (\|F\| 2.4e-26) | |

setup saves its state in hp/data/modecount_state_D<D>_M<M>[_kf<kf>].npz. The two setup states were moved here from the
worktree's hp/data; copy one back there for a count to reuse it.
