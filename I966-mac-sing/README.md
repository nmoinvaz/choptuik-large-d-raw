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

## Results of the second request (2026-11-21 08:14:12 to 08:15:15 UTC, `exits2.txt`, all exit 0)

**Locate** (`locate966_leg14.txt` and `.json`, 14.6 s; `locate966_leg13.txt` and `.json`, 11.0 s; 49 MB). The pair
reading (`pairs.py` → `pairs966.txt`, exit 0):

| D0 | nearest stable pole off the axis: D* | \|s\| | arg | approximants | root test | \|s\| / root − 1 |
|---|---|---|---|---|---|---|
| 260.8483 | 262.0784 ± 0.9730i | 1.5683 | 38.3° | 9 | 1.5682 | +0.01% |
| 260.9271 | 262.0784 ± 0.9730i | 1.5074 | 40.2° | 9 | 1.4927 | +0.98% |
| 261.0721 | 262.0783 ± 0.9730i | 1.3997 | 44.0° | 9 | 1.4120 | −0.87% |
| 261.1415 | 262.0784 ± 0.9730i | 1.3507 | 46.1° | 9 | 1.3533 | −0.19% |
| 261.2061 | 262.0784 ± 0.9730i | 1.3068 | 48.1° | 9 | 1.3244 | −1.33% |
| 261.2697 | 262.0784 ± 0.9731i | 1.2652 | 50.3° | 9 | 1.2636 | +0.13% |
| 261.3914 | 262.0767 ± 0.9731i | 1.1902 | 54.8° | 9 | 1.1963 | −0.51% |
| 261.5124 | 262.0771 ± 0.9731i | 1.1251 | 59.9° | 9 | 1.1327 | −0.67% |

**The pair is confirmed by the fixed reading.** All 8 bases (260.8483 to 261.5124) match the root test to 1.4%. Over
them, D_re ranges over 0.0017 (262.0767 to 262.0784) and D_im over 0.0001 (0.9730 to 0.9731), against the bound 0.05.

Controls of `pairs.py`, each exit 1 as required:
- `--mutate=drift` adds 0.03 per base to D_re (`pairs966_drift.txt`);
- `--mutate=root` scales the root test by 1.1 (`pairs966_root.txt`).

The first form of the control shifted only the last base by 0.1. It could not fail, since the other 7 bases still
held (exit 0), so it was replaced after its first run.

Beside the nearest pole, at every base:
- a second and third stable cluster within 0.012 of it (262.0826 to 262.0886, ± 0.9705 to 0.9721i);
- `locate`'s recurrence fit at 262.0825 to 262.0826 ± 0.9721i;
- a farther stable pair behind the bases at 258.3606 ± 2.2687i (3 to 5 approximants; not listed at 261.5124).

The type of the pair's singularity (pole or branch point) is not read here. Whether the pair moves with the horizon
order, as #1008 found for order 130's fold, is not tested.

The duplicate base 261.1415: leg 13's copy gives the same nearest pole to the last printed digit (D_re and D_im
differences 0.0) and a root test 2.2e-16 away.

**Rows over leg 13** (`type966_leg13.txt`, 37.1 s, 43 MB). Delta's own series:

| D0 | ratio: D* (s) | ratio: mu | Dlog: D* (s) | Dlog: mu |
|---|---|---|---|---|
| 260.8483 | 260.9714 (0.1230) | +23.74 | 262.7834 (1.9351) | +1.057 |
| 260.9271 | 261.2662 (0.3391) | +35.18 | 269.9989 (9.0718) | +0.349 (S, spreads 0: one approximant) |
| 261.0721 | 261.0477 (−0.0244) | +43.78 | 264.4827 (3.4106) | +1.055 |
| 261.1415 | 261.1846 (0.0431) | +37.44 | 265.8674 (4.7259) | +1.052 |

Over legs 13 and 14 (8 bases), no three bases agree on D* to 0.01 in either estimator. mu is in the S band at one
base only, from one approximant. **No real fold is read** from 260.8483 to 261.5124.

**The first diagnostic was wrong in its radius.** Its root test |c_31|^(−1/31) is 1.76 to 2.45, against `locate`'s
envelope fit of 1.13 to 1.57, which includes the prefactor. So its point (262.39 to 262.66 ± 1.49 to 1.78i) is not the
pair's. Its angle from the sign runs (43° to 60°) follows the Padé argument (38° to 60°). Leg 13's signs and the
rough reading are in `signs966_leg13.txt` and `runs966_leg13.txt`.

