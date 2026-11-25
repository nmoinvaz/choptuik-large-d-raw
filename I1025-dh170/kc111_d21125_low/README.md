# I1025-dh170/kc111_d21125_low: #1025 the k_c 111 state at D 21.125, the LOW scan (lambda 0.840 to 0.865 and the repeat of 0.860)

Machine: dh170 (Fedora, i7-7700, 4 cores / 8 logical CPUs, 31 GiB), session `choptuik-dh170-i1025` (the claude-me2 continuation of session 5e14df5b after t5's account switch). Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1025. Written 2026-11-25 07:21:43 UTC, before any run of this folder.

## Order (the coordinator t5's hc, 25 Nov), quoted in full
"#1025, next for dh170 (same k_c 111 state, same scan driver and checks): (1) first report Delta of the k_c 111 regrid against the sequence (k_c 71 1.121651758, 79 1.121592805, 87 1.121577253, 95 1.121573197, your k_c 103 value) and its step ratio. (2) Then a low scan below your window, where ln|det| dips at the 0.870 edge: lambda 0.840, 0.850, 0.860, 0.865 plus the repeat of 0.860, 5 processes of 1 thread at nice 10, one round. Register predictions first: a root in (0.860, 0.870) or (0.865, 0.870) with orientation '- to +' (an orientation flip against k_c 103's '+ to -') if the dip is a root; none if it is not. Report the robust changes with printed orientation, and ln|det| beside k_c 103's at the same lambdas. Raw kc111_d21125_low/, README first."
t5's follow-up, after my flag that no k_c 103 point exists below 0.875: "no k_c 103 points; the k_c 111 low scan only, with ln|det| beside k_c 95 and 103 where they exist, as you propose."

## Part (1): Delta against the sequence (reported to t5 at 07:20 UTC; the numbers are in the records)
| k_c | Delta at D 21.125 | step to the next k_c | ratio of that step to the one before |
|---|---|---|---|
| 71 | 1.121651758 (t5) | -5.8953e-5 | |
| 79 | 1.121592805 (t5) | -1.5552e-5 | 0.2638 |
| 87 | 1.121577253397 (dh370's record; t5's 1.121577253) | -4.0569e-6 | 0.2609 |
| 95 | 1.121573196527 (my record) | -2.3374e-6 | 0.5762 |
| 103 | 1.121570859155 (my record) | -1.2886e-6 | 0.5513 |
| 111 | 1.121569570593 (my record, `../kc111_d21125/l1kc111dh170h.jsonl`) | | |
The ratio is not constant (about 0.26 twice, then about 0.55 to 0.58 twice); no extrapolation is made. The k_c 71 to 87 values come from other machines and builds at the digits t5 and dh370 gave, so the first two ratios carry about 1e-4 relative error.

## Inputs (copies in `in/`, `prev/` and here; `in_blobs.txt` and `prev_blobs.txt` list their `git hash-object --no-filters` blobs and the driver refuses any other blob)
| item | where | blob |
|---|---|---|
| the k_c 111 state at D 21.125 (tag l1kc111dh170h), the state of the order | `sol_l1kc111dh170h_D21.1250.npy` (= `../kc111_d21125/`, raw 487e7a726 and later) | edbb419e |
| its record (D 21.125, k_c 111, |F| 4.634281e-10, 3742 steps, psi-constraint 6.196e-4, Delta 1.121569570593) | `l1kc111dh170h.jsonl` | a0a52e86 |
| the parent's acceptance (ACCEPTED 22:35:05 UTC 24 Nov by `kc111_syscheck_1025.py` with both controls exit 1 and the k_c 103 check refusing the result) | `VERDICT_parent.txt` | |
| the scan driver (unmodified), the reader's imports, the reader, the repeat check, the k_c 111 check | `in/d18_hybsign.py`, `in/d185_scan_read.py`, `in/read_lower.py`, `in/repeat_check.py`, `in/kc111_syscheck_1025.py` | e089207a, 7c9d400f, 89309d3c, aaf598a9, 85aeb312 (all equal to the parent's) |
| the parent's ten evaluations (lambda 0.870 to 0.910 and the repeat of 0.890), 8 files, read together with the new points | `prev/scan_D21.125_p*.jsonl`, `prev/scan_D21.125w_p*.jsonl` | in `prev_blobs.txt` |
The worktree is the parent's (`~/Source/choptuik-large-d-1025k79` at 48c36355; dss_ell, ell_ddm, ell_dd, ddnp equal 505d8399; its `solver/matter/data/` holds the same state and record, blob checked), the venv `~/Source/choptuik-large-d-1058b/.venv` (Python 3.14.10, multidouble 5.1.0 avx2). **No regrid and no new acceptance run**: the state is the parent's accepted one, pinned by blob, and every scan process re-checks it before its point (`d18_hybsign.py` compares |F| and the `freeze_from` step count with the record and exits 3 unless it is "the record system").

