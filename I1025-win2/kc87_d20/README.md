# I1025-win2/kc87_d20: win2's k_c 79 D 20 state regridded to k_c 87 and scanned at lambda 1.20 to 1.33

Written before the run, 2026-11-23 02:58 UTC (`date -u`). Machine win2 (desktop-pc, Windows 11, Core Ultra 7 265K, 20 threads, 95 GB), the win2 session. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1025. Coordinator: t5.

## Order (the coordinator's task, #1025 comment 7090320838, "win2: k_c 87 at D 20, from win2's own k_c 79 D 20 state", 2026-11-23 03:05 UTC; hc of about 03:10 UTC)

**Why.** The same-build k_c 79 to 87 change at D 20, as dh170 does at D 19.75. The scan also tests the ln|det| minimum without a sign change at 1.31 (k_c 79, D 20, `../kc79_d20/`) for a close pair.

- **Step 1, regrid:** pin win2's accepted k_c 79 D 20 state and record (raw c9d6762c) and dh610's `kc87_syscheck_1025.py` (blob 6df5d960, raw ec9fb489:I1025-dh610/kc87_d195/in/). `kc79_syscheck_1025.py` accepts the source (controls exit 1) and the k_c 87 check refuses it. Then `ell_refine.py <k_c 79 D 20 tag> 79 l1kc87win2d20 87 1 20.0 <the lambda_0 of the k_c 79 D 20 regrid> --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma`, started through WMI with the headless conhost. Accept only by `kc87_syscheck_1025.py` (selftest 0, `--mutate=F` and `--mutate=steps` exit 1) with `kc79_syscheck_1025.py` refusing the result.
- **Step 2, after ACCEPTED:** `d18_hybsign.py` at 1.20 to 1.28 by 0.01 (9 values), 1.29 to 1.33 by 0.005 (9 values) and a repeat of 1.25: 19 evaluations on 7 processes of 1 thread, beside leg 3 of the leap. Then `read_lower.py` selftest, `shift`, `round2` and the reader.
- **Report:** Delta beside k_c 79's 1.092257255093; every robust change by position, lambda_1 beside 1.248340; what the 0.005 grid shows at 1.31. Leg 3 of the leap runs on untouched (`../kc71_leap/`). Memory: alerts only.
- **Estimate:** regrid about 2 h (5281 s at k_c 79); scan 3 rounds of about 25 min each.

## Inputs (pinned in `inputs/`, checked with `git hash-object --no-filters`)