## Third request: leg 10, before the crossing (coordinator, 2026-11-21)

**Inputs.** Leg 10's 18 jets, `I966-dh370/ks_chain3b/leg10_D256.1776_ks293/jet_pin3_D*.npz`, from 256.1776 to
260.6706 (N 31, ks 293). Commands as before: `jet_singularity.py locate JETS --json OUT` and `singularity_type.py
rows JETS --delta`.

**The reading** (the coordinator's, fixed before the run): if the same pair, to 0.05, is seen from before the
crossing, it does not come from the crossing. A pair that appears or moves only past 260.85 ties it to the crossing.

How I apply it (`pairs10.py`, fixed before the run):

- the reference is the pair of legs 13 and 14, 262.078 ± 0.973i;
- "the same pair, to 0.05": a stable pole of `locate` (any of the four it keeps, not only the nearest) with
  |D_re − 262.078| ≤ 0.05 and |D_im − 0.973| ≤ 0.05. From leg 10's bases the pair need not be the nearest
  singularity, so the root-test match is not required here;
- "seen from before the crossing": the same pair at three or more consecutive leg 10 bases. Then exit 0;
- "appears only past 260.85": no leg 10 base shows it. Then exit 2;
- "moves only past 260.85": leg 10 shows a pole off the axis, stable to 0.05 over three or more consecutive bases,
  at more than 0.05 from the reference, and no base shows the reference pair. Reported with exit 2, and named as
  the moved case;
- anything else (the pair at only one or two bases): exit 3, undecided, reported as is;
- a limit: `locate` keeps only the four nearest stable poles, so a pair behind four nearer ones would not show.

Controls, each of which must change the verdict:

- `--mutate=plant` adds the reference pole to every base's list (detection), and must give exit 0;
- `--mutate=move` moves the reference by 0.1 in D_re. It must give a nonzero exit when the plain run gives 0, and is
  vacuous otherwise.

The fold reading for rows applies over leg 10 as before.

## Results of the third request (2026-11-21 08:20:39 to 08:24:22 UTC, `exits3.txt`, all exit 0)

**The pair, from leg 10** (`locate966_leg10.txt` and `.json`, 55.5 s, 49 MB; `pairs10.py` → `pairs10_966.txt`,
exit 0). **The pair is seen before the crossing, so it does not come from the crossing.** It is among `locate`'s
stable poles at the 15 consecutive bases from 257.1452 to 260.6706, at 262.0783 to 262.0847 ± 0.9684 to 0.9758i
(ranges 0.0063 and 0.0074, against 0.05). Its clusters grow from 3 approximants at the far bases to 9 near the
crossing.

At the first three bases (256.1776 to 256.8479) it is not a stable pole. Those bases list three stable poles, below
the limit of four, so the limit did not hide it.

The controls exit as required: `--mutate=plant` 0 (`pairs10_966_plant.txt`), and `--mutate=move` 2
(`pairs10_966_move.txt`; not vacuous, since the plain run gave 0).

Two other stable pairs are at every leg 10 base:
- P2 = 258.36 ± 2.27i (258.3531 to 258.3646 ± 2.2679 to 2.2962i), all 18 bases;
- 254.68 ± 3.50i, at 9 of the 18.

**Rows over leg 10** (`type966_leg10.txt`, 166.7 s, 43 MB). No real fold is read.
- Delta's ratio D* jumps at every base (s from −0.60 to +0.46, mu +14 to +42).
- Dlog's mu is in the S band at no base. It reads P (−0.81) at 259.4568 only, at s 11.3, and gives no estimate at
  260.0073.
- No three bases agree to 0.01.

**Diagnostic, outside the criteria: the root test against the two pairs** (`geom.py` → `geom966.txt`). Over all 26
bases of legs 10, 13 and 14 (256.1776 to 261.5124), the root-test radius of Delta's series equals the distance from
the base to the nearer of two fixed points to 2.2%:
- P1 = 262.0810 ± 0.9729i, the median over 23 bases;
- P2 = 258.3606 ± 2.2688i, the median over 25.

P2 is the nearer up to 259.4568, and P1 from 259.7352. The root test is smallest near 258.44 (2.2690, against
P2's imaginary part 2.2688), as a fixed pair's distance is when the chain passes its real part.

**For the next bases** (fixed before any of them lands): Re of the pair is read as staying at 262.08 when the nearest
stable pole off the axis is within 0.05 of P1 in D_re and D_im, and the root test is within 5% of |D0 − P1|. If both
hold, the radius on the real line is smallest at D0 ≈ 262.08, at about 0.973.

## Next bases (`newbase.sh`, `nextcheck.py`; outputs `*_D<base>.*`, `exits_new.txt`)

| D0 | raw | nearest stable pole off the axis | root test, \|D0 − P1\|, difference | nextcheck, move control | Delta: ratio D* (mu), Dlog D* (mu) |
|---|---|---|---|---|---|
| 261.6229 | 3a4c2671 | 262.0768 ± 0.9734i (9 approximants) | 1.0841, 1.0754, +0.81% | PASS (0), FAIL (1) | 261.4735 (+32.1), 270.3069 (+1.108) |
| 261.6746 | 3dfb078d | 262.0767 ± 0.9733i (9 approximants) | 1.0537, 1.0544, −0.06% | PASS (0), FAIL (1) | 261.7282 (+39.2), 270.3444 (+1.145) |
| 261.7748 | e544743f | 262.0768 ± 0.9733i (9 approximants) | 1.0212, 1.0199, +0.12% | PASS (0), FAIL (1) | 261.9763 (+38.3), 264.4613 (+0.085) |
| 261.8239 | f54bd692 | 262.0767 ± 0.9734i (9 approximants) | 1.0027, 1.0063, −0.36% | PASS (0), FAIL (1) | 261.9000 (+40.0), 293.3994 (+1.328) |
| 261.9176 | 80d803ea | 262.0887 ± 0.9705i (9 approximants) | 0.9816, 0.9865, −0.50% | PASS (0), FAIL (1) | 261.9070 (+43.4), no Dlog estimate |

Note from 261.9176: three stable clusters sit at every base since 261.0721. Since 261.3914 they lie at 262.0767 to 262.0771 ± 0.9731 to 0.9734i, 262.0826 to 262.0830 ± 0.9719 to 0.9721i, and 262.0882 to 262.0887 ± 0.9705i (`locate966_leg14.json`, `locate966_D*.json`). As the base nears Re 262.08, the one with the smallest Im becomes the nearest, so the table's pole changes cluster there; none of them moved. The recurrence fit stays at 262.0828 ± 0.9722i.
| 262.0099 | bb7b64f3 | 262.0887 ± 0.9705i (9 approximants) | 0.9617, 0.9755, −1.41% | PASS (0), FAIL (1) | 261.8773 (+43.0), 274.3542 (+1.257) |
| 262.1011 | ae5cce13 | 262.0887 ± 0.9705i (9 approximants) | 0.9615, 0.9731, −1.19% | PASS (0), FAIL (1) | 261.5218 (+28.8), 282.6851 (+1.124) |

Note at 262.1011: the base has passed Re 262.08 (the pair now lies at arg 90.7° to 91.4°). The root test is 0.9615, its smallest so far, against the nearest cluster's distance of 0.9706. A real stable pole appears there for the first time, at 265.0469 (4 approximants, 2.95 ahead); none of the 32 earlier bases (256.1776 to 262.0099) lists one. One base is no reading, so the watcher follows it.
| 262.1920 | dce381d5 | 262.0885 ± 0.9707i (9 approximants) | 0.9824, 0.9792, +0.33% | PASS (0), FAIL (1) | 262.2638 (+37.8), 273.2447 (+1.093) |

Note at 262.1920: past Re 262.08 the root test rises again (0.9615 at 262.1011, 0.9824 here), as a fixed pair's distance does. The real stable pole is listed a second time, at 265.0816 (4 approximants), 0.035 from 265.0469 at the previous base. Rows give no real reading near it (Dlog D* 273.24, mu +1.093).
| 262.2833 | dcd2f585 | 262.0882 ± 0.9705i (9 approximants) | 0.9916, 0.9937, −0.21% | PASS (0), FAIL (1) | 262.3443 (+28.9), 359.9728 (+0.786) |

Note at 262.2833: the root test rises to 0.9916 (−0.21% from |D0 − P1|). The real stable pole is listed a third time, at 265.0779 (4 approximants). Over 262.1011 to 262.2833 it is 265.0469, 265.0816 and 265.0779, a range of 0.035, so it does not hold to 0.01. Locate gives it no exponent, and rows give no real reading near it (Dlog D* 359.97 here). No fold is read.
| 262.3756 | 3fcc674b | 262.0872 ± 0.9710i (9 approximants) | 1.0122, 1.0165, −0.43% | PASS (0), FAIL (1) | 262.4502 (+30.7), 672.9987 (+3.803) |

Note at 262.3756: the root test is 1.0122 (−0.43% from |D0 − P1|). The real stable pole is listed a fourth time, at 265.0788 (4 approximants, 2.70 ahead). Over its last three bases (262.1920 to 262.3756) it is 265.0816, 265.0779 and 265.0788, a range of 0.0037, under 0.01. The fixed fold reading is on rows' estimators of Delta, which do not see it (they track the nearer pair; Dlog D* 673.0 here), and locate gives it no exponent. So no fold is read, and it is reported as a candidate: a real Padé pole held to 0.004 over three bases.

## The real pole near D 265.08: readings fixed 2026-11-21 14:49:34 UTC (the coordinator's, before any further base)

The real stable Padé pole was listed at 262.1011 (265.0469), 262.1920 (265.0816), 262.2833 (265.0779) and 262.3756
(265.0788). Those four bases are not counted below.

**(1) Position.** Over the next three new bases, the real stable Padé pole's Re lies within 0.01 of its mean (max |Re −
mean| ≤ 0.01). Then a real singularity of the order-293 system near that D is read, type unknown. Until then each base
reports it as a candidate. The pole is the real stable pole of `locate` (D_im ≤ 0.05) nearest the base.

**(2) Type** (`subdom.py`, written before it reads a real series):

- The estimator is the Dlog estimator on Delta's series with the nearest conjugate pair divided out. g'/g (g = df/dh)
  has a simple pole at each algebraic singularity, with residue mu − 1. It is multiplied by
  a(h) = (1 − h/s1)(1 − h/s̄1), with s1 the base's nearest stable pole off the axis from `locate`. That cancels the
  pair's poles. The Padé approximants [L/M] (M 3 to 9, L M − 1 to M + 1) of a·g'/g give the real pole nearest the
  origin (Re > 0, |Im| below 5% of the modulus), as in `singularity_type.py`. At that pole, mu = 1 + residue / a(s).
  Poles with a corrected residue within 0.05 of 0 or of +1 are skipped, as there. The result is the median over the
  approximants, with its spread.
- **The planted check comes first:**
  - the plant is a conjugate square-root pair at the latest base's s1 (P1 − 262.3756 = −0.2946 + 0.9729i), plus a
    real square-root point at s2 = 2.8;
  - the amplitude ratio is as in the data: a least-squares fit of Delta's c_1..c_31 at 262.3756 to
    2 Re(A1 b_k / s1^k) + A2 b_k / s2^k, with b_k the coefficients of (1 − x)^(1/2) and s2 = 265.0788 − 262.3756.
    The fit assumes square roots; the fitted |A2| / |A1| is used;
  - N 31, relative noise 1e-12 (`singularity_type.py`'s);
  - it passes if the estimator recovers mu to 10% (|mu − 0.5| ≤ 0.05) and the point's distance to 0.5% (|s − 2.8|
    ≤ 0.014);
  - `--mutate=move` builds the point at 2.8 + 0.5 and judges it against 2.8, which must fail;
  - reported beside it, not judged: the same plant with a pole pair (mu1 = −1), the plain Dlog estimator without
    the division, and the division with s1 off by 0.006 (the three clusters' spread; the data's s1 is not exact).
- **Reading, once (1) is met:** the type comes from the median of the estimator's mu over the three bases of (1):
  - within 0.1 of 1/2: a fold. A fold near D 265.08 would cap the ks 293 chain there;
  - within 0.2 of −1: a pole;
  - otherwise not resolved.

### The planted check of (2): passes by its letter, but does not validate the estimator for the data

Run 2026-11-21 14:51 UTC (file time) (`subdom_amp.txt`, `subdom_planted.txt`, `subdom_planted_move.txt`; 1.4 s, 43 MB per run):

- Amplitudes (`amp` at 262.3756, the fixed fit over c_1..c_31): |A2|/|A1| 6.55. The fit does not describe Delta's
  coefficients: the median relative misfit is 0.81 and the largest 1.06.
- Planted check: the divided-out Dlog estimator gives s 2.7917, mu +0.5213 (spreads 1.8 and 0.65 over 20
  approximants): PASS. `--mutate=move` gives s 3.2790 against 2.8: FAIL, as required.
- Unjudged lines:
  - the pole pair: s 2.7975, mu +0.5158;
  - the division with s1 + 0.006: s 2.7905, mu +0.5222;
  - **the plain Dlog without the division: s 2.7964, mu +0.5163.** It sees the planted point just as well. On the
    data, the plain Dlog never sees anything near 265 (`type966_D*.txt`: D* 264 to 673).

So this plant is easier than the data, and the division is not what finds the point in it.

Diagnostic (`ampdiag.py` → `ampdiag.txt`, outside the protocol): the same fit over orders k0..31 for k0 1, 10, 16 and 21,
with and without the second pair P2. Its misfit is 0.13 to 0.81, and |A2|/|A1| grows from 6.5 to 1.6e8 as k0 rises. So
the square-root two-term model does not describe the data, and the data does not fix "the relative amplitudes" through
it. At every fitted ratio, the plain Dlog recovers the planted point.

The estimator has not been run on a real series. Its type reading waits for the coordinator's decision on the plant.

### The type check of (2), as amended: fixed 2026-11-21 14:53:52 UTC (the coordinator's, before any real run)

It replaces the planted check above (`subdom.py scan`):

- The plant is as above: the pair at s1 = −0.2946 + 0.9729i with A1 from `amp`, and the real square-root point at
  2.8, N 31, noise 1e-12. Only A2 changes: |A2|/|A1| = 6.5497 / 2^j for j = 0, 1, 2, ... (to j = 40 at most).
- **Realism:** j* is the first j at which the plain Dlog (`singularity_type.dlog_fit`, no division) fails the bars
  (|mu − 0.5| ≤ 0.05 and |s − 2.8| ≤ 0.014) on the square-root-pair plant, as it fails on the data. The scan's plain
  results for the pole pair are reported beside it.
- **Pass:** at j*, j* + 1 and j* + 2, the divided-out estimator meets the same bars on the square-root-pair plant and
  on the pole-pair plant (mu1 = −1). `--mutate=move` (the point built at 3.3, judged against 2.8) fails at each of the
  six.
- If no j up to 40 has the plain Dlog failing, or the divided-out estimator fails at any of the six, the type stays
  not resolved at N 31. `scan` exits 0 when the check passes, 2 otherwise.
- Reading (1) runs as set.

### Result of the amended type check (`subdom_scan.txt`, 2026-11-21 14:55 UTC file time, exit 2; 6.3 s, 42 MB)

| j | \|A2\|/\|A1\| | plain Dlog, square-root pair | divided-out, square-root pair | divided-out, pole pair | move control |
|---|---|---|---|---|---|
| 0 | 6.5497 | s 2.7964, mu +0.5163: meets | | | |
| 1 | 3.2749 | s 2.7958, mu +0.5292: meets | | | |
| 2 (j*) | 1.6374 | s 2.7803, mu +0.5686: fails | s 2.7834, mu +0.5707: FAIL | s 2.7898, mu +0.5617: FAIL | fails at both |
| 3 | 0.8187 | | s 2.7649, mu +0.6264: FAIL | s 2.7823, mu +0.6186: FAIL | fails at both |
| 4 | 0.4094 | | s 2.7352, mu +0.7143: FAIL | s 2.7587, mu +0.7090: FAIL | fails at both |

**The type stays not resolved at N 31.** Where the plain Dlog stops recovering the point, the divided-out estimator
stops too. Its mu drifts up as the point weakens (+0.57, +0.63, +0.71), and it misses the 0.5% bar on s. Dividing out
the pair does not make it better than the plain estimator in this plant. The estimator is not run on a real series.
Reading (1), the position, runs at the next bases.