## Commands (a systemd user unit, so no terminal owns it)
```
systemd-run --user --unit=i1025-k111l-s --working-directory=$PWD systemd-inhibit --what=sleep --why="#1025 kc111_d21125_low scan" --mode=block ./run_scan.sh
```
`run_scan.sh` (lists in `stage.conf`): 5 single-thread processes (OMP, OpenBLAS, MKL, VECLIB, RAYON threads 1) at nice 10, one `d18_hybsign.py` point each: **p0 0.840, p1 0.850, p2 0.860, p3 0.865, p4 0.860 (the repeat, another process than p2)**. Files: `scan/scan_D21.125low_p<p>.jsonl`, `scan/scanlow_p<p>.raw` (with `time -v`). At the end: `read_lower.py` selftest and its two mutations, the reader on the low window **0.840 to 0.870** (the new points with the parent's 0.870, in `combined/`) and on **0.840 to 0.910** (with all of the parent's ten evaluations), `repeat_check.py`, `SCAN_DONE.txt`. Guards tried before the run (dry mode, each exit 1): a wrong state blob ("the state or record is not 00000000 / a0a52e86"), a missing parent verdict, a changed `prev/` file (`ctl_stateblob.txt`, `ctl_verdict.txt`, `ctl_prev.txt`); the dry run passes with the true pins.

## Acceptance and stop rules
1. **Scan.** Every process prints the record system (3742 steps equal); `read_lower.py` selftest exit 0, mutations `shift` and `round2` exit 1; the repeat of 0.860 agrees (sign, ln|det| within 1e-6, noise signs, float64 sign).
2. **Stop and report on:** a process that does not print the record system (exit 3); an exception; **no robust change in the window (I report and do not widen)**; any point still running after 8 h (reported, not killed). Nothing is killed on memory (alert only: `alert.log` if MemAvailable falls below 2048 MiB). I change nothing at a stop.

## Reading and prediction, fixed now (by position)
Every robust change with bracket (0.005 wide), det-linear estimate and estimator range (the spread over interpolation choices of `d185_scan_read.changes`, not an enclosure), **orientation as printed** (hybrid sign below the change to the sign above; information, not identity); the edge signs; changes touching a non-robust point listed and not counted; ln|det| minima without a sign change flagged; the repeat's bits. A change is robust when both neighbouring points pass the 1e-15 noise test (2 seeds). The reading is made twice: on 0.840 to 0.870 (the order's low window, with the parent's 0.870 as the upper neighbour) and on 0.840 to 0.910 (all fourteen evaluations). ln|det| is tabulated beside the k_c 95 scan (my `../kc95_d21125/scan`, lambda 0.865 to 0.895) and the k_c 103 scan (`../kc103_d21125/scan`, lambda 0.875 to 0.895) at the lambdas where they exist; **no k_c 103 point exists below 0.875 and no k_c 95 point below 0.865** (t5: do not run them). The absolute ln|det| depends on the size N, so the beside-table compares the shape (the step to the next lambda), not the level.
**t5's prediction, registered here before any scan:** if the dip at the parent's 0.870 edge (ln|det| 0.656 below its neighbour 0.875) is a root, there is a robust change in (0.860, 0.870) or (0.865, 0.870), read on the grid as the brackets (0.860, 0.865) and (0.865, 0.870), with printed orientation **'- to +'** (hybrid sign - below, + above: against the k_c 95 and 103 roots' '+ to -'); **none if it is not a root.**

## Predictions (mine, information; the parent's numbers: round 1 11225 to 11264 s with 4 processes, 19330 to 19749 s with 6 or 7 on 4 cores)
- **Exactly one robust change in 0.840 to 0.870 about 55%; none about 35%; two or more about 10%.** Given one: its bracket is on the grid (0.865, 0.870) about 55%, (0.860, 0.865) about 30%, below 0.860 about 15%; its printed orientation is '- to +' about 95%. Given none: every new point + and ln|det| keeps falling toward lower lambda below the edge value about 60% (it rises again about 40%).
- ln|det| at 0.865 below its value at 0.870 (-3636.7363) about 70%; at 0.860 below that at 0.865 about 60%.
- Every point noise-robust about 70% (a point next to a root may fail the noise test). The repeat of 0.860 bit-identical about 90%. The float64 sign differs from the hybrid at more than half of the five points about 30%.
- Reasoning behind the first line (shape only, not a fit, no planted check): the parent's ln|det| above 0.875 falls smoothly (-0.020, -0.207, -0.297, -0.351, ..., -0.432 per 0.005) and the k_c 95 scan fell to its root in the same way from 0.865 up; a fall of 0.656 between 0.875 and 0.870 against a smooth baseline of about -0.5 to -0.55 per step is what a zero a few grid steps below 0.870 would add, and also what a smooth bend would give.
- Time: each point 12500 to 17500 s about 70% (5 processes on 4 cores; expected about 14500 s, so the scan ends about 4 h after its start, about 11:45 UTC if it starts at 07:40; range 11:10 to 12:40 UTC); peak RSS of a scan process (one point each) below 4 GiB about 85% (the parent's one-point processes 3.19 to 3.42 GiB); lowest MemAvailable above 8 GiB about 90%.

## Budget
The scan: 5 single-thread processes at nice 10 on the 4 cores (8 logical CPUs; nothing else of mine runs). Memory: alert only; 5 processes of about 3.4 GiB each is about 17 GiB of the 28 GiB free.

## Log
- 2026-11-25 07:21:43 UTC: README written before the run; folder set up (pins, `stage.conf`, `run_scan.sh` adapted from the parent's; dry run passes; three guard controls exit 1). Part (1) and the flag on k_c 103 reported to t5 at 07:20 UTC; t5's ruling: no k_c 103 points.
