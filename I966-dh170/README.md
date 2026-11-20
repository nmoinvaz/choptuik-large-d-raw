# I966-dh170: near_null read of the first ks_chain3b state accepted by the floor rule (D 253.3365)

Machine dh170 (Fedora 45, i7-7700, 4 cores / 8 threads). Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/966. Task: coordinator's hc 2026-11-20 about 01:31 UTC,
"one near_null read beside the M 384 series (accept the slowdown)": the state `I966-dh370/ks_chain3b/leg07_D252.8861_ks293/anm_pin3_D253.3365.npz` (D 253.3365, final |F| 1.36e-32,
the corrector's own dDelta +2.12e-38), the first ks_chain3b state accepted by the floor rule. Post σ_Δ, σ_2 and the pinned correction's Δ component on #966, as the #949 relay did.

## Setup (the #949 setup, unchanged)

- Worktree `~/Source/choptuik-large-d-935` at main 787f1006, its 4.8.2 `.venv`; `hp/near_null.py` unchanged since c714694a. Command, as for the #949 ks_chain3b reads:
  `near_null.py ~/scratch949 STATE --k=6 --its=16 --its=32 --threads=2 --json=NAME.json` at nice 10 (the later `--its=32` wins, as in `queue949.txt`), 2 threads because the #1014 M 384 series runs
  beside it (6 threads, `I1014-dh170/stage3_1014.sh`). `read966.sh` runs the three jobs below at once.
- The state is copied by `I949-dh170/sync949.sh` byte for byte from the committed blob of origin/main of the raw repository (sync 3b53c7ce) into `~/scratch949/`.

## Runs and pass criteria, written before the first run

| run | command (after `near_null.py ~/scratch949 STATE --k=6 --its=16`) | pass |
|---|---|---|
| `c3b_ks293_D253.3365` | `--its=32 --json=c3b_ks293_D253.3365.json` on the D 253.3365 state | exit 0, the six vectors' convergence below 1e-6 for the two lowest as in the earlier reads; reports σ_Δ, σ_2, Δ share, σ_2/σ_Δ, the pinned step's Δ component with its sign |
| `ctl_planted` | `--planted=1` on `I903-win2/ks_chain/leg07_D222.0000_ks240/anm_pin3_D229.0509.npz` (the #949 control state) | exit 0: the planted fold is recovered |
| `ctl_planted_mut` | the same with `--mutate=scale_block` | exit 1 (the control can fail) |

The earlier #949 results of the same code: ctl_planted exit 0 and ctl_planted_mut exit 1 (427 s each at 4 threads). The read is judged only with the two controls from the same hp build.

## Result (2026-11-20 02:02 UTC; `exits_966.txt`, `c3b_ks293_D253.3365.json`/`.log`)

Controls (same hp build 787f1006, same near_null.py): `ctl_planted` exit 0 (wall 1626 s), `ctl_planted_mut` exit 1 (1559 s, `check: FAIL`, as it must). The read: exit 0, wall 1771 s at 2 threads beside the #1014 series, max rss 175 MB. `msg966.py --selftest` passes; `--mutate` and `--mutate=sign` fail as they must.

| | D 253.3365 (leg 7, floor rule) | D 252.8861 (leg 6, #949's last read) |
|---|---|---|
| σ_Δ (vector 1) | 1.145843e-18, Δ share 0.925, convergence 2e-07 | 1.404926e-18, share 0.853, 5e-07 |
| σ_2 (vector 2) | 1.292203e-18, Δ share 0.067, convergence 3e-07 | 1.585324e-18, share 0.139, 7e-07 |
| σ_2/σ_Δ | 1.128 | 1.128 |
| pinned step dz + J⁻¹c, its Δ component | **+2.120e-38** (max 2.120e-38, norm 1.569e-37, Δ share 1.000) | +2.570e-61 |
| the corrector's own dΔ (coordinator's hc) | +2.12e-38 | |
| \|F\|/σ_Δ (final \|F\| 1.36e-32, from the coordinator) | 1.2e-14 | |

- The pinned correction's Δ component equals the corrector's own dΔ to the printed digits (+2.120e-38 against +2.12e-38), by code that shares nothing with it (near_null.py's octo-double LU against the chain's corrector). It is 20 orders under the 1e-18 bar and under σ_Δ's own scale by the same margin; |F|/σ_Δ = 1.2e-14 fails the strict reading as at earlier states.
- σ_Δ interval slope from D 252.8861 to 253.3365: 0.4526 against the frozen D-trend baseline 0.3491 (at the interval's midpoint, `dtrend_frozen949.json`): **excess +0.1035**, the first above 0.10 (the four before it: +0.0801, +0.0803, +0.0827, +0.0896, `I949-dh170/track949.csv`). Control: the same formula on the D 252.8861 row gives 0.4398 and +0.0896, equal to the csv. #949's trigger needs three states in a row above 0.10 and #949 is closed, so this is a reading, not a verdict. The slope compares states accepted under different |F| (4.5e-35 to 1.4e-32); their σ_Δ do not depend on it at this level (pinned correction 2.1e-38 against σ_Δ 1e-18).
