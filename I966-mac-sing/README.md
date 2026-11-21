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

| D0 | raw | nearest stable pole off the axis | root test, \|D0 − P1\|, difference | 265.078 − D0 | nextcheck, move control | Delta: ratio D* (mu), Dlog D* (mu) |
|---|---|---|---|---|---|---|
| 261.6229 | 3a4c2671 | 262.0768 ± 0.9734i (9 approximants) | 1.0841, 1.0754, +0.81% | 3.4551 | PASS (0), FAIL (1) | 261.4735 (+32.1), 270.3069 (+1.108) |
| 261.6746 | 3dfb078d | 262.0767 ± 0.9733i (9 approximants) | 1.0537, 1.0544, −0.06% | 3.4034 | PASS (0), FAIL (1) | 261.7282 (+39.2), 270.3444 (+1.145) |
| 261.7748 | e544743f | 262.0768 ± 0.9733i (9 approximants) | 1.0212, 1.0199, +0.12% | 3.3032 | PASS (0), FAIL (1) | 261.9763 (+38.3), 264.4613 (+0.085) |
| 261.8239 | f54bd692 | 262.0767 ± 0.9734i (9 approximants) | 1.0027, 1.0063, −0.36% | 3.2541 | PASS (0), FAIL (1) | 261.9000 (+40.0), 293.3994 (+1.328) |
| 261.9176 | 80d803ea | 262.0887 ± 0.9705i (9 approximants) | 0.9816, 0.9865, −0.50% | 3.1604 | PASS (0), FAIL (1) | 261.9070 (+43.4), no Dlog estimate |

Note from 261.9176: three stable clusters sit at every base since 261.0721. Since 261.3914 they lie at 262.0767 to 262.0771 ± 0.9731 to 0.9734i, 262.0826 to 262.0830 ± 0.9719 to 0.9721i, and 262.0882 to 262.0887 ± 0.9705i (`locate966_leg14.json`, `locate966_D*.json`). As the base nears Re 262.08, the one with the smallest Im becomes the nearest, so the table's pole changes cluster there; none of them moved. The recurrence fit stays at 262.0828 ± 0.9722i.
| 262.0099 | bb7b64f3 | 262.0887 ± 0.9705i (9 approximants) | 0.9617, 0.9755, −1.41% | 3.0681 | PASS (0), FAIL (1) | 261.8773 (+43.0), 274.3542 (+1.257) |
| 262.1011 | ae5cce13 | 262.0887 ± 0.9705i (9 approximants) | 0.9615, 0.9731, −1.19% | 2.9769 | PASS (0), FAIL (1) | 261.5218 (+28.8), 282.6851 (+1.124) |

Note at 262.1011: the base has passed Re 262.08 (the pair now lies at arg 90.7° to 91.4°). The root test is 0.9615, its smallest so far, against the nearest cluster's distance of 0.9706. A real stable pole appears there for the first time, at 265.0469 (4 approximants, 2.95 ahead); none of the 32 earlier bases (256.1776 to 262.0099) lists one. One base is no reading, so the watcher follows it.
| 262.1920 | dce381d5 | 262.0885 ± 0.9707i (9 approximants) | 0.9824, 0.9792, +0.33% | 2.8860 | PASS (0), FAIL (1) | 262.2638 (+37.8), 273.2447 (+1.093) |

Note at 262.1920: past Re 262.08 the root test rises again (0.9615 at 262.1011, 0.9824 here), as a fixed pair's distance does. The real stable pole is listed a second time, at 265.0816 (4 approximants), 0.035 from 265.0469 at the previous base. Rows give no real reading near it (Dlog D* 273.24, mu +1.093).
| 262.2833 | dcd2f585 | 262.0882 ± 0.9705i (9 approximants) | 0.9916, 0.9937, −0.21% | 2.7947 | PASS (0), FAIL (1) | 262.3443 (+28.9), 359.9728 (+0.786) |

