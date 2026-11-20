# I1057-dh170: ks_chain3b states past D 259.7352 read with near_null and the #949 fits (code unchanged)

Machine: dh170 (i7-7700, 8 logical CPUs, 31 GB; the reads take 2 threads beside #1014's B2 run). Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1057 (coordinator's hc and body, 2026-11-20 16:38 UTC).
Source of the states: dh370's ks_chain3b, leg 10 (ks 293), `I966-dh370/ks_chain3b/leg10_D256.1776_ks293/anm_pin3_D<D>.npz`, synced by `sync949.sh` into `~/scratch949` from origin/main of the raw repository (byte for byte).

## Question and work (the issue)
Does the bump in σ_Δ's excess over its frozen trend (peak +0.2948 at D 257.6920, +0.0269 at D 259.7352, #949 closing comment 7044974624) close, and does a fold approach as dh370's D-series tail grows (about 30 times per step at D 260.01 to 260.47, #966)? Keep reading ks_chain3b's new states past D 259.7352 with `step949.sh` and its fits unchanged (σ_Δ, the Δ share, the slopes, the excess, the fold fit on the last five states, the two-mode fit). The first read is D 260.0073, which I dropped at the #949 stop.

## What is copied from `I949-dh170/` (raw 5c37fc8b), unchanged
The fits and trackers: `fold949.py`, `track949.py`, `pairfold949.py`, `row949.py`, `twomode949.py`, `stopcheck949.py` (kept, no longer called), `queue_new949.py`, `sync949.sh`; the inputs: `baseline949.json` (frozen 2026-11-18 00:01:39 UTC), `dtrend_frozen949.json`, `ctl_planted.json`, `from941/`, and every `*_D*.json` state record (the 103 near_null records of #949). Copied with `cp -p`; `hashes1057.txt` has the sha256 of each and `cmp` against the original is part of the first run's log (`setup1057.log`).
Changed paths only: `step1057.sh` (step949.sh with this folder's path, and `stopcheck1057.py` in place of `stopcheck949.py`, because the old stop rule, excess below 0.10 twice, is already met), `run1057.sh` (run949.sh with this folder and `exits_1057.txt`, `STOP1057`), `autoqueue1057.sh` (autoqueue949.sh with this folder). New code: `stopcheck1057.py` and `selftests1057.sh`.

## Pass criteria, written before any state is read
1. Selftests first: `selftests1057.sh` runs the six scripts' selftests (each must exit 0) and each `--mutate` (must exit 1), and the new `stopcheck1057.py --selftest` with its mutation. All must be as required before the lane starts.
2. Every state: `check: pass` in its log, ‖J v₁‖/σ₁ = 1.000000, σ_Δ converged to better than 1e-3 relative (the log's "converged to").
3. The fits' code and pass criteria are not touched: the fold fit is valid only if all four conditions are true (TTTT); the two-mode fit's reading (no avoided crossing) needs its Δ-share check to agree with the measured shares.
4. Post format as #949: one row per state with the fold fit and the two-mode fit on the last five states, ending with the coordinator's caveat from #948.

## Stop rule (the issue, fixed before the first read)
(a) A TTTT fold window: report at once on #966 and #1057. (b) The excess within ±0.05 for 5 states in a row (counted from D 260.0073; the run counting D 259.7352 is also printed). (c) dh370's leg boundary at D 266.18 or a leg 11 restart at ks 315, whichever comes first. (d) 2026-11-21 12:00 UTC. `stopcheck1057.py` prints which of these hold after each state.

## Log
- 2026-11-20 16:38 UTC: folder made, README first.
- 16:39 to 16:41 UTC: `selftests1057.sh` (also copied `relay_dh370_949.py` for its selftest): 7 selftests exit 0 and 8 mutations exit 1, "selftests1057: all ok" (`selftests1057.log`); `stopcheck1057.py --selftest` has 13 planted cases (the band edge 0.05 counts, 0.0501 does not, a planted -0.08 breaks the run, D 259.7352 is not a new state, TTTT valid versus TTTT not valid, D 266.18 and ks 315, the deadline) and its mutation (the band with no lower bound) fails. `selftest_twomode949.log` regenerated (exit 0) because `twomode949.py` requires it.
- 16:49:04 UTC: the lane started with the `-935` worktree at main 17ae55bf, which I had fast-forwarded at the #949 close (standing instruction to update after a run ends). `hp/near_null.py` differs between 787f1006 (the reader of every #949 row) and 17ae55bf (it keeps newton_o's Jacobian and residual instead of forming them again; the same bits by its own note, not checked here). That broke "code unchanged", so I stopped the lane and its near_null by exact pid after 20 s (`exits_1057.txt` NOTE line, partial log kept as `c3b_ks293_D260.0073.log.aborted_hp17ae55bf`), put `-935` back on 787f1006 (`git checkout --detach 787f1006`, tree clean) and restarted at 16:49:41 UTC with `hp 787f1006` in the start line. `-935` stays on 787f1006 until #1057 ends.
- 16:49:41 UTC: lane 1 at 2 threads (`run1057.sh lane 1`, `THREADS=2`, nice 10, systemd-inhibit) and `autoqueue1057.sh` (sync every 5 minutes) running; first read D 260.0073.

## Closing summary (2026-11-20 18:11 UTC, stop rule (c): dh370's leg 11 restart at ks 315)

**Answer.** The bump did not close: the excess fell to +0.0146 (D 260.0073) and then turned up again, +0.0294 at D 260.2515 and +0.0804 at D 260.4708, with σ_Δ's slope back up from 0.347 to 0.412 and the Δ share down from 0.991 to 0.960 while σ_2/σ_Δ keeps falling (1.183). No fold window passed (the last reads TTFF, D* 262.85), so no fold is claimed. I stopped on rule (c): dh370 pushed the restart at ks 315 (leg 11, raw fc4b254e, 2026-11-20 17:36:36 UTC) before my reads of D 260.2515 and 260.4708, and I learned of it from the coordinator at 18:04 UTC; leg 10's last two states, D 260.6706 and 260.8483, were pushed and queued but not read.

States read: 3 (D 260.0073, 260.2515, 260.4708; `c3b_ks293_D<D>.log/.json`, 2 threads, `hp 787f1006`, 830 to 875 s each). Not kept: the first start of D 260.0073 at `hp 17ae55bf` (`.aborted_hp17ae55bf`) and the read of D 260.6706, stopped 8 s in (`.aborted_at_stop`).

| D | σ_Δ | Δ share | σ_Δ slope | baseline | excess | σ_2 (σ_2/σ_Δ) | σ_2 slope | σ_pair, slope | pair D*(4)/(5), shifts | rule | pinned Δ |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 260.0073 | 3.7920e-20 | 0.991 | 0.3471 | 0.3325 | +0.0146 | 5.4985e-20 (1.450) | 0.728 | 1.582e-14, +0.4524 | 277.843 (-1.263) / 277.216 (-1.112) | not met | -4.434e-49 |
| 260.2515 | 3.4717e-20 | 0.987 | 0.3613 | 0.3319 | +0.0294 | 4.5196e-20 (1.302) | 0.803 | 1.416e-14, +0.4527 | 279.299 (-1.457) / 278.514 (-1.298) | not met | +7.234e-42 |
| 260.4708 | 3.1720e-20 | 0.960 | 0.4117 | 0.3313 | +0.0804 | 3.7538e-20 (1.183) | 0.847 | 1.282e-14, +0.4529 | 281.172 (-1.872) / 280.091 (-1.576) | not met | +1.650e-47 |

| # | check | verdict | number |
|---|---|---|---|
| 1 | selftests first | pass | `selftests1057.log`: 7 selftests exit 0, 8 mutations exit 1; `stopcheck1057.py` 13 planted cases and its mutation (the band without its lower bound) fails |
| 2 | code unchanged | pass | 119 `cmp` matches against `I949-dh170/` (`setup1057.log`), `hashes1057.txt`; paths and labels only in `step1057.sh`, `run1057.sh`, `autoqueue1057.sh` |
| 3 | every state's σ_Δ converged and its check | pass | 3 of 3 `check: pass`, ‖J v₁‖/σ₁ = 1.000000, σ_Δ converged to 3e-15, 0 and 1e-10 (D 260.0073, 260.2515, 260.4708) |
| 4 | rule (a), a TTTT fold window | not met | the windows ending D 260.0073 and 260.2515 read FFF− (no finite D*), the one ending D 260.4708 reads TTFF (D* 262.85, s 0.190, conditions 3 and 4 false) |
| 5 | rule (b), excess within ±0.05 at 5 new states in a row | not met | 2 of 5 (+0.0146, +0.0294), then +0.0804 |
| 6 | rule (c), dh370's leg boundary D 266.18 or a leg 11 restart at ks 315 | met | the restart, push fc4b254e, 17:36:36 UTC (leg 10 steps 14 to 17, D 260.2515 to 260.8483) |
| 7 | rule (d), 2026-11-21 12:00 UTC | not reached | |
| 8 | two-mode fit (3 windows) | no avoided crossing | γ 0 in all three, rms of ln σ 1.32e-2, 1.26e-2, 1.08e-2; the fit has no mixing (Δ share 1.000) against measured 0.985 to 0.991 and, in the last window, 0.960 at its last state |

Discrepancies and corrections, reported and not fixed:
- Rule (c) had fired at 17:36 UTC, 4 minutes before my read of D 260.2515 started and 18 minutes before it ended. `stopcheck1057.py` sees only states I have read (D ≥ 266.18 or ks ≥ 315 in `track949.csv`), not dh370's pushes, and `leg11_D260.8483_ks315/` held only `anm_run.log` at that time. So two reads (D 260.2515 and 260.4708, 29 minutes of 2 threads) ran after the rule had fired. Not a wrong result: both are posted as rows.
- The `-935` fast-forward at the #949 close (above, README log): the first start used `hp 17ae55bf`, restarted at `hp 787f1006` after 20 s.
- Two counts in posted rows were corrected by comment id (σ_2/σ_Δ "third state" to "fourth", comment 7045634384).
- `claimed949.txt` lists D 260.6706 and 260.8483 as claimed or queued (`queue949.txt`) although they were not read; a restart reads D 260.6706 first.
- Reading, not a result: the first bump (D 253 to 259.7) had σ_2/σ_Δ rising from 1.1 to 1.85 with the Δ share falling to 0.9395; this second rise has σ_2/σ_Δ falling from 1.85 to 1.18 with the Δ share falling from 0.991 to 0.960. The two lowest modes are approaching each other, and the constant-slope two-mode law with γ = 0 does not describe it.

Recommended tasks (coordinator opens the issues):
1. **Read leg 10's last two states and leg 11's first states.** What: run `step1057.sh` on D 260.6706 and 260.8483 (both pushed, in `queue949.txt`; about 14 minutes each at 2 threads) and on leg 11's states at ks 315 as dh370 pushes them, with the same post format. Why: the excess is +0.0804 and rising, σ_2/σ_Δ is 1.183 and falling, and the fold window just reached TTFF with D* 262.85, 2.4 past the last state; dh370's leg 11 starts from D 260.8483. Acceptance: a TTTT window is reported at once on #966 and the issue; the excess and the Δ share per state; the planted controls (`selftests1057.sh`) pass first. Depends on: dh370's pushes; `-935` stays on 787f1006 for the reader.
2. **Add leg 11 (ks 315) to the rule (c) check.** What: make `stopcheck1057.py` watch the raw repository for `leg11_*_ks315` and report the restart as it is pushed, instead of only reading states already read. Why: it missed rule (c) this time. Acceptance: a planted push of a `ks315` folder fires it and a ks 293 folder does not.
