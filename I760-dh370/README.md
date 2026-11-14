# I760-dh370: the chain's series at three of #603's newest bases, toward the near track at 258.60 + 2.79i

Machine dh370 (Fedora 45, i7-8700, 12 threads), issue https://github.com/nmoinvaz/choptuik-large-d/issues/760.

Scripts: #712's, with only the folder, the bases and the bars' track changed (written by the coordinator): `run760.sh`
(the 24-order series, `anm_run.py --save_jet 2` with #603's chain_nsr flags, at D 256.5686, 257.6853 and 258.7829, in
#712's worktree choptuik-large-d-685 at main f40deb4a and venv), `stage_summary760.sh` (jet_singularity.py summary,
table685.py, report760.py, and repro_check760.py with its control), `repro_check760.py`, `report760.py`.

Bars, written before any series was read (#760): (1) each series equals #603's record of the step from its base in all
25 norms and both pivots, and the control (the next base's record) differs; (2) Delta's root test within 5% of
|T - D0|, T = 258.60 + 2.79i; (3) the Pade pole of Delta within 0.4 of T has Im D* within 0.1 of 2.79. Track A
(255.71 + 4.99i) is listed at each base. On #712's three bases read as new, bar 2 passes only at D 255.37 (-0.7%), and the
control `--mutate=shiftT` (T moved by 1.0) fails bar 3 at every base.

## Results (dh370, 2026-11-14)

Code: main f40deb4a in worktree `choptuik-large-d-685`, the venv of `choptuik-large-d-614` (the 3c35f0c build), 12 threads, nice 10,
unit `i760`. Raw commit: the commit that adds this section (`git log -- I760-dh370/README.md`).

Answer: Track T (258.60 + 2.79i) is a stable Pade pole of Delta with Im D* within 0.1 of 2.79 at D 256.5686 and 257.6853, and it is not
seen at D 258.7829, where every one of the 24 rows' nearest poles and Delta's nearest Pade poles lie on the real axis at D* about 259.95
(|s| 1.09 to 1.18, root test 1.220). The root test is within 5% of |T - D0| only at D 256.5686. Track A (255.71 + 4.99i) is not among Delta's
stable poles at any of the three bases.

### Runs

| run | exit | wall |
|---|---|---|
| `anm_run.py --save_jet 2`, N 24, #603's chain_nsr flags, D 256.5686 | 0 | 2332 s |
| the same at D 257.6853 | 0 | 2331 s |
| the same at D 258.7829 | 0 | 2335 s |
| `stage_summary760.sh` (`jet_singularity.py summary`, `table685.py`, `report760.py`, `repro_check760.py` and its control), 10:39:18 to 10:48:36 UTC | 0 (`summary760.log` ends `exit 0`) | 558 s |

The series ran 08:42:25 to 10:39:03 UTC, no Traceback in any log.

### The bars at each base (T = 258.60 + 2.79i)

| base D0 | (1) series equal #603's record | (2) root test of Delta, \|T - D0\|, ratio | (3) Pade pole of Delta within 0.4 of T: \|s\| arg n, D*, Im D* - 2.79 | track A's pole (255.71 + 4.99i) |
|---|---|---|---|---|
| 256.5686 | met, 25 of 25 norms, pivots equal | 3.604, 3.451, +4.4%: **met** | 3.461, 54.7°, n 7, 258.57 + 2.82i, +0.033: **met** | none among Delta's stable poles |
| 257.6853 | met, 25 of 25, pivots equal | 2.431, 2.936, -17.2%: **failed** | 2.988, 72.9°, n 4, 258.57 + 2.86i, +0.065: **met** | none |
| 258.7829 | met, 25 of 25, pivots equal | 1.220, 2.796, -56.4%: **failed** | none within 0.4 of T: **failed** | none |

### Where the singularities are

| base D0 | Delta's other stable Pade poles (D*) | the 24 rows' nearest pole, median D* (Im D* range), rows within 0.4 of T | recurrence fit D* (spread) |
|---|---|---|---|
| 256.5686 | 259.80 + 1.27i (n 7) | 258.53 + 2.84i (2.82 to 2.86), 24 | 259.65 + 2.00i (0.64) |
| 257.6853 | 259.61 + 1.18i (n 5) | 259.27 + 1.98i (1.18 to 2.84), 8 | 259.83 + 1.37i (0.40) |
| 258.7829 | 259.96 + 0.00i (n 8), 260.17 + 0.00i (n 5), 259.51 + 1.25i (n 8), 259.77 + 1.61i (n 4) | 259.95 + 0.00i (0.00 to 0.00), 0 | 260.03 + 0.00i (2.09) |

At D 258.7829 the rows' nearest poles have \|s\| 1.091 / 1.171 / 1.183 (min / median / max), all at argument 0.0°, and the median \|s\|
is -4.3% from the rows' median root test. Tracks (`table760.txt`, D* within 0.4 of the track's median, least squares over its bases):

| track | bases | D* per base | drift per unit D0 (Re, Im) |
|---|---|---|---|
| A, 255.71 + 5.00i | 8, D0 252.25 to 255.77 (not seen at the three new bases) | Re 255.64 to 255.77, Im 4.95 to 5.04 | -0.036, +0.009 |
| T, 258.59 + 2.80i | 5, D0 255.06 to 257.69 (9 poles at 257.69, none at 258.78) | Re 258.53 to 258.61, Im 2.78 to 2.84 | -0.009, +0.019 |
| 259.61 + 1.18i | 4, D0 255.77 to 258.78 | (259.84, 1.17), (259.80, 1.27), (259.61, 1.18), (259.51, 1.25) | -0.117, +0.015 |
| 259.95 + 0.00i | 1, D0 258.78 (26 poles) | (259.95, 0.00) | none (one base) |

The recurrence fit's single pair moves toward the axis, Im D* 2.00, 1.37, 0.00 at the three new bases (slope -0.586 per unit D0 over its
eleven bases from D 252, reaching 0 at D0 = 259.6). It is the estimator #711 dropped for three fixed singularities, and its spreads are 0.64, 0.40 and
2.09, so it is listed and not relied on.