Note at 262.2833: the root test rises to 0.9916 (−0.21% from |D0 − P1|). The real stable pole is listed a third time, at 265.0779 (4 approximants). Over 262.1011 to 262.2833 it is 265.0469, 265.0816 and 265.0779, a range of 0.035, so it does not hold to 0.01. Locate gives it no exponent, and rows give no real reading near it (Dlog D* 359.97 here). No fold is read.
| 262.3756 | 3fcc674b | 262.0872 ± 0.9710i (9 approximants) | 1.0122, 1.0165, −0.43% | 2.7024 | PASS (0), FAIL (1) | 262.4502 (+30.7), 672.9987 (+3.803) |

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

## The conformal-map route: fixed 2026-11-21 14:57:55 UTC (the coordinator's order, before any planted or real run)

**Order.** Reading (1) comes first, over the next three new bases. If the position does not hold, this route stops
there. If it holds, the planted check below runs. Only if that passes does the estimator run on the three bases of (1).

**The map** (`confmap.py`). A Möbius map of the unit disk onto the disk |h − c| < R, with R = s2 − c:
h = φ(w) = c + R (w − a) / (1 − a w), a = c / R. It sends w = 0 to h = 0 and w = 1 to the real point s2. Its other
images:
- the conjugate pair s1 and P2 = 258.3606 ± 2.2688i map outside the unit disk;
- infinity maps to w = 1/a.

c is chosen on a grid of 0.001 to maximize the smallest of |w(s1)|, |w(P2)| and 1/a. For the plant's geometry
(262.3756, s2 2.8) that is c 1.264: pair at |w| 1.2105, P2 at 1.3676, infinity at 1.2152, the real point at 1. At a
real base, s1 is the base's nearest stable pole off the axis, and s2 is the real stable pole from `locate`, minus D0.

**The mapped estimator.**
- Delta's c_1..c_N are composed with φ to give the series d_1..d_N of f(φ(w)), exactly from c_1..c_N, since φ(0) = 0.
- `singularity_type.dlog_fit` is applied to d.
- Its real pole w* maps back to s = φ(w*). The exponent is unchanged by the map.

**The planted check** (`confmap.py scan`, the strict protocol of 14:53:52):
- the plant of `subdom.py`: the pair at s1 = −0.2946 + 0.9729i with A1 from `amp`, and the real square-root point
  at 2.8, N 31, noise 1e-12, with |A2|/|A1| = 6.5497 / 2^j;
- j* is the first j at which the plain Dlog (unmapped) fails the bars (|mu − 0.5| ≤ 0.05, |s − 2.8| ≤ 0.014) on the
  square-root-pair plant;
- at j*, j* + 1 and j* + 2, the mapped estimator must meet the bars for the square-root pair and for the pole pair;
- `--mutate=move` must fail at each of the six: the point is built at 3.3, the map is built for 2.8, and it is judged
  against 2.8;
