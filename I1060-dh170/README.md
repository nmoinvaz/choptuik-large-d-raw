# I1060-dh170: #1060's step 17 of ks_chain3b (D 260.6706 -> 260.8483) rerun with --base_polish 0 on main 8179068d, dh170

Machine dh170 (Fedora 45, i7-7700, 8 logical CPUs, 31 GiB RAM). Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1060 (moved here from dh610's queue by the coordinator's hc, 21 Nov ~04:20 UTC;
dh610's step 1, comment 7056545751, raw `I1060-dh610` 94a868a0, did not reproduce the stored state: Delta differed by 1.188e-20, with a base polish moving 64 base entries by 5.4e-52).

## What this runs
dh610's `run1060.sh` command (blob 5549c544b87e, quoted below) with `--base_polish 0` added, as dh610's `run1060b.sh` (blob 3681bda29a3b) already does. `--threads 10` as leg 10 ran, `nice -n 10`, a 3 h cap by exact pid,
the main 8179068d build of #1058 on this machine (worktree `~/Source/choptuik-large-d-1058b`, clean at 8179068d, venv `~/Source/choptuik-large-d-1058b/.venv`, hpkernel with `set_exact_recip`), OUT `step17_s1_nobp/` in this folder.
Run script `run1060_dh170.sh` = `run1060b.sh` with paths and the cap only changed (diff in the log below); `report1060b.py` with its leg-10 path only changed; `cmp1060.py` (blob fce27737ee43) and `seriesdiff1060.py` (blob 762ce3d2fd64) unchanged.
State root `~/scratch1060/raw/`: the leg 10 files of raw origin/main bd0c3b93 (`I966-dh370/ks_chain3b/leg10_D256.1776_ks293/`: `anm_pin3_D260.6706.npz` (the input), `anm_pin3_D260.8483.npz` (the reference), `jet_pin3_D260.6706.npz`,
`pred_pin3_D260.8483.npz`, `anm_run.jsonl`, `anm_run.log`), each blob checked against its tree id with `git hash-object --no-filters` (all equal; the two states also equal the copies in `~/scratch949`).

Command (as `run1060_dh170.sh` runs it, from `~/Source/choptuik-large-d-1058b/hp`, `RAW=$HOME/scratch1060/raw`):

    anm_run.py $RAW <OUT>/step17_s1_nobp --state I966-dh370/ks_chain3b/leg10_D256.1776_ks293/anm_pin3_D260.6706.npz --kfreeze 3 --held_fit data/held_fit.json --N 31 --eps 1e-14 --h_max 2 --threads 10 --corrector od --tol_od 2e-34 --qd_it 40 --lam_stall 0.04 --od_junk 0 --jet_o 1 --reseed 2 --reseed_q 1 --held_o 1 --reseed_o 3 --save_pred 1 --od_accept natural --save_jet 1 --od_strong 4 --reseed_start pred --a_rule reseed --a_scale 0.00715 --jet_tangent_from 1 --series_split 1 --a_rise 1 --proj_start pred --reseed_o_stop 1 --od_floor_delta 1e-30 --proj_o 1 --reseed_qd_bar 1e-13 --steps 1 --ks 293 --keep_plan 0 --D_max 300 --base_polish 0

It is leg 10's own line (dh370's `run966m.sh chainm`, F3m + `--reseed_qd_bar 1e-13 --steps 400 --ks 293 --keep_plan 0 --D_max 266.1776`, `--series_split 1`) with `--steps 1`, `--D_max 300` and `--base_polish 0` (dh610's run1060.sh, same words without the last flag).

## Reading (the coordinator's, fixed before the run)
- **Equal bits** (D_str, `a`, Delta and the exactly summed parts, `cmp1060.py bits` exit 0): the base polish caused the 1.188e-20, and main 8179068d's build reproduces dh370's 1aa4a4fb chain step on Linux.
- **Unequal bits**, with this run's series row 0 equal to the stored base (the base unmoved): the build (1aa4a4fb python on the 40f4b4a5 kernel against main 8179068d) or the machine.
- Unequal bits with series row 0 moved even with `--base_polish 0`: neither reading applies; reported as it is (`report1060b.py`).
- Expected (the coordinator's addendum): equal bits. #586 ("Is the load's base polish the whole cause? #578's step with --base_polish 0", closed) found it: the coordinator's review there, 12 Nov: "The polish is the whole cause:
  without it the loaded step equals the in-memory one in every bit (the file hash differs only in the meta field source; the arrays' hash is the same, 69958b4298bc659a)." #587 and #593 resumed two chains exactly with `--base_polish 0`.
  What this run adds is the build and the machine: main 8179068d on Linux (dh170) against dh370's 1aa4a4fb.
- If `a` or D_str differ from leg 10's (no state at D 260.8483, or `cmp1060.py` prints "a equal False"): report both logs' step lines and stop (the script's own rule).

## Controls (the script runs them first and stops if one is wrong)
`cmp1060.py`: the stored state against itself identical (exit 0); one byte of z3 / z7 / z0 flipped must read DIFFERENT (exit 1); a planted 1e-120 shift agrees with `close` at 1e-100 (exit 0) and a planted 1e-90 shift does not (exit 1); `bits` against the planted 1e-120 differs.
`report1060b.py --selftest` (three branches of the reading) PASS and `--selftest --break` exits 1 (run 04:30 UTC before the start). `seriesdiff1060.py`'s own controls run inside the report (series against itself differs in 0 entries; one ulp moved differs in exactly 1).

## Resources
`/usr/bin/time -v` of the run (user, system, CPU %, maximum RSS) in `step17_s1_nobp.log`; `watch1060.sh` samples every 30 s into `memlog_1060.log` (alert-only: ALERT lines in `alert1060.log` at MemAvailable under 3, 2, 1 GiB; it stops nothing) and
applies the coordinator's priority rule (the anm_run python is reniced to 19 while the #1057 lane is reading a state, back to 10 after; `prio1060.log`). Beside it: the #1057 lane (2 threads, nice 10) and nothing else of mine.
Reference timing: dh610's step 1 (i7-12700, 20 threads) took 1275 s; this machine has 8 logical CPUs for 10 threads.

## Log
- 2026-11-21 04:30:57 UTC: folder prepared (copies of dh610's tools, derived scripts, leg 10 references); dh610's run1060.sh command and run1060b.sh command are equal apart from the OUT name and the added flag.
- 2026-11-21 04:32:03 UTC: **run started** 04:31:08 UTC (`run1060_dh170.sh` bash pid 1037330, /usr/bin/time pid 1037367, python 1037369; `watch1060.sh` pid 1037385): comparator controls all as required (`ctl_b/ctl_*.txt`: stored state against itself identical; one byte of z3, z7, z0 flipped DIFFERENT; planted 1e-120 agrees, 1e-90 disagrees; bits against the planted state DIFFERENT), the worktree is clean at 8179068d, hpkernel has set_exact_recip. The log says: "base polish skipped (--base_polish 0): the stored state is the base". Load at the start 0.10 (the #1057 lane idle). Memory at the start: MemAvailable 29.3 GiB.
- 2026-11-21 04:38:10 UTC: dh370's leg 13 step 2 (D 261.1415) queued 04:36 and its read started 04:37:16: `watch1060.sh` reniced the anm_run python 10 -> 19 at 04:37:40 (`prio1060.log`). Finding: the lane's near_null reads run at nice 19, not 10 (the lane was started under `nice -n 10` and `run1057.sh` adds its own `nice -n 10`, which adds up to 19), so anm_run at 19 gives the read an equal share, not priority. Fix after this read, between reads: stop the lane by its exact pids and start it again without the outer `nice` (reads then run at nice 10, anm_run at 19 during a read). A SIGSTOP of the anm_run is not used: its stall rules may read the wall clock.
- 2026-11-21 05:17 UTC: **correction on the priority rule.** `watch1060.sh` logged "nice 19 -> 10" at 05:06:43 UTC after the D 261.1415 read ended, but that renice did not take effect: an unprivileged user can raise a thread's nice, not lower it, and the script's `renice` output goes to /dev/null. The anm_run python has run at nice 19 since 04:37:40 UTC (`ps`: ni 19 at 05:15 and 05:16 UTC; the order said nice 10). Effect: wall time only (it yields to anything at nice 10 or lower), not the bits. The watcher is left running (editing a running bash script is unsafe); its later renices to 19 are no-ops. The lane was restarted between reads at 05:06:59 without the outer nice, so its reads run at nice 10 and take priority over the run at 19. The D 261.1415 read, at nice 19 beside the run at 19, took 1757 s (969 s for the previous state).
