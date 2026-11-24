# I1025-dh610/kc87_leg_lambda: lambda_1 on dh370's k_c 87 leg states (tag l1kc87Ldh370), in rotation with macm3, dh170 and winb, one folder per D

Machine dh610 (Fedora 45, i7-12700, 20 logical CPUs, 62 GB RAM, Linux). Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1025. Written 2026-11-24 07:31 UTC, before any run of this folder. The k_c 87 roots are not yet physical. A root is identified by position, never by sign orientation (printed as the reader prints it, not compared across k_c).

## Order (coordinator t5, hc, 24 Nov), in part
"With your idle threads until 08:35 (8 processes, nice 10; the k_c 79 leg keeps priority when its state lands): join the k_c 87 lambda_1 rotation on dh370's leg (raw I1025-dh370/kc87_leg/, tag l1kc87Ldh370) with macm3, dh170 and winb: take the newest accepted state not yet taken by them (check I1025-macm3/kc87_leg_lambda/, I1025-dh170/kc87_leg_lambda/, I1025-win/kc87_leg_lambda/ on raw; winb takes D 21.09375). Per point: pin by blob, kc87_syscheck accept (controls exit 1, kc79 refusing), d18_hybsign 0.005 grid over +-0.015 around (your k_c 79 reading at that D + 0.002) plus a repeat of the middle, read_lower; prediction within 0.005 in the README first. Raw I1025-dh610/kc87_leg_lambda/<D>/."
Then, when I reported that no accepted state was free at 07:28 UTC and proposed D 21.125 (the next one, expected about 08:45 UTC): "agreed: D 21.125 when it lands, as you laid out; winb keeps D 21.09375."

