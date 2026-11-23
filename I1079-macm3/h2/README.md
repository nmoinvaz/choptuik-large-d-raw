# I1079-macm3/h2: hypothesis H2 of Theorem A(3) at the two excited zeros, lemma 6b1(3)'s covering at each centre (#1079)

Machine: macm3 (Apple M3, 8 CPUs, 24 GB, macOS 26.3.1, arm64; runner macm3b). Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1079. Written 2026-11-23 16:57 UTC, before any H2 run.
Task from the coordinator (hc after H1 and H3's acceptance, raw d8c28245; the plan is #1079's comment "H1 and H3 hold at both excited zeros; H2 next"), given as:
"Go on H2: per zero, A_lemmas_M section 9's M = 3 commands for `lemma6b1_cover_M.py` with `--x=<that zero's p^, full decimal strings> --h=1e-11 --tag=_exc1 / _exc2` (CERTIFY_M_NTAY/NJAC do not apply). PILOT first, both zeros side by side at 2 processes each (start after the D 20.8125 scan ends):
`probe --M=3` (not rigorous; report each inner row's disc radii and whether any disc fails), `ray --c1`, `row --j=11`; stop and report. Then `rows`, `check --json` (must PASS), `c1check`, `mutate --j=11` (no disc may certify), and section 7's inclusion of X_c's hull in p^ +-1e-11
(read which script; if it has no `--x`, stop and tell me). Raw `I1079-macm3/h2/`, README first; `--resume` after a restart."

## What it is

Theorem A(M)'s hypothesis (H2): a complete lemma 6b1(M) covering (`lemma6b1_cover_M.py`) whose parameter box contains X_c, the box on which the point certificate proves one simple zero (A_lemmas_M section 6). The covering proves y+ analytic on the annular sector
{25 <= |u| <= 260, -3pi/4 <= arg u <= 0} (u = 1/xi^2) for every x in its box. At the fundamental it is centred on p^ with h = 1.1e-9 (6b1's covering of section 5.3). Here, one covering per excited zero, centred on that zero's p^ (the boxes' `p`, full decimal strings) with **h = 1e-11**,
an axis-aligned box that contains each certified box's hull (the hulls' radii are at most 4e-13, the coordinator's note). Zero 1 (x1, tag `_exc1`): the box M3x1E2 (1e-12, 1e-13); zero 2 (x2, tag `_exc2`): M3x2E2 (1e-12, 1e-12).

## Code and settings

Worktree `~/Source/choptuik-large-d-1079f` (clean, detached, `feat/certify-excited` at **89553c6b1645c1a5711a4d17fb71306963b963a7**; `lemma6b1_cover_M.py` as main's a4cd5eaa), python-flint 0.9.0, FLINT 3.6.0, Python 3.14.3, numpy 2.5.4 (`~/Source/venv-macm3-1058b`).
Every command takes `--x`, `--h`, `--tag` (the run folder `solver/proof/lemma6b1_runs_M3<tag>/`: `ray.json`, `row_JJ.json`); `CERTIFY_M_NTAY/NJAC` do not apply (the covering has its own orders: `disc_params`, ORDER 12 and DISC_PREC 128). `OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1`, `nice -n 10`, own sessions under caffeinate. Memory alerts only.
The two zeros side by side, 2 processes each (4 in all, beside nothing else once the D 20.8125 scan has ended).

## The steps

1. **Pilot** (per zero, then stop and report): `probe --M=3 --x=<p^> --h=1e-11 --tag=_excN` (NOT rigorous: discs at double-precision centre values, to choose disc radii and orders; its output lists each row's disc radii and Lambda; the design's inner rows assume y+'s nearest singularity about 12.7 away on |u| = 25, 15 at 25 e^(-3 i pi/4) for the fundamental's design) in one process, and
   `ray --c1 --M=3 --h=1e-11 --tag=_excN --x=<p^>` (the C^1 ray run, about 30 min at the cloud's load) in the other; then `row --M=3 --h=1e-11 --tag=_excN --x=<p^> --j=11` (the hardest row, about 26 min there). Stop and report.
2. **Complete** (after the coordinator's word on the pilot, or as ordered): `rows` (the other 11 rows, two processes with `--only=`), `check --json=lemmas_M_runs/lemma6b1_check_M3_excN.json` (must print PASS), `c1check` (planted truth for the C^1 sets), `mutate --j=11` (the wrong-sign fast term: no disc may certify).
3. **The inclusion** of X_c's hull in p^ +- 1e-11, by section 7's script. I read first which script: `theorem_A_sets_M.py` takes `--M`, `--raw`, `--mutate`, `--selftest` only; for M = 3 it reads the fundamental's box `data/A_M_box_M3_1e-10.json` (its `CERT[3]`) and X_b = c +- 1.1e-9; it has **no `--x` and no `--box`**. So at that step I stop and tell the coordinator, as ordered.
   (The hull is a number I can print from the boxes without it; I do not call that the script's result.)

Stops: any failing check or a disc that does not certify; a step-size underflow; the coordinator's "stop and report" after the pilot. On a failure: its cause, nothing changed. `--resume` after a restart (the runs save their state).

## Not predicted, named before

No numerical prediction was given. What the pilot measures: whether the fundamental's disc design (radii and orders by row radius) certifies at the excited centres, where y+ is larger (B3 0.81 and 0.98 against 0.14) and its singularities may be nearer.


## Pilot results (2026-11-23, 17:09:17 to 17:11:10 UTC; python-flint 0.9.0, FLINT 3.6.0; both zeros side by side, 2 processes each)

**Verdict: the pilot passes at both zeros: no probed disc fails, `ray --c1` completes, and every one of row 11's 12 discs certifies. Stopped here, as ordered.** The runs took about 1 minute each (the fundamental's, on the cloud: 193 s per ray leg and 1566 s for row 11), `steps_h2.txt`.

**`probe --M=3`** (NOT rigorous; double-precision centre values, inflated boxes; `logs/I1079_h2_probe_exc{1,2}.log`, 20 s each): `ok True` for all 42 probed discs at each zero (the fundamental's stored probe: 40, all True). Per row, at the design's disc radius r and order n (`disc_params`), Lambda (sup|y - y0|) on the ray / on the axis:

| row | \|u\| | design (r, n) | x1 ray / axis | x2 ray / axis | fundamental (stored) ray / axis |
|---|---|---|---|---|---|
| 0 | 262.0 | (24, 70) | 0.171 (0.355) / 0.180 (0.233) | 0.170 (0.324) / 0.180 (0.25) | 0.179 (0.75) / 0.176 (0.298) |
| 6 | 102.16 | (24, 70) | 0.198 (30.8) / 0.214 (3.28) | 0.194 (21.5) / 0.215 (2.57) | 0.227 (155) / 0.207 (10.9) |
| 7 | 79.6 | (16, 60) | 0.154 (2.15) / 0.174 (1.77) | 0.151 (2.28) / 0.175 (1.92) | 0.180 (1.42) / 0.167 (0.906) |
| 8 | 61.84 | (16, 60) | 0.179 (3.98) / 0.197 (3.04) | 0.174 (4.2) / 0.198 (3.31) | 0.214 (17.1) / 0.192 (1.48) |
| 9 | 47.14 | (10, 50) | 0.140 (4.16) / 0.158 (2.96) | 0.136 (4.38) / 0.158 (3.24) | 0.174 (2.97) / 0.153 (1.37) |
| 10 | 36.04 | (10, 50) | 0.204 (8.45) / 0.196 (5.19) | 0.197 (8.83) / 0.196 (5.72) | 0.250 (13.7) / 0.193 (2.19) |
| 11 | 26.98 | (6, 50) | 0.146 (9.37) / 0.130 (4.86) | 0.142 (9.77) / 0.131 (5.39) | (stored probe's row 11 is at \|u\| 25.96) 0.197 (8.6) / 0.133 (1.97) |

The largest Lambda over all probed discs: 0.214 (x1), 0.215 (x2), 0.250 (fundamental). The probe's rows are 0 and 6 to 11 (the default rows of `probe`); the design's other rows (1 to 5) are certified by `rows`.

**`ray --c1 --M=3 --h=1e-11 --tag=_excN --x=<p^>`** (`logs/I1079_h2_ray_exc{1,2}.log`, 55 s and 60 s): start data at |u| = 262.0 from the old sector lemma (r0 = 0.1): centre radius 7.04e-70 (x1) and 1.39e-69 (x2), state set over X = p^ +- 1e-11: radius 1.36e-11; 11 legs (x1: 50, 52, 55, 57, 63, 70, 69, 64, 66, 65, 75 steps; x2: 47, 49, 52, 55, 58, 65, 64, 60, 61, 60, 63);
the state set's radius over X grows to 3.59e-10 (x1) and 2.75e-10 (x2) at |u| = 26.98 (the fundamental's run with h = 1.1e-9: 5.03e-07). `ray.json` 2.3 MB each (in `lemma6b1_runs_M3_exc{1,2}/`).

**`row --j=11`** (the hardest row, |u| = 26.98, r = 6, n = 50; `logs/I1079_h2_row11_exc{1,2}.log`, 54 s and 48 s): all 12 discs (0 to 11 of 11) `ok True`; Lambda 0.130 to 0.149 (x1), 0.131 to 0.145 (x2) (the fundamental's: 0.128 to 0.179); box radius at the last disc 2.0e-10 (x1), 2.4e-10 (x2) (fundamental 3.4e-05); sup|y - y0| 9.363 down to 4.86 (x1), 9.767 down to 5.394 (x2) (fundamental 7.544 down to 1.858); 582 (x1) and 518 (x2) Lohner steps (fundamental 834).

**Next, as ordered** (after the coordinator's word): `rows` (the other 11 rows, two processes), `check --json` (must PASS), `c1check`, `mutate --j=11`; then the inclusion: `theorem_A_sets_M.py` gains `--cert=<box JSON> --ray=<the covering's ray.json>` for M = 3 on `feat/certify-excited` at c40fbc77 (worktree `~/Source/choptuik-large-d-1079g`; unset, unchanged): `--M=3 --cert=<that zero's box> --ray=lemma6b1_runs_M3_excN/ray.json`, and `--selftest` with the same two options (its centre mutation must fail).


## H2 verdict (2026-11-23, rows 17:13 to 17:21, check and inclusion 17:21 to 17:23 UTC; python-flint 0.9.0, FLINT 3.6.0)

**Verdict: H2 holds at both excited zeros: a complete lemma 6b1(3) covering over p^ +- 1e-11, which contains each certified box's hull, and the inclusion of the hull in the covering's box holds.** Each zero: all 12 rows (0 to 11) saved, 183 discs, every disc `ok True` (none `ok False`, none underflowed); `check --json` PASS; `c1check` True; `mutate --j=11`: 0 of 12 discs certified; inclusion HOLD, its selftest PASS.
`rows` ran as two processes per zero (rows 0, 2, 4, 6, 8, 10 and 1, 3, 5, 7, 9: 482 s and 427 s (x1: 508 s and 427 s), x2: 482 s and 399 s), `steps_h2.txt`; the committed run folders are `lemma6b1_runs_M3_exc1/` and `_exc2/` (`ray.json` 2.3 MB, `row_00.json` to `row_11.json`), the check's json `lemma6b1_check_M3_exc{1,2}.json`.

| | x1 (box M3x1E2 (1e-12, 1e-13), tag `_exc1`) | x2 (box M3x2E2 (1e-12, 1e-12), tag `_exc2`) | fundamental (A_lemmas_M 5.3, 10) |
|---|---|---|---|
| covering box | p^ +- 1e-11 | p^ +- 1e-11 | p^ +- 1.1e-9 |
| `check --json` | **PASS** | **PASS** | PASS |
| tiles glued; meeting sets (polar rectangles); links | 183; 579; 461 | 183; 579; 461 | 183; 579; 461 |
| discs per row (rows 0 to 11) | 25 23 20 18 16 13 11 13 10 12 10 12 | the same | (183 in all) |
| disc radius r, order n by row | 24/70 (rows 0 to 6), 16/60 (7, 8), 10/50 (9, 10), 6/50 (11) | the same | the same design |
| max Lambda per row | 0.180 to 0.215 (largest at row 6) | 0.180 to 0.216 (row 6) | |
| max box radius: row 0 to row 11 | 2.1e-11 to 3.6e-10 | 2.6e-11 to 2.8e-10 | row 11's last disc 3.4e-05 |
| max sup\|y - y(c)\|: row 0 to row 11 | 0.247 to 9.36 | 0.263 to 9.77 | |
| ray (C^1 run) | 686 steps, 59 s | 634 steps, 55 s | |
| `c1check` (planted truth: y+ at the centre and at x +- h e_i inside the saved sets; rows 1, 6, 9, 11) | True (set radii 2.54e-11, 4.95e-11, 1.20e-10, 3.73e-10) | True (2.54e-11, 5.03e-11, 1.23e-10, 2.87e-10) | |
| `mutate --j=11` (the wrong-sign fast term) | 0 of 12 discs certified (must be 0) | 0 of 12 (must be 0) | |
| inclusion, `theorem_A_sets_M.py --M=3 --cert=<box> --ray=<ray.json>` (c40fbc77, worktree 1079g) | **HOLD**: the hull of the certificate's ball inside X_b, slack +8.359e-12 at B3 | **HOLD**, slack +8.278e-12 at B3 | |
| its `--selftest` with the same options | PASS (clean holds; the centre mutation fails: "(2) X_c outside X_b") | PASS (same) | |

X_b = the covering's ball: centre c = ray.json's x, radius 1e-11 as arb rounds it up (1e-11 + 1.425e-20); |p^ - c| is at most 1.5e-77 in every coordinate. X_c's hull half-widths: x1 A 1.00e-12, w/w_inf 1.00e-12, B3 1.64e-12, C3 1.63e-13; x2 A 1.00e-12, w/w_inf 1.00e-12, B3 1.72e-12, C3 1.37e-12.
The sets are 1e3 narrower than the fundamental's (1e-11 against 1.1e-9), which is why the runs take about a minute where the fundamental's took about 30 minutes per row on the cloud (the coordinator's reading).

**Status of Theorem A(3)'s hypotheses at each excited zero** (A_lemmas_M section 6): the point certificate (Krawczyk test, controls, recheck): passes; (H0) the certificate's own start-data run (the coordinator's reading; no second look); (H1) lemma S, the old sector lemma and the flat estimate over p^ +- 1e-6: pass; (H2) the 6b1 covering and the inclusion: pass (above); (H3) lemma 6a(3): rho_6a 0.01259 (x2) and 0.01365 (x1): pass. Every run named in the hypotheses passes with its controls at both zeros.
This is a statement about the runs; the assembly of the theorem, the trusted code and the follow-on (a second implementation and an independent review, as Theorem A's) are the coordinator's.
