# I1075-rpi5: #1025 on the rpi5: multidouble's Python package, a control against the Linux k_c 79 rows, then the k_c 79 point at D 20

Machine: `rpi5-ubuntu` (Raspberry Pi 5, 4 x Cortex-A76, 8 GB RAM, aarch64). Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1075 (task of
#1025). Coordinator t5 (hc, 2026-11-22). Written before the runs, 2026-11-22 21:25 UTC by the clock. Every run is a systemd user unit at nice 10.

## Order

0. **Setup.** Worktree `~/Source/choptuik-large-d-1075` at 505d8399 (detached; its `solver/matter` is the #1025 code). New venv `~/Source/venv-1025`
   (the uv-managed Python 3.14.10 at `~/.local/bin/python3.14`, numpy, scipy) and multidouble's Python package from the commit the issue names,
   `pip install "multidouble @ git+https://github.com/nmoinvaz/multidouble@8c4360ac0be804d081faeea524e5c1c6e2fffaaa#subdirectory=python"`
   (release 5.1.0; main's `hp/pyproject.toml` names it, 505d8399's names 482c6835, release 4.6.0 and 4.8.2: the issue's command is followed).
   Check that `multidouble` (with `dd_logdet`) and `dss_ell`, `ell_ddm`, `ell_refine`, `ell_delta` of `solver/matter` import. Stop and report if the build fails.
1. **Control.** `d18_hybsign.py` (blob e089207a, unmodified) on dh370's k_c 79 D 19.125 state and record (`I1025-dh370/kc79_d19125/`, raw c58e5052;
   blobs 3ff3fcb5 and 15ac964f), lambda 1.50, one process. Report the relative difference of ln|det| from dh370's -2537.823195774449 (bar 1e-9),
   with dh170's `control_check_k79.py` (blob 484801fd; the same control, a nine-case selftest and a `--mutate`). Pass: rpi5 is a Linux build like the
   others (dh170 1.1e-15, dh610 0.0 against dh370; winb's Windows build differs by 1.9e-6). Fail: report the offset; rpi5's scans are read only on its own
   regrids, as winb's.
2. **Regrid (when win2 pushes its k_c 71 D 20 state).** `I1025-win2/kc71_leap/states/sol_l1kc71Lw1025b_D20.000000.npy` and its line in `l1kc71Lw1025b.jsonl`
   (expected about 23:00 UTC). win2's `kc71_syscheck.py` (4cd86cd4) on it, with its two controls; then `ell_refine.py` to k_c 79 as dh370's D 19.5 regrid
   (`../I1025-dh370/kc79_d195/README.md`), lambda_0 from `ell_delta.lam0_at(20, *ell_delta.lam0_table())`, 3 threads; accepted only by
   `kc79_syscheck_1025.py` (29dce7ea) and its two controls (`--mutate=F`, `--mutate=steps`, both must exit 1).
3. **Scan.** The accepted state, lambda 1.22 to 1.32 at 0.01 (11 values) plus a repeat of 1.27 (on another process than the first), 3 processes of 1 thread,
   `d18_hybsign.py` (e089207a), read with `read_lower.py` (89309d3c) after its selftest and mutations (shift, round2; both must exit 1). The line through
   k_c 79's D 19.25 (1.469975) and D 19.5 (1.397565) has slope -0.2896 per unit D and reaches about 1.253 at D 20 (the issue: 1.25 to 1.26; information, not a
   pass rule). Roots are identified by position, not sign orientation. Report every robust change with its det-linear estimate and range, the edge signs and any
   ln|det| minimum without a change; the first round's per-point time.

## Acceptance (fixed before the runs)

- Step 0: every import above succeeds.
- Step 1: the control reported against its bar (1e-9 relative in ln|det|, equal hybrid sign, noise-robust, `the record system` printed).
- Step 2: win2's source check accepts the state and record and both its controls exit 1; `kc79_syscheck_1025.py` accepts the regrid (|F| at most 1e-9,
  `freeze_from` gives the record's steps, |F| within 1%) and both its controls exit 1. A regrid that exits non-zero, or hits its cap, is a stop.
- Step 3: `read_lower.py` selftest exit 0 and both mutations exit 1; each scan process prints `the record system`; the repeat is bit for bit; every
  robust change is reported with its det-linear estimate and range.

## Inputs (raw origin/main of the order's day; `run_control.sh` refuses any other blob)

| item | raw path | blob |
|---|---|---|
| k_c 79 D 19.125 state (dh370) | `I1025-dh370/kc79_d19125/sol_l1kc79dh370_D19.1250.npy` | 3ff3fcb5 |
| its record | `I1025-dh370/kc79_d19125/l1kc79dh370.jsonl` | 15ac964f |
| dh370's scan rows (the reference, lambda 1.50 twice, bit-identical) | `I1025-dh370/kc79_d19125/scan/scan_D19.125_1025.jsonl` | read from raw |
| scanner | `I1025-mac/d18/d18_hybsign.py` | e089207a |
| control check (dh170's) | `I1025-dh170/kc79_d19125low/in/control_check_k79.py` | 484801fd |
| reader | `I1025-dh170/lower_root/read_lower.py` | 89309d3c |

Code: `solver/matter` at 505d8399: `ell_refine.py`, `dss_ell.py`, `ell_ddm.py`, `ell_dd.py`, `ddnp.py` have the blobs of dh370's 48c36355
(631e5801, 5d28c19e, 86578fee, 7e58fcbc, 9b1fb195); `ell_delta.py` differs (059180e6 here, fde699f5 at 48c36355), checked below.

## Cost, written before the runs

dh370's control point took 3813 s on one thread (i7-8700), dh170's 793 to 810 s on 4 threads (peak RSS 1.69 GiB). The regrid took 2240 s on 6 threads there (peak RSS
1.2 GB); on 3 Cortex-A76 threads expect several times that. Three scan processes of about 1.7 GB each fit in 8 GB; the swap is already full of other jobs.

## Status

**Step 0, setup: passes (with one omission fixed).** 21:23 to 21:26 UTC. Worktree `choptuik-large-d-1075` at 505d8399, clean. Venv `~/Source/venv-1025`: Python 3.14.10 (uv-managed),
numpy 2.5.5, scipy 1.18.1, mpmath 1.4.1, multidouble 5.1.0 built from 8c4360ac on this machine (aarch64; `multidouble.isa()` = `neon`; the build took 2 min). Imports
(`imports.txt`): `multidouble` with `dd_logdet`, `dss_ell`, `ell_ddm`, `ell_delta`, and `ell_refine.py -h` all exit 0; `ell_delta.lam0_at` reproduces dh370's lambda_0 (19.0 2.1156378446,
19.125 2.1150338480, 19.5 2.1132623525) and gives 2.1110019498 at D 20. The first start of the control (21:26:18, `control/attempt1_stopped_no_mpmath/`) stopped after 4 s:
`ell_ddm.DDEll` imports `mpmath` when it is built, the new venv had none, and the step-0 imports did not build it. mpmath was installed, added to the step-0 check, and the control
restarted at 21:28:09. (That first start printed `the record system` with |F| 2.9292e-10 before it stopped.)

**Step 1, control: FAIL against the bar (relative difference 1.691e-8, bar 1e-9); sign, noise test and record system agree.** `d18_hybsign.py` (e089207a) on dh370's D 19.125 state
(3ff3fcb5) and record (15ac964f), lambda 1.50, one process of 3 threads, 21:28:09 to 22:12:47 UTC (2678 s wall, 2666 s in the point, user 5940 s, peak RSS 1.83 GB). `control_check_k79.py`
(484801fd; selftest exit 0, `--mutate` exit 1) reads (`control/control_check.txt`):

| | rpi5 | dh370 (x86_64 Linux, 1 thread) | difference |
|---|---|---|---|
| record system | printed, \|F\| 2.9292154743e-10, 2949 steps | \|F\| 2.9254572718e-10 (dh170: 2.9245852e-10), 2949 | \|F\| +1.3e-3 relative (within the 1% rule) |
| hybrid sign, noise test on blocks 0-11 | -1, robust | -1, robust | equal |
| ln\|det\| | -2537.823238700405 | -2537.823195774449 | -4.29e-5, relative 1.691e-8 |
| float64 sign, ln\|det\| (not used) | +1, -2536.5936641067 | -1, -2534.506173253555 | sign differs, 2.09 apart |

So rpi5 is not a bit-twin of the Linux builds (dh170 differs from dh370 by 1.1e-15, dh610 by 0.0; winb's Windows build by 1.9e-6): this aarch64 build (NEON, OpenBLAS aarch64 kernels)
is 1.7e-8 away. The plain float64 determinant's sign (ill-conditioned, not used) differs too. By the order, rpi5's scans are read only on its own regrids, as winb's: the D 20 state
is regridded here, so nothing in step 2 or 3 depends on the other machines' absolute ln|det|. The time of this point at 3 threads alone is 2666 s (dh370: 2055 to 3813 s on 1 thread of an i7-8700).
Not done (not asked): a 1-thread repeat on this machine (would say whether the offset depends on the thread count here) and the ln|det| response to the 1e-15 noise of blocks 0-11.
