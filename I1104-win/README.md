# I1104-win: the kappa 0.5 re-solve of my k_c 143 D 23.0 state (#1104's first run), then the root scan and the secant with the Rust block 12 (winb)

Written before the run, 2026-11-27 18:31:55 UTC (the time of the README-first push; later pushes keep it). Nothing of this order had been run when the order, the bars and the estimates below were written. Run beforehand, read-only: the step count `freeze_from` gives for my k_c 143 state at kappa 0.5 (`steps_check_1104.txt`), the pins, the dry run of the re-solve driver. Runner: the winb session (surface-laptop-4, Windows 11, i7-1185G7 4 cores / 8 threads, 32 GB); coordinator t5.

## Order (t5, quoted)

**t5's hc of 2026-11-27 18:23 UTC (the next task for winb):** "Next task: #1104, its first run (the record: my newest #1104 comment; read #1104's body and #1101 comment 7224728711 first). Re-solve your k_c 143 D 23.0 state at kappa 0.5 with ell_refine.py: the same worktree, settings, threads and cap as your regrid, only --kappa 0.5, source your k_c 143 record and state, new tag with k050. Bars: |F| <= 5e-10, steps 6587 +- 132. Then scan lambda 0.080, 0.095, 0.110, 0.125 on the Rust block and the secant at tol 5e-5 on the change; widen to 0.065 and 0.140 if none. New raw folder I1104-win/, README with the bars first. Report the start (pilot) and the root."

**t5's #1104 comment 7225436553 (2026-11-27 18:23 UTC), the run and the reading:** "**Run (winb).** Its k_c 143 D 23.0 state at kappa 0.7 (raw `I1025-win/kc143_d23/`, root 0.0537365 by its secant at tol 5e-5, bracket [0.05371549, 0.05374049]) re-solved at kappa 0.5 with ell_refine.py, the same worktree, settings and cap as its regrid, `--kappa 0.5`. Bars: |F| <= 5e-10 and steps 1.4 x its kappa 0.7 count +- 2% (4705 -> 6587 +- 132). Then the scan on the Rust block at lambda 0.080, 0.095, 0.110, 0.125 and the secant at tol 5e-5 on the change, widening to 0.065 and 0.140 if none. **Reading.** delta_143 = root(kappa 0.5) - 0.0537365, against k_c 127's delta_127 = +0.04904. If the correction falls with k_c as the step does (h proportional to 1/k_c), delta_143/delta_127 = (127/143)^p: 0.62 for p = 4, 0.70 for p = 3, 0.79 for p = 2. The order p comes from macm3's R3. Estimate: about 12 h for the re-solve (the kappa 0.7 regrid took 8.8 h here), then about 3 h for the root."

**t5's hc of 2026-11-27 ~18:27 UTC (after my estimate of about 44000 s against the cap of 43200 s, and my question):** "cap 64800 s (18 h). Your estimate is right, and a kill at 12 h would waste the run. Your reading of the reports is right too: a #1104 comment at the start and one at the root." So: the re-solve's cap is **64800 s**; I post one comment on #1104 when the re-solve starts and one at the root.

**t5's hc of 2026-11-28 08:37 UTC (the scan accepted; the secant order):** "#1104 k_c 143 kappa 0.5 scan accepted: one robust change (0.095, 0.110). Ruling: refine it before any reading (a two-point det-linear estimate was 3.8e-4 off at R0, #1109 stage 1c2). Run the secant: python d18_secant.py run <record> <state> 23.0 0.095 0.110 secant_k050.jsonl --tol=1e-6 --maxev=12 --b12=rust --b12_threads=2 --ends=<the scan's records of 0.095 and 0.110> --pin=<state,record blobs>, one process, nice as before, timeout 14400. Report status, final bracket, the det-linear root inside it, evaluations and seconds; push raw I1104-win and post the table as a file I can post (or post it yourself if gh works there)."

