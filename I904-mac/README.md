# I904-mac: the held fit's degree spread d6 − d10 past D 248, from #608's chains' own jets, against the departure

Machine: the Mac (Apple M5), one process at nice 10, stored data only. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/904

Code: `hp/held_spread.py` on branch wip/xf-904 (474cf172), run as `python3 held_spread.py run RAW --out=run.json`. The mutations are `--mutate=base|fit`. PYTHONPATH is the #523 build (i599/site2). Checks registered on #904 before any number was computed.

Data:
- d6 chain: `I608-dh610/restart2_d6`, `I836-dh370/drop` (the step 252.6966 → 252.7855) and `I608-dh610/restart4_d6`. 30 states, 31 jets, ending at D 253.432804.
- d10 chain: `restart2_d10` and `restart3_d10`. 32 states, 34 jets, ending at 253.897447.
- Targets: #603's state D values with chain − series (`I805-mac/table.json`), from 248.02 to 253.35.

## Checks

| check | result | verdict |
|---|---|---|
| mutation base (jet bases moved 1e-6) | C1 1.7e-10 | fails, as it must |
| mutation fit (the other degree's fit) | C2 3.7e-7 / 4.0e-7 | fails, as it must |
| C2: every state's held values follow its own chain's fit from the first state | d6 0 (exact), d10 6.5e-54 | pass, across the #836 state too |
| C1: each jet at the next state's D against that state's Δ, bar 1e-20 | up to 4.0e-15 (d6, 253.42) and 1.5e-15 (d10, 253.82) | **fails as registered**, cause below |

C1's misses are the chains' own corrector moves. At 61 of 63 steps the miss equals the step's logged `moved` (the Δ correction from the series' prediction) to a ratio of 0.96–1.04 (`c1_vs_moved.log`). The two others:
- **252.7855:** the d6 junction, where #836's state came from 252.6966 and not from the 252.7411 jet. The miss there is 1.5e-16.
- **252.0:** a log line matched to the wrong attempt, 6e-19 against 2.6e-18.

So C1 measures the series' prediction error at a step's end, not the evaluation. A jet's Δ inside a step is good to about that move, ≤ 4e-15, which is ≤ 2e-4 of the smallest |d6 − d10| among the targets. I set the 1e-20 bar from #805's ≤ 1.7e-29 for #603's own steps, and #608's chains move 1e-19 to 4e-15 per step past 250.5.

## Results (`run.log`)

| D | d6 − d10 | chain − series | r | \|d6 − d10\|·p_min | \|dep\|·p_min |
|---|---|---|---|---|---|
| 248.0194 | +1.055e-10 | +3.731e-10 | +0.283 | 1.8e-38 | 6.4e-38 |
| 248.6298 | +2.084e-11 | +1.818e-9 | +0.012 | 1.8e-39 | 1.6e-37 |
| 249.0113 | −1.517e-10 | +3.287e-9 | −0.046 | 8.2e-39 | 1.8e-37 |
| 249.3927 | −4.667e-10 | +4.792e-9 | −0.097 | 2.0e-38 | 2.0e-37 |
| 249.8696 | −1.086e-9 | +4.854e-9 | −0.224 | 2.1e-38 | 9.4e-38 |
| 250.1676 | −1.580e-9 | +1.804e-9 | −0.876 | 1.7e-38 | 1.9e-38 |
| 250.4656 | −2.125e-9 | −6.108e-9 | +0.348 | 1.4e-38 | 4.1e-38 |
| 250.8381 | −2.859e-9 | −2.739e-8 | +0.104 | 8.8e-39 | 8.4e-38 |
| 251.3038 | −4.043e-9 | −8.136e-8 | +0.050 | 7.3e-39 | 1.5e-37 |
| 251.8859 | −7.600e-9 | −1.994e-7 | +0.038 | 7.2e-39 | 1.9e-37 |
| 252.2497 | −1.328e-8 | −2.797e-7 | +0.047 | 1.0e-38 | 2.1e-37 |
| 252.6135 | −2.466e-8 | −3.011e-7 | +0.082 | 1.8e-38 | 2.2e-37 |
| 253.0682 | −5.305e-8 | −3.457e-8 | +1.534 | 7.8e-39 | 5.1e-39 |
| 253.2103 | −6.661e-8 | +1.841e-7 | −0.362 | 7.8e-39 | 2.2e-38 |
| 253.3524 | −8.304e-8 | +5.046e-7 | −0.165 | 7.9e-39 | 4.8e-38 |

The jets' truncation estimates are 1e-29 or less everywhere (`run.log`).

| acceptance | result | verdict |
|---|---|---|
| A1: r constant to 30% over 251–253.43 (7 targets) | median +0.048, max\|r\|/min\|r\| 40, signs mixed | **not constant; drift above a factor 3** |
| A2: d6 − d10 at 250.1676 against #905's adjoint, −1.683e-9 | −1.580e-9, ratio 0.94 | within a factor 2 |

## Reading

d6 − d10 changes sign near 248.7. Past that it is negative, smooth and growing, with |d6 − d10|·p_min between 0.7e-38 and 2.1e-38 from 249 to 253.35, so it grows at the weak pivot's rate. The departure follows the same 1/p_min envelope, up to 2.2e-37/p_min, but changes sign twice in 250.2–253.2 (#805). So r is not constant. The held fit's spread is about a tenth of the departure's envelope and has one sign, so it is not the departure's source.

The adjoint (#905) predicts the held spread at 250.17 to 6% from the chains themselves, so the held values enter linearly there.
