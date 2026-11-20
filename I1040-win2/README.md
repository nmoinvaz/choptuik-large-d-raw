# I1040-win2: step_timing_check.py (#1040's timing fix, PR #1047) run once on win2 with the #1034 build, and its control

Machine win2 (desktop-pc, Windows 11, Core Ultra 7 265K, 20 threads, 95 GB), the win2 build session. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1040 (closed; the coordinator's hc of 2026-11-20, read 04:32 UTC, asks for both exits to be posted on it). Companion folder: `I1034-win2/` (the build this check uses).

## Setup (written 2026-11-20 04:35 UTC, before any run)

| | |
|---|---|
| code | `hp/` of the worktree `D:/choptuik-i1034`, detached at **main 9980cd93** ("hp: drop the per-part seconds from test_stall's point records"; #1047, #1040's timing fix: adds `t_call` and `t_fill` to `driver.newton_step`'s info, docstrings; the coordinator: no bits change). Tree `2317adb595b9a93a96d30731d2f8cda3a253cc40`. `hp/step_timing_check.py` is that commit's |
| kernel | the hpkernel built there into the new venv `C:\Users\nathan\Source\venv-i1034` by `I1034-win2/run_build.sh` (`hp/build.sh`, fat LTO). The checker's default `--driver=checkout` loads this checkout's `hpkernel/driver.py` into that package; its first output line names both files |
| state | the script's default `data/lowD_states/highm15_D3.7000_M80.npz` (M 80, dense path), from the checkout |
| commands | from `hp/`, with venv-i1034's python, BelowNormal (inherited): `step_timing_check.py --reps=3 --threads=4` (want **exit 0**, all five checks PASS), then `step_timing_check.py --reps=2 --threads=4 --mutate=drop` (want **exit 1, check 1 FAIL**). Run **once** each, no retry. Driver `run_1040.sh`, called by `I1034-win2/run_all.sh` after the build and before step 5's chains, so that my own jobs do not load the timing; logs `step_timing.log`, `step_timing_drop.log`, `summary_1040.txt`, `exits_1040.txt` |
| caps | by the exact root pid, command line checked for `step_timing_check.py`, `taskkill /T /F /PID`: 900 s and 600 s (the coordinator's estimate is "a few minutes in all", taken as 5 min for the pair, times 3) |
| load | win2 is not idle: #1003's K 49 (`amp_flint_par.py`, 2 x 3 processes) and win2b's #1033 runs run beside it (the machine read 100% total CPU at 04:33 UTC). Each log records the total CPU %, the available memory and the python process count before and after. The script's own design (it carries the Jacobian's seconds from the dense calls to the block calls at their wall-to-CPU ratios) is meant for a loaded machine; the readings below say what its checks claim |

## Revision 14:28 UTC (still before any run): the coordinator's order to run it first, on a quiet machine

Context (not mine): the coordinator reopened #1040 at 08:21 UTC after dh610's run beside #1033's 8-thread run and #1021's recount (raw `I1040-dh610/` d1f01c6e): `--reps=3 --threads=4` exit 1 (checks 2 and 4, +12.98% and -12.02% against 5%), the control exit 1 with checks 1, 2 and 4 failing. The coordinator's prediction, written on #1040 before any rerun: on a quiet machine (load under 2) the plain run exits 0 and the mutated run fails check 1 only; if the quiet run also fails, the check's design is revised under review, and no threshold changes before then. The coordinator's hc to me (about 14:20 UTC): when the build ends, run the check first, while win2 is quiet (win2b holds off), then #1034's steps 5 and 2; post both exits on #1040 with the machine's load during the run.

What I changed in `run_1040.sh` for that, before the build ended:
- **Quiet gate.** "Load under 2" is read as under 2 busy threads of this machine's 20, i.e. total CPU under 10%. Before the first command the total CPU % is averaged over 3 samples 2 s apart, every 30 s, and the check starts when two consecutive averages are under 10%. If that has not happened within 2700 s the check is **not run** (summary line `NOT RUN`, `exits_1040.txt`), step 5 goes on, and I tell the coordinator and run the pair later on a quiet machine; it is never spent as its "once" on a busy machine.
- **Load during the run.** `load_watch1040.ps1` writes the total CPU %, the same as busy threads of 20, the available memory and the three busiest processes to `load.log` every 5 s from the start of the gate until `step_timing.done`; each command's own log also has the load before and after, and the summary line gives its time window. The post quotes the mean and maximum of `load.log` over each command's window. The sampler and my own alert-only watches add a little load themselves (the sampler's WMI queries; a test showed about one thread's worth with the build running), counted in what is quoted.
- The pair is the first step after the build in `I1034-win2/run_all.sh`, so step 5's three chains and the cargo test compile do not run during it. My own two watches (alert-only) and a Monitor shell run during it.
- The two commands, the caps (900 s and 600 s) and the "once" rule are unchanged.

Not changed: no threshold of the check, no code of the check.

## Readings fixed before the run

1. `--reps=3 --threads=4`: exit 0, with the script's five checks PASS (1 dense closure within 0.5%; 2 block closure within 5%; 3 the old reading falls short of C_b by more than 90%; 4 the fixed reading, `t_jac` within 5% of C_b and `t_fill` equal to step_timing's second entry; 5 the control can fire). The script's last line is `step_timing_check: PASS`.
2. `--reps=2 --threads=4 --mutate=drop`: exit 1, last line `step_timing_check: FAIL (checks ...)`, with **check 1 FAIL**. The coordinator's prediction for a quiet machine is that **only check 1** fails; I record which other checks fail and report any departure from the prediction.
3. A check that fails in reading 1 (checks 2 and 4 carry tolerances that a loaded machine can move) is reported with its numbers and the load, and nothing is rerun to make it pass or loosened; the coordinator decides. A cap hit or a wrong exit is a result.

## Result (written 2026-11-20 15:26 UTC)

**The plain run exits 1 (want 0): checks 1, 2 and 4 FAIL. The control exits 1 (want 1) with checks 1, 2 and 4 FAIL, not check 1 alone. Neither of the coordinator's predictions for a quiet machine held on win2.** Each command ran once (`exits_1040.txt`): the quiet gate passed after 283 s (15:23:36 UTC, total-CPU averages 5.3% then 0.3%), `step_timing` ran 15:23:43 to 15:23:58 (root pid 16132, 15 s, no cap), `step_timing_drop` 15:24:13 to 15:24:28 (root pid 35872, 16 s). Build: #1034's `hp/build.sh` at main 9980cd93 in venv-i1034 (exit 0, 5 h 5 min; the check's first line names `hpkernel` in venv-i1034 with multidouble 4.9.1 and multishoot 3.3.0, and the driver `D:\choptuik-i1034\hp\python\hpkernel\driver.py`); state `highm15_D3.7000_M80.npz`, M 80, 97 plan steps, 4 threads.

| run | command | exit | want | failing checks |
|---|---|---|---|---|
| 1 | `--reps=3 --threads=4` | **1** | 0 | **1, 2, 4** |
| 2 | `--reps=2 --threads=4 --mutate=drop` | 1 | 1, check 1 FAIL (predicted: only check 1) | **1, 2, 4** |

Run 1 (`step_timing.log`): 1 FAIL (the four dense entries miss at most 2.51% of a dense call, bar 0.5%; per dense call 0.2%, 2.5%, 0.4%); 2 FAIL (block closure -21.28%, the median of +19.2%, -21.6%, -21.3%, bar 5%; C 4.17 CPU s); 3 PASS (the old reading is at most 6.88e-3 of C_b; it misses 99.31% of the Jacobian); 4 FAIL (`t_jac` against C_b +21.54%, bar 5%; `t_fill` is step_timing's second entry in every call: True); 5 PASS (the dense factorization is at least 11.97% of the call). Run 2 (`step_timing_drop.log`): 1 FAIL as the control requires (the dense entries miss up to 28.79%), 2 FAIL (-28.19%, the median of -13.0% and -43.3%), 4 FAIL (+25.94%), 3 PASS, 5 PASS.

The calls (seconds; block = `driver.newton_step` in block storage, dense = `newton_mixed(block=False)`; "wall - entries" is the time no step_timing entry holds):

| run | rep, kind | wall | CPU | entries: residual, Jacobian, factorization, solve | wall - entries |
|---|---|---|---|---|---|
| 1 | 0 block | 0.968 | 3.70 | 0.0340, 0.0051, 0.0207, 0.0055 | 0.903 |
| 1 | 0 dense | 1.215 | 4.12 | 0.0340, 0.9406, 0.1455, 0.0925 | 0.0027 |
| 1 | 1 dense | 1.895 | 5.69 | 0.0307, 1.3881, 0.2985, 0.1307 | 0.0475 |
| 1 | 1 block | 1.708 | 6.06 | 0.0560, 0.0081, 0.0768, 0.0248 | 1.543 |
| 1 | 2 block | 1.554 | 5.86 | 0.0680, 0.0042, 0.0337, 0.0129 | 1.436 |
| 1 | 2 dense | 2.065 | 6.77 | 0.0463, 1.5531, 0.3393, 0.1186 | 0.0078 |
| 2 | 0 block | 0.979 | 3.81 | 0.0340, 0.0052, 0.0211, 0.0051 | 0.914 |
| 2 | 0 dense | 1.161 | 3.92 | 0.0352, 0.8869, 0.1570, 0.0795 | 0.0026 |
| 2 | 1 dense | 1.726 | 5.17 | 0.0334, 1.0980, 0.4549, 0.0979 | 0.0422 |
| 2 | 1 block | 1.778 | 6.06 | 0.0757, 0.0041, 0.0551, 0.0063 | 1.637 |

**What the numbers say (observations, not a verdict on the check).** The first call of a run is the fastest, in both runs: the block call's wall time goes 0.968 -> 1.708 -> 1.554 s and its process CPU seconds 3.70 -> 6.06 -> 5.86 for the same work, and the dense call's 1.215 -> 1.895 -> 2.065 s (CPU 4.12 -> 5.69 -> 6.77); run 2 shows the same (0.979 -> 1.778 s, CPU 3.81 -> 6.06). So the CPU seconds of one call are not stable here either, which is the premise the check carries C_b over from the dense to the block calls on (the same break as dh610's, there put down to load); I did not test why (frequency or core type on this hybrid CPU are guesses, not tested). The unaccounted time of the block call, which is the Jacobian's columns, and the dense call's Jacobian entry are close call by call: 0.903 against 0.941 (rep 0), 1.543 against 1.388 (rep 1), 1.436 against 1.553 (rep 2) seconds in run 1, 0.914 against 0.887 and 1.637 against 1.098 in run 2 (the last pair differs by 49%). That comparison is not one of the check's criteria. Check 1's failure comes from the second dense call of each run (gaps 0.0475 and 0.0422 s, against 0.003 to 0.008 s for the others).

**Load during the runs (`load.log`, a sampler of mine every 5 s; the quiet gate passed, but the window itself was not clean).** The gate's averages were 5.3% and 0.3% of the 20 threads (1.1 and 0.07 busy threads). The `load before` of run 1, taken by my own wrapper at 15:23:36 (a PowerShell counter call), read 12.3, 9.8, 11.6% (about 2.3 busy threads). The sampler's lines from just before the first command to just after the second (the commands ran 15:23:43 to 15:23:58 and 15:24:13 to 15:24:28; the check's own 4 threads are in the lines at 15:23:48 and 15:24:15, python 380% and 177%; the others are before, between or after them):

| time (UTC) | total CPU % | busy threads of 20 | three busiest processes |
|---|---|---|---|
| 15:23:34 | 30 | 6.0 | bash 41%, MsMpEng 36%, msedge 20% |
| 15:23:41 | 25 | 5.0 | bash 76%, WmiPrvSE 16%, MsMpEng 16% |
| 15:23:48 | 46 | 9.2 | python 380% (the check), bash 65%, MsMpEng 16% |
| 15:23:55 | 10 | 2.0 | SpotifyLauncher 16%, WmiPrvSE 16%, System 10% |
| 15:24:02 | 0 | 0 | WmiPrvSE 20%, tailscaled 10% |
| 15:24:09 | 38 | 7.6 | WmiPrvSE 21%, System 10%, MsMpEng 5% |
| 15:24:15 | 28 | 5.6 | python 177% (the check), WmiPrvSE 10%, grep 5% |
| 15:24:22 | 26 | 5.2 | bash 81%, svchost 20%, bash 20% |
| 15:24:29 | 12 | 2.4 | WmiPrvSE 14%, tvnserver 4%, System 4% |
| 15:24:36 | 11 | 2.2 | python 194%, python 184%, python 97% (step 5's first chains starting) |

So the machine was quiet at the gate, but around the two windows it carried my own wrappers (bash, the sampler's WMI queries), Defender and desktop programs (Edge, Spotify) besides the check, and I cannot show that the load stayed under 2 busy threads beyond the check's own 4. Available memory 55.7 to 56.4 GB; no python process other than the check's; nothing of win2b's ran (its message of 14:29 UTC).

Not changed: no threshold, no code of the check. A rerun would need a cleaner "quiet" than my own tooling allows (sampler off, nothing else started); it is the coordinator's call.

Files: `step_timing.log`, `step_timing_drop.log`, `load.log`, `exits_1040.txt`, `summary_1040.txt`, `run_1040.sh`, `lib1040.sh`, `load_watch1040.ps1`, `step_timing.done`.