**t5's hc of 2026-11-28 08:39 UTC (after my cost estimate: about 2450 s an evaluation on 2 threads, 5 evaluations in 14400 s):** "thanks for the cost read. Change: --b12_threads=4 and tol 1e-5 (the kappa shifts are about 0.05 and the scatter about 1e-3, so 1e-5 is ample; 5 to 6 evaluations), and write 28800 into I1104-win/cap_seconds.txt. Count the threads against your budget with the negative-mass jobs there; if 4 does not fit, keep 2 with the same tol and cap. Everything else as ordered."

**The secant as it runs (the 08:39 order replaces the 08:37 one and the plan below):** `d18_secant.py run` on my record and state between 0.095 and 0.110, `--tol=1e-5 --maxev=12 --b12=rust --b12_threads=4`, `--ends` the scan's two records at 0.095 and 0.110 (`scan_k050_D23_ends.jsonl`, 818 B, a binary copy of the scan's lines, blob 944e5150), `--pin` the state and record blobs (856ce129, 8c05d1a9), one process, BelowNormal, **cap 28800 s** (`cap_seconds.txt` holds 28800; the driver's own default is 14400 and the file overrides it at every poll, every change logged). The records go to `secant/secant.jsonl` (t5's file name `secant_k050.jsonl` is a path of the command; the folder here is `secant/`). The scan's det-linear estimate 0.098957 is not read: t5 ruled "refine it before any reading". **Threads against the budget** (4 to 6 threads at BelowNormal, my notes): 4 fit. A negative-mass job (`convergence.py 6`, I114-win, not mine) runs here (laptop 32 % CPU at 08:39 UTC, 21 GB free memory); the scan ran 2 x 2 Rust threads of mine beside it at a laptop mean of 60.0 % (max 80 %, lowest free memory 12.83 GB) with no alert. **Differences from the plan and the bars below:** tol 1e-5 (the bars say 5e-5), maxev 12 (10), 4 threads, cap 28800 s (the stop rule below says 43200 s for the secant); t5 ordered all of them.

Why a re-solve: #1101 comment 7224728711 (Test K and K4): finer mode-matrix steps on a fixed state (`--kappa_mm`) mix two discretizations and give no valid root; "each kappa point needs a re-solve at that kappa, then its root".

Stop rules (t5's, as in my k_c 143 lane): stop and report on not accepted, an exception (an array limit included), more than one robust change, or any step over its cap (the re-solve: 64800 s; the scan and the secant: 43200 s each; the secant: 28800 s by t5's hc of 2026-11-28 08:39 UTC). The no-robust-change case is not a stop here: t5 ordered the widening to 0.065 and 0.140.

## Registered before the run (t5's bars, my estimates)

**The bars:**

