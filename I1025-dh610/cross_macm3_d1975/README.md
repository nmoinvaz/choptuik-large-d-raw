# I1025-dh610/cross_macm3_d1975: macm3's k_c 87 D 19.75 state evaluated on Linux at lambda_1 1.32, 1.33, 1.34, to find whether the state or the determinant's evaluation differs between builds

Machine dh610 (Fedora 45, 20 logical CPUs, 64 GB RAM, Linux). Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1025. Written 2026-11-23 05:39:51 UTC, before any run of this folder.

## Order (coordinator t5, the #1025 comment 7092564937 "The D 19.75 split is the build, and a cross-check of which part" and hc), in part
dh170's k_c 87 on Linux, round 1 (raw I1025-dh170/kc87_d1975), puts the root near lambda_1's line at 1.325410, in (1.32, 1.33); dh170's k_c 79 is 1.326378 (Linux). macm3's k_c 87 is 1.338993, in (1.33, 1.34) (macOS, regridded
from the same k_c 79 state with the same command). At lambda 1.33 the two builds' hybrid signs differ, each noise-robust by its own test. **Which part differs: the regridded state, or the determinant's evaluation?** Each build
evaluates the other's state at the same lambda. dh610 (Linux), beside its D 19.75 k_c 95 scan: pin macm3's accepted k_c 87 D 19.75 state and record (raw I1025-macm3/kc87_d1975/, at 03c79c79 or later). dh610's
`kc87_syscheck_1025.py` must accept them on Linux (|F| and steps as recorded). Then run `d18_hybsign.py`, unmodified, on that state at lambda 1.32, 1.33 and 1.34: 3 processes of 1 thread, nice 10, each printing the record
system. Report each lambda's hybrid sign, noise signs, float64 sign and ln|det|, beside macm3's values on its own state (its scan files) and dh170's on the Linux state. Memory alerts only. (macm3 does the same on dh170's state
352107a8 / record 6078a0b4, after its #1076 pass.)

