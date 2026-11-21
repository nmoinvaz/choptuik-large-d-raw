# I966-mac-sing: the nearest real singularity of the order-293 chain ahead of D 261.6 (leg 14's saved jets)

Machine: the Mac (Apple M-series, 10 cores), helper session xfchecks, one process at nice 19. Issue
https://github.com/nmoinvaz/choptuik-large-d/issues/966, on the coordinator's request of 2026-11-21.

## Why

Along leg 14 of dh370's ks_chain3b (horizon order 293), the a-series tail e_N+1 went 9.2e-15, 3.9e-14, 4.5e-14,
7.7e-13, and |z_N| grew about 5 times per base. A real singularity ahead would show both. Where it is decides how
urgent the order raise is. Earlier work: #782 (`singularity_type.py`, the type of the order-130 chain's nearest real
singularity), #799 (D* 259.903 from bases 0.24 to 0.27 before it, by that script), #1008 (that fold is order 130's).

## Inputs and code

- Jets: `I966-dh370/ks_chain3b/leg14_D261.1415_ks293/jet_pin3_D*.npz` (`anm_run.py --save_jet 2`, 8 parts, N 31,
  series in h = D − D0), at raw 98e9e284. Bases: 261.1415, 261.2061, 261.2697, 261.3914, 261.5124, and each new one
  as it lands.
- Code: `hp/singularity_type.py` and `hp/jet_singularity.py` of the code repository's main at 607c1df3 (sha256
  4994867e... and 58c6a2b7...). `singularity_type.py` is unchanged since d284a229, the commit #799 ran.
  `jet_singularity.py` has changed since then only in its planted cases, not in `load_jet` or `row_series`.
- Python: venv-314 (Python 3.14, mpmath, numpy).

## Commands (#799's, from `I799-dh370/run799.sh` lines 31-32, no other arguments)

    python singularity_type.py planted [--mutate=move]
    python singularity_type.py rows JET.npz [JET.npz ...] --delta

