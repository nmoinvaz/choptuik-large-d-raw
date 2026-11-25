# I1078-dh370/m160_root: the matched determinant's root at D 3.044375, M' 160 (gamma and its change from M' 96)

Written 2026-11-25 about 02:35 UTC by the clock, before any run of this folder. Machine `dh370-fedora` (Fedora, i7-8700, 6 cores / 12 threads, 31 GB). Issue #1078 (the sign of det M(lambda) at D 3.044375; the matched determinant of #1083). Coordinator t5's order (hc, 2026-11-25 after 02:32 UTC), to split #1078 with win2's t25, which keeps M' 96 and M' 128.

## Order (t5's)
"#1083 PASSES all four criteria; I close it. Next, #1078 at M' 160 ...: the true root of the matched determinant at D 3.044375 at M' 160. M' 96 gave lambda 6.3317279956246395 (gamma 0.15793476926), with one sign change on a 0.25 grid from 4.5 to 7.5 (win2, #1078). State: raw I1072-dh370/in3/tmap_lowDhm_x0.000157-0.975_D3.0444_M384_L0.4_M160_s1.9635.npz, pinned by blob. In your ~/Source/choptuik-large-d-1083 worktree with the #1082 venv: HP_DENSE_M_MAX=160 python3 mode_matched.py four <O>/four_M160.jsonl <state> --threads=6 first (must show sign -1, one smooth line, like M' 96). Then python3 mode_matched.py root <O>/root_M160.jsonl <state> --lam0=6.3317279956 --threads=6 (6 threads, nice 10). Raw I1078-dh370/, README first. Dense matrices of about 1.3 GB each, alerts only. Report the root, gamma, and gamma(M' 160) - gamma(M' 96), with #1078's bar: 1e-8 between M' 128 and 160."

## Pins
- State `I1072-dh370/in3/tmap_lowDhm_x0.000157-0.975_D3.0444_M384_L0.4_M160_s1.9635.npz`, git blob **9ccd7a9e** (raw origin/main at 02:34 UTC; copied to `in/`), 361814 bytes.
- Code: worktree `~/Source/choptuik-large-d-1083` at 7c6177e1 (wip/mode-horizon-1083), `hp/mode_matched.py` blob 3dd81b39, the same as #1083 part 2 (`../../I1083-dh370/`). Python: the #1082 venv `~/Source/choptuik-large-d-1082/.venv/bin/python` (a9975061 build). Run from the worktree's `hp/`.
- Reference at M' 96 (t5/win2): lambda 6.3317279956246395, gamma = 1/lambda = **0.15793476925904296** (`cmd_root` writes gamma = 1/lam).

