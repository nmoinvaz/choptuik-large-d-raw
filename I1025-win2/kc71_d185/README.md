# I1025-win2/kc71_d185: a third k_c at D 18.5: the k_c 63 state regridded to k_c 71 (ell_refine.py --no-gamma), accepted at the record class's |F|, and scanned over lambda 1.55 to 2.49 at 0.02

Machine win2 (desktop-pc, Windows 11, Core Ultra 7 265K, 20 threads, 95 GB), the win2 build session, beside win2b's jobs. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1025. Task: the coordinator's hc of 2026-11-21 (~23:05 UTC), after
`../d185map/` (post 7070622344): at k_c 63 the D 18.5 roots are 1.6770 and 2.4204; at k_c 55 win2b finds 1.87 to 1.88 and 2.21 to 2.22 (comment 7070186508), so none is k_c-stable. A k_c 71 state shows which is nearer convergence.
(1) Make it: regrid the k_c 63 D 18.5 state to k_c 71 with `ell_refine.py --no-gamma`, accept it only at the record class's |F| (about 3e-10) with a converged step count; a regrid that does not converge stops the task with a report.
(2) Scan it, lambda 1.55 to 2.50 at 0.02 (48 points), with `d18_hybsign.py`, the noise test and the float64 sign, split over 4 processes with one point repeated in each pair, 4 threads each, 8 h caps.

## The regrid command: what raw holds, and what I run (written 2026-11-21 23:10 UTC, before any run)

The hc says to make the state "the way win2b made its k_c 71 D 16.75 state" and to quote that command from raw `I1025-win2b` before running. I searched `I1025-win2b` (README, `run1025*.sh`, logs, `kc55/`), `I1025-win` and `I1025-mac`: there is no k_c 71 state at D 16.75, and no `--no-gamma` call, in `I1025-win2b`.
The `ell_refine.py` calls that make k_c 71 states or use `--no-gamma`, quoted from raw:

| where | command (quoted) | what it is |
|---|---|---|
| `I1025-win/run_kc71_1025.sh` (winb), log `I1025-win/kc71_D16.5.log` | `ell_refine.py l1kc63Fw1025b 63 l1kc71Fw1025 71 1 16.5 2.1454677 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60` | k_c 63 to k_c 71 at D 16.5, with the lambda search (no `--no-gamma`) |
| `I1025-win2b/run1025e.sh` line 61 (win2b), log `I1025-win2b/kc71c_D16.5.log` | `ell_refine.py l1kc71Fw1025 71 l1kc71Fw1025c 71 1 16.5 2.1408016 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60` | a re-search at k_c 71, D 16.5 (record `l1kc71Fw1025c`: F 2.085e-10, 3202 steps), lambda search on |
| `I1025-mac/lane_k.sh` (xfkappa) | `run ell_refine.py l1kc47Fx1025 47 l1kc55Fq1025 55 1 16.75 2.0928 $OPT --wait 60 --no-gamma`, `OPT="--kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12"` | k_c 47 to k_c 55 at D 16.75 with `--no-gamma` |
| `I1025-mac/lane_t.sh` (xfkappa) | `ell_refine.py l1kc63Fw1025 63 l1kc71Fm1025 71 1 17 2.026546497375959 $OPT` | k_c 63 to k_c 71 at D 17 |

So the nearest to the order is the combination of the first row (k_c 63 to k_c 71) and the third (`--no-gamma`, the options `OPT`). **The command I run** (`run_kc71.sh`; usage: `ell_refine.py src kc_src tag kc l "D" lam0 ...`; with `--no-gamma` the lambda search is skipped and `lam0` is not used, I give it lambda_0 = 2.1181259879 at D 18.5):

```
python.exe -u ell_refine.py l1kc63Wm1025 63 l1kc71Wm1025 71 1 18.5 2.1181259879 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma
```

