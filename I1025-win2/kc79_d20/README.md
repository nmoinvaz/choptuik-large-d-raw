# I1025-win2/kc79_d20: win2's k_c 71 D 20 state regridded to k_c 79 and scanned at lambda 1.20 to 1.32

Written before the run, 2026-11-22 22:37 UTC (`date -u`). Machine win2 (desktop-pc, Windows 11, Core Ultra 7 265K, 20 threads, 95 GB), the win2 session (runner of `../kc71_leap/`). Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1025. Coordinator: t5.

## Order (t5's hc, about 22:55 UTC 22 Nov)

k_c 71 has come apart by D 19.5 (its root near the line is 1.3715 against k_c 79's 1.397565 and k_c 87's 1.399169), so k_c 71's D 20 roots decide nothing about lambda_1: **the k_c 71 scan at D 20 is not run** (its waiter was stopped by exact pid). Instead, when the leap's D 20 state lands and reproduces its record:
1. regrid it to k_c 79 with `ell_refine.py` as winb did (raw `I1025-win/kc79_d19`: the command, lambda_0 from `ell_delta.lam0_at(20)`, `--no-gamma`), accepted only by `kc79_syscheck_1025.py` and both controls, 8 threads, through the headless launcher;
2. scan the accepted k_c 79 state at lambda 1.20 to 1.32 at 0.01 (13 values) plus a repeat of 1.26, 6 processes of 1 thread, read with `read_lower.py` (raw `I1025-dh170/lower_root`, blob 89309d3c). k_c 79's line (1.5397, 1.5058, 1.4700, 1.4316, 1.3976 at D 19 to 19.5) puts lambda_1 near 1.25 to 1.26 (information).
Each step's verdict is reported to t5. The scans are read on win2's own regrid (Windows build). The leap goes on within its cap (leg 2, root 16420, cap 03:17:35 UTC 23 Nov); its states are pushed as they land.

## Inputs (pinned; raw origin/main, copied into `inputs/`, checked with `git hash-object --no-filters`)

