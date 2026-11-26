# I1025-win2/prec_k103_cheap: the cheapest precision check of the hybrid determinant's sign beside the k_c 103 root at D 21.125

Machine win2 (Windows 11, 20 logical CPUs, 95.5 GB RAM; runner win2 claude-me2, Sonnet 5.5). Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1025. Written 2026-11-26 01:00 UTC, **before the first run of this folder**. It follows the capped run `../prec_kc111_d21125/` (all four jobs hit the 6 h cap with no lambda finished: the all-double-double matrix is the cost), whose README holds the full description of the script.

## Order (coordinator t5, hc, 26 Nov ~00:59 UTC), verbatim
"(2) #1025, the paused precision check, cheapest version: k_c 103 only (0.880, 0.885), d18_hybsign_prec.py with --noise=1e-12,1e-10 --alldd=0, 2 processes, cap 14 h each. Both BelowNormal; keep commit-charge alerts on."
(The same message orders a hp build, item (1), kept in `../hp_form_s_build/`. The earlier standing note of 25 Nov, "with the new matrix" of branch wip/ell1-speed, is not part of this order: `d18_hybsign_prec.py` on wip/ell1-speed (6010e37b) is the same blob a3a1368c and does not import `ell_fastm`, so no faster matrix is wired into it; this run uses the script as pinned.)

