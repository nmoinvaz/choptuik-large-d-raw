# I1025-win/kc87_leg_lambda: lambda_1 on dh370's k_c 87 leg states (tag l1kc87Ldh370), in rotation with macm3 and dh170 (winb)

Machine `surface-laptop-4` (Windows 11, 4 cores, 32 GB; runner winb). Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1025. Written 2026-11-24 07:30 UTC, before any run of this folder; the D 21.125 part added ~09:27 UTC, before that run. This file is the index and the method; each state has its own folder `<D>/` with its README (written before that scan), outputs and result.

## Order (the coordinator t5's hc of 2026-11-24 ~07:22 UTC, the winb part, quoted)

"Next task: lambda_1 on dh370's k_c 87 leg states (raw I1025-dh370/kc87_leg/, tag l1kc87Ldh370; dh370 pushes each accepted state), in rotation with macm3 and dh170: take D 21.09375 when it lands (~07:40 UTC), then each time the newest state not yet taken by them (check I1025-macm3/kc87_leg_lambda/ and I1025-dh170/kc87_leg_lambda/ on raw). Per point: pin by blob, kc87_syscheck_1025.py accept (controls exit 1, kc79 refusing), d18_hybsign 0.005 grid over +-0.015 around the prediction plus a repeat of the middle, read_lower. Prediction (README first): k_c 79's reading at that D + 0.002, within 0.005 (D 21.09375: 0.8837 from k_c 79's 0.881686). Raw I1025-win/kc87_leg_lambda/<D>/."

Taken by the others so far (raw, 07:36 UTC): macm3 D 21.0625 (`I1025-macm3/kc87_leg_lambda/21.0625`, one change 0.894588), dh170 D 21.03125 (`I1025-dh170/kc87_leg_lambda/21.03125`). **t5's second hc (~07:36 UTC, quoted):** "your k_c 87 state is on raw: dh370's D 21.09375, commit 6fdda342, I1025-dh370/kc87_leg/sol_l1kc87Ldh370_D21.093750.npy blob e32cefac, record l1kc87Ldh370.jsonl blob fad4c79a. Prediction (README first): 0.8860 within 0.005 (macm3's k_c 87 0.894588 at D 21.0625 - 0.28 x 0.03125). After it macm3 takes every later point, so report and stop." So the first point is D 21.09375 alone, and its prediction is the second hc's 0.8860 (the first hc's 0.8837 is replaced).

**t5's third hc (~09:23 UTC, after the D 21.09375 reading 0.885927, quoted):** "One more point, a build check: dh370's k_c 87 state at D 21.125 (raw commit 4ab4abcb: I1025-dh370/kc87_leg/sol_l1kc87Ldh370_D21.125000.npy blob 078ab7d8, record l1kc87Ldh370.jsonl blob 8046644b), the same state macm3 read on macOS (0.877108). Same pipeline; d18_hybsign 0.865-0.890 by 0.005 plus a repeat of 0.875. Written before (README first): within 0.002 of macm3's 0.877108 (the build spread at k_c 87). Raw I1025-win/kc87_leg_lambda/21.125/. Then report and stop." So the series is two points: D 21.09375 (read) and D 21.125 (the build check).

## Method (the same for every D)

1. **Pins.** The state and the record come from dh370's raw commit that pushed the state (`git show <commit>:I1025-dh370/kc87_leg/<file>`), are hashed with `git hash-object --no-filters` and compared with git's blob ids. The scripts are pinned by blob as in the table below. `prep_pins_1025.txt` in each folder lists every blob.
2. **State check** (the driver stops and hc's t5 if any is not as written): the selftests of `kc87_syscheck_1025.py` and `kc79_syscheck_1025.py` exit 0; `kc87_syscheck_1025.py` accepts the state (exit 0: the record is k_c 87 at D, its |F| at most 1e-9, the state's |F| within 1% of the record's, `freeze_from` gives the record's step count); `--mutate=F` and `--mutate=steps` exit 1 each; `kc79_syscheck_1025.py` on the same state exits 1 (refuses it: not k_c 79).
3. **Scan.** `d18_hybsign.py` (e089207a, unmodified) at the grid of 7 values over +-0.015 around the prediction (0.005 apart) plus a repeat of the middle value: 8 evaluations in 4 processes of 1 thread (two rounds, the repeat on another process than the first), BelowNormal, cap 10800 s by exact pids, started outside my terminal (`Win32_Process.Create` of `conhost.exe --headless cmd.exe /c go_kc87_1025.cmd`), a keep-awake helper (`SetThreadExecutionState`, power plan untouched), an alert-only memory watcher (hc to t5 below 1 GB free; kills nothing), a sampler (60 s). Every process must print "the record system" first (exit 3 and no reading otherwise).
4. **Read.** `read_lower.py` (89309d3c) with its selftest and the controls `--mutate=shift` and `--mutate=round2` (exit 0, 1, 1), then the reader on the window. The driver hc's t5 every line the reader printed. Roots are read by position, never by sign orientation. I do not interpret; t5 rules.

## Pins (common)

| item | raw path | blob |
|---|---|---|
| k_c 87 check | `I1025-dh610/kc87_d195/in/kc87_syscheck_1025.py` | 6df5d960 |
| k_c 79 check (must refuse a k_c 87 state) | `I1025-win/kc79_d19/kc79_syscheck_1025.py` | 29dce7ea |
| scanner, change finder | `I1025-mac/d18/d18_hybsign.py`, `I1025-mac/d18/d185_scan_read.py` | e089207a, 7c9d400f |
| reader | `I1025-dh170/lower_root/read_lower.py` | 89309d3c |
| code | the worktree `choptuik-i1025k79` at 48c36355 (`dss_ell.py`, `ell_ddm.py`, `ell_dd.py`, `ddnp.py` equal 505d8399's) | |

## States

| D | dh370's commit | written before (prediction) | window | status | result |
|---|---|---|---|---|---|
| 21.09375 | 6fdda342 (pushed 2026-11-24 07:35:57 UTC) | one change within 0.005 of 0.8860 (t5's second hc) | 0.870 to 0.900 | finished 09:23:16 UTC (scan 07:38:16 to 09:23:16, 6300 s, exits 0,0,0,0); raw dc563392f, #1025 comment 7127502443 | one robust change, - to +, det-linear 0.885927, range [0.885587, 0.885927] (reader line as printed; met by position, t5 rules) |
| 21.125 | 4ab4abcb (pushed 2026-11-24 08:44:24 UTC) | build check: one change within 0.002 of macm3's 0.877108 (t5's third hc) | 0.865 to 0.890 | finished 11:03:17 UTC (scan 09:27:17 to 11:03:17, 5760 s, exits 0,0,0,0); raw 9f1d5c3ec, #1025 comment 7129645338 | one robust change, - to +, det-linear 0.877108, range [0.876464, 0.877108] (reader line as printed; equal to macm3's macOS 0.877108; met by position, t5 rules) |
