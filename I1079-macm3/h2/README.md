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