### Controls

| control | result |
|---|---|
| `repro_check760.py --control` (each series against the next base's record) | DIFFERS at all three (0 of 25 norms, pivots differ), `exit 0`. This exit is the control working (`exit 1` only if a series matched the wrong record), which is how #712's `repro_check712_control.txt` reads. It corrects the brief, which expected `exit 1`. |
| `report760.py ... --mutate=shiftT` (T moved by +1.0), `report760_shiftT.txt`, run with the venv python since system python3 has no numpy | bar 3 fails at every base ("none within 0.4 of T"), and bar 2 fails at every base (-12.5%, -28.1%, -58.1%) |
| tool check: Delta's Pade poles, root test and rows of the nine bases of #712 and earlier against `I712-dh370/jet_712.json` | equal at all nine |

### Not decided, reported as it is

1. At D 258.7829 the nearest singularity is on the real axis, ahead of the chain at D* about 259.95 (Pade poles 259.96 and 260.17, the recurrence fit's 260.03). That the branch ends or turns there is a reading of these poles, not a test, and the status is *numerical evidence*.
2. T is absent at D 258.7829, where the real-axis pole is at |s| 1.17 and T would be at 2.80. Whether T is gone or hidden behind the nearer pole is not tested, a 24-order series sees the nearest poles first.
3. The root test falls with D0 as 3.604, 2.431, 1.220, roughly the way the distance to a fixed point ahead does, and equals the rows' median |s| to -4.3% at D 258.7829. It follows the nearest singularity, T only at D 256.5686.
4. The Pade poles on the real axis differ by 0.21 between orders (n 8 at 259.96, n 5 at 260.17), so D* is known to about that much.

### Recommended tasks

1. **The series at the next two or three of #603's states past D 258.78.** What: the same command, then the summary and report with the bars on the real-axis pole at 259.95 + 0.00i (|s| and root test against 259.95 - D0). Why: the root test and the poles say the chain's real-axis continuation ends within about 1.2 of D 258.78. Acceptance: the series equal #603's records in 25 norms and both pivots with the control differing; the nearest Pade pole has Im D* 0.00 within 0.1 and Re D* within the n 8 / n 5 spread (about 0.2) of 259.95; the root test within 5% of D* - D0; each fails or is reported as failed. Depends on: #603's states past D 258.7829. Estimate: about 40 min per series at 12 threads.
2. **Is the real-axis singularity a square-root branch point or a pole?** What: from the three coefficient sets at D 256.57, 257.69 and 258.78, the Domb-Sykes / ratio exponent of the nearest singularity (`jet_singularity.py locate`'s `Domb-Sykes s` and `fall from order 5` lines, read at the new bases), with a planted series of a known square-root point at 259.95 and of a simple pole. Why: it decides whether the branch turns (a fold in D) or ends. Acceptance: the planted controls return their exponents to 10%; the real series' exponent is reported with its spread. Depends on: this issue. Estimate: coordinator code, then minutes.