## States on raw when this was written (origin/main 2026-11-24 07:31 UTC)
| D | pushed by dh370 | taken by |
|---|---|---|
| 21.03125 | 22bea94f | dh170 (scan since 05:52 UTC) |
| 21.0625 | 2b316941 | macm3 (its README of 07:14 UTC) |
| 21.09375 | not yet (expected about 07:40 UTC) | winb |
| 21.125 | not yet (expected about 08:45 UTC; dh370's points take about 3900 s with 6 threads, pushed a few minutes later) | me, when it lands |
I take a state only after checking the three rotation folders on raw for it at that moment.

## Method (the same for every D; `lane_k87l.sh D CENTER PRED`)
1. **Pin** by blob: `fetch_k87.sh D` takes the state `sol_l1kc87Ldh370_D<D:.6f>.npy` and the record `l1kc87Ldh370.jsonl` (it grows) from the commit that added the state, checks the blobs against git's, requires a record row of D with k_c 87, writes `<D>/in_blobs.txt` and `source_commit.txt`, and the pins are pushed before the scan. The scripts are the ones of my k_c 79 leg and k_c 87 D 21.0 lanes (`in/`, `in_blobs.txt`): `kc87_syscheck_1025.py` 6df5d960, `kc79_syscheck_1025.py` 29dce7ea, `d18_hybsign.py` e089207a (unmodified), `read_lower.py` 89309d3c, `repeat_check.py` aaf598a9, `leg_read.py` 5cae2639, `d185_scan_read.py` 7c9d400f, `d18c_read.py` 1383470f.
2. **Accept**: selftests (kc79_syscheck 0, kc87_syscheck 0, read_lower 0 and its two mutations 1 1, repeat_check 0, leg_read 0 and its mutation 1); `kc87_syscheck_1025.py` exit 0 on the state and the record row of D, `--mutate=F` and `--mutate=steps` exit 1 each, `kc79_syscheck_1025.py` on the same state exit 1 (refuses). Otherwise the lane stops and I report.
3. **Scan**: `d18_hybsign.py` at the grid centre -0.015 to +0.015 by 0.005 (7 values) and a repeat of the centre: 8 processes of 1 thread at nice 10, in `~/Source/choptuik-large-d-1025f` at 505d8399, code of `~/Source/choptuik-large-d-1025g` at 48c36355 for the check; python `~/Source/venv-i1058` (3.14.10). Every process must print "the record system". It refuses to start with less than 8 x 2.5 GB + 4 GB available; nothing is stopped or terminated for memory (Nathan's rule of 2026-11-08), the sampler only writes MEMALERT.txt below 4 GiB.
4. **Read**: `read_lower.py` on the window, `repeat_check.py` on the merged rows, `leg_read.py read` against the prediction with bar 0.005. The order has no widening: no robust change is reported as read. The estimator range is a spread over interpolation choices, not an enclosure; the bracket is the 0.005 grid step; the float64 sign is information, the hybrid sign is read.
Stop and report on any failure; change no code. `test_21.0625/` is a test of the lane on dh370's D 21.0625 state (macm3's point; `dry` and `check` modes only, 30 s on one thread, no scan): pins by the fetch (state blob f9a592e5 and record blob 3fb006df, the same as macm3's README names), selftests 0 0 0 1 1 0 0 1, `kc87_syscheck_1025.py` exit 0, both controls exit 1, `kc79_syscheck_1025.py` exit 1. The fetch's own control: with `K87_KC=79` it exits 2 (a record row of another k_c is refused), for a D not on origin it exits 1.

## Threads (stated before)
Now: the #1076 recount 2. When this scan runs: 8. When the k_c 79 leg's D 21.1875 state lands (about 08:35 UTC) its scan takes 8 more: 2 + 8 + 8 = 18 of 20 logical CPUs, so neither stops the other; if a third job were to start the sum would be checked first.

## D 21.125 (written before its pins and scan, 2026-11-24 07:31 UTC)
**Prediction (t5's rule):** my k_c 79 reading at D 21.125 (0.872088, `../kc79_leg/D21.125/`) + 0.002 (the k_c 87 minus k_c 79 step at D 21.0 was +0.002147, `../kc87_d21/`) = **0.874088**; the k_c 87 estimate (det-linear) within 0.005 of it.
**Grid:** centre = 0.874088 rounded to 0.005 = **0.875**; lambda 0.860, 0.865, 0.870, 0.875, 0.880, 0.885, 0.890 and a repeat of 0.875: 8 evaluations, one process each (p0..p6 the grid, p7 the repeat); window read `read_lower.py scan 0.860 0.890`.
**Command:** `bash start_k87.sh 21.125 0.875 0.8741` (unit `i1025-k87l-21_125`: waits for the state, pins, pushes the pins, takes the lock `/tmp/claude-1000/kc87_leg_lambda.lock`, runs the lane).
**Predictions (mine, before the run):**
- `kc87_syscheck_1025.py` accepts the state on this build with both controls exit 1 and the k_c 79 check refusing: 92%. All 8 processes print the record system: 90%. The repeat of 0.875 bit-identical: 92%. Every point noise-robust: 80%.
- Exactly one robust change in the window: 82% (none 10%, two or more 8%). Its det-linear estimate within 0.005 of 0.874088: 75%; within 0.002: 40%. The k_c 87 minus k_c 79 (0.872088) step in [0.000, 0.004]: 60%. Edge signs unequal: 85%.
- The float64 sign differs from the hybrid at one or more points: 65%.
- Seconds per point 3500 to 5200 s (60%; the k_c 87 points at D 21.0 took 3483 to 4845 s with 16 processes and the recount beside); the lane (pins line to the scan's end) within 1.8 h (65%). Peak RSS per process below 2.6 GiB (85%; D 21.0: 2.03 to 2.19 GiB).
- The D 21.125 state is on origin by 09:10 UTC (70%).

## Status
- 2026-11-24 07:31 UTC: folder, scripts (`fetch_k87.sh`, `lane_k87l.sh`, `wait_k87.sh`, `start_k87.sh`, `notify_k87.sh`), pins and README written and tested (`test_21.0625/`); the unit for D 21.125 is started after this README is pushed.
