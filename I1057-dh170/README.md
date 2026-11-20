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