| file | origin | blob |
|---|---|---|
| `sol_l1kc79W20m1025_D20.0000.npy` (the k_c 79 D 20 state) | raw c9d6762c, `I1025-win2/kc79_d20/` | 7e288cc8 |
| `l1kc79W20m1025.jsonl` (its record, one line, equal to `rec_k79_D20.0000.jsonl`) | raw c9d6762c | d659667f |
| `kc79_syscheck_1025.py` | `I1025-win/kc79_d19/` | 29dce7ea |
| `kc87_syscheck_1025.py` | raw ec9fb489, `I1025-dh610/kc87_d195/in/` | 6df5d960 |
| `read_lower.py`, `d185_scan_read.py` | `I1025-dh170/lower_root/` | 89309d3c, 7c9d400f |
| `d18_hybsign.py` (xfkappa's scanner) | `I1025-mac/d18/` | e089207a |

The worktree's copy of the state (`D:/choptuik-i1025k79/solver/matter/data/sol_l1kc79W20m1025_D20.0000.npy`, where the k_c 79 regrid wrote it) has the same blob 7e288cc8. Code: worktree `D:/choptuik-i1025k79` at 48c36355 (solver code = 505d8399, `ell_refine.py` 631e5801, `ell_delta.py` fde699f5), venv-md510 (multidouble 5.1.0). Leg 3 runs in `D:/choptuik-i1025k71`.

## Step 1: the regrid (`regrid87_d20.sh`)

```
ell_refine.py l1kc79W20m1025 79 l1kc87win2d20 87 1 20.0 2.1110019498 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma
```

lambda_0 = 2.1110019498 is the k_c 79 D 20 regrid's (`ell_delta.lam0_at(20)`, error 3.8e-7; unused with `--no-gamma`). 8 BLAS threads, BelowNormal, cap 21600 s by the exact root pid with the `ell_refine.py` command-line check (`crun` of `../kc71_leap/lib_kcl.sh`; its planted test is in `../kc71_leap/`), started outside the terminal through `../kc71_leap/cim_start.ps1` (the headless form, `conhost.exe --headless cmd.exe /c`). Before it: both `--selftest` runs exit 0; `kc79_syscheck_1025.py` accepts the source, its `--mutate=F` and `--mutate=steps` exit 1; `kc87_syscheck_1025.py` refuses the source (it is k_c 79, not 87). **Acceptance (fixed now):** `kc87_syscheck_1025.py REC STATE 20 WTM` exits 0 (the record's |F| at most 1e-9, the record is k_c 87 at D 20, the state reproduces its record: `freeze_from` gives the record's steps and |F| within 1%), its controls on the same numbers are refused, `--mutate=F` and `--mutate=steps` exit 1, and `kc79_syscheck_1025.py` exits 1 on the result. A refusal, a failed control or a regrid that does not converge stops with a report; no retry. The accepted record goes into `regrid_accepted.txt` beside the k_c 79 source's numbers.

**Rehearsal of the source checks (`rehearsal/`, no regrid):** the k_c 79 check accepts the source (record |F| 4.4105e-10, 2800 steps, controls refused), both mutations exit 1, the k_c 87 check refuses it ("the record is not k_c 87 at D 20 (kc 79, D 20.0)"), both selftests pass.

## Step 2: the scan (`scan87_d20.sh`, starts itself when `regrid_accepted.txt` exists)

xfkappa's `d18_hybsign.py` (e089207a, unchanged) on the accepted k_c 87 state and its record line, the 1e-15 noise test (2 seeds) and the float64 sign; first line of each process: the record-system check (exit 3 if not). **Lambda 1.20 to 1.28 by 0.01 (9 values), 1.290 to 1.330 by 0.005 (9 values), and a repeat of 1.25: 19 evaluations in seven processes of one thread:**

| process | lambda, in this order |
|---|---|
| P1 | 1.25, 1.20, 1.21 |
| P2 | 1.25, 1.22, 1.23 |
| P3 | 1.24, 1.26, 1.27 |
| P4 | 1.28, 1.290, 1.295 |
| P5 | 1.300, 1.305, 1.310 |
| P6 | 1.315, 1.320 |
| P7 | 1.325, 1.330 |

BelowNormal, caps 28800 s by the exact root pids, `P4_WT_MATTER` the k_c 79 worktree. **The repeat gate** (`pair87.py`, a copy of `../kc79_d20/pair79.py`): the first records of P1 and P2 (both 1.25) must agree in hybrid sign, noise signs, float64 sign and ln|det| within 1e-6, else the seven scans are killed by exact pid (planted cases and `--break` in `selftest_pair87.txt`). **Reading:** `read_lower.py SCAN_DIR 1.20 1.33` as it prints (its selftest and `--mutate=shift` and `--mutate=round2`, both exiting 1, run first); roots by position. Threads: the regrid 8 + leg 3 of the leap 4 = 12 of 20; the scan 7 + 4 = 11.

## Run

Both drivers start outside the terminal through `../kc71_leap/cim_start.ps1`, BelowNormal, as soon as this README is pushed and the plan is posted on #1025: the regrid driver at once, the scan driver waits for `regrid_accepted.txt`. No script sends hc; verdicts are read from `summary_kc87.txt` and `exits_kc87.txt` and reported by hand.

## Result

Not yet run.