| step | bar |
|---|---|
| source | the k_c 143 check (`kc143_syscheck_1025.py` e15b0ee2) accepts my kappa 0.7 state and record (exit 0), its `--mutate=F` and `--mutate=steps` exit 1, the k_c 135 and k_c 127 checks refuse it (exit 1), and the gate below refuses it (exit 1: kappa 0.7, 4705 steps) |
| re-solve (t5's) | exit 0 inside the cap; the **gate** `gate_k050_1104.py` (d145145e; dh370's `gate_R1.py` form) exits 0 on the result: D 23.0, k_c 143, kappa 0.5, **\|F\| <= 5e-10, steps 6455 to 6719 (6587 +- 132)**; its selftest exits 0, `--mutate=f` and `--mutate=steps` exit 1 |
| re-solve (my addition, the state against its record) | `kc143_syscheck_1025.py` exits 0 on the result (it takes kappa from the record: the state's \|F\| within 1 % of the record's, `freeze_from` gives the record's step count), its selftest 0, `--mutate=F` and `--mutate=steps` exit 1, the k_c 135 check refuses the result (exit 1) |
| scan | `d18_secant.py` selftest 0 and its three mutations 1 1 1, `ell_b12rs.py` selftest 0 and `--mutate=nolam`, `--mutate=harm` 1 1 first; exits 0, 0; lambda 0.080, 0.095, 0.110, 0.125 (two processes, `--b12=rust --b12_threads=2`); the reader prints **exactly one robust change**; if none, 0.065 and 0.140 are scanned (t5's widening); more than one is a stop. The float64 sign and the orientation are reported as printed |
| secant | on the robust bracket, `--tol=5e-5 --maxev=10`, the scan's end records reused (`--ends`), Rust block, one process; exit 0 wanted; exit 4 with a valid bracket is reported as printed for t5's ruling |
| the root (t5 reads it) | no pass or fail bar from t5. Reported against t5's reading below |

**t5's reading, with my arithmetic (not t5's numbers):** delta_143 = root(kappa 0.5) - 0.0537365; delta_127 = +0.04904 (0.09500769 - 0.045968, #1101). The predicted ratios (127/143)^p are 0.6221 (p = 4), 0.7005 (p = 3), 0.7887 (p = 2), so delta_143 would be +0.03051, +0.03435, +0.03868 and the kappa 0.5 root at k_c 143 **0.0842, 0.0881, 0.0924**: all inside (0.080, 0.095), the bracket the four scan points would give. The root of the secant is the det-linear root `lam_lin` of its final bracket. A root is a kappa 0.5 root at k_c 143, D 23.0: data for #1104's fit in k_c and kappa, not a threshold (t5, #1025).

**My own estimates (not predictions of the order):**

- **Steps:** `freeze_from` on my kappa 0.7 state at kappa 0.5 gives **6582** (at kappa 0.7: 4705, the record's); t5's 6587 is 1.4 times 4705. The re-solved state's own count may differ a little; the bar is 6455 to 6719.
- **Re-solve time:** the kappa 0.7 regrid took 31576 s here (4705 steps, 4 threads, BelowNormal). If the time is proportional to the steps at one k_c: 1.4 x 31576 = **44200 s (12.3 h)**, t5's "about 12 h"; range 30000 to 64800 s (the cap). The hc at 21600 s and the cap are in the driver.
- **Memory:** the kappa 0.7 regrid peaked at 7.44 GB private; if it grows with the steps, about 8 to 10.5 GB. The scan processes were 5.5 GB each at 4705 steps: about 7 to 8 GB each at 6582 steps; the two together stay under 17 GB of 32 GB.
- **Scan:** one evaluation on two processes at once took 2616 to 2823 s at 4705 steps; times 1.4: **about 3700 to 4000 s**; two rounds: **7500 to 8500 s (2.1 to 2.4 h)**, plus about 3800 s if the widening is needed (0.065 and 0.140 in parallel).
- **Secant:** one evaluation on one process and 4 Rust threads took 1572 to 1601 s at 4705 steps; times 1.4: about 2200 s. A bracket 0.015 wide to a width under 5e-5 needs about 6 interior evaluations (4 to 9): **13000 s (3.7 h), 9000 to 20000 s**.
- **Secant at t5's 08:37/08:39 settings (written 2026-11-28 08:41 UTC, before the launch):** at kappa 0.5 the scan's evaluations were 2853 to 2856 s with the matrix at 1150 to 1158 s and block 12 at 1667 to 1675 s on 2 threads (two processes at once); the kappa 0.7 secant on one process and 4 threads took 1572 to 1601 s (matrix 690 to 694 s, block 12 856 to 883 s). Scaling the matrix by the scan's kappa ratio (1.20) and keeping the block: **about 1750 s an evaluation (1600 to 2000 s) on 4 threads**; t5 expects 5 to 6 interior evaluations: **8800 to 10500 s (2.4 to 2.9 h)**, 5 to 9 evaluations 8000 to 17000 s, 12 evaluations 21000 s; all under the cap of 28800 s. On 2 threads I wrote 2450 s an evaluation (2200 to 2900 s; the hc of 08:38 UTC).
- **The whole run:** about **18 h**, range 14 to 27 h (t5's estimate: 12 h plus 3 h). Almost all of it is the re-solve.

## The source (mine)

| item | value |
|---|---|
| source state | raw `I1025-win/kc143_d23/sol_l1kc143winbd23_D23.0000.npy`, 74808 bytes, **blob 866c434b** (the same in raw and here; `inputs/`, and in `solver/matter/data/` of the re-solve worktree, where the regrid wrote it) |
| source record | `l1kc143winbd23.jsonl`, 374 bytes with CR LF, **blob 88f0be8b** here (the raw copy stores LF: blob 46d232d2; see the k_c 143 README): k_c 143, D 23.0, kappa 0.7, u0 0.04, Ks 30, \|F\| 3.1672972784891065e-10, F_start 3.086036210347967e-06, **steps 4705**, constraint 6.113106423317232e-4, Delta 1.174309794771696, 31559 s, src `l1kc135win2d23` |
| its root | 0.0537364592 (det-linear), bracket [0.05371549, 0.05374049] (raw `I1025-win/kc143_d23`, 4078d4757; t5 accepted it at 18:23 UTC; #1025 comment 7225477905) |
| checks (raw `I1025-mac/checks/`) | `kc127_syscheck_1025.py` 898ebefa, `kc135_syscheck_1025.py` b353d466, `kc143_syscheck_1025.py` **e15b0ee2** (accepts the source; it takes kappa from the record, so it also checks the kappa 0.5 result) |
| gate | `inputs/gate_k050_1104.py` **d145145e** (made here from dh370's `gate_R1.py`, raw `I1101-dh370/R1`: the same clauses with k_c 143 and the bars 6455 to 6719); its selftest has 9 planted cases |
| re-solve code | worktree `choptuik-i1025k79` at 48c36355 (`ell_refine.py` 631e5801, `ell_delta.py` fde699f5, `dss_ell.py` 5d28c19e, `ell_ddm.py` 86578fee, `ell_dd.py` 7e58fcbc, `ddnp.py` 9b1fb195): the code of my k_c 127 and k_c 143 regrids |
| scan and secant code | worktree `choptuik-i1102` at d4b6b6ce: `d18_secant.py` 9706e506, `ell_b12rs.py` a1fff74f; ellrs (my #1102 Windows build, `i1102_1025/site/ellrs`, `.pyd` ddd5a082, `__init__.py` 76c7cfbc); readers `read_lower.py` 89309d3c, `d185_scan_read.py` 7c9d400f, `d18_hybsign.py` e089207a |
| lambda_0 | 2.0992182200 (`ell_delta.lam0_at(23.0, ...)`; unused with `--no-gamma`; the driver checks that it prints this string) |
| python | `venv-md510` (python 3.14.10, numpy 2.5.4, scipy 1.18.1, multidouble 5.1.0) |

## The run

1. **Pins and source checks** (the re-solve driver): the checks, the gate, the readers, the state and record against their blobs (inputs/ and the worktree's `data/` copies), the worktree and its solver files, `lam0_at(23.0)`; the source checks of the bars table. Any failure is a stop with an hc.
2. **Re-solve** (the order's command, one process, `OPENBLAS/OMP/MKL/RAYON_NUM_THREADS=4`, BelowNormal, no window, cwd the worktree's `solver/matter`, killed by the exact pid at the cap of 64800 s, hc at 21600 s if still running): `ell_refine.py l1kc143winbd23 143 l1kc143winbk050d23 143 1 23.0 2.0992182200 --kappa 0.5 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma`. If a file `cap_seconds.txt` is in this folder the driver reads the cap from it at every poll (only on t5's word; every change is logged).
3. **Acceptance:** the two blocks of the bars table; marker `regrid_accepted.txt` (state and record blobs). The driver's hc reports steps and their ratio to 4705, \|F\|, constraint, Delta beside the source's.
4. **Scan** (by the chain, only if the marker exists; the scan driver is made while the re-solve runs and dry-tested before it ends): `d18_secant.py scan ... --b12=rust --b12_threads=2`, two processes, shares `0.095,0.080` and `0.110,0.125`, then the reader on the folder and an hc with its lines.
5. **Secant** (by hand after I read the reader; only if exactly one robust change; the scan files are pushed first).
6. **Beside each stage:** a sampler (60 s), an alert-only memory watcher (hc below 1 GB, kills nothing) and a keep-awake helper (`SetThreadExecutionState`, power plan untouched), each its own process. The chain is started as `Win32_Process.Create` of `conhost.exe --headless cmd.exe /c go_k050d23_1104.cmd`; the session check must report no `claude` in any chain.
7. **Reports:** an hc to t5 at the end of each step; a **#1104 comment at the start of the re-solve** ("the start (pilot)") and one at the root. I take "pilot" to mean the start report of this first run; t5 confirmed "a #1104 comment at the start and one at the root".

## Files made here

`README.md`; `steps_check_1104.py` and `steps_check_1104.txt`; `gate_k050_1104.py`; the driver `k050d23_regrid_driver_1104.py` (derived from my k_c 143 regrid driver by `make_k050d23_1104.py`), `k050d23_watch_alert_1104.py`, `sample_driver_k050_1104.ps1`, `keepawake_1104.py`, `session_check_1104.ps1`, `go_k050d23_1104.cmd`, `publish_k050d23_1104.sh`, `push_1104.sh`; later the marker, the state and record, the scan and secant files, `rows/` (samplers, watcher and keep-awake logs).

## Status

**The re-solve STARTED 2026-11-27 18:32:46 UTC** (the README-first push of 18:31:55 UTC, raw 2b737f70d; #1104 start comment 7225606945). The source checks passed as wanted (k_c 143 check exit 0, `--mutate=F` and `--mutate=steps` 1 1, k_c 135 and k_c 127 checks 1 1, the gate on the kappa 0.7 source 1). `ell_refine.py` pid 10740 under the chain `conhost.exe --headless` 25160 <- cmd 19616 <- driver 21416 / 16568; cap 64800 s (kill 2026-11-28 12:32:46 UTC), hc at 21600 s; the session check shows no `claude` in any chain (`session_check_regrid.txt`). Sampler, alert-only watcher and keep-awake helper beside it. The scan and secant drivers were built (`make_k050d23_1104_part2.py`, derived from my k_c 143 drivers) and dry-tested while it runs, 18:35 to 18:50 UTC: the scan driver on stand-ins (my kappa 0.7 files under the kappa 0.5 names) in 9 tests, all as wanted (`selftest_scan_dry_1104.txt`: good run, no marker, wrong blob and an existing scan file each logged as REFUSE in the dry run, one value / three shares / a value three times / `--out` without `--dry` exit 2, and the widening round `0.065;0.140 --first=2 --window=0.065,0.14` planning files p2, p3 and the reader window 0.065 0.14); the secant driver on a stand-in stage in 4 tests, all as wanted (`selftest_secant_dry_1104.txt`: the kappa 0.5 gate refuses the kappa 0.7 stand-in, a wrong ends blob and a wrong LO HI are refused, a missing `--ends-blob` exits 2). The first run of test 4 of the scan driver did not log the refusal for an existing scan file (the check looked in the real folder, not in the stand-in); I made it look in the folder the state comes from (the same folder in a real run) and reran all nine tests.

**The lane is done (2026-11-28 10:54 UTC).** Re-solve 2026-11-27 18:32:46 to 2026-11-28 06:58:03 UTC, exit 0, 44717 s, ACCEPTED 06:58:47 UTC (state blob 856ce129, record blob 8c05d1a9; |F| 3.127e-10, steps 6582). Scan 07:00:53 to 08:36:38 UTC, exits 0, 0, 5745 s, one robust change (0.095, 0.110). Secant 08:43:35 to 10:52:21 UTC (tool pid 9008 under cmd 18712 / conhost 9716, driver 17776 / 13856; the session check shows no `claude` in any chain, `session_check_secant.txt`), **exit 4, status nonrobust: robust bracket [0.095, 0.0957226], det-linear root 0.0956935**, 6 evaluations, 7688 s. **t5's ruling (hc 10:53 UTC):** the root is about 0.09570 (robust bracket [0.095, 0.0957226], the non-robust 0.0956905 puts it in [0.0956905, 0.0957226]); posted on #1104 by t5 (comment 7238194210). No further kappa points: #1104 waits for #1111 stage 2. Nothing of mine runs on the laptop now.

**Blobs here and in raw.** The text files made on this laptop have CR LF; raw stores them with LF, so the raw blobs differ from the local ones named above (the `.npy` state is the same, 856ce129): record `l1kc143winbk050d23.jsonl` local 8c05d1a9, raw eb328251; `scan_k050_D23_p0.jsonl` local 01711e61, raw 754abc3d; `scan_k050_D23_p1.jsonl` local 0137c9eb, raw 3877b40a; `scan_k050_D23_ends.jsonl` local 944e5150 (818 B, the two scan lines as a binary copy), raw fabfb7cb. The pins in the drivers and the `--pin` of the tool are the local blobs.

Pushed 2026-11-28 10:55:52 UTC.

## Result

**Re-solve** (`ell_refine.py l1kc143winbd23 143 l1kc143winbk050d23 143 1 23.0 2.0992182200 --kappa 0.5 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma`, 4 threads, BelowNormal, cap 64800 s; the hc at 21600 s went out at 00:32 UTC): exit 0, 44717 s (12.4 h; my written 44200 s, range 30000 to 64800 s). As printed (`regrid_summary.txt`): record (kappa 0.5): |F| 3.1274325972598344e-10, F_start 1.0862747675244939e-09, steps 6582, constraint 0.0006113097815493973, Delta 1.1743097644977076; the kappa 0.7 source record at D 23.0: |F| 3.1672972784891065e-10, steps 4705, constraint 0.0006113106423317232, Delta 1.174309794771696; Delta(kappa 0.5) minus Delta(kappa 0.7) = -3.027398842725404e-08; steps ratio 1.3989373007438894. Peak working set 6.91 GB, peak private 7.44 GB, lowest free memory 15.45 GB, peak commit 20.0 GB, cpu 94463 s. Bars: |F| 3.127e-10 <= 5e-10 and steps 6582 in 6455 to 6719: met (gate exit 0).

**Scan** (`d18_secant.py scan ... --b12=rust --b12_threads=2`, two processes, lambda 0.095, 0.08 and 0.11, 0.125; 07:00:53 to 08:36:38 UTC, exits 0, 0, 5745 s; my written 7500 to 8500 s: 23 % below). Each evaluation 2853 to 2856 s (matrix 1150 to 1158 s, block 12 1667 to 1675 s, `dd_logdet` 29 s), against 2616 to 2823 s at kappa 0.7 (4705 steps): 1.01 to 1.09 of it, not the 1.4 I wrote. Peak private 5.51 GB each, laptop CPU mean 60.0 % (16 to 80), lowest free memory 12.83 GB (sampler) and 13.22 GB (alert-only watcher, 0 alerts). The reader (`read_lower.py`, `read_lower_k050_D23.log`), lines as printed:

```
points 4 in 0.080-0.125; not noise-robust: none
hybrid signs: 0.080- 0.095- 0.110+ 0.125+
float64 sign differs from the hybrid sign at: [(0.08, '-', '+'), (0.095, '-', '+'), (0.11, '+', '-'), (0.125, '+', '-')]
repeated points: none
  robust change (0.095, 0.110), - to +, det-linear 0.098957, range [0.095177, 0.098957]
robust changes: 1; touching a non-robust point (not counted): none
ln|det| local minima without a sign change: none
endpoint signs: - at 0.080, + at 0.125
read_lower exit 0
```

All four points are noise-robust (dln 3.64e-05 at 0.095, 8.18e-06 at 0.08, 5.62e-06 at 0.11, 6.42e-06 at 0.125). Exactly one robust change, so no widening. The float64 sign differs from the hybrid sign at all four points, as printed; I do not interpret it. t5 ruled (hc 08:37 UTC): refine before any reading.

**Secant** (`d18_secant.py run` at d4b6b6ce, blob 9706e506, `--tol=1e-5 --maxev=12 --b12=rust --b12_threads=4`, `--ends` the scan's records at 0.095 and 0.110, one process, BelowNormal, cap 28800 s from `cap_seconds.txt`): started 2026-11-28 08:43:35 UTC, ended 10:52:21 UTC, **exit 4, status nonrobust** ("not robust at 0.09569046743437838"), wall 7726 s, tool 7688 s. The tool stopped by its own rule at a non-robust interior point (dln 1.42e-01 against the limit 0.1; the two noise signs equal the hybrid sign), 6 evaluations (the two reused ends and 4 interior), maxev 12 and the cap not reached. The bracket is valid: **robust bracket [0.095, 0.09572259506339031]**, width 7.226e-04, signs [-1, +1] (- to +, as in the scan), **det-linear root 0.09569348946703232** (Brent 0.09572259506339031). The non-robust point 0.09569046743437838 has hybrid sign - and puts the root in [0.09569046743437838, 0.09572259506339031] (not robust, so not the bracket). `secant/secant.log` as printed (`secant_summary.txt` has the same lines):

```
pins: state 856ce129f556747dd53cfde973edc48388a2423f (wanted 856ce129f556747dd53cfde973edc48388a2423f), stub 8c05d1a9ed5a0ded7ad0d2b61606e2a2c39ff4fd (wanted 8c05d1a9ed5a0ded7ad0d2b61606e2a2c39ff4fd)
D 23.0 k_c 143: |F| 3.1265975054e-10 (record 3.1274325973e-10), steps 6582 (record 6582): the record system
bracket (0.095, 0.11), tol 1e-05, maxev 12, mode matrix fast (jac), block 12 rust, noise 1e-15, dln <= 0.1, sol_l1kc143winbk050d23_D23.0000.npy
block 12 by ellrs (avx512, products dgemm, 4 threads)
  lam 0.095 (lo): hybrid -1 ln|det| -4693.8981185427, noise [-1.0, -1.0] dln None, robust True; float64 +1 -4686.7014493683 (2853 s [1150, 1675, 29])
  lam 0.11 (hi): hybrid +1 ln|det| -4692.8719342642, noise [1.0, 1.0] dln None, robust True; float64 -1 -4692.4924832751 (2853 s [1151, 1673, 29])
  lam 0.0989573679472922 (interior): hybrid +1 ln|det| -4692.8731780855, noise [1.0, 1.0] dln 7.70e-07, robust True; float64 -1 -4690.1442293772 (1929 s [1063, 840, 27])
  lam 0.09604500702556346 (interior): hybrid +1 ln|det| -4694.7051374162, noise [1.0, 1.0] dln 5.03e-05, robust True; float64 -1 -4690.2606259583 (1921 s [1056, 838, 27])
  lam 0.09572259506339031 (interior): hybrid +1 ln|det| -4697.0689241238, noise [1.0, 1.0] dln 6.29e-04, robust True; float64 -1 -4689.7572969936 (1919 s [1052, 840, 27])
  lam 0.09569046743437838 (interior): hybrid -1 ln|det| -4702.5418439241, noise [-1.0, -1.0] dln 1.42e-01, robust False; float64 +1 -4691.4614770531 (1917 s [1051, 839, 27])
root: status nonrobust (not robust at 0.09569046743437838), bracket [0.095, 0.09572259506339031] width 7.226e-04, signs [-1.0, 1.0], det-linear 0.09569348946703232, Brent 0.09572259506339031, 6 evaluations, 7688 s
```

| # | lambda | role | hybrid sign | hybrid ln&#124;det&#124; | float64 sign | dln | seconds | parts (s) | robust bracket after |
|---|---|---|---|---|---|---|---|---|---|
| 0 | 0.095 | lo (reused from the scan) | - | -4693.8981185427 | + | none (reused) | 2853 (scan) | 1150, 1675, 29 | |
| 1 | 0.11 | hi (reused from the scan) | + | -4692.8719342642 | - | none (reused) | 2853 (scan) | 1151, 1673, 29 | [0.095, 0.11] |
| 2 | 0.0989573679472922 | interior | + | -4692.8731780855 | - | 7.70e-07 | 1929 | 1063, 840, 27 | [0.095, 0.098957] |
| 3 | 0.09604500702556346 | interior | + | -4694.7051374162 | - | 5.03e-05 | 1921 | 1056, 838, 27 | [0.095, 0.096045] |
| 4 | 0.09572259506339031 | interior | + | -4697.0689241238 | - | 6.29e-04 | 1919 | 1052, 840, 27 | [0.095, 0.095723] |
| 5 | 0.09569046743437838 | interior | - | -4702.5418439241 | + | 1.42e-01 (**not robust**) | 1917 | 1051, 839, 27 | stop: exit 4, bracket stays [0.095, 0.095723] |

The first interior point, 0.0989573679, is the scan's det-linear estimate (0.098957). The float64 sign differs from the hybrid sign at all 6 records, as printed; it is not part of the tool's robust test and I do not interpret it.

**t5's ruling (hc 2026-11-28 10:53 UTC, quoted):** "secant ruled: root about 0.09570 (robust bracket [0.095, 0.0957226]; the nonrobust 0.0956905 puts it in [0.0956905, 0.0957226]); posted on #1104 with your table. Push raw I1104-win. Then no further kappa points: #1110 found the roots at k_c 127 carry about 1e-2 of state scatter, so #1104 waits for #1111 stage 2." t5 posted the root on #1104 (comment 7238194210, 10:53 UTC, t5's text and table from the driver's hc); I posted nothing, to avoid a second comment. Reading (t5's, quoted from that comment): "#1110 (closed) found that converged states at k_c 127, D 23 fix lambda_1 only to about 1e-2 ... This root is the same kind of measurement, so it carries that scatter. No kappa order is read from it, and no further kappa points are run until #1111 stage 2 (a root that does not ride the decaying-mode ladder) exists."

**Against the numbers written before the run (arithmetic only, no reading):** delta_143 = root - 0.0537365 = +0.04196 at lam_lin 0.0956935 (from +0.04126 at the bracket's low end to +0.04199 at its high end), against delta_127 = +0.04904: ratio 0.8556 (0.8414 to 0.8562). The roots written beforehand for p = 4, 3, 2 were 0.0842, 0.0881, 0.0924: the measured root lies in (0.095, 0.110), above all three (they were inside (0.080, 0.095)). The scan's two-point estimate 0.098957 was 3.26e-3 above lam_lin.

**Cost against the estimates written before the run:**

| item | written | measured |
|---|---|---|
| each interior evaluation (one process, 4 Rust threads) | about 1750 s (1600 to 2000 s) | 1917 to 1929 s (mean 1921 s): inside the range, 10 % above the central value |
| of an evaluation | matrix about 830 s, block 12 about 880 s | matrix 1051 to 1063 s, block 12 838 to 840 s, `dd_logdet` 27 s |
| interior evaluations | 5 to 6 (t5; mine 5 to 9) | 4, the fourth non-robust |
| the run | 8800 to 10500 s (5 to 6 evaluations); cap 28800 s | 7688 s (tool), 7726 s (driver wall): 27 % of the cap, below the range because the tool stopped at the non-robust point |
| peak private memory | not written for the secant (scan: 7 to 8 GB each; measured 5.51 GB) | 5.60 GB (peak working set 4.21 GB), peak commit 17.4 GB |
| cpu | not written | 16827 s |
| lowest free memory | not written | 16.91 GB (sampler), 16.87 GB (alert-only watcher, 0 alerts) |

The matrix part took 1051 to 1063 s on this run against 690 to 694 s at kappa 0.7 on the same thread count; the negative-mass job (`convergence.py 6`, not mine) ran beside it; I did not establish the cause or whether it ran beside the kappa 0.7 secant. Laptop CPU mean 49.4 % (16 to 88), 128 sample times with no gap over 62 s. No alert, nothing killed; the keep-awake helper held until the driver ended (7815 s, cleared with ES_CONTINUOUS, `rows/secant_keepawake.log`); the System log (Kernel-Power, Power-Troubleshooter, Kernel-Boot) shows no event in 07:54 to 10:54 UTC. The hc at 7200 s went out at 10:43:35 UTC; the driver's end hc at 10:53:36 UTC.

**Lane summary:** re-solve 44717 s (6582 steps), scan 5745 s (one robust change (0.095, 0.110)), secant 7726 s (exit 4 at a non-robust point, bracket [0.095, 0.0957226], det-linear 0.0956935): the three steps sum to 58188 s (16.2 h); the wall clock from the first check (2026-11-27 18:32:11 UTC) to the end of the last driver (2026-11-28 10:53:36 UTC) is 58885 s (16.4 h; my written 18 h, range 14 to 27 h). No step over its cap, no exception, no stop condition of the order; the only stop was the tool's own exit 4, reported for t5's ruling.
