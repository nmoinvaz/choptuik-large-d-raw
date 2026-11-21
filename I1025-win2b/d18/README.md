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

Step 2, the dd M sign check, only after the gate passes: `ell_ddm.py selftest` (must PASS) and `selftest --mutate=slices` (must FAIL), 1800 s caps; then `ell_ddm.py det STATE 18 63 LAMBDA --noise 1e-24,1e-20,1e-16` at root - 0.005 and root + 0.005 (rounded to 10 decimals), two processes in parallel, 20 BLAS threads each as at D 17 (the hybrid has 4, as ordered), BelowNormal, caps 10800 s each by exact pid after a command-line check. A dd sign counts if its 5 variants agree and 1e-24 noise (both seeds) leaves it unchanged; the 1e-20 and 1e-16 noise are information.

**Reading, fixed now (Amendment 3, `read_d18_dd.py`, selftest with 8 planted cases):** opposite counting dd signs, in either orientation, each equal to the hybrid's sign at the hybrid evaluation nearest that point, mean the upper root passes. The same counted sign at both: no root between them. A sign that does not count: neither reading applies. Opposite signs that differ from the hybrid's nearest ones: the dd disagrees with the hybrid (no pass). The orientation is information.

Caps: hybrid 21600 s, by exact pid. One line per event in `../exits_1025.txt`. Progress posts on #1025 every 3 h and at the end, with cpu and memory.

## Log

(appended below as the run goes)
- 2026-11-21 07:44:44 UTC: README, stub (blob cb45e95e), `d18_gate.py` and `read_d18_dd.py` (selftests pass) and `d18_chain.sh` written and pushed before the run; the chain is launched waiting for the D 17 dd check.
