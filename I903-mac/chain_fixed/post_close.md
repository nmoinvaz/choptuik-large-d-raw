## #903 xfkappa: the order-142 arm, closed (2026-11-18 01:00 UTC, Mac)

**Order 142 follows track C's 1/n series past #603's departure, to D 251.13.** Δ142 − series runs smoothly from −2.25e-12 at D 246.26 to −3.06e-12 at 250.84, inside track C's ±8.1e-11. Over the same states #603's order-130 chain departs from that series by up to 2.7e-8. The chain stopped at D 251.128 on the coordinator's order, before any base reached the counted range (D ≥ 257.5), so its fold was not read. The fold's order dependence goes to #603 (order 130), macm3b's order-135 chain and win2b's order-tied chain with #949's σ_Δ tracker. The chain can resume from `anm_pin3_D251.1277.npz` if those readings disagree.

Correction: #805's "series" is track C, the 1/n series fitted below D 245 (`I801-mac/real.json`), not #603's jets. My posts from 6951735466 on called it "#603's series". The sums below are therefore Δ142 − track C.

| criterion | result |
|---|---|
| fold shift D*(142) − D*(#841): truncation's if > 0.05, not if < 0.01 | **not read**: stopped at D 251.128, below the counted bases |
| each series against the chain's next own state (bound 1e-18; `--mutate=base` must fail, and it does) | pass, max 2.04e-30 over 32 series |
| Δ142 − track C at #603's 11 states, D 246.26–250.84 | −2.25e-12 to −3.06e-12, monotone, against track C's ±8.1e-11 (a spread over its 19 fits) |
| re-planning against order at D 225.13 (q130r2, one kernel) | re-planning moves Δ by −1.10e-20, so the rungs' lifts are the order's |

| D (#603) | Δ142 − Δ603 | #603 chain − series (#805) | Δ142 − series |
|---|---|---|---|
| 246.26 | +8.8052e-11 | −9.0304e-11 | −2.251e-12 |
| 247.04 | +1.6084e-10 | −1.6320e-10 | −2.356e-12 |
| 247.53 | +6.4828e-11 | −6.7256e-11 | −2.428e-12 |
| 248.02 | −3.7559e-10 | +3.7309e-10 | −2.506e-12 |
| 248.63 | −1.8211e-9 | +1.8185e-9 | −2.610e-12 |
| 249.01 | −3.2894e-9 | +3.2867e-9 | −2.684e-12 |
| 249.39 | −4.7950e-9 | +4.7922e-9 | −2.749e-12 |
| 249.87 | −4.8569e-9 | +4.8541e-9 | −2.836e-12 |
| 250.17 | −1.8068e-9 | +1.8039e-9 | −2.897e-12 |
| 250.47 | +6.1049e-9 | −6.1079e-9 | −2.964e-12 |
| 250.84 | +2.7388e-8 | −2.7391e-8 | −3.055e-12 |

The last column is limited by the digits `delta_cmp.txt` prints, about ±5e-13 at D 250.84.

Past D 247 the horizon rung refinement capped the steps near a 0.5. It diverged at a 0.625 and a 1, and both steps were refused. At D 251.008 the corrector's first damped step left the basin at a 0.477 and 0.238, with |F| going from 2e-35 to 1e-23, as #944 found at orders 150 and 160. a 0.119 then recovered in 15 iterations to 1.9e-61 (comments 6964845951 and 6965483044). The chain ran from 2026-11-16 14:24 to 2026-11-18 00:47 UTC, 34.4 h at 8 threads, with 32 bases from D 225.13.

### Discrepancies
- **Unexplained:** this chain's rung refinement floors at 1e-43 to 1e-54, and at 1e-28 to 1e-30 at a 1 near D 242–246. #603's, at order 130 with the same flags, reaches 2e-79 to 6e-80 in 3 corrections.
- **The kernel switch of 07:02 UTC Nov 17 (#942) did not reach this chain.** site2's `__init__.py` was lost after the chain loaded site2's kernel at 14:24 UTC Nov 16, and the chain ran on that kernel throughout.
- **Track C was mislabeled** as "#603's series" in my posts, corrected above.

### Recommended
- A cheap test that separates order from state: refine the rung at one state, for example D 248.13 at a 0.5, with ks 130 and with ks 142.
- Resume from D 251.128 only if the order readings disagree.

Raw: `I903-mac/chain_fixed/` (all states, series, predictions, log, `exits_chain.txt`) and `I903-mac/README.md`, at choptuik-large-d-raw 7e33e6ea.