## What the script computes per lambda with these options (read: `inputs/d18_hybsign_prec.py`, blob a3a1368c)
`S.mode_matrix(z, lam)` in float64 (blocks 0-12, one `slogdet`: the float64 sign), `E.mode_matrix(z, lam, only=[12])` in double-double (block 12), the hybrid matrix and its `dd_logdet` (the hybrid sign and ln|det|); then, for each amplitude in `--noise` (1e-12 and 1e-10) and 2 seeds (100, 101), `dd_logdet(H + a * noise * mask * H, Hl)` with the noise on blocks 0-11 only. `--alldd=0` skips the all-double-double matrix, the expensive part. The noise amplitude 1e-15 (d18_hybsign.py's own test) is dropped by `--noise`. Reading per lambda: `state-limited` when 1e-12 or 1e-10 flips the hybrid sign, else `robust`.

**What the reduced check cannot show:** with `--alldd=0` the sign of float64 rounding in blocks 0-11 is not tested (no all-double-double sign, no 1e-15 noise), so `rounding-limited` cannot be read, and a `robust` reading means only "stable to relative noise up to 1e-10 on blocks 0-11" (the converged state's own error is |F| about 4.6e-10).

## Inputs (pinned by `git hash-object --no-filters`; `inputs/blobs.txt`; the driver refuses any other blob)
| item | blob |
|---|---|
| `inputs/d18_hybsign_prec.py` (wip/ell1-highD 18566122; the same blob on wip/ell1-speed 6010e37b) | a3a1368c |
| dh170's k_c 103 state at D 21.125, `inputs/kc103/sol_l1kc103dh170g_D21.1250.npy` (raw I1025-dh170/kc103_d21125) | ad9b1dc8 |
| its record `inputs/kc103/l1kc103dh170g.jsonl` (|F| 4.626407e-10, 3476 steps, constraint 1.146e-3, Delta 1.121570859155) | ac60dbfc |
| dh170's own hybrid rows (control c4), `inputs/kc103/dh170_merged_D21.125.jsonl` | 15feca49 |
| `prec_verdict.py` (the capped run's verdict script, unchanged) | d881adf0 |
Code: worktree `D:/choptuik-i1025k79` at 48c36355 (`dss_ell.py`, `ell_ddm.py`, `ell_dd.py`, `ddnp.py` equal 505d8399's, checked by the driver), python 3.14 with multidouble 5.1.0 (`venv-md510`), `P4_WT_MATTER` = that worktree's `solver/matter`. One thread per process (`OMP/OPENBLAS/MKL/RAYON_NUM_THREADS=1`).
dh170's rows at D 21.125 (k_c 103): lambda 0.880 hybrid +1 (ln -3288.588168), 0.885 hybrid -1 (ln -3290.549209; **his float64 sign there is +1, differs from the hybrid**), 0.895 -1; his root is 0.8844.

## Registered readings (fixed before the first run)
Points: **k_c 103 lambda 0.880 and 0.885**, one process each.
- **(N) numerical**: at least one of the two points reads `state-limited` (1e-12 or 1e-10 flips its hybrid sign): the sign beside the k_c 103 root is not determined by the converged state, so the root is not resolved at the 0.005 grid at this k_c (evidence for the numerical drift; the registered reading of the capped run, restricted to its state-limited half).
- **(S) stable to state noise**: both points `robust`: the signs survive relative noise up to 1e-10 on blocks 0-11. This does **not** decide numerical against real: float64 rounding in blocks 0-11 is untested, so `prec_verdict.py` prints `undecided` (2 of the 4 points beside the roots exist) and the all-double-double sign (`--alldd=1`) stays the open test.
- Control c4 (`prec_verdict.py`): the hybrid sign here equals dh170's at 0.880 and 0.885 (a difference = the control FAILS and there is no verdict) and the ln|det| agrees to 1e-3 (a larger difference with the sign equal is printed as information).
Expected time: dh170's hybrid points took 3,484 to 8,717 s at k_c 103 in a single process; this run adds 4 `dd_logdet` per lambda (a few tens of seconds), so **1 to 3 h per lambda**, longer under contention. The cap is 14 h (50,400 s) per job by the exact root pid (`crun`); a capped job is a stop and is reported.

## Commands (`run_prec_cheap.sh`, started through `kc71_leap/cim_start.ps1`, BelowNormal)
1. Pins (blobs above, worktree 48c36355, solver files equal 505d8399); selftests `d18_hybsign_prec.py --selftest` (exit 0) and `--selftest --mutate=class` (exit 1); `prec_verdict.py --selftest` (exit 0) and `--selftest --mutate` (exit 1).
2. Two jobs at once, `d18_hybsign_prec.py REC STATE 21.125 LAM OUT --noise=1e-12,1e-10 --alldd=0`, lambda 0.880 and 0.885.
3. After both: `prec_verdict.py` into `verdict.txt` and `summary_prec.txt`.

## Acceptance (fixed before the run)
Pins as above; the four selftest exits as written; each process prints "the record system" (|F| within 1% of the record, 3476 steps; else exit 3 and I report it); the control c4 passes; the verdict is the one `prec_verdict.py` prints, with each lambda's line and its time reported as it lands.

## Status
- 2026-11-26 01:00 UTC: folder, README (registered readings), inputs and driver written; the driver starts next.
- 2026-11-26 01:01 UTC: the driver started through `kc71_leap/cim_start.ps1` (BelowNormal): selftests 0 1 0 1, pins ok; root pids 55408 (lambda 0.880) and 54512 (lambda 0.885), workers (the real python children) 51592 and 63968; each printed the record system (|F| 4.6279976910e-10 against the record's 4.6264065251e-10, steps 3476 = 3476).
- 2026-11-26 01:07 UTC: **STOPPED by the coordinator's order** (hc ~01:06 UTC: "the quest comes first: stop the two precision-check processes now by exact pid (record it; they restart after the build), which should lift the headroom over your 38 GB gate ... Don't use NOGATE, and don't touch drivers or reboot."). After a command-line check: `taskkill /T /F` on the launcher's conhost 61104 (tree: cmd 39528, bash 58472, 64688), which left the driver's own bash tree standing (its parent was a dead pid), then `taskkill /T /F` on the driver 52884 (`run_prec_cheap.sh`; its tree 63332, 62884, 64352, 59052, the stubs 55408 and 54512, and the workers 51592 and 63968). 01:07:31 and 01:07:50 UTC. Each worker had used about 355 CPU seconds, no lambda finished, no record written (`prec_k103_lam*.jsonl` absent), no `prec.done`, no `prec_refused.txt`. The first logs are kept as `stopped_run1_prec_k103_lam*.log`. **No reading.** The commit headroom rose from 30.8 to 31.8 GB (these two jobs held 1.2 GB private). Restart after the build, when the coordinator orders it: the same `run_prec_cheap.sh` (it refuses only if a record or `prec.done` exists), through `cim_start.ps1`.