- reported, not judged: the plant with P2 added (as a square-root pair, at A1's amplitude), and the map built with s2
  off by 0.01 and with s1 off by 0.006.

If it fails, the type stays not resolved at N 31. If it passes, the type comes from the median mu over the three
bases of (1): within 0.1 of 1/2 a fold, within 0.2 of −1 a pole, otherwise not resolved.
| 262.4705 | fcf73363 | 262.0871 ± 0.9709i (9 approximants) | 1.0472, 1.0480, −0.08% | 2.6075 | PASS (0), FAIL (1) | 262.6633 (+27.9), 334.4578 (+1.601) |

Reading (1), base 1 of 3 (262.4705): the real stable pole is at 265.0780 (4 approximants). `reading1.py` (pending, exit 3) gives the verdict once three new bases have landed; its control `--mutate=shift` adds 0.02 to the first base.
| 262.5706 | 86484665 | 262.0871 ± 0.9709i (9 approximants) | 1.0866, 1.0892, −0.23% | 2.5074 | PASS (0), FAIL (1) | 262.5092 (+34.9), 325.0839 (+2.356) |

Reading (1), base 2 of 3 (262.5706): the real stable pole is at 265.0778 (4 approximants); 265.0780 at base 1. Pending (exit 3).
| 262.6802 | cdc91937 | 262.0871 ± 0.9709i (9 approximants) | 1.1410, 1.1426, −0.14% | 2.3978 | PASS (0), FAIL (1) | 262.3202 (+21.8), 272.3348 (-20.768) |

## Reading (1): MET (`reading1.py` → `reading1.txt`, exit 0)

| base | real stable pole (approximants) |
|---|---|
| 262.4705 | 265.0780 (4) |
| 262.5706 | 265.0778 (4) |
| 262.6802 | 265.0778 (4) |

The mean is 265.0779, and the largest |Re − mean| is 0.0001, against the bound 0.01. **A real singularity of the order-293
system is read near D 265.078, type unknown.** The control `--mutate=shift` (+0.02 at the first base) gives 0.0135,
NOT met, exit 1 (`reading1_shift.txt`).

## The conformal-map type check: FAIL (`confmap_scan.txt`, 2026-11-21 16:44 UTC file time, exit 2; 8.6 s, 41 MB)

The map for s2 2.8 has c 1.264, which puts the pair at |w| 1.2105, P2 at 1.3676 and infinity at 1.2152. j* = 2, as in
`subdom_scan.txt`.

| j | \|A2\|/\|A1\| | mapped, square-root pair | mapped, pole pair | move control |
|---|---|---|---|---|
| 2 | 1.6374 | s 2.8378, mu +0.5445: FAIL (s) | s 2.7906, mu +0.5615: FAIL | fails at both |
| 3 | 0.8187 | s 3.1107, mu +0.4023: FAIL | s 2.7792, mu +0.6179: FAIL | fails at both |
| 4 | 0.4094 | s 3.0951, mu +0.5263: FAIL (s) | s 2.7585, mu +0.7113: FAIL | fails at both |

For the square-root pair, mu is within 10% at j 2 and 4, but s misses the 0.5% bar by 0.038 and 0.295. The spreads
over approximants in mu are 1.0 to 1.2. Unjudged at j 2: P2 added gives s 2.9763, mu +0.4147; s2 + 0.01 and s1 + 0.006
give s 2.84, mu +0.54. **By the fixed protocol, the type stays not resolved at N 31.** The mapped estimator is not run
on a real series.

## The plant protocol at N 47 and N 63: fixed 2026-11-21 16:45:57 UTC (the coordinator's, before the run)

**Reading** (the coordinator's): the order of a one-off series to compute at D 262.7908 is the smallest N at which one
of the two estimators (divided-out or mapped) passes all six. If neither passes by N 63, the type waits for the chain
itself to reach D 265.

**What changes with N** (`scanN.py N`; written before it runs):
- The geometry is the same: s1 = −0.2946 + 0.9729i, s2 2.8, A1 and the start ratio 6.5497 from `amp`, noise 1e-12,
  P2 for the map. The plant gains orders 32 to N.
- j* is found again at each N, with the plain Dlog at that N's degrees.
- **The Padé degrees grow with N.** As written, both estimators use M 3 to 9 (L ≤ M + 1). So they read at most the
  first 21 coefficients, and the plants' first 31 coefficients and noise draws are the same at every N. With those
  degrees, N 47 and N 63 would repeat N 31 exactly and could not decide anything. So M runs from 3 to
  M_max = ⌊(N − 1)/3⌋ − 1, which uses the same two thirds of the Dlog series as at N 31:
  - N 31: M_max 9, as before;
  - N 47: M_max 14;
  - N 63: M_max 19.

  The same rule holds for the plain Dlog (`singularity_type.MS`), the divided-out estimator and the mapped one.
- As a check that this reasoning holds, `scanN.py N --mmax 9` runs the old degrees at N 47 and must reproduce N 31's
  verdicts.
- Bars, pair types, the move control and exits are unchanged: exit 0 when one estimator passes all six, 2 otherwise.

## Result at N 47 and N 63 (`exits_scanN.txt`, 2026-11-21 16:47:02 to 16:50:30 UTC; all exit 2)

- **The check:** `scanN.py 47 --mmax 9` (`scanN47_m9.txt`, 11.0 s) reproduces the N 31 numbers of `subdom_scan.txt` and
  `confmap_scan.txt` to the printed digit. So the old degrees could not have decided anything.
- **N 47, M 3..14** (`scanN47.txt`, 50.1 s, 41 MB): j* = 2 (plain Dlog s 2.7857, mu +0.5623). Neither estimator passes
  any of the six.
- **N 63, M 3..19** (`scanN63.txt`, 144.9 s, 41 MB): j* = 2 (plain Dlog s 2.7898, mu +0.5558). The mapped estimator
  passes one of six (square-root pair at j 2: s 2.7938, mu +0.5484). The divided-out estimator passes none.
- The move control fails at all 12 of its runs per N (3 ratios, 2 pair types, 2 estimators).

| N | j* | plain Dlog at j* (s, mu) | divided-out: passes of 6 | mapped: passes of 6 | mapped, square-root pair, mu at j 2, 3, 4 |
|---|---|---|---|---|---|
| 31 | 2 | 2.7803, +0.5686 | 0 | 0 | +0.5445, +0.4023, +0.5263 |
| 47 | 2 | 2.7857, +0.5623 | 0 | 0 | +0.5614, +0.6145, +0.7001 |
| 63 | 2 | 2.7898, +0.5558 | 0 | 1 | +0.5484, +0.5924, +0.6658 |

**Reading: neither estimator passes all six by N 63, so the type waits for the chain itself to reach D 265.** No
one-off series is ordered from this check. With N, the pole-pair and weaker-point cases move toward mu 1/2 only slowly,
for example the mapped square-root pair at j 4 goes from +0.70 at N 47 to +0.67 at N 63. And j* stays at 2 as the plain
Dlog improves with them.
| 262.7908 | 8caffc64 | 262.0871 ± 0.9709i (9 approximants) | 1.1974, 1.2043, −0.57% | 2.2872 | PASS (0), FAIL (1) | 262.5082 (+29.6), 515.1630 (+2.826) |

Note at 262.7908: the real singularity read near 265.078 is listed at 265.0778, now with 6 approximants (4 before), 2.29 ahead. That is within 0.0002 of the three bases of reading (1).

## The front test at D 262.7908 (#1064, dh610's three jets): how they are read, fixed 2026-11-21 17:36:02 UTC

**Inputs.** dh610 pushes three jets to `I1064-dh610/front_D262.7908/`, all from dh370's base
`anm_pin3_D262.7908.npz`:
- (a) ks 293 on the state's plan, the control;
- (b) ks 293 re-planned;
- (c) ks 395.

Each is read with `newjet.sh TAG RAWPATH`: `newbase.sh`'s steps, with outputs named by tag.

**Readings** (the coordinator's, in #1064's last comment):
- the real pole's Re moving by more than 0.01 from (a) to (b) means it belongs to the plan;
- moving by more than 0.01 from (b) to (c) means it belongs to the truncation;
- under 0.01 in both means neither, at this resolution;
- P1 is read the same way, in Re and Im.

**What is compared** (`front_compare.py`, fixed before any of the three lands):
- **The real pole:** locate's real stable pole (D_im ≤ 0.05) nearest 265.078, within 0.5 of it. If a jet has none,
  that is reported as no real pole, and no move is read for it.
- **P1:** locate lists up to three stable clusters near the pair, at about 262.0768, 262.0829 and 262.0871, about
  0.01 apart. "The nearest pole" can switch cluster between runs, and that alone would fake a move of about 0.01. So
  P1 is the cluster off the axis with the most approximants, ties going to the one nearest 262.081 ± 0.973i. Its move
  is read against the same rule in the other jet.
- Reported beside them, not read:
  - every cluster matched to its nearest in the other jet;
  - locate's recurrence fit, one value per series.
- **Control checks:**
  - (a) against dh370's jet: Delta's c_k relative differences (`deltadiff.py`) and the two locate results, which
    must agree to the printed digit;
  - `front_compare.py --mutate=move` adds 0.02 to (c)'s real pole, and must read "truncation".

**Accepted by the coordinator (2026-11-21 17:37:45 UTC, before any front jet):** the P1 rule stands, and the decision rests on the real
pole. Its spread over bases is 0.0001, so 0.01 is a clear test. P1's clusters sit 0.01 apart, the size of the bar, so
a P1 move is reported but decides nothing alone. The three readings go to #1064 once (c) is read.

### Amendment (2026-11-21 17:41:18 UTC, the coordinator's, #1064 comment of 17:40:24 UTC; before any front jet is read)

**Run (c) is dropped.** At the front the raise fails even for one added order (dh170's part 3). It is replaced by
**(c′)**: two jets at D 237.7132, ks 307 and ks 395 (`I1064-dh610/front_D262.7908/order_arm_D237.7132/`).

**(a) against (b)** at D 262.7908 is unchanged. `front_compare.py` takes two files, (a) and (b), and reads only
(a) − (b). If (b) fails at its first step, that failure is its result.

**(c′)'s reading:** every stable pole within reach of each jet is reported (`order_compare.py K307.json K395.json`).
P2 (258.361 ± 2.269i) is expected nearest, at distance 20.8, and P1 and the real pole at 265.078 are read only if
seen. A pole that moves by more than 0.01 between K 307 and K 395 belongs to the truncation. A pole not seen in both
gets no reading.

How poles are matched (fixed now): each stable pole of K 307 is paired with the nearest stable pole of K 395 within
0.05 |s| (locate's own clustering tolerance). An unpaired pole is "not seen in both". The move is the larger of |ΔRe|
and |ΔIm|. The poles within 0.1 of P2, P1 or 265.078 are named.

Control: `--mutate=move` adds 0.02 to K 395's pole nearest P2. It must read "truncation" for P2, when P2 is seen.

**Dry run of `order_compare.py` on a real base at D 237.7132** (dh370's `leg00_D237.7132_ks291/jet_pin3_D237.7132.npz`,
ks 291, given as both K 307 and K 395; a tool test, not a reading; `locate966_dry_leg00_D237.7132.txt`):
- the root-test radius is 8.606;
- the stable poles are 238.0752 ± 8.4379i (|s| 8.446, n 5), 234.4315 ± 8.0070i (8.653, n 3) and 242.2589 ± 7.7834i
  (9.014, n 4);
- P2 (|s| 20.8), P1 (24.4) and the real pole at 265.078 (27.4) are not listed. `locate` keeps the four nearest stable
  poles, so from this D the poles of the front lie behind nearer ones;
- the tool pairs the three poles with moves of 0, and `--mutate=move` reads "truncation" for the moved pole. For P2
  the control is vacuous, since P2 is not seen.

If the ks 307 and ks 395 jets look like this one, (c′) reads only these poles at |s| 8.4 to 9.0 and gives no reading for
P2, P1 or the real pole.

**Dry runs for the moved order arm** (amendment 2, #1064 comment 7066694656; tool runs, not readings):

| base (dh370's jet, ks 293) | root test | stable poles kept (limit 4) | P2 / P1 / real 265.078 (distance) |
|---|---|---|---|
| leg10 D 256.1776 (raw 448fdb5f) | 3.1433 | 258.3605 ± 2.2688i (n 9), 258.3536 ± 2.2962i (n 3), 254.6766 ± 3.5009i (n 7) | P2 seen (3.15); P1 (5.98) and the real pole (8.90) not seen |
| leg02 D 250.7060 (raw 02063e60) | 4.7038 | 250.9407 ± 4.7832i (n 9), 254.6766 ± 3.5008i (n 7), 247.0562 ± 6.2843i (n 5) | none seen (7.98, 11.42, 14.37) |

At both bases fewer than four poles are kept, so the limit hides nothing: P1 and the real pole are not stable poles
there. From 256.1776 an order arm can read P2 and the pair 254.68 ± 3.50i. From 250.7060 it can read neither P2 nor
anything of the front. The pair 254.6766 ± 3.5009i is at the same place, to 1e-4, from both bases.

**Accepted (2026-11-21 17:45:32 UTC, #1064's newest comment):**
- the order arm at D 256.1776 reads P2, as its most-populated cluster within 0.1 of 258.361 ± 2.269i (the n 9 one in the
  dry run), and the pair near 254.6766 ± 3.5009i, the same way;
- D 250.7060 is only a chain-start test and gets no reading;
- the real pole's direct test is the plan arm (b) at D 262.7908.

`order_compare.py` reads named poles by that rule: for each of P2, P1, the real pole and 254.677 ± 3.501i, the
most-populated stable cluster within 0.1 of it in each jet. That is the read value. The pairing of all poles is
reported beside it.
| 262.8471 | 9c9ba932 | 262.0871 ± 0.9709i (9 approximants) | 1.2381, 1.2383, −0.02% | 2.2309 | PASS (0), FAIL (1) | 262.8519 (+30.7), no Dlog estimate |

Note at 262.8471: the real pole is at 265.0778 (6 approximants). The ratio fit gives s 0.0048 with a small spread (6.1e-3), but mu +30.65, far outside the square-root band, at one base only, so no fold is read.

## The real pole on the chain's path: reading fixed 2026-11-21 18:05:25 UTC (the coordinator's, #966 comment 7066990195)

P1 stays the nearest singularity until D 263.425, where P1 and the real pole are both 1.653 away. Past that, the real
pole should take over. The per-base table gains a column `265.078 − D0` beside the root test.

**Reading** (`reading_real.py`):
- two bases in a row with D0 > 263.5 and the root test within 5% of 265.078 − D0 confirm the real pole on the
  chain's path;
- the root test more than 5% above 265.078 − D0 at two bases in a row means the pole is not there;
- `--mutate=scale` multiplies each root test by 1.2, which must read "not there" once two bases past 263.5 exist.

**Amended (2026-11-21 18:07:04 UTC, the coordinator's):**
- (1) a root test more than 5% *below* 265.078 − D0 at two bases in a row past 263.5 means some other singularity is
  nearer. It is reported as that, with no reading on the real pole. `reading_real.py` exits 0 when the pole is
  confirmed, 1 when it is not there, 2 when another singularity is nearer, and 3 while pending.
- (2) a planted check before any real base: synthetic rows at D 263.6 and 263.7, with radii (265.078 − D) × 1.00, ×
  1.20 and × 0.80, must give confirm, not there and nearer singularity. `--mutate=scale` must flip the × 1.00 case.

**Planted check of `reading_real.py`** (`planted_real/`, synthetic rows at D 263.6 and 263.7 with no poles):

| radius | reading | exit |
|---|---|---|
| (265.078 − D) × 1.00 | CONFIRMED | 0 |
| × 1.20 | NOT THERE | 1 |
| × 0.80 | ANOTHER SINGULARITY NEARER | 2 |
| × 1.00 with `--mutate=scale` | NOT THERE (flipped) | 1 |

All four are as required.
| 262.9679 | 85493cd1 | 262.0871 ± 0.9709i (9 approximants) | 1.3145, 1.3165, −0.15% | 2.1101 | PASS (0), FAIL (1) | 262.7822 (+43.0), 310.9014 (+1.681) |

## The front jets (dh610, raw 8bf5af2a): read 2026-11-21 18:26 UTC; the plan arm waits on the control

The jets' sha256 match dh610's `jets_sha256.txt`. (b)'s plan differs from (a)'s: 3229ae03… against 2f2fb22d…, 23 steps
each. The order arm's two bases share plan 5de37a18… (21 steps).

| comparison | Delta's c_k, largest relative difference | real pole 265.0778 | P1 (n 9 cluster) 262.0871 ± 0.9709i | other poles | reading |
|---|---|---|---|---|---|
| dh370's jet against (a) (`front_dh370_vs_a.txt`) | 1.5e-17 (k 11) | difference 0 (double) | 0 | the n 7 and n 4 clusters: 0 | information: the control's size is invisible at the 0.01 scale |
| (a) against (b) (`front_a_vs_b.txt`) | 4.0e-16 (k 11) | 0 | 0 | 0; root test 2.2e-16 | moves 0 < 0.01: not the plan at this resolution (**waiting on the control**) |
| (c′) K 307 against K 395 at D 237.7132 (`order_k307_vs_k395.txt`) | (dh610: whole jet 4.1e-11) | not seen | not seen | 238.0752 ± 8.4379i, 234.4315 ± 8.0070i, 242.2589 ± 7.7834i: at most 5.3e-15 | near poles: neither at this resolution. P2 and the 254.68 pair are not seen from D 237.7, so no reading |

Controls: `front_compare.py --mutate=move` reads "plan" for the moved real pole, and `order_compare.py --mutate=move`
reads "truncation" for the moved pole. The near poles at D 237.7132 are also those of dh370's ks 291 jet (the dry run),
to the printed digit.
| 263.0929 | dd1d7743 | 262.0871 ± 0.9709i (9 approximants) | 1.4090, 1.4038, +0.37% | 1.9851 | PASS (0), FAIL (1) | 263.0409 (+42.7), 270.9619 (+1.093) |

Note at 263.0929: the root test is 1.4090, still along |D0 − P1| (+0.37%), and 29.0% below 265.078 − D0 (1.9851); the path reading is pending until 263.5. The real pole is at 265.0778 (6 approximants). A second real stable pole appears, at 267.1413 (3 approximants, the stability minimum). locate now keeps four poles (two pair clusters and the two real poles), so the limit is reached, and the n 4 cluster at 262.0768 is no longer listed.

Correction and addition at 263.0929 (from this base on, `locate6.py` also lists up to 6 stable poles; the coordinator, 2026-11-21): there are 4 stable poles in all at this base. So the limit hides nothing, and the 262.0768 cluster is not stable here, rather than pushed off the list as the note above implied. The second real pole at 267.1413 (3 approximants) is reported at each base for persistence. A string of real poles past 265.08 is what Padé approximants give along a branch cut, so it is information only, with no reading.
| 263.2241 | 73f15ecb | 262.0870 ± 0.9708i (9 approximants) | 1.4975, 1.5011, −0.23% | 1.8539 | PASS (0), FAIL (1) | 262.5934 (+32.5), 274.9322 (+1.161) |

Note at 263.2241: the root test is 1.4975, along |D0 − P1| (−0.23%), and 19.2% below 265.078 − D0 (1.8539); the path reading is pending until 263.5. The 6-pole list has 4 stable poles in all: the pair clusters 262.0870 ± 0.9708i (n 9) and 262.0786 ± 0.9729i (n 6), the real pole 265.0778 (now n 8), and the second real pole at 267.1586 (n 3, 0.017 from 267.1413 at 263.0929). The second real pole is information only.
| 263.3677 | 5d3c1f2f | 262.0870 ± 0.9708i (8 approximants) | 1.6098, 1.6131, −0.21% | 1.7103 | PASS (0), FAIL (1) | 264.2710 (+47.4), 265.1721 (+0.701) |

Note at 263.3677: the root test is 1.6098, along |D0 − P1| (−0.21%), and 5.9% below 265.078 − D0 (1.7103). P1 (1.6131) is still nearer than the real pole; the path reading is pending until 263.5. The 6-pole list has 5 stable poles, so the 4-pole list drops one: the pair clusters 262.0870 ± 0.9708i (n 8) and 262.0786 ± 0.9729i (n 6); the real pole as two clusters, 265.0777 (n 8) and 265.0780 (n 4); and the second real pole at 267.1647 (n 4, after 267.1413 and 267.1586). Rows' plain Dlog gives, for the first time, D* 265.1721 with mu +0.7008, but from one approximant only (spreads 0). Its estimator fails the planted check for this geometry, so that is no reading.
| 263.4439 | 7bd2376a | 262.0870 ± 0.9713i (8 approximants) | 1.6809, 1.6745, +0.38% | 1.6341 | PASS (0), FAIL (1) | 262.9015 (+18.9), 273.9527 (+1.150) |
