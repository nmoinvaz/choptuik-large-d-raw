# I1012-win2: M = 9, level 5's finite-difference step raised (--h5)

Machine win2 (desktop-pc, Core Ultra 7 265K, Windows 11, Python 3.14.10), the win2 build session (claude-me2), runner. Issue
https://github.com/nmoinvaz/choptuik-large-d/issues/1012 (coordinator task, #1011's finding). Raw output of this task only.

Code: main 23844822 (its change in `solver/inner_stokes` is `hier_nb.py --h5=REL` and `--h7=REL`, level 5's and 7's relative finite-difference step, passed to the spawn workers by the environment variables
HIER_NB_H5 / HIER_NB_H7 like `--h3`; hier's default step is 1e-6 relative, `1e-6 * max(|b|, 1e-3 |A|)`, i.e. 8.4e-9 and 2.7e-9 absolute for level 5). The worktree `D:\choptuik-inner` stays at
656396fd while #1011's two runs execute from it, and is fast-forwarded to origin/main only after they have ended. venv `C:\Users\nathan\Source\venv-i962` (numba 0.68.1, llvmlite 0.50.0, numpy 2.5.4, scipy 1.18.1).
win2b's ks_chain2 and #945 run beside it; nothing is run from or changed in `D:\choptuik-i962`.

## Written down before any #1012 run (2026-11-19 08:04 UTC; #1011's runs are still going)

Order (the coordinator's hc and the issue): #1011's runs end first (their 3 h caps end at 10:42:35 UTC; `I1011-win2`, posted on #1011), then the plumbing control, then the runs.

**Done before the control, without a solve** (a scratch extract of main 23844822's `solver/inner_stokes`, no worktree touched): `unit_h5.py` calls `LazyHier.h(l, x)` at #999's pretuned x with HIER_NB_H5 unset, `1e-6`, `1e-4`, and a wrong
variable name (`unit_h5_result.txt`): level 5's step is exactly 1 x, 1 x, **100 x** and 1 x hier's default; levels 3 and 7 never move; a mutated expectation (100 x read as 1 x) fails. So `--h5=1e-6` is bit-identical to the default
step by arithmetic (same double, same expression) and `--h5=1e-4` changes level 5's step by a factor 100.

1. **Plumbing control** (`control_run1012.py`, `control1012.py`; the issue's step 1): #1011 run 1's command (XI 0.11, AP 0.105, `--floor_max=1e-4 --verbose=2`, `--procs 2`, rtol 1e-13) with `--h5=1e-6` and with `--h5=1e-4`, side by
   side, each stopped by its own pid when its first `level 5 (low): stop at` line appears (or at 600 s). `--h5=1e-6` must equal #1011 run 1's log line for line up to and including that stop line (seconds and addresses
   normalized): **pass**. `--h5=1e-4` must differ before that line (its first level-5 iteration): **pass if it differs**. Either failing stops the task and is reported. The comparison script's self-tests (the log against itself passes, other radii and a
   dropped line fail) are in `logs/selftest_control1012.txt`.
2. **Runs** (`chain1012.py`): #1011's two runs with `--h5=1e-4` added, side by side: (XI 0.11, AP 0.105) and (XI 0.105, AP 0.105), 3 h cap each, killed with their process tree. Command: `INNER_NB_RTOL=1e-13 python -u hier_nb.py 9
   2.719219 1.000022 --x=0.148977988,0.014770713,0.008424206,0.001511189,0.000474205,0.00012168 --xi1=0.15 --pretune --fixA --schur --predict --procs 2 --h3=1e-4 --h5=1e-4 --floor_max=1e-4 --verbose=2 --approach=5:AP --polish=5:XI`.
3. **Stage 2**: if neither first level-5 solve ends below 1e-6, **run 1 again with `--h5=1e-3`** (XI 0.11, AP 0.105; the issue's wording; the coordinator's hc can be read as both runs, so the XI 0.105 run at 1e-3 is not started
   unless asked). It starts as soon as both first solves have ended, beside the stage-1 runs, which go on to their caps. If either first solve is below 1e-6, stage 2 is not started and that run goes on to the zero within its cap.
   The driver's decision and its selftest (stage 2 starts for first solves 6.0 and 8.0, not for 5e-7 and 8.0; fails under `--mutate=anyone` and `--mutate=nokill`): `logs/selftest_chain1012.txt`.
4. **Radii check** on each log's `level radii` line (`check_polish.py LOG XI AP`, its mutation fails).
5. **Report** (the issue): per run, level 5's and level 3's solves (end |r|, stop reason, accepted trials) and the run's end r_1 to r_9 (`summarize1007.py`; its checks are tested in `I1007-win2/logs/selftest_summarize1007.txt`); beside #1011's table.
6. **Acceptance** (the issue): level 5's first solve below 1e-6 is the success case, then the run goes on to the zero within its cap. If the stop reason stays "every trial rejected" at |r_5| above 1, the Jacobian's step is not the
   cause either, and that is the report.

Deviation to note: the issue says "run 1 again with `--h5=1e-3`" and the hc says "then #1011's two runs with --h5=1e-4 ... and --h5=1e-3 if neither first solve gets below 1e-6"; I follow the issue (run 1 only) as the task's record.

## Added by the coordinator's hc, 08:14 UTC 19 Nov (before any level-5 solve of the h5 = 1e-4 runs had ended)

- **Success is any level-5 solve below 1e-6, not only the first** (the coordinator notes it on the issue). The driver's "later solve below 1e-6" notice is the matching check; the runs have 3 h caps already, so nothing is extended.
- Report each later level-5 solve's end |r_5| and stop reason too (`summarize1007.py` lists every solve with both stages' stops and accepted iterations).
- If the later solves floor near 4e-5 with every trial rejected (as #1011's XI 0.11 run did, 3.92e-5), that may be the integrator's floor at rtol 1e-13 rather than the Jacobian, and the next run is the same command at `INNER_NB_RTOL=1e-14`, which lowered M = 7's floors (#976, #977, #981). Not started before the h5 = 1e-4 results are read; it is a new command with its own pre-registration.

## Stage 3, written down at 08:35 UTC 19 Nov before it starts (from the coordinator's hc of 08:15 UTC and the second milestone)

State at 08:33 UTC (the h5 = 1e-4 runs' second level-5 solves and the h5 = 1e-3 run's first): h5 = 1e-4, XI 0.11: solve 1 1.72e-2, solve 2 **4.25e-5** (stops: every trial rejected, approach 1.03e-2, polish 4.25e-5); h5 = 1e-4, XI 0.105: 1.25e-2, then 3.90e-3
(the default step gave 11.5 there); h5 = 1e-3, XI 0.11: first solve 4.50e-2. The XI 0.11 floor at 4.25e-5 on "every trial rejected" equals #1011's 3.92e-5 at the default step, so it does not move with h5, which is the condition the hc named.

- **Stage 3** (`chain1012c.py`): that run (XI 0.11, AP 0.105, `--h5=1e-4`, `--floor_max=1e-4`, `--verbose=2`, `--procs 2`, BelowNormal) again at **`INNER_NB_RTOL=1e-14`**, 3 h cap, started beside the three runs above. The environment variable reaches the spawn workers
  (probe: a pool of two reads 1e-14 in os.environ and in inner_nb.RTOL_OVERRIDE, None when unset). No log-for-log control applies (the rounding changes from the first integration), so the plumbing check is that probe plus the first log lines' |r_9| values differing from the 1e-13 log's.
- **What would show an integrator floor:** its second level-5 solve ends clearly below 4.25e-5 (the 1e-13 run's), with the stop reason read from the log; the same floor at 1e-14 means it is not the integrator's. Any level-5 solve below 1e-6 is the success of #1012.
- The driver's selftest (one success notice for a stub's later solve of 5e-7, no process left; it fails under `--mutate=anysolve` and `--mutate=nokill`): `logs/selftest_chain1012c.txt`.
- The driver and the pattern of my first milestone waiter: that waiter grepped "below 1e-6", which also matches the driver's header line, and fired at 08:24:48 with no solve below 1e-6. I changed it to the notice text ("solve ended at/below") and tested it on real and synthetic lines.

## The h5 = 1e-3 run stopped, and how stage 3 will be read (written 08:37 UTC 19 Nov, before stage 3's second level-5 solve exists)

- **The `--h5=1e-3` run (XI 0.11, AP 0.105, pid 25632) was stopped at 08:36:58 UTC on the coordinator's word**, 780 s in, own process tree by taskkill /T /F on the exact pid (the driver's exit file says "exit 1": the kill). Its reading is its first level-5 solve only: **4.50e-2** (2535 residuals, 518 s; accepted iterations 4.7e-2, 3.8e-2, 4.9e-2, 4.5e-2; both stages stopped on "every trial rejected"), worse than `--h5=1e-4`'s 1.72e-2 and far better than the default's 11.9 (`logs/summary_h5_1e-3_at_stop.txt`). The two `--h5=1e-4` runs and stage 3 go on.
- **Stage 3's reading** (the coordinator's two outcomes, with the cut written down now): the 1e-13 floor of the XI 0.11 second solve was 1.17e-4 (#999), 3.92e-5 (#1011) and 4.25e-5 (this issue's `--h5=1e-4` run), a spread of a factor 3. The 1e-14 run's second solve ending **below 1.4e-5 (a factor 3 under 4.25e-5)** is "clearly below": an integrator floor, and the next run is rtol 1e-15 if `inner_nb` accepts it. An end between 1.4e-5 and 1.3e-4 (the 1e-13 spread) is "about 4e-5 again": the floor is in the problem at this radius, and levels 7's and 9's steps are next. The number and the stop reason are reported either way, and a value in between is reported as such. Later level-5 solves of every run are reported too.

## Stage 4, written down at 09:06 UTC 19 Nov before it starts (the coordinator's hc, ~09:00 UTC)

Reading of stage 3 (milestone 3, comment 7004516203): the rtol 1e-14 run's second level-5 solve ended at 1.38e-3, not lower than the 1e-13 run's 4.25e-5, so the integrator is ruled out; an end that varies x10 between solves of one run points at the nested levels 7 and 9 feeding level 5 their solves' noise.

- **The XI 0.105 stage-1 run (pid 9100) is stopped** on the coordinator's word, by taskkill /T /F on that exact pid: its reading is its two level-5 solves, 1.25e-2 and 3.90e-3 (`logs/summary_xi0105_h5_1e-4_at_stop.txt`; its exit file will say "exit 1": the kill). The XI 0.11 `--h5=1e-4` run (pid 28816) and stage 3 (pid 10848) go on.
- **Stage 4** (`chain1012d.py`), in its place: XI 0.11, AP 0.105, `INNER_NB_RTOL=1e-13`, `--h5=1e-4 --h7=1e-4 --h9=1e-4` (levels 5, 7, 9 at 100 x hier's step), `--floor_max=1e-4 --verbose=2`, `--procs 2`, BelowNormal, 3 h cap, from `D:\choptuik-h9b`, a git archive of main 299c4eb9's
  `solver/inner_stokes` (299c4eb9 adds `--h9`; `D:\choptuik-inner` stays at 23844822 under the live runs; `D:\choptuik-h9` is an earlier identical extract, left as it is; no directory was removed).
- **Unit check first** (`unit_h579.py`, `unit_h579_h9b_result.txt`): on that extract, step ratios to hier's default are 100 at a level set to 1e-4, 1 at 1e-6 or unset, other levels unmoved, in the cases h5, h7, h9, all three at 1e-4, all three at 1e-6 and a wrong variable name; the mutation (the h9 case's 100 read as 1) fails.
  The driver's selftest and mutations: `logs/selftest_chain1012d.txt`. No log-for-log control applies (a different step changes the first level-5 Newton step), and the 1e-6 case of the unit check stands in for it.
- **Report** (the hc): each level-5 solve's end and stop reason, and level 7's and 9's solve ends beside level 5's: for each level-5 solve, the minimum, median and maximum of the level-7 and level-9 solves inside it (`levels1012.py`, with a check that its counts equal the log's totals and a mutation).
  Reading to test: if level 5's second-solve ends drop clearly below the stage-1 `--h5=1e-4` run's 4.25e-5 and 3.86e-4, the nested levels' step was feeding level 5 noise; if they stay at 1e-5 to 1e-3, it was not. Any level-5 solve below 1e-6 is the success of #1012.

## Stage 4 started, with one crash first (09:09 UTC 19 Nov)

- **The XI 0.105 stage-1 run (pid 9100) was stopped at 09:06:45 UTC** (3241 s of its 3 h; own tree by taskkill /T /F; its exit file says "exit 1": the kill). Its reading: level-5 solves 1.25e-2 and 3.90e-3, both stages of both stopped on "every trial rejected" (`logs/summary_xi0105_h5_1e-4_at_stop.txt`).
- **First launch of stage 4 at 09:06:46 crashed after 10 s** (`..._CRASH1_missing_seedfile.log`, renamed, kept): `hier.py` reads its seed from `../inner_amp/data/sigF_w1.0000_K15_J1000_phys.json`, which my extract of only `solver/inner_stokes` did not hold (FileNotFoundError at `seed_from_C`). My unit check does not call the seed, so it could not
  catch this. I added the 12 files of `solver/inner_amp/data` (a git archive of 299c4eb9, byte-equal to it) to `D:\choptuik-h9b` (adding files only; nothing was removed anywhere, `D:\choptuik-h9` is untouched), checked that `seed_from_C` loads from `h9b` (length 8) and fails from `h9` (the control), and relaunched at 09:07:53 UTC (pid 18224). No number comes from the crashed launch.
- **Per-level report** (`levels1012.py`; check and mutation in `logs/selftest_levels1012.txt`). `logs/levels1012_so_far.txt` at 09:10 UTC, on the two live logs: during level 5's first solve (before the leakage Jacobian K exists) level 7's solves have a median of 3.5e-5 and a maximum of 9.5e-5 (rtol 1e-14: 4.2e-5 and 8.7e-5),
  the size of level 5's later ends; in the second and third solves level 7's median is 5e-8 to 1.1e-7 (maximum 7e-7) and level 9's about 1e-9 (maximum 6.5e-9), three or more orders below level 5's ends (4.25e-5, 3.86e-4).

## Stage 1's XI 0.11 `--h5=1e-4` run finished by itself (09:38 UTC 19 Nov; started 08:12:48, ended 09:36:59, exit 0 after 5051 s, FIXED-A line, no Traceback)

Files: `logs/summary_xi011_h5_1e-4_final.txt`, `logs/levels1012_xi011_h5_1e-4_final.txt`, `logs/selftest_summarize1007_v2.txt`.

| quantity | this run (XI 0.11, AP 0.105, `--h5=1e-4`, rtol 1e-13) | #999 (same radii, default step, efad7afd) |
|---|---|---|
| level-5 solves, end |r_5| | 1.72e-2, 4.25e-5, 3.86e-4, 5.95e-4, 1.39e-3 | 7.43, 1.17e-4, 6.73e-4, 3.92e-4, 3.37e-4 |
| stops of every level-5 stage | "every trial rejected with a fresh Jacobian" (10 of 10) | not printed (old format) |
| level 3 | one accepted iteration (lam 1) to 21.5, then "every trial rejected" at 21.5 (27252 residuals, 5035 s) | solved at 7.57 |
| end r_3, r_5, r_7, r_9 | 21.5, 3.9e-4, 4.2e-7, 2.2e-9 | 7.6, 3.4e-4, 3.0e-8, 2.2e-10 |
| final r_1 | +1.9e5 - 1.2e6 i | +5.7e5 - 8.9e4 i |
| wall time | 5051 s | 2270 s |

The end values are the accepted state's: r_5 3.9e-4 equals the third solve (3.86e-4) and the fourth and fifth solves (5.95e-4, 1.39e-3) belong to rejected level-3 trials, so my summarizer's end check, which expected the last solve's value, fired on this log
(the check's assumption was wrong, as it had been for r_9 in #999's log). It now requires the end value to equal one of the log's level-k solves (`summarize1007.py` v2 in this folder; real logs pass, changing r_5 or r_9 in the F_k/F_1 line trips it: `logs/selftest_summarize1007_v2.txt`; the copy in `I1007-win2` still has the stricter check).

Level 7's and 9's solve ends beside level 5's (`levels1012.py`): in level 5's first solve level 7 has a median of 3.5e-5 and a maximum of 9.5e-5; in the later four solves level 7's median is 4.7e-8 to 1.1e-7 (maximum 6.9e-7) and level 9's about 1.1e-9 to 1.3e-9 (maximum 6.6e-9), three or more orders below level 5's ends.

Reading: the larger level-5 step (`--h5=1e-4`) removes the first solve's stall at about 11 (1.7e-2), but level 5's later solves end at 4e-5 to 1.4e-3, no lower than the default step's 1e-4 to 7e-4, and level 3 ends at 21.5, worse than #999's 7.57 (one run each). So the Jacobian step is what limited the first solve; it does not limit the later solves or level 3.

## Stages 3 and 4 stopped; stage 5 written down at 09:59 UTC 19 Nov before it starts (the coordinator's hc, ~09:55 UTC)

**Stopped on the coordinator's word, by taskkill /T /F on their exact pids:** stage 4 (`--h5 --h7 --h9 = 1e-4`, pid 18224) at 09:56:54 UTC after 2940 s, and stage 3 (rtol 1e-14, pid 10848) at 09:56:50 after 4881 s. Their exit files say "exit 1": the kill. Readings (`logs/summary_stage4_at_stop.txt`, `logs/summary_stage3_at_stop.txt`, `logs/levels1012_stage{3,4}_at_stop.txt`):
stage 4's first level-5 solve ended at 197 (levels 7 and 9 broken: level 7 solves 0.25 to 3.2, level 9 median 3e-5, 425 "every trial rejected"); stage 3's solves were 1.89e-2, 1.38e-3, 3.97e-4, no lower than the 1e-13 runs' band.
Conclusion of the hc: levels 7 and 9 keep hier's default 1e-6 step, only level 5 needs a larger one; rtol 1e-14 is not needed.

**Stage 5** (`chain1012e.py`, selftest and mutations in `logs/selftest_chain1012e.txt`), two runs side by side from `D:\choptuik-h9b` (299c4eb9), XI 0.11 / AP 0.105, `INNER_NB_RTOL=1e-13`, `--floor_max=1e-4 --verbose=2 --procs 2 --h3=1e-4`, BelowNormal, 3 h caps:
- **(a) `--h5=3e-4`** (h7, h9 default; `--predict` and `--schur` on): brackets the level-5 step. Known first solves: default 1e-6: 11.9; 1e-4: 1.72e-2; 1e-3: 4.50e-2. Unit check: level 5's step is 300 x the default, other levels 1 x, a mutation expecting 100 fails (`unit_h53e-4_result.txt`).
- **(b) `--h5=1e-4` without `--predict`** (`--schur` kept): tests whether the leakage Jacobian K that `--predict` uses for every nested re-solve keeps level 5's later solves at 4e-5 to 1.4e-3 (rpi5 found K's blocks 8e3 to 4e4 times larger at M = 9 than at M = 7). K is computed after level 5's first solve, so (b)'s first solve must equal stage 1's
  (`--h5=1e-4` with `--predict`) line for line up to the `Jacobian K computed` line, which says 10 residuals with `--predict` and 8 without (the driver checks the count; `control1012e.py`, below, the lines). Both are plumbing controls that can fail.
- **Reading of (b), written now:** K matters if a level-5 solve from the second on ends **below 1e-5** (a factor 4 under the lowest end, 4.25e-5, of the `--predict` runs), or if level 3 ends clearly below 21.5. The same 4e-5 to 1.4e-3 band means `--predict` is not what holds level 5 there; above 1.4e-3 (the highest end seen) means it was helping. Any level-5 solve below 1e-6 is the success of #1012.
- **Reading of (a):** the first solve against 1.72e-2 (1e-4) and 4.5e-2 (1e-3), and the later solves against the same band; the best level-5 step is the one with the lowest first solve, reported with its later solves.
- Report each level-5 solve's end and stop reason, and level 3's, as before (`summarize1007.py` v2 and `levels1012.py`).

## Stage 6 written down at 10:27 UTC 19 Nov, and a mistake of mine in its selftest (the coordinator's hc, ~10:20 UTC)

**Stage 6** (`chain1012f.py`): when both stage-5 runs have reached their caps (12:59:21 UTC) or ended, close the level-5 step bracket with **`--h5=3e-5` (c) and `--h5=1e-5` (d)** side by side, with `--predict` as stage 1, XI 0.11 / AP 0.105, rtol 1e-13, `--floor_max=1e-4 --verbose=2 --h3=1e-4`, `D:\choptuik-h9b` (299c4eb9), 3 h caps.
The driver waits for the two stage-5 exit files and starts only then (stop rule: nothing is started if they are not both there by 13:15 UTC). Unit check of the steps (30 x and 10 x the default, a mutation fails): `unit_h5_3e-5_1e-5_result.txt`. After these, #1012's closing summary with the full table by step, rtol, nested steps and `--predict`.

**The mistake** (10:20 to 10:27 UTC): the first version of `chain1012f.py`'s selftest took its list of wait files from the module-level `WAIT_FILES`, which in the outer selftest process (where `SELF` is false) names the REAL stage-5 exit files, so the selftest removed and then created
`...h53e-4_win2.exit` and `...h51e-4_nopredict_win2.exit` with the text "exit 0" while those two runs were live, and its inner driver waited for its own files forever, so the selftest hung. The runs never read those files and the stage-6 driver was not running, so nothing started early.
I stopped the hung selftest tree by pid, moved the two fake files to `void_mistaken_selftest/` (they are not exit files of anything), and fixed the selftest: it now creates or removes only its own `_wait_selftest_*` files (asserted), checks that the real files are untouched, and kills an inner driver that does not finish in 60 s.
A further slip: the original foreground loop kept running after I killed its first case and ran the remaining selftest cases concurrently with my rerun, which garbled a first set of results (`waited 30.5 s`, interleaved output); those numbers are void, and the rerun was made after no selftest process remained.

Addendum (10:30 UTC): the old foreground loop's later cases, still running the buggy selftest code, created a SECOND pair of fake exit files at 10:24:28 UTC after I had moved the first pair; I found them at 10:28 (their time stamps and "exit 0" text are not the drivers' format), moved them to `void_mistaken_selftest/FAKE2_*`, confirmed no selftest process remained, and reran the selftest from a clean state (the real exit files absent before and after): it passes and its three mutations fail (`logs/selftest_chain1012f.txt`; its wait threshold was loosened from 2 s to 1 s because the files appear 2.5 s after the launch and the first check was 2.0 s). The stage-6 waiting driver was launched at 10:30:23 UTC (pid 27060) and has started nothing; the stage-5 runs (a: pid 34140, b: pid 20036) are untouched and still running.

## The noise of r5, written down at 11:24 UTC 19 Nov before the measurement (the coordinator's hc, ~11:05 UTC, from xfchecks' #1021: M = 3 shows a residual whose noise exceeds what the step can resolve)

**Measurement** (`noise_r5.py`, `noise_chain.py`; `D:/choptuik-h9b`, rtol 1e-13, default steps, no `--predict`): at ONE fixed x, #1012 stage 1's XI 0.11 state at its second level-5 solve's |r_5| = 4.254e-5 (from the log, 9 decimals; its corrected |r_5| is 5.9e-3 once rounded), the Schur-corrected residual
(K from `leak_jac` at the nested-solved state, copied into a FRESH `Hier` per sample so that chord-Jacobian state cannot carry over) is recomputed after re-solving the nested levels 7 and 9 from starts perturbed by x (1 + rel u), u uniform(-1, 1), seed 1012. The spread of the corrected r_1, r_3, r_5, r_7, r_9 over the samples is the noise at that x.
- **Control A** (`noise_r5_zero`, done 11:23): identical starts, 3 repeats from fresh objects: the spread must be exactly 0 (it is: every row 0.000e+00, 23 s per sample, setup 84 s; K's largest row-5 entry 2.0e17).
- **Control B** (x5, rel 1e-12, 6 samples): perturbing the LEVEL-5 unknowns by 1e-12 relative must move r_5c by about K_55 dx_5 (about 2 expected from K = 2e17 and dx_5 ~ 1e-14 to 1e-15), i.e. clearly above the nested-start spread, else the measurement cannot see a signal.
- **The measurement**: nested starts at rel 1e-12 (16 samples) and at rel 1e-10 (16 samples). If the spread of r_5c is the same at both (within a factor 2) it is NOISE of the evaluation; if it grows with rel (about x100) it is the response to the perturbation, not noise.
- **Reading**, written now: the level-5 floor of 4e-5 to 1.4e-3 (every step, rtol and K setting tried) is explained by noise if the std of r_5c (either component) is at least 1e-5 and rel-independent; it is not if the std is below 1e-6. Between 1e-6 and 1e-5 is reported as unresolved. The omega error the noise induces needs M = 9's outer Jacobian, which does not exist here
  (M = 7's has singular values 1e4 and 5e3); the std of the corrected r_1 under the same perturbations is reported as the noise on the outer residual, and the translation to omega is left to the coordinator.

## The noise of the corrected r5 (results at 12:26 UTC 19 Nov; the reading was written at 11:24 UTC, before the data)

Fixed x: #1012 stage 1's XI 0.11 state at |r_5| 4.254e-5 (9 decimals; corrected |r_5| there 5.9e-3, raw 3.2e-2), rtol 1e-13, default steps, `--schur` with K from `leak_jac` at the nested-solved state (largest row-5 entry of K 2.0e17, K_55 block about 2.4e14), a FRESH Hier per sample.
Files: `noise_r5.py`, `noise_chain{,2,3}.py`, `noise_analyze.py`, `logs/noise_r5_*.{log,json}`, `logs/noise_analyze.txt`.

| corrected residual | std, nested starts at 1e-12 rel (16) | std at 1e-10 rel (16) | ratio | max deviation (1e-12) |
|---|---|---|---|---|
| r_5 (B5, C5) | 8.3e-4, 1.9e-4 (norm 8.5e-4) | 1.2e-3, 3.4e-4 (norm 1.2e-3) | 1.4, 1.8 | 3.4e-3, 4.4e-4 |
| r_3 (B3, C3) | 22.7, 6.7 (norm 24) | 28, 10 | 1.2, 1.5 | 96, 24 |
| r_1 (re, im) | 5.9e5, 4.9e5 (norm 7.7e5) | 7.0e5, 5.9e5 | 1.2, 1.2 | 2.4e6, 2.0e6 |
| r_7 (B7, C7) | 2.2e-7, 2.7e-7 | 3.3e-7, 3.4e-7 | 1.5, 1.2 | 5.6e-7, 8.2e-7 |
| r_9 (B9, C9) | 6.7e-10, 2.5e-10 | 1.3e-9, 1.7e-10 | 1.9, 0.7 | 2.5e-9, 7.0e-10 |

**Reading, against the cut written before the data:** the std of r_5c is above 1e-5 and the same at both perturbation sizes within a factor 2 (ratios 0.7 to 1.9 over all rows): it is the evaluation's NOISE, not a response to the perturbation.
It sits on the floor of level 5 (the 8e-5 to 1.4e-3 ends of every step, rtol and K setting, and 4e-5 as a lower tail), and the corresponding noise of the higher rows sits on those rows' ends: level 3's ends 7.6 and 21.5 (the two finished runs that reached level 5's floor, #999 XI 0.11 and stage 1; stage 5's first level-3 iterations are 31 and 13) against std 24, and |r_1| at those ends 5.8e5 and 1.2e6 against std 7.7e5 (the finished runs where level 5 had not reached its floor end higher: r_3 2e4 to 3e5, |r_1| 8e8 to 3e10).
So the runs end where their residual's noise is; nothing tried (step, rtol, nested steps, `--predict`) can lower an end below its noise.

**Controls, with the corrections they forced.** A (zero perturbation, 3 repeats from fresh objects): every row's spread exactly 0, passed. B (the level-5 unknowns at 1e-12 rel, 6 samples): I had written that r_5c must move by about K_55 dx_5 (about 2) and it moved by about 1e-3, so
**my expectation was wrong**: the corrected residual's slope in x_5 is the Schur complement, not K_55. B' (1e-9 and 1e-8 rel): the response was still at the noise, and my slope-fit check passed but its mutation (exchanging the two offset components of every sample) did NOT fail,
because that only permutes the fitted matrix's columns: the check could not fail and I replaced the mutation by one that breaks the pairing (`--mutate=shuffle`: median residual 1.01 and CHECK FAILED, against 0.01 on the real data). B'' (1e-7 and 1e-6 rel, the solver's own finite-difference step is 1e-6): the slope is clean,
S = [[1.20e7, 1.34e6], [-1.75e6, 1.17e7]] (singular values 1.22e7 and 1.17e7), the fit's median relative residual over the 8 samples above 10 x the noise 1%, max 28%. The Schur complement is 2e7 times smaller than K_55.
**x_5's resolution** the r_5 noise corresponds to: sigma / S = 7e-11 in B5 and in C5, 8e-9 and 5e-8 of their values.

**What it does not give:** the omega error. M = 9 has no outer Jacobian here (the corrected r_1's slope in (A, omega) at the inner-selected solution needs the dA and dw solves of M = 7's protocol, each noise-limited at M = 9); r_1's noise is 7.7e5 (std norm), 7 orders above M = 7's 0.02 to 0.3, and M = 7's J (singular values 1e4, 5e3) would turn it into an error of order 100 in (A, omega/omega_inf).
Whether M = 9's J is larger by those orders is unmeasured. One fixed x, one state of the rounded log values, 16 samples per setting.