`rows --delta` gives, per base:
- Delta's own series (the last entry) by two estimators: the ratio fit (Domb-Sykes, windows k0 8..14) and Dlog Padé
  (the nearest real pole of [L/M] of g'/g);
- the median and range over the 24 rows of largest |z_8|.

Each estimator gives s (the distance in D to the singularity) and mu (its exponent), each with a spread. The spreads
are over windows or approximants of one method, not error bars. D* = D0 + s.

## Criteria (fixed before any real series was read)

**The planted control.** `planted` exits 1 by design: since #782 its docstring records that the contaminated plants
fail the 10% bar. So `--mutate=move` also exits 1, and the exit code does not separate the two. The control is read
line by line (accepted by the coordinator, 2026-11-21):

- the control passes when the 2 clean plants (s 1.17) and the 2 near plants (s 0.457) pass, and the 2 contaminated
  plants fail as documented;
- the mutation passes when all 6 plants fail.

Caveats: the plants have N 24, and leg 14's jets have N 31. The near plant sits at s 0.457. The estimator of mu is
validated to 10% only for an isolated singularity (#782, #799).

**The readings** (the coordinator's, fixed before the run):

- D* the same to 0.01 over three or more bases, with mu near 1/2, means a real fold of this system ahead at D*;
- D* receding as the bases advance, or the poles off the real axis, means none is read.

How I apply them, fixed before the run:

- "the same to 0.01": for Delta's ratio estimate and for its Dlog estimate separately, the range (max − min) of D*
  over three or more consecutive bases is at most 0.01;
- "mu near 1/2": mu in the script's S band, [0.25, 0.75];
- "receding": D* grows with D0 by more than 0.01 over the bases;
- "off the real axis": `rows` keeps only real poles (|Im| below 5% of the modulus), so a Dlog "no estimate" is reported
  as no real pole. Complex poles are not computed here (`jet_singularity.py locate` is not run).

When the two estimators disagree, both are reported, and no fold is read.

## Results

**The planted control** (`planted.txt`, `planted_move.txt`; identical to `I799-dh370/type799_planted.txt`): the clean
and near plants pass, and the contaminated ones fail as documented. Under `--mutate=move` all six fail. Both conditions
hold. 2.6 s and 42 MB each.

**Leg 14, five bases** (`type966_leg14.txt`, 2026-11-21 08:08:19 to 08:09:05 UTC, exit 0; 46.2 s user, 0.09 s sys,
49.2 MB maximum resident). Delta's own series:

| D0 | ratio: D* (s) | ratio: mu | ratio spreads (s, mu) | Dlog: D* (s) | Dlog: mu | Dlog spreads (s, mu) |
|---|---|---|---|---|---|---|
| 261.1415 | 261.1846 (0.0431) | +37.44 | 0.14, 4.0 | 265.8674 (4.7259) | +1.052 | 1.5e3, 6.3e3 |
| 261.2061 | 261.6154 (0.4094) | +26.33 | 0.55, 12 | 266.4851 (5.2791) | +0.985 | 50, 9.3 |
| 261.2697 | 261.2047 (−0.0650) | +35.65 | 0.24, 11 | 269.6315 (8.3617) | +0.934 | 7.4, 3.3 |
| 261.3914 | 261.3478 (−0.0435) | +46.20 | 0.61, 87 | 264.6647 (3.2733) | +0.991 | 19, 0.31 |
| 261.5124 | 261.9057 (0.3933) | +42.26 | 17, 160 | 265.1132 (3.6008) | +1.058 | 20, 0.34 |

The 24 rows of largest |z_8| (median, and range over rows):

| D0 | ratio: D* | ratio: mu | Dlog: D* | Dlog: mu |
|---|---|---|---|---|
| 261.1415 | 260.757 (260.345 to 261.185) | +33.0 (+29.1 to +48.9) | 320.730 (265.867 to 502.786) | +1.388 (+0.861 to +2.498) |
| 261.2061 | 261.276 (260.859 to 261.615) | +37.5 (+25.9 to +41.7) | 295.389 (266.485 to 317.554) | +1.211 (+0.985 to +2.115) |
| 261.2697 | 261.314 (260.987 to 261.425) | +34.4 (+28.4 to +38.2) | 295.566 (269.631 to 454.070) | +1.196 (+0.934 to +2.107) |
| 261.3914 | 261.400 (261.204 to 261.823) | +33.1 (+30.2 to +48.2) | 306.965 (264.665 to 382.858) | +1.258 (+0.991 to +1.416) |
| 261.5124 | 261.747 (261.662 to 261.906) | +38.2 (+36.0 to +42.3) | 451.974 (265.113 to 523.881) | +2.019 (+1.058 to +2.437) |

**Reading: none is read.**

- Delta's ratio D* jumps between 261.18 and 261.91 (range 0.72), and s is negative at two bases.
- Delta's Dlog D* lies between 264.66 and 269.63 (range 4.97).
- No three bases agree to 0.01 in either estimator.
- mu is outside the S band at every base: +26 to +46 by the ratio fit, +0.93 to +1.06 by Dlog. The Dlog medians are
  residues within about 0.07 of 0, where the doublet filter sits (0.05). That is the mark of a spurious pole, not of a
  singularity.

**Diagnostic, outside the criteria** (`signs.py` → `signs966_leg14.txt`, `runs.py` → `runs966_leg14.txt`). At every
base, Delta's c_1..c_31 change sign in runs of 3 or 4:

    D0 261.1415  ----++++----++++----+++----++++
    D0 261.5124  ---+++---+++---+++---+++---+++-

A conjugate pair off the real axis gives this pattern, and a single real singularity does not; it also breaks the
ratio fit. The root test |c_31|^(−1/31) falls from 2.132 to 1.757 over the bases. A rough reading (angle π / mean inner
run, radius from that root test) puts a pair at 262.60 ± 1.56i at D0 261.1415 and at 262.39 ± 1.52i at D0 261.5124.
That reading is not a validated estimator. `jet_singularity.py locate` (Delta's Padé poles, #799's other step) would
test it; it was not run here.

## Second request: locate on leg 14, then rows and locate over leg 13 (coordinator, 2026-11-21)

**Command.** #799 ran Delta's locate through `I799-dh370/report799.py`. That script calls
`row_series(Z, "delta")` and `locate_one(c, m["D"], label="delta")` of `jet_singularity.py`, with no other arguments.
`jet_singularity.py locate JET.npz ... --json OUT` runs the same function on the same row (`--row delta` is the
default), at DPS 80:

    python jet_singularity.py locate JET.npz ... --json OUT

It reports these, each with D_re = D0 + Re s and D_im = Im s:
- the stable Padé poles of Delta's series: clusters over M 2..10 within 0.05 relative, in at least 3 M, not doublets,
  not inside 0.85 of the root-test radius, |s| at most 50, folded to Im ≥ 0; the four nearest are kept;
- the recurrence fit;
- Domb-Sykes;
- the root-test radius (upper envelope of |c_k| fitted over k N/2..N).

**Leg 13's jets** are at raw 98227588: 260.8483, 260.9271, 261.0721 and 261.1415, N 31, ks 293. Its 261.1415 jet
is not bit-identical to leg 14's 261.1415 jet: its state was not re-converged as leg 14's base was. Delta's c_k
differ by at most 1.4e-13 relative (`deltadiff.py` → `deltadiff_261.1415.txt`). The base counts once, as leg 14's.
Leg 13's copy is run too, as a check of how sensitive the estimators are to that difference.

**The locate reading** (the coordinator's, fixed before the run): a conjugate pair of Delta's Padé poles, stable to
0.05 in real and imaginary part across three or more bases, at a distance matching the root test, confirms the pair.
Otherwise the diagnostic stays unvalidated. How I apply it, fixed before the run:

- a pair: a stable pole of `locate` with D_im > 0.05 (its conjugate is implied by the fold to Im ≥ 0);
- stable across bases: at each base, the nearest such pole. Over three or more consecutive bases (leg 13 and leg 14
  in order of D), the range (max − min) of its D_re is at most 0.05, and so is the range of its D_im;
- distance matching the root test: |s| within 5% of `locate`'s root-test radius at each of those bases (#799's bar 2
  used 5%);
- if the nearest pair fails, another chain of pairs that meets all three is reported as well, and named as found
  after the nearest one failed.

**Rows over leg 13.** `singularity_type.py rows --delta` on leg 13's four jets. The fold readings above apply over
leg 13 and leg 14 together.