**Written before the runs (the coordinator's, put here as ordered):**
- Linux on macm3's state gives macm3's signs: the states differ, and the determinant code agrees across builds. Then a 7×10⁻⁶ difference between two regrids moves the root by 0.014 at D 19.75. lambda_1 there is then fixed only to about that much, unless the states are converged further.
- Linux on macm3's state gives Linux's signs: the macOS evaluation of the determinant differs, and macOS's roots past D 19.5 are not used until the cause is found.

## Inputs (copies in `in/`; `in_blobs.txt` lists their `git hash-object --no-filters` blobs; the lane refuses any other blob)
| item | source | blob |
|---|---|---|
| macm3's k_c 87 D 19.75 state (accepted by its VERDICT 23:55:54 UTC 22 Nov) | I1025-macm3/kc87_d1975/sol_l1kc87macm3d1975_D19.7500.npy at raw 03c79c79 | 5825f5d0 |
| its record: D 19.75, k_c 87, \|F\| 3.980170323712351e-10, 3124 steps, Delta 1.086003680648846 (source dh170's k_c 79 state) | same folder, l1kc87macm3d1975.jsonl (blob equals dh170's copy `ref_macm3_l1kc87macm3d1975.jsonl`) | 84f75a48 |
| macm3's scan of its own state (16 points, 1.26 to 1.40, repeat of 1.33), for the comparison | same folder, scan/scan_D19.75_1025.jsonl, copied as `in/ref_macm3_scan_D19.75_1025.jsonl` | 702717f3 |
| my k_c 87 check; the scanner (xfkappa's, unmodified) | I1025-dh610/kc95_d1975/in/ (= kc87_d195/in/) | 6df5d960; e089207a |
| the comparison script (mine), with its selftest and a mutation control | `compare_cross.py` | 93d5e98d |
dh170's rows on the Linux state are not in raw yet (his folder has the `scan/scan_p*.raw` of the start only); they go into the comparison as `in/ref_dh170_scan_D19.75_1025.jsonl` when they are pushed, and until then his signs are the order's: his root is in (1.32, 1.33), macm3's in (1.33, 1.34), so at 1.32, 1.33, 1.34 his signs are -, +, + (derived, labelled so in the output).
Code: scan worktree `~/Source/choptuik-large-d-1025f` at 505d8399 (clean), check worktree `~/Source/choptuik-large-d-1025g` at 48c36355, python `~/Source/venv-i1058/bin/python` (3.14.10, numpy 2.5.4, scipy 1.18.1, multidouble avx2).

## Commands (a systemd user unit `i1025x` under `systemd-inhibit`, `lane_cross.sh` via `start_cross.sh`)
1. Pins; selftests (`kc87_syscheck_1025.py --selftest` 0, `compare_cross.py selftest` 0, `selftest --mutate` 1); MemAvailable at least 3 x 4 GB + 4 GB or no start.
2. **Check:** `kc87_syscheck_1025.py l1kc87macm3d1975.jsonl sol_l1kc87macm3d1975_D19.7500.npy 19.75 <worktree>/solver/matter`, with `--mutate=F` and `--mutate=steps` (both must exit 1). Anything else stops the lane before the evaluations.
3. **Evaluations:** in `solver/matter` of the scan worktree, one process per lambda, nice 10, 1 thread each (OPENBLAS/OMP/MKL threads 1):
   `d18_hybsign.py in/l1kc87macm3d1975.jsonl in/sol_l1kc87macm3d1975_D19.7500.npy 19.75 <1.32|1.33|1.34> run/xscan_D19.75_p<p>.jsonl`; each process prints the record system first; cap 28800 s by `timeout -s TERM` (a time cap only).
4. `compare_cross.py run/xscan_D19.75_1025.jsonl in/ref_macm3_scan_D19.75_1025.jsonl [dh170 rows]` writes `compare.txt`.

## Acceptance (fixed before the run)
- The check accepts macm3's state on Linux: exit 0 (|F| at most 1e-9, `freeze_from` gives 3124 steps = the record's, the state's |F| within 1% of the record's 3.980170324e-10); `--mutate=F` and `--mutate=steps` exit 1. A control that fires stops the work, and I report it; no bar is loosened.
- Each of the three processes prints "the record system" (a first line of the same form as in the scans: |F| and steps beside the record's). Otherwise that point is not read.
- The reading is the two lines above, applied to the three hybrid signs: **A** all three equal macm3's (-, -, +); **B** all three equal dh170's (-, +, +); **neither** otherwise (reported as printed). The noise signs, the float64 sign and ln|det| are reported per lambda. The relative difference of ln|det| to macm3's own is information (the bar of the earlier same-state control, `../kc79_d195/control_check.py`, is 1e-9 relative; it is not a pass rule here).

## Predictions, registered before the run (information)
- The check accepts macm3's state on Linux with both controls firing about 90% (a macOS state passed the k_c 79 check here at D 19.25, |F| 0.33% apart).
- Reading A about 65%, B about 25%, neither about 10%. (The two regrids' Delta differ by 1.4e-6, 1.0860022726 against 1.0860036806, a slack the residual |F| of 4e-10 times dDelta/dF 1.35e9 leaves open; that favours A. The macOS NEON and Linux AVX2 builds are not bit-identical, which keeps B possible.)
- ln|det| on the same state, relative difference to macm3's: below 1e-9 about 35%, below 1e-6 about 75%.
- A point 1800 to 2500 s on this machine beside the four k_c 95 scan processes (the order's estimate: 2300 s); the three points together about 40 min.

## Status
- 2026-11-23 05:39:51 UTC: folder, inputs, lane and the reading prepared before any run. The D 19.75 k_c 95 scan (../kc95_d1975, unit i1025w) is running beside (started 05:08:36 UTC, 4 processes).
