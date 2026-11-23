# I1025-dh610/kc79_leg: lambda_1 on each point of win2's k_c 79 leg (`I1025-win2/kc79_leap`, tag l1kc79Lw1025d), one subfolder per D

Machine dh610 (Fedora 45, i7-12700, 20 logical CPUs, 64 GB RAM, Linux). Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1025. Written 2026-11-23 16:59 UTC, before any run of this folder. The k_c 79 roots are not yet physical.

## Order (coordinator t5, hc, after `../kc79_d205_fine`, raw 6b99c854; the #1025 comment of "17:45", posted 16:54Z), in part
"D 20.5 accepted (raw 6b99c854); ell1_best now 1.07787 +-0.0026 (main 2cacf13d). Next, beside the recount (8 threads, nice 10), #1025 comment of 17:45 UTC: lambda_1 on each point of win2's k_c 79 leg (raw kc79_leap/states, l1kc79Lw1025d), from point 3 (D 20.84375, ~17:55) on: pin state and record by blob, kc79_syscheck_1025.py (controls exit 1), d18_hybsign on a 0.005 grid over +-0.015 around the prediction plus a repeat of the middle point (as kc79_d205_fine), read_lower. Predictions (README before each): D 20.84375 0.958, 20.875 0.947, 20.90625 0.936, each +-0.01. No change in the window: widen once by 0.015 toward the end signs, then report. Raw I1025-dh610/kc79_leg/<D>/, README first. Report each point."
The comment: "macm3 keeps D 20.8125, already running, and then works only on #1079"; "Predictions come from the best rows (slope about -0.345 per unit D past D 20.5)"; "A point with no change in its window is widened once by 0.015 on the side its end signs point to, then reported."
Memory alerts only (standing rule).

## Method, per point D (`lane_leg.sh D CENTER PRED`, one lane at a time under a lock: 8 threads beside the #1076 recount's up to 12, 20 at most, all at nice 10)
1. **Pin** win2's state `states/sol_l1kc79Lw1025d_D<D:.6f>.npy` and the record file `states/l1kc79Lw1025d.jsonl` by git blob, as they are in the commit that added the state (`fetch_point.sh`, from origin/main of the raw repo after a fetch; `D<D>/in_blobs.txt`, `D<D>/source_commit.txt`); the pins are pushed before the scan starts. The leg's commits carry state and record together.
2. **Accept** the state: `kc79_syscheck_1025.py` (blob 29dce7ea) on the record row of D and the state (exit 0; `--mutate=F` and `--mutate=steps` exit 1). A refusal stops the lane and I report it.
3. **Scan:** `d18_hybsign.py` (e089207a, unmodified) at CENTER-0.015 to CENTER+0.015 by 0.005 (7 values; CENTER is the multiple of 0.005 nearest the prediction) plus a repeat of CENTER: 8 evaluations on 8 processes of 1 thread, nice 10, in `~/Source/choptuik-large-d-1025f` at 505d8399; each process prints the record system first (exit 3 if not).
4. **Read:** `read_lower.py` (89309d3c) on the window, `repeat_check.py`, `leg_read.py read` (the change by position beside the prediction, bar 0.01; selftest exit 0 and `--mutate` exit 1 first).
5. **No robust change in the window:** widen once by 0.015 (three values at 0.005 steps) toward the window edge where the hybrid ln|det| is lower (`leg_read.py widen`; |det| falls toward a root, which then lies beyond that edge), run them (3 processes), read the widened window, report. **My reading of the order's "the side its end signs point to":** with equal end signs the signs themselves name no side, and the orientation of a sign change differs between D's and builds (at k_c 79: dh170's D 20.375 reads "+ to -", D 20.5 "- to +"), so the ln|det| trend is used; the reading prints the end signs, and I compare the side with the previous point's printed orientation and report it if the two disagree. One or several robust changes: reported as read, no widening; several: no pairing, I report them all.
Code: `ell` pieces as in `../kc79_d205_fine` (`~/Source/choptuik-large-d-1025g` at 48c36355 for the check, `~/Source/choptuik-large-d-1025f` at 505d8399 for the scan); python `~/Source/venv-i1058/bin/python` (3.14.10, numpy 2.5.4, scipy 1.18.1, multidouble 5.1.0 avx2).

## Inputs (`in/`; `in_blobs.txt`; the lane refuses any other blob)
| item | blob |
|---|---|
| `kc79_syscheck_1025.py`, `d18_hybsign.py` (xfkappa's), `read_lower.py`, `d185_scan_read.py`, `d18c_read.py`, `repeat_check.py` | 29dce7ea, e089207a, 89309d3c, 7c9d400f, 1383470f, aaf598a9 |
| `leg_read.py` (mine; selftest exit 0, `--mutate` exit 1) | in `in_blobs.txt` |
Per point: win2's state and record (`D<D>/in_blobs.txt`).

## Pilots (before any point; `pilot_D20.8125/`, nothing of it is a result)
- `pilot_D20.8125/check*.txt`: `kc79_syscheck_1025.py` on win2's published D 20.8125 state and record (blobs 141bc9bc, b60b5403; commit c39988cb) on this build: ACCEPTED (record |F| 4.6705546488e-10, the state's 4.6692192516e-10, 2696 steps = the record's), `--mutate=F` exit 1, `--mutate=steps` exit 1. The leg's states pass the check on Linux. (D 20.8125 is macm3's; no scan here.)
- `pilot_D20.8125/fake_scanner_lane_test/`: the lane run end to end on that state with a stand-in scanner (planted rows, written for the test, no determinant evaluated): one run without a sign change (the lane reads no change, picks the high side, runs three more values, reads the widened window 0.945 to 0.990 and reports) and one with a planted change (read as one change, 0.957500, within 0.01 of 0.958, no widening). The scan is replaced, everything else is the production lane.

## Predictions of the coordinator (written before each run) and the windows
| D | prediction (+-0.01) | grid centre | window (7 values) | if widened low | if widened high | state expected on origin |
|---|---|---|---|---|---|---|
| 20.84375 | 0.958 | 0.960 | 0.945 to 0.975 | 0.940, 0.935, 0.930 | 0.980, 0.985, 0.990 | about 17:55 UTC |
| 20.875 | 0.947 | 0.945 | 0.930 to 0.960 | 0.925, 0.920, 0.915 | 0.965, 0.970, 0.975 | about 19:15 UTC |
| 20.90625 | 0.936 | 0.935 | 0.920 to 0.950 | 0.915, 0.910, 0.905 | 0.955, 0.960, 0.965 | about 20:35 UTC |
Win2's cadence on this leg is about 80 minutes a point (D 20.78125 pushed 15:10 UTC, D 20.8125 at 16:34 UTC), so the three states land at about 17:55, 19:15 and 20:35 UTC; a point takes me about 40 minutes (one round of 8 evaluations, one more round if widened). Beyond D 20.90625 the prediction of each point is written in its README before its run from the previous point's measured root minus 0.345 x 0.03125 = 0.0108 (the order's slope), bar 0.01, and told to the coordinator in the report of the previous point.

## Results (filled after each point)
| D | state commit | source check | window | robust change (det-linear, bracket) | minus prediction | repeat | verdict |
|---|---|---|---|---|---|---|---|

## Status
- 2026-11-23 16:59 UTC: folder, pilots, lane and the reading prepared before any run; units for D 20.84375, 20.875 and 20.90625 wait for their states on origin.