cwd `D:/choptuik-i1025k71/solver/matter` (a new worktree at 48c36355, `ell_refine.py` blob 631e5801, `dss_ell.py`, `ell_ddm.py`, `ell_dd.py`, `ddnp.py` equal 505d8399's, `ell_delta.py` equals 48c36355's, checked by the driver), venv-md510 (multidouble 5.1.0), 4 BLAS threads, BelowNormal, cap 21600 s by the exact root pid
(win2b's k_c 71 D 16.5 solve took 95 minutes to its state at 4 threads). The input is `sol_l1kc63Wm1025_D18.5000.npy` (blob 33c1a58b, the same blob as `..._D18.500000.npy` that the hc names), copied into the worktree's `data/`; the options are those of the k_c 63 record (kappa 0.7, u0 0.04, Ks 30, rk 1).
Outputs: `data/sol_l1kc71Wm1025_D18.5000.npy` and the record `data/l1kc71Wm1025.jsonl`, copied here. If the coordinator has another command in mind, the regrid is the first part of the run and can be restarted within its first hour at the cost of that hour.

## The coordinator's answers to the two open points (hc, received after the launch at 23:11:27 UTC and noted here at 23:12 UTC 21 Nov)

- **The command:** the coordinator confirms it. The reference to a k_c 71 D 16.75 state of win2b's was wrong (win2b never made one; skipping that was approved); winb's k_c 63-to-71 regrid with xfkappa's `--no-gamma` form and the k_c 63 record's options, as above, is the right command. The regrid keeps running (root pid 40412, started 23:11:27 UTC); nothing was restarted.
- **The grid:** 1.55 + 0.02 i for i = 0 to 47, up to 2.49, is fine: every root of interest (1.6772, 1.87 to 1.88, 2.21 to 2.22, 2.4204) lies inside.

## Acceptance of the regrid (fixed before the run)

`kc71_syscheck.py` accepts the state only when (1) the record is k_c 71 at D 18.5 with **|F| <= 1e-9** (the record class: 2.1e-10 to 2.8e-10 in the k_c 55, 63 and 71 records at D 16.5 to 18.5; the k_c 63 D 18.5 record is 2.767e-10), and (2) the saved state reproduces its record the way `d18_hybsign.py` checks it before every scan:
`S.freeze_from(z, kappa)` gives the **record's step count** and the state's |F| is within 1% of the record's. That is the "converged step count": a count that comes back and an |F| that does not move. Two controls run on the same numbers (a record with |F| x 1.5 and a record with one more step must both be refused); `--selftest` checks the verdict on planted numbers.
**A regrid that does not converge stops the task with a report, and no scan starts:** the call exits non-zero or is capped, or writes no state or record, or the state is not accepted.

## The scan (written before the run)

- State and record: the accepted k_c 71 state and its record line (D 18.5); xfkappa's `d18_hybsign.py` (blob e089207a, as in `../d18mid/`, `../d18hi/`, `../d185map/`); `P4_WT_MATTER=D:/choptuik-i1025k71/solver/matter`, 4 threads each, BelowNormal, venv-md510, caps 28800 s (8 h) by the exact root pid; its own record-system check runs first in every process (exit 3 stops it).
- **Window: lambda 1.55 to 2.49 at 0.02, 48 points** (1.55 + 0.02 i, i = 0 to 47). The hc says "1.55 to 2.50 at 0.02 (48 points)": 2.50 is not on a 0.02 grid from 1.55 (1.55 + 0.02 x 47.5), and 48 points reach 2.49; I start at 1.55, so every point is also a point of the k_c 63 grid of `../d185map/` (a 0.01 grid) and of win2b's k_c 55 grid. The top 0.01 of the stated range is not scanned; the roots to be compared (k_c 63: 1.677016, 2.420394; k_c 55: 1.873934, 2.213669) are inside.
- **Four processes:** P1 = 1.77, then 1.55 to 1.75 (12 evaluations); P2 = 1.77, then 1.79 to 2.01 (13); P3 = 2.25, then 2.03 to 2.23 (12); P4 = 2.25, then 2.27 to 2.49 (13). The pairs (P1, P2) and (P3, P4) each repeat one point (1.77 and 2.25), evaluated first in both, so the pair gate compares them when the first points exist (the reader's repeated-point rule, same machine and code: same sign, ln|det| within 1e-6, noise-robust; a disagreement kills all four scans by exact pid and stops, AGENTS.md: a control that fires on real data stops the work).
  The 48 distinct points are covered once each (the repeats are the 1.77 of P1 and P2 and the 2.25 of P3 and P4).
- Each point: the hybrid sign (float64 blocks 0-11, double-double block 12), the noise test (1e-15 relative noise on blocks 0-11, 2 seeds), the float64 sign beside.
- Timing (information): win2b's k_c 71 D 16.5 hybrid evaluations took about 1060 s each (15 in 15950 s, several processes at once), against about 440 s at k_c 63; so 12 to 13 evaluations take about 3.5 to 4 h per process, against the 8 h caps; the regrid about 1.5 to 2 h before it.

## Reading (the coordinator's, fixed before the run, with the definitions of `kc71_read.py`)

The k_c 71 roots are the robust sign changes of xfkappa's reader (`d18d_read.py` 6b608903, pinned copy in `../d18mid/pinned/`) on the four scan files together (both grid points noise-robust; a change touching a non-robust point is listed, not counted); each root is its det-linear estimate x71 (the bracket and the estimator range are information, not a bound).
Reference roots at D 18.5, by the same reader: **k_c 63: 1.677016 (minus to plus) and 2.420394 (plus to minus)** (xfkappa's three scans and `../d185map/`, `inputs/`); **k_c 55: 1.873934 (minus to plus) and 2.213669 (plus to minus)** (win2b's merged scan of `I1025-win2b/kc55/`, blob 24179d07, `inputs/kc55_scan_merged.jsonl`). `kc71_read.py` recomputes them from the input files and stops if they differ from these numbers.

- A k_c 71 root is **63-near** when it is within 0.02 of a k_c 63 root and farther than 0.02 from every k_c 55 root; **55-near** the reverse; **neither** otherwise (the k_c 63 and k_c 55 roots are at least 0.19 apart, so "both" cannot occur).
- **Every k_c 71 root 63-near (and at least one): k_c 63 is nearer convergence. Every root 55-near: k_c 55 is nearer. Anything else (a root near neither, a mix, no root): neither, not converged at these k_c**, with each root listed with its class.
- Beside, not read: orientation of each root (not compared across k_c; the sign convention across states is xfkappa's check), the ln|det| local minima without a sign change (win2b's k_c 55 scan has one at 1.68 without a change), the float64 sign, the signs against the k_c 63 and k_c 55 scans at the common grid points.
- A cap that fires, or a scan that exits non-zero, is a result: the points done are read and reported as partial; nothing is rerun or loosened.

## Controls

`kc71_syscheck.py --selftest` and its two built-in controls (the F x 1.5 and steps + 1 records are refused); `kc71_read.py --selftest` (planted root lists: 63-near, 55-near, neither, mixed, none, at the bar's two sides) and `--selftest --break` (exit 1), and its recomputation of the reference roots; `pair_check.py --selftest` and `--break`; the reader's selftest (0) and `--mutate=orient` (1); `kc71_read.py` was run on a planted k_c 71 scan (roots 1.683 and 2.4251) and read it as 63-near, k_c 63 nearer; the scans' record-system check.
The acceptance check was run on the k_c 63 D 18.5 record and state through the same code path (before the run): |F| 2.7722e-10 against the record's 2.7672e-10 and 2461 steps against 2461; it refuses only because the record is k_c 63.

## Result (regrid 2026-11-21 23:11:27 to 00:07:39 UTC; scans 22 Nov 00:07:43 to 02:58 UTC; reading 02:59 UTC)

### Part 1: the regrid converged and the state is accepted

`ell_refine.py ... --no-gamma` (the command above) exited 0 in 3372 s (the record's own `seconds`: 3358). The record (`l1kc71Wm1025.jsonl`, blob 1609d76b; the state `sol_l1kc71Wm1025_D18.5000.npy`, blob 28bf6bac, 37368 bytes), against the k_c 63 source's:

| | k_c 71 (this run) | k_c 63 (`l1kc63Wm1025.jsonl`, the source) |
|---|---|---|
| \|F\| | 2.8314362448e-10 | 2.7672415504e-10 |
| F_start (after the regrid, before the solve) | 1.259e-05 | 5.344e-05 |
| steps | 2772 | 2461 |
| constraint | 9.994e-04 | 1.912e-03 |
| Delta | 1.0560300475 | 1.0560243815 (+5.67e-06 to k_c 71) |

**Acceptance (`syscheck.txt`): ACCEPTED.** The record's |F| 2.83e-10 is at the class bar (<= 1e-9; the class is 2.1e-10 to 2.8e-10); the saved state reproduces its record: `freeze_from` gives **2772 steps = the record's** and the state's |F| is 2.8314362448e-10, equal to the record's; both controls on the same numbers refuse (a record with |F| x 1.5, one with steps + 1). Each of the four scan processes then passed the scanner's own record-system check (|F| 2.8314362448e-10 against the record's 2.8314362448e-10, steps 2772 = 2772).

### Part 2: the scan (lambda 1.55 to 2.49 at 0.02, 48 points)

All four processes ran to the end (exit 0, no cap): P1 12 evaluations in 9437 s (749 to 809 s per point, mean 785 s), P2 13 in 10301 s (748 to 896 s, mean 792 s), P3 12 in 9384 s (744 to 811 s, mean 781 s), P4 13 in 10270 s (743 to 887 s, mean 790 s); 4 threads each, BelowNormal, nothing else of win2b's running. About 790 s per point,
less than the 1060 s of win2b's k_c 71 D 16.5 evaluations. All 48 points are noise-robust. **The pair gate passed at 00:21:30 UTC** (828 s after the scans started): 1.77 (P1, P2): +1, ln|det| -2236.0928122605 in both; 2.25 (P3, P4): -1, ln|det| -2222.9234889399 in both; differences 0.0 (bar 1e-6).

**The reading (`kc71_read.txt`, `kc71_read.py`, xfkappa's reader 6b608903 unchanged; the control that recomputes the reference roots passed):**

| k_c 71 root | bracket | orientation | det-linear x71 | estimator range (information) | delta from lambda_0 = 2.1181259879 | nearest k_c 63 root | nearest k_c 55 root | class |
|---|---|---|---|---|---|---|---|---|
| 1 | (1.67, 1.69) | minus to plus | **1.675995** | [1.675995, 1.676550] | -0.442131 | 1.677016, 0.001021 away | 1.873934, 0.197939 away | **63-near** |
| 2 | (1.79, 1.81) | plus to minus | **1.809322** | [1.809322, 1.809619] | -0.308804 | 1.677016, 0.132306 away | 1.873934, 0.064612 away | **neither** |

**OVERALL: neither: not converged at these k_c** (classes: 63-near, neither), by the rule fixed before the run (every root 63-near would have put k_c 63 nearer; every root 55-near, k_c 55; anything else is neither).
No robust change touches a non-robust point; **no ln|det| local minimum without a sign change** (ln|det| has its minimum, -2239.634, at 1.81, beside root 2).

What the logs show, beside the reading and with no cause claimed:

- **Root 1 sits where k_c 63's root is:** 1.675995 against 1.677016 (difference -0.001021; the k_c 71 range [1.675995, 1.676550] and k_c 63's [1.677016, 1.677225] are 0.00047 apart), and 0.198 from k_c 55's 1.873934.
- **Root 2 is at 1.809322, near neither:** 0.065 from k_c 55's 1.873934 (a root of the opposite orientation) and 0.132 from k_c 63's 1.677016 (the opposite orientation again). The roots of its own orientation (plus to minus) are 2.420394 at k_c 63 and 2.213669 at k_c 55 (0.611 and 0.404 away). **From 1.81 to 2.49 the sign is minus at all 35 points: k_c 71 has no root near 2.4204 or 2.2137.**
- The plus region between the two k_c 71 roots is [1.675995, 1.809322], width 0.133; at k_c 63 the plus region is [1.677016, 2.420394] (width 0.743) and at k_c 55 [1.873934, 2.213669] (0.340). Orientation and the sign convention across k_c are not compared (the coordinator's reading; xfkappa's check), so this is a statement of where each scan's own sign changes are.
- float64 beside: 2 float64 sign changes, in (1.65, 1.67) and (1.85, 1.87), not the hybrid's (1.67, 1.69) and (1.79, 1.81); float64 differs from the hybrid at 4 of 48 points (1.67, 1.81, 1.83, 1.85). At k_c 71 the float64 sign does not give the roots.
- Hybrid signs at the grid points the other scans also have: equal to k_c 63's at 17 of 48 and opposite at 31; equal to k_c 55's at 20 of 43 and opposite at 23 (each scan's own det-sign convention).

`points_kc71.md` lists the 50 evaluations (48 points and the two repeats). The regrid log is `regrid.log`; the worktree `D:/choptuik-i1025k71` (48c36355) holds the regrid's `data/` (the state and record are copied here; nothing else of it is needed).

Memory: lowest available 46.18 GB, peak commit 59.59 GB of 101.47 GB (the four scans together), page file peak 2610 MB (as at the start); no alert fired (no `alerts.log`).
Slips: none in the run. Before it: my first README insert lost backticked text to an unquoted heredoc (repaired at once, the commands were not affected); the command mismatch and the grid conflict were named before the run and answered by the coordinator (above). `__pycache__` folders from importing my scripts were removed before the push.