| file | raw origin | blob |
|---|---|---|
| `kc79_syscheck_1025.py` | `I1025-win/kc79_d19/` | 29dce7ea |
| `read_lower.py` | `I1025-dh170/lower_root/` | 89309d3c |
| `d185_scan_read.py` (the change finder read_lower.py imports, xfkappa's) | `I1025-dh170/lower_root/` | 7c9d400f |
| `d18_hybsign.py` (xfkappa's scanner) | `I1025-mac/d18/` | e089207a |
| `kc71_syscheck.py` (the source acceptance) | `I1025-win2/kc71_leap/` | 4cd86cd4 |

Code: worktree `D:/choptuik-i1025k79` at 48c36355 (`dss_ell.py`, `ell_ddm.py`, `ell_dd.py`, `ddnp.py` equal 505d8399's, `ell_refine.py` 631e5801, `ell_delta.py` fde699f5; the driver checks all of it), venv-md510 (multidouble 5.1.0). The leap runs in another worktree (`D:/choptuik-i1025k71`) and is not touched.

## Step 1: the regrid (`regrid79_d20.sh`)

Waits for the leap's D 20 state (`../kc71_leap/states/sol_l1kc71Lw1025b_D20.000000.npy` and its `.4f` name, each at least 60 s old, equal) and its record line (`"D": 20.0`). **Source acceptance first:** `kc71_syscheck.py` (the record's |F| at most 1e-9, the saved state reproducing its record: `freeze_from` gives the record's step count and |F| within 1%) with its two built-in controls, and `--mutate=F` and `--mutate=steps` each exiting 1. A refusal stops the task with a report.

```
ell_refine.py l1kc71Lw1025b 71 l1kc79W20m1025 79 1 20 2.1110019498 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma
```

winb's command at D 19 (raw `I1025-win/kc79_d19/README.md`) with only D, the source tag, the output tag and lambda_0 changed (`ell_delta.lam0_at(20)` = 2.1110019498, error 3.8e-7; unused with `--no-gamma`). cwd `solver/matter` of the k_c 79 worktree, 8 BLAS threads, BelowNormal, cap 21600 s by the exact root pid (command-line check `ell_refine.py`; planted test of that cap logic in `../kc71_leap/`, `crun`). A regrid that does not converge (non-zero exit, cap, no state or record) stops with a report, no retry.

**Acceptance (fixed now):** `kc79_syscheck_1025.py REC STATE 20 WTM` exits 0 (the record's |F| at most 1e-9, the record is k_c 79 at D 20, the state reproduces its record: `freeze_from` gives the record's steps, |F| within 1%), its two controls on the same numbers are refused, and `--mutate=F` and `--mutate=steps` each exit 1. The accepted record (|F|, steps, constraint, Delta against the k_c 71 source) goes into `regrid_accepted.txt`, `summary_kc79.txt` and the post on #1025.

**Cost, from winb's D 19 regrid (laptop, 4 threads): 5595 s wall, cpu 9425 s (about 1.7 cores), peak private 2.48 GB, 2976 steps.** Estimate here: 1 to 1.6 h; the leap runs beside it (4 threads).

**Rehearsal before the run (nothing of the regrid itself):** the pre-steps on the D 19.5 state of the leap (`rehearsal_D19.5/`): pins ok, the source accepted by `kc71_syscheck.py` with both controls refused and `--mutate=F`, `--mutate=steps` exit 1; and `kc79_syscheck_1025.py` on winb's D 19 k_c 79 state with this build: ACCEPTED (|F| 2.8501e-10 against the record's 2.8482e-10, 2976 steps = the record's), both controls refused, both `--mutate` exit 1 (`rehearsal_D19.5/winb_d19_syscheck_on_win2.txt`).

## Step 2: the scan (`scan79_d20.sh`, starts itself when `regrid_accepted.txt` exists)

xfkappa's `d18_hybsign.py` (e089207a, unchanged) on the accepted k_c 79 state and its record line, the 1e-15 noise test (2 seeds) and the float64 sign; its first line is the record-system check (exit 3 if not). **Lambda 1.20 to 1.32 at 0.01 (13 values) plus a repeat of 1.26: 14 evaluations in six processes of one thread:**

| process | lambda, in this order |
|---|---|
| P1 | 1.26, 1.20, 1.21 |
| P2 | 1.26, 1.22, 1.23 |
| P3 | 1.24, 1.25 |
| P4 | 1.27, 1.28 |
| P5 | 1.29, 1.30 |
| P6 | 1.31, 1.32 |

BelowNormal, caps 28800 s by the exact root pids (command-line check `d18_hybsign.py`), `P4_WT_MATTER` the k_c 79 worktree. **The repeat gate** (`pair79.py`): the first records of P1 and P2 (both 1.26) must agree in hybrid sign, noise signs, float64 sign and ln|det| within 1e-6, else the six scans are killed by exact pid and the task stops (planted cases and `--break` in `selftest_pair79.txt`). **Reading:** `read_lower.py SCAN_DIR 1.20 1.32` as it is (its selftest and both `--mutate` controls are run first, `selftest_read_lower.txt`); roots are named by position, never by orientation, and printed as the reader prints them. The line's lambda_1 estimate near 1.25 to 1.26 is information, not a reading rule.

Estimate: a k_c 79 point at one thread is not measured here; at four threads winb's laptop took 1320 s a point at k_c 79 D 19, so about 1 to 2 h for the three evaluations of the longest process.

## Run

Both drivers start outside the terminal through `../kc71_leap/cim_start.ps1` (the headless form, `conhost.exe --headless cmd.exe /c`), BelowNormal: the regrid driver as soon as this README is pushed (it waits for the D 20 state), the scan driver at once too (it waits for `regrid_accepted.txt`). No script sends hc; verdicts are read from `summary_kc79.txt` and `exits_kc79.txt` and reported by hand.

## Result

Not yet run.
