# I1104-win: the kappa 0.5 re-solve of my k_c 143 D 23.0 state (#1104's first run), then the root scan and the secant with the Rust block 12 (winb)

Written before the run, 2026-11-27 18:31:55 UTC (the time of the README-first push; later pushes keep it). Nothing of this order had been run when the order, the bars and the estimates below were written. Run beforehand, read-only: the step count `freeze_from` gives for my k_c 143 state at kappa 0.5 (`steps_check_1104.txt`), the pins, the dry run of the re-solve driver. Runner: the winb session (surface-laptop-4, Windows 11, i7-1185G7 4 cores / 8 threads, 32 GB); coordinator t5.

## Order (t5, quoted)

**t5's hc of 2026-11-27 18:23 UTC (the next task for winb):** "Next task: #1104, its first run (the record: my newest #1104 comment; read #1104's body and #1101 comment 7224728711 first). Re-solve your k_c 143 D 23.0 state at kappa 0.5 with ell_refine.py: the same worktree, settings, threads and cap as your regrid, only --kappa 0.5, source your k_c 143 record and state, new tag with k050. Bars: |F| <= 5e-10, steps 6587 +- 132. Then scan lambda 0.080, 0.095, 0.110, 0.125 on the Rust block and the secant at tol 5e-5 on the change; widen to 0.065 and 0.140 if none. New raw folder I1104-win/, README with the bars first. Report the start (pilot) and the root."

**t5's #1104 comment 7225436553 (2026-11-27 18:23 UTC), the run and the reading:** "**Run (winb).** Its k_c 143 D 23.0 state at kappa 0.7 (raw `I1025-win/kc143_d23/`, root 0.0537365 by its secant at tol 5e-5, bracket [0.05371549, 0.05374049]) re-solved at kappa 0.5 with ell_refine.py, the same worktree, settings and cap as its regrid, `--kappa 0.5`. Bars: |F| <= 5e-10 and steps 1.4 x its kappa 0.7 count +- 2% (4705 -> 6587 +- 132). Then the scan on the Rust block at lambda 0.080, 0.095, 0.110, 0.125 and the secant at tol 5e-5 on the change, widening to 0.065 and 0.140 if none. **Reading.** delta_143 = root(kappa 0.5) - 0.0537365, against k_c 127's delta_127 = +0.04904. If the correction falls with k_c as the step does (h proportional to 1/k_c), delta_143/delta_127 = (127/143)^p: 0.62 for p = 4, 0.70 for p = 3, 0.79 for p = 2. The order p comes from macm3's R3. Estimate: about 12 h for the re-solve (the kappa 0.7 regrid took 8.8 h here), then about 3 h for the root."

**t5's hc of 2026-11-27 ~18:27 UTC (after my estimate of about 44000 s against the cap of 43200 s, and my question):** "cap 64800 s (18 h). Your estimate is right, and a kill at 12 h would waste the run. Your reading of the reports is right too: a #1104 comment at the start and one at the root." So: the re-solve's cap is **64800 s**; I post one comment on #1104 when the re-solve starts and one at the root.

Why a re-solve: #1101 comment 7224728711 (Test K and K4): finer mode-matrix steps on a fixed state (`--kappa_mm`) mix two discretizations and give no valid root; "each kappa point needs a re-solve at that kappa, then its root".

Stop rules (t5's, as in my k_c 143 lane): stop and report on not accepted, an exception (an array limit included), more than one robust change, or any step over its cap (the re-solve: 64800 s; the scan and the secant: 43200 s each). The no-robust-change case is not a stop here: t5 ordered the widening to 0.065 and 0.140.

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

README first. Not started when this was written.

Pushed 2026-11-27 18:31:55 UTC.

## Result

Not yet run.
