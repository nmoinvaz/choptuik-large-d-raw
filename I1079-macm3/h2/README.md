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