## Commands (as ordered; the details I add are marked)
1. `four`: `HP_DENSE_M_MAX=160 python mode_matched.py four $O/four_M160.jsonl <state> --threads=6`, `OMP/OPENBLAS/MKL_NUM_THREADS=6`, nice 10. Its default lambda are the four at 5.1408197887857 ... 5.1408197887866 of #1083 (criterion 1), where the M' 96 state gave f = [-1, -1.00000000005, -1.0000000001, -1.00000000014], line residual 4.4e-13, pivot ratio 5.2e-8 (`../../I1083-dh370/2_four.log`).
2. `root`: `python mode_matched.py root $O/root_M160.jsonl <state> --lam0=6.3317279956 --threads=6`, nice 10. **Mine:** the same `HP_DENSE_M_MAX=160` in its environment (the order shows it for `four` only; `python/hpkernel/driver.py` line 33 reads it as the dense-matrix size cap, default 128, and M' 160 is above it), default `--xtol=1e-11` (the `find_lam` tolerance, 1e-11 in lambda), matched layout (`--match=valley`, the default), without `--both` (D_out is noise at this D, #1082/#1083).
3. A systemd user unit `i1078m160` under `systemd-inhibit`, nice 10; `run_m160.sh`. Caps (mine): `four` 8 h, `root` 24 h (M' 96's determinants took about 790 s; M' 160's are expected at 4 to 5 times that). The gate between the two: `four` must exit 0 and print all four f negative (sign -1), otherwise the chain stops and I report.

## Registered reading, before the runs
- `four`: PASS as at M' 96: sign -1 at the four lambda, line residual at most 1e-6 (criterion 1), pivot ratio above 1e-20. A different sign or a line residual above 1e-6 stops the chain.
- `root`: one sign change in the first bracket, lambda near 6.33; gamma = 1/lambda; report lambda, gamma, **gamma(160) - gamma(96)** against the M' 96 value 0.15793476925904296. #1078's bar is 1e-8 between M' 128 and M' 160 (win2 has M' 128); I do not have M' 128, so I report the 160 - 96 difference and make no statement about the bar. An error bar on lambda is `find_lam`'s `xtol` 1e-11 (a bracket tolerance, not an enclosure; a spread over plan or layout choices is not included).
- Controls: none ordered at M' 160. The matched layout's controls (`four --match=out` must exit 1; the planted root and its two controls) were run at M' 96 in #1083 on this same code; I state that and do not claim them at M' 160.
- Cost, before the first determinant: M' 96 took 790 s per determinant (4 threads' worth of memory-bound LU at 6 threads); M' 160 with matrices of 1.3 GB each is estimated at 3000 to 4000 s per determinant: `four` 3.5 to 4.5 h, `root` 5 to 10 determinants, 4 to 11 h. The first determinant's time replaces this.
- Memory: about 1.3 GB per dense matrix, a few at once (estimate 6 to 10 GB peak); `i1088a-build2` (t5's subagent, a build with timeout 4 h) runs beside. Memory watchers alert only; nothing is killed.
- Load: this job takes 6 threads, the #1080 walk d about 1.3 cores, `i1088a-*` as t5 sets; the total is above the 6 threads of the earlier arrangement. t5's order says 6 threads.

## Status

- Gate check before the run: the gate's parser (`run_m160.sh`) exits 0 on #1083's M' 96 `2_four.log` (f all negative) and 1 on its control `2b_four_match_out.log` (f = [1, 63.3, -3.27, 0.037]).

- 2026-11-25 02:35:42 UTC: `run_m160.sh` started as unit `i1078m160` (see `steps.txt`).

## Amendment 1 (t5's hc, 2026-11-25 shortly after 02:40 UTC; recorded before the change)
"Skip 'four' at M' 160 to save ~4 h: the matched determinant is validated at M' 96 on two machines. Go straight to root with HP_DENSE_M_MAX=160 and --lam0=6.3317279956, and replace the four-gate by the root's own check (one sign change, its pivot ratio printed). Watch memory beside i1088a-build2 (alert only); if MemAvailable falls under 2 GB, say so at once."
- `four` was running (unit `i1078m160`, started 02:35:42 UTC, no determinant finished); by this order I stop that unit (`systemctl --user stop`: TERM to its process group) and start `root` alone. Its partial files are kept as `four_M160_stopped_by_order.*`. M' 160 has no `four` reading; the matched layout's checks are #1083's, at M' 96.
- The root's own check replaces the gate: **one sign change in the first bracket** (`root of D_m ... (N sign changes in the first bracket, ...)`, N = 1) and **the pivot ratio** (smallest over the determinants of pivot_min / pivot_max, printed on each determinant line; the bar of criterion 1 is above 1e-20). It is read after the root ends (`root_check.txt`), not before it starts; the parser fails on a log with two sign changes (tested on a copy of #1083's step 3 log with the count changed to 2).
- Memory (alert only, nothing killed): MemAvailable under 2 GB is reported to t5 at once.
- New unit `i1078m160b`, script `run_m160b.sh`: `root` alone, 6 threads, nice 10, `HP_DENSE_M_MAX=160`, `--lam0=6.3317279956`, default `--xtol=1e-11`, cap 24 h.

## Pause for the build's memory (t5's hc, 2026-11-25 about 02:43 UTC)
t5: "pause: SIGSTOP your M' 160 root by exact pid now, and SIGCONT it when i1088a-build2 has ended (its rustc gone). Record both times in the README." The rustc of `i1088a-build2` (pid 2440227) held 25.2 GB at 02:41 UTC, MemAvailable 2.7 GB and falling.
- **SIGSTOP** to pid 2441418 (the python of `mode_matched.py root`, resident 0.42 GB, the first determinant 5 min in) at **2026-11-25 02:42:55 UTC** (`steps.txt`). Nothing was killed; its `timeout 86400` wrapper keeps counting wall time (cap 24 h, the pause is expected to last about 20 to 25 minutes).
- **SIGCONT** to pid 2441418 at **2026-11-25 03:13:40 UTC** (t5's hc: "resume now (SIGCONT by exact pid); the peak is past"), the rustc of `i1088a-build2` (pid 2440227) still alive at 2.8 GB resident, MemAvailable 24.8 GB. Paused from 02:42:55 to 2026-11-25 03:13:40 UTC. (The watcher armed to resume at the rustc's exit will find the process running and send nothing.)

## First determinant (2026-11-25 04:33 UTC)
`lam 6.331627995600: sign -1 ln|det| 1285.272457 pivots 1.01e-04..1.58e+02 (5880.0 s)`: the first point of `find_lam` is lam0 - 1e-4 (lam0 = 6.3317279956); sign **-1** as at M' 96 below the root, smallest pivot ratio 6.4e-7 (bar 1e-20). The 5880 s is wall time and includes the 1845 s of the pause (SIGSTOP 02:42:55 to SIGCONT 03:13:40), so about 4035 s of running: 5.1 times M' 96's 790 s, at 3.7 cores shared with t5's `form_s.py jump` and the #1080 walk d (load 11 to 13) against 6 at M' 96. The root needs at least 5 determinants (5 at M' 96's D 3.15 in #1083 step 3, 10 to 11 in `d315`): expect 6 to 12 h more.
