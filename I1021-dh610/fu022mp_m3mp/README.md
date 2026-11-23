# I1021-dh610/fu022mp_m3mp: the --m3mp recount of #1021's 17 unresolved leaves (fu022mp pass 3's cache, argcount at feat/inner-mp 58108b67)

Machine dh610 (Fedora 45, i7-12700, 20 logical CPUs, 64 GB RAM, Linux). Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1076 (#1021's guard-blocked points valued with the M = 3 inner solve in extended precision). Written 2026-11-23 09:34:55 UTC, before any run of this folder. This is numerical evidence; the counts stay on hold until the sheet check of the new points (criterion 4 of `I1021-mac/fu022mp/README.md`).

## Order (coordinator t5, the #1076 comment 7096737456 and hc, 23 Nov), in part
"One recount with `--m3mp`, which values every point the walk needs that float64 leaves without value, inside the recount. Code: `feat/inner-mp` at 58108b67 (`argcount --m3mp`, `value_mp` with chord steps, `m3mp_check.py`), in a worktree. Inputs, pinned by blob at raw 81794560: cache `I1021-macm3/fu022mp/m3/points_M3_r0.17.jsonl` (3a12c814), seed `.../points_M3_r0.2.jsonl` (a0543a5c), cells `I1021-mac/rpi5_fu021/in/cells_unresolved11.jsonl` (07a872bb), `prefix_keys.py` (32ad6e19); copy the cache and seed into `I1021-dh610/fu022mp_m3mp/m3/`. Preflight: `m3mp_check.py <the pinned cache's pass-2 state>` (raw efed06f1's `points_M3_r0.17.jsonl`) with `--procs=2`; it must exit 0 (PASS); a failure stops the run. Recount, from `solver/inner_stokes`, as a `systemd-run --user` unit, nice 10, one BLAS thread, under `timeout 24h`: `argcount.py --M=3 --recount=<cells> --r1=0.17 --r1b=0.2 --seed=<OUT>/m3/points_M3_r0.2.jsonl --m3fix --m3maxrhs=2.4e6 --m3wall=3600 --m3noisecap=1e7 --procs=12 --retry --m3mp --out=<OUT>/m3 --tag=M3_fu022mp_m3mp_r0.17` (the record's arguments, plus `--m3mp`, with `--procs` 12 for the valuing; procs changes no value). Then: `prefix_keys.py` (fu021's cache to this one) must exit 0, with every later record of an old key a valued `fu: \"mp\"` row. Report: the unresolved count and the zeros (leaf_sum, located points), the number of mp rows (valued or not), and per-point seconds. Push at the end and every 2 h. Estimate: the first level is about 61 points at ~1000-2500 s each on 12 workers, so 1.5-3.5 h; deeper levels add more."
Memory alerts only (hc).

## Pass 3 as read by the coordinator (the starting point, raw 81794560, macm3)
17 unresolved leaves, leaf_sum 2 (a second zero of R_1 in the box A 3.41-3.66 x wf 0.21-0.31 at A 3.526538, wf 0.211482 at xi1 0.17), 61 new points guard-blocked, 5 more lost-S_3 points `--retry`d without value.

## Inputs (`in_blobs.txt` lists the `git hash-object --no-filters` blobs; the lane refuses any other)
| item | path here | blob |
|---|---|---|
| pass 3 cache (3605 lines) | `m3/points_M3_r0.17.jsonl` (the run appends to it) | 3a12c814 |
| seed | `m3/points_M3_r0.2.jsonl` | a0543a5c |
| cells | `in/cells_unresolved11.jsonl` | 07a872bb |
| prefix_keys.py | `in/prefix_keys.py` | 32ad6e19 |
| fu021's cache (the old side of prefix_keys; sha256 981f49fc... as `I1021-mac/fu022mp/SHA256SUMS_fu021`) | `in/fu021_points_M3_r0.17.jsonl` (raw I1021-rpi5/fu021/m3) | a4611080 |
| the pass 2 cache for the preflight (raw efed06f1, 3468 lines) | `in/points_M3_r0.17_efed06f1.jsonl` | 7512d5e8 |
Code: `~/Source/choptuik-large-d-1076`, detached at 58108b67 (branch feat/inner-mp), clean. Python `~/Source/venv-i1058/bin/python` (3.14.10, numpy 2.5.4, scipy 1.18.1, mpmath 1.3.0, python-flint 0.9.0).

## Commands (`lane_m3mp.sh` via `start_m3mp.sh` = systemd user unit i1076a under `systemd-inhibit` with the alert-only memory log; each step stops the lane when it fails)
1. Pins; refuses to start with less than 16 GiB available.
2. `argcount.py --selftest` (exit 0) and `--mutate=nosplit`, `--mutate=conj`, `--mutate=norecount` (exit 1 each), as the earlier #1021 runs did.
3. Preflight: `m3mp_check.py in/points_M3_r0.17_efed06f1.jsonl --procs=2` (its work folder under `tmp/`, not pushed): exit 0 and "m3mp check: PASS", else STOP.
4. The recount, the order's command, 12 processes of 1 thread (OMP, OPENBLAS, MKL = 1), nice 10, timeout 24h, log `logs/recount.log`, sampler `logs/sampler.log` every minute; outputs in `m3/` (the cache is appended after each batch; count file `count_M3_fu022mp_m3mp_r0.17.json`, leaves `leaves_M3_fu022mp_m3mp_r0.17.jsonl`).
5. `prefix_keys.py in/fu021_points_M3_r0.17.jsonl m3/points_M3_r0.17.jsonl` (exit 0 wanted) and its own control `--mutate=edit` (exit 1 wanted); then `summarize_m3mp.py` into `summary_m3mp.txt` (its selftest reads macm3's pass 3 and pass 2 count files as their comments say, and its `--mutate` must fail).
Progress pushes are snapshots of a cache an argcount process is appending to, so a pushed cache may end inside a line; the final push is the clean one.

## Acceptance (fixed before the run)
- Selftests as wanted; preflight exit 0 with PASS (else the recount is not started and I report it); the recount exits 0 (124 is the cap; I report it); `prefix_keys.py` exits 0 and its control exits 1.
- Reported: the unresolved count and the zeros (leaf_sum, located points at xi1 0.17 and 0.2), the mp rows (valued or not, from the cache's `valued`), the per-point seconds from the log, what each later record of an old key is (valued mp row, mp row without value, `--retry` row), and the wall.

## Predictions, registered before the run (information)
- Selftests `0 1 1 1` (95%); preflight PASS (85%), taking 10 to 35 min (60%; "about 25 min on the Mac" with 2 processes).
- The recount exits 0 within 24 h (80%); the first level's mp points take 1000 to 2500 s each as the coordinator estimates (60%); the whole run 2 to 8 h (55%).
- At least 70% of the mp rows are valued (60%).
- Unresolved leaves at the end: fewer than 17 (70%), 0 (20%), more than 17 (15%). leaf_sum is 2 or more (80%); the zero at A 3.5265, wf 0.2115 is still found (80%); no more than 3 zeros (85%).
- `prefix_keys.py` exits 0 (90%) and every later record of an old key is a valued `fu: "mp"` row (50%; the `--retry` rows of the five lost-S_3 points had no value in passes 1 to 3).

## Status
- 2026-11-23 09:34:55 UTC: folder, inputs, lane and summarizer prepared before any run. The reproducibility test of `../../I1025-dh610/repro_d1975` runs beside this: up to 8 threads of it and 12 of this, 20 in all, all at nice 10.
- 2026-11-23 10:16 UTC: **the recount stopped at once, exit 1, wall 0 s, cache unchanged (3605 lines)**, after the preflight printed "m3mp check: PASS" (10:15:57 UTC; 40 min: the two points valued in 1226 s and 2449 s). Cause: `argcount.py` line 359 at 58108b67 passes `repr(p[0])` of the walk's numpy float64 to `value_mp`, and under numpy 2 that is the string `np.float64(3.3185956)`, which mpmath cannot parse; the preflight's points are Python floats. Details in `logs/recount_failure.txt` and `logs/recount.log`, the proposed one-line change in `m3mp_float.diff` (not applied; the worktree is clean at 58108b67). Waiting for the coordinator.

## Attempt 2 (written 2026-11-23 10:19:20 UTC, before any run of it): the bug of attempt 1, and the new pin f860d30e
**The bug (attempt 1, code at 58108b67; its logs are in `logs/attempt1/`, the failure note in `logs/attempt1/recount_failure.txt`):** `Multiplier.mp_batch` in `argcount.py` passed `repr(p[0])`, `repr(p[1])`, `repr(r["F3re"])` and `repr(r["F3im"])` to `value_mp`; the walk's points are numpy float64, and under numpy 2 (2.5.4, the `requirements.txt` pin) their `repr` is `np.float64(3.3185956)`, which `mpmath.mpf` rejects (`ValueError`). `m3mp_check.py` passed (10:15:57 UTC) because its points were Python floats; the recount stopped at once (exit 1, wall 0 s, cache unchanged at 3605 lines). I proposed `m3mp_float.diff` (kept here, superseded).
**The coordinator's reply (hc, "my bug"):** fixed on the branch at **f860d30e**: `mp_batch` passes `repr(float(...))` for the point, F_3 and r_1, and `m3mp_check.py` now uses numpy float64 points, as the walk passes them, so the preflight covers that path. The new commits since 58108b67 are c234fb8a (adds `zero_mp.py`, not used by the recount) and f860d30e (the fix; `git diff --stat 58108b67 f860d30e`: `argcount.py` 6 lines, `m3mp_check.py` 6, `zero_mp.py` 102 new). The order: option (1), a fresh worktree at f860d30e (clean), the preflight on the same pass-2 cache with `--procs=2` (must PASS), then the same recount command (12 processes, `--m3mp`, timeout 24h), `prefix_keys.py` and its edit control; "if the walk path shows any other error, stop and report it the same way".
**What changed in this folder:** code is now `~/Source/choptuik-large-d-1076b`, detached at f860d30e, clean (the lane pins it); the unit is i1076b; nothing else differs (inputs, pins, commands, acceptance and the reading of the first attempt stand). The attempt 1 predictions stand for the recount; new ones:
- The preflight, now on numpy float points, passes (90%) in 25 to 60 min (attempt 1: 40 min).
- No further error in the walk path before the first extended-precision point of the recount is valued (75%); if there is one, the lane stops and I report it.
