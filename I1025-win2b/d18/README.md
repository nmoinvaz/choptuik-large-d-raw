# I1025-win2b/d18: #1025 the upper root near lambda_1 at D 18, k_c 63

Machine: win2 (Intel Core Ultra 7 265K, 20 cores, Windows 11), runner `win2b`. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1025
Written before the run (2026-11-21 07:44 UTC).

## Order

The coordinator (hc ~07:30 UTC 21 Nov, approved as set below at ~07:42 UTC): xfkappa's D 18 scan (comment 7059398916; hybrid signs on winb's D 18 state at step 0.01: minus at 1.70-1.77, plus at 1.78-1.80, minus at 1.81-1.90, all noise-robust) finds two sign changes, in (1.77, 1.78) and (1.80, 1.81). The lower root is bisected at 1.7749781027; the upper is only placed near 1.806298 (the det-linear estimate). **Bisect the upper one** with `p4_hybrid.py` on winb's D 18 state, 4 threads, BelowNormal, 6 h cap by exact pid; the P4 rules with the outer-edge rule; then the full dd M sign at the root -/+ 0.005, two processes in parallel (the roots are 0.031 apart, so -/+ 0.02 would straddle the other one), read by winb's Amendment 3 (opposite counting dd signs, in either orientation, each equal to the hybrid's own sign nearest that point). It starts after the D 17 dd check (`../d17/dd/`) has ended: `d18_chain.sh` waits for `d17dd done` in `../exits_1025.txt`.

## The window (a mismatch with the order, ruled by the coordinator)

`p4_hybrid.py` (blob a402559b) has a fixed ladder: the grid guess * (1 - w, 1, 1 + w) at w = 0.02, 0.06, 0.15, 0.35, stopping at the first w with a sign change. It cannot search exactly [1.800, 1.810]. A guess of 1.805 gives the grid [1.7689, 1.805, 1.8411], which holds both roots (two grid changes, and the script would take the lower one: the two interval midpoints are equally far from the guess). The coordinator approved this instead (hc ~07:42 UTC): **the script stays unmodified and the guess is 1.825**, so the w 0.02 grid holds the upper root only and keeps the lower one (1.775) outside it.

| w | lower | guess | upper | step |
|---|---|---|---|---|
| 0.02 | 1.788500 | 1.825 | 1.861500 | 0.036500 |
| 0.06 | 1.715500 | 1.825 | 1.934500 | 0.109500 |
| 0.15 | 1.551250 | 1.825 | 2.098750 | 0.273750 |
| 0.35 | 1.186250 | 1.825 | 2.463750 | 0.638750 |

Expected from xfkappa's scan (same state): hybrid signs plus at 1.7885, minus at 1.825, minus at 1.8615, so one grid change, in [1.7885, 1.825], with the upper root there (det-linear estimate 1.806298: 0.488 grid steps above the outer lower point, 1.512 below the outer upper one). The lower root 1.7749781 lies 0.0135 below the outer lower point (0.37 steps), so it stays outside the grid. This is the upper root's orientation: plus below, minus above. The guess only centres the window; no value of the root is assumed.

## Inputs (raw origin/main c5e36fb8, by `git show`, checked with `git hash-object --no-filters`)

| item | raw path | blob |
|---|---|---|
| state | `I1025-win/out/sol_l1kc63W1025_D18.000000.npy` (winb's leap state, k_c 63, D 18, Delta 1.0445951948) | 45e72c6a5c22ee3f0196f7b08f07fecfe3a07b21 |
| record | `I1025-win/out/l1kc63W1025.jsonl` (its D 18 line: F 2.630345255831752e-10, 2552 steps, kappa 0.7, u0 0.04, Ks 30, no lambda) | c33039dfa38b... (full id in `in/`; the same line xfkappa's D 18 stub used) |
| stub | `in/stub_l1kc63W1025_D18_guess1.825.jsonl`, made by `make_stub_d18.py`: the D 18 line unchanged plus lam_guess 1.825 and lam = the guess (p4_hybrid's filter needs one; its minus_record reads root minus guess) | cb45e95ecdda8a7760d9205d7df44bbda17d636f |
| `p4_hybrid.py` | `I1025-mac/p4_hybrid.py`, unmodified | a402559b5d37661b49da50f07f877af21fd29b3a |
| edge/pass rules | `I1025-mac/d18/d18_check.py` (P4 rules plus the outer-grid-point edge rule; selftest passes, `../d17/d18_check_selftest.log`) | 08969ea28fbd6cb0d83e17c2d4ded1901ce6b209 |

Hybrid code: worktree `D:/choptuik-1025p4` at 505d839940456a3d04321d75cf66cc3b5bc831c4, venv-md510 (multidouble 5.1.0). dd code: win2's worktree `D:/choptuik-i1025d` (48c36355, read only; `dss_ell.py`, `ell_ddm.py`, `ddnp.py`, `ell_dd.py` identical to 505d8399). xfkappa's scan on this state found the record system (|F| 2.6296e-10 against 2.6303e-10, 2552 steps).

## Rules (fixed before the run)

Step 1, the hybrid row passes the gate (`d18_gate.py`; selftest with 8 planted cases, `d18_gate_selftest.log`) if all hold: (1) record system (steps equal, |F| within 1% or 1e-13); (2) one sign change on the search grid and one over all evaluations in lambda order; (3) every evaluation's sign unchanged under 1e-15 relative noise on blocks 0-11 (2 seeds); (4) final bracket at most 1e-7; (5) the outer-grid-point edge rule: the root at least 0.05 grid steps from the outer grid point on its side; (6) **bracket check, added by the coordinator: the root lies in the scan's bracket (1.800, 1.810)**, so it is the upper root. **If any fails, stop and report; the dd check is not run.**

Step 2, the dd M sign check, only after the gate passes: `ell_ddm.py selftest` (must PASS) and `selftest --mutate=slices` (must FAIL), 1800 s caps; then `ell_ddm.py det STATE 18 63 LAMBDA --noise 1e-24,1e-20,1e-16` at root - 0.005 and root + 0.005 (rounded to 10 decimals), two processes in parallel, 20 BLAS threads each as at D 17 (the hybrid has 4, as ordered), BelowNormal, caps **21600 s (6 h) each** by exact pid after a command-line check (changed by the coordinator's hc ~09:53 UTC 21 Nov, written here before the dd step; it replaces the 10800 s above, which cut both D 17 dd points after their noise lines and before `det` wrote its record; win2's D 18 points took 3856 to 7611 s under load). A dd sign counts if its 5 variants agree and 1e-24 noise (both seeds) leaves it unchanged; the 1e-20 and 1e-16 noise are information.

**Reading, fixed now (Amendment 3, `read_d18_dd.py`, selftest with 8 planted cases):** opposite counting dd signs, in either orientation, each equal to the hybrid's sign at the hybrid evaluation nearest that point, mean the upper root passes. The same counted sign at both: no root between them. A sign that does not count: neither reading applies. Opposite signs that differ from the hybrid's nearest ones: the dd disagrees with the hybrid (no pass). The orientation is information.

Caps: hybrid 21600 s, by exact pid. One line per event in `../exits_1025.txt`. Progress posts on #1025 every 3 h and at the end, with cpu and memory.

## Log

(appended below as the run goes)
- 2026-11-21 07:44:44 UTC: README, stub (blob cb45e95e), `d18_gate.py` and `read_d18_dd.py` (selftests pass) and `d18_chain.sh` written and pushed before the run; the chain is launched waiting for the D 17 dd check.
- 2026-11-21 07:46:29 UTC: **early start, stopped.** The chain's wait pattern (`d17dd done` anywhere in `../exits_1025.txt`) matched the chain's own log line, so the hybrid started at 07:45:02 while the D 17 dd points were still running (3392 s into their 10800 s caps; both alive, unaffected). Against the order (this follow-on starts after the D 17 dd check), I stopped it at ~07:46 by exact pid after a command-line check (python 35680 and its child, chain bash 11764); nothing had been written to the hybrid record. Its 40 s of log is kept in `aborted_0745/hybrid_D18.log`. The pattern is now `^1025 d17dd (done|STOP)` (start of line), and the chain is relaunched, waiting. No result of the stopped start is used.
- 2026-11-21 09:49:43 UTC: the chain started the hybrid by itself when the D 17 dd check ended (`1025 d17dd done` 09:49:11).
- 2026-11-21 09:53:40 UTC: **chain restarted for the cap change.** The coordinator's hc (arrived about 09:53 UTC, before the clock read of 09:54:24): raise each dd cap from 10800 s to 21600 s (6 h). The chain is a running bash script, and an edit in place is not reliably seen by bash (it reads its script in chunks), so I stopped it by exact pids after command-line checks (chain bash 28232 and its tree: crun subshell 24744, hybrid python 26024 and child 35328; the launcher wrappers 30860 and 9108 were already gone) 3 min 57 s into the hybrid. Only the record-system line had been written (|F| 2.6321882772e-10 against the record 2.6303452558e-10, steps 2552 against 2552); no evaluation, no jsonl. That log is kept in `aborted_0953/hybrid_D18.log`, and no result of it is used. `d18_chain.sh` now has `crun det_lo 0 21600` and `crun det_hi 0 21600` (and the header comment); nothing else in it changed. The hybrid starts again from the stub (cap 21600 s as before).
- If a dd process is cut by its cap again after its noise lines, the signs in its log are read with a converter tested through `read_d18_dd.py` first (the D 17 converter `../d17/dd/det_log_to_jsonl.py` is tested through `read_d17_dd.py` only). The coordinator's rule for D 17: the 5 variants and the noise signs are what the rule reads; the cut float64 `slogdet` is information only.
- 2026-11-21 12:16:27 UTC: hybrid done (second start, from 09:54:48): root 1.8074339746330934, 17 evaluations, one grid change and one over all, bracket 3.55e-8, noise-robust, 8490 s; grid signs + at 1.7885, - at 1.825 and 1.8615. Gate (`gate_D18.log`): PASS (P4 rules, edge distances [0.519, 0.481, 0.519], bracket (1.800, 1.810) pass). The dd selftests were as required (exit 0 and exit 1); det_lo (1.8024339746) and det_hi (1.8124339746) started 12:16:48 UTC, caps 21600 s each. The hybrid's nearest signs: + at 1.805487 (lower point), - at 1.809002 (upper point), so a pass reads plus below and minus above.
- 2026-11-21 14:02:51 UTC: dd done, both det processes exit 0, 6363 s each, not capped (dd M built in 1576 s and 1556 s, 182.6 s and 182.9 s per LU). Lower 1.8024339746: dd signs +,+,+,+,+ (agree), noise at 1e-24, 1e-20, 1e-16 all +,+; ln|det| -1925.2739361474; float64 sign -1 (ln|det| -1923.2986919883). Upper 1.8124339746: dd -,-,-,-,- (agree), noise all -,-; ln|det| -1924.7652759197; float64 sign +1 (ln|det| -1923.7549230245). `read_d18_dd.py` (`dd/d18_dd_read.log`, selftest passes, 8 planted cases, rerun 14:03): **ROOT PASSES**, the counting dd signs are opposite and equal the hybrid's nearest signs (+ at 1.805487, 3.05e-3 away; - at 1.809002, 3.43e-3 away); orientation plus below, minus above. The float64 M's sign is opposite to the dd sign at both points (information only, not read).
