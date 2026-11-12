# I458-macm3: gamma's root resolution at D 40 and D 58 over five find_lam brackets (kf 13, M 32 and M 48)

Machine: macm3 (Apple M3, 24 GB RAM), venv-macm3-314 (Python 3.14.3, python-flint 0.9.0, FLINT 3.6.0, hpkernel cp314 neon built 2026-11-09 02:44, as for #273). Code: a git worktree ~/Source/choptuik-large-d-b458 at main c845cc99 (hp/gamma_dd.py with --bracket and --xtol). Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/458 (recommended by macm3 in #273's summary; assigned by the coordinator, comment of 2026-11-12 10:34 UTC with the commands).

Runs (common.sh run(), chain1.sh, chain2.sh and chain3.sh, one thread per run, three runs at a time, nice 10, caffeinate -is): python3 -u hp/gamma_dd.py <raw>/gamma_STATE_NAME.jsonl hp/data/states/STATE.npz --threads=1 --polish=4 --M48 --kf48=13 --bracket=A,B --xtol=1e-16 > gamma_STATE_NAME.log, for the states up7_D40.0201 (sha256 d5cc8be5de0ab765...; root 2.0627796726) and up12_D58.0060 (sha256 dc5f2053880e5494...; root 2.0455297615) with the brackets b1 to b5 of the issue, the control b1r (b1 again: must equal b1 bit for bit in lambda(32) and lambda(48)) and the control none (a bracket without a sign change: must exit 1 with lam null). 14 runs.

Written before the run (the issue's). Per D: table lambda(32) and lambda(48) per bracket, their spread (max - min) over b1 to b5 and n_det, with #273's kf 13 values beside them (lambda(48) 2.062779672619633 at D 40, 2.0455297614777623 at D 58). The spread of lambda(48) is the root's resolution at that D; #266 gave about 1e-14 at D 50 and 5e-13 at D 58; report whether the D 58 spread is within a factor 3 of 5e-13; a spread at or below 2e-15 means brentq's tolerance, not det M's noise, set it. If b1r differs from b1 or none does not exit 1: stop and report. Each run's floor check and tails as in #273; a run that exits 1 for another reason is reported, not rerun.

## Results


(2026-11-12 11:23 UTC, macm3) All 14 runs finished (exits.txt): the twelve bracketed runs exit 0, the two none controls exit 1 with lam null ("no sign change of det M in the bracket"). Started 10:36:38 UTC, last exit 11:22:26 UTC (46 min). Run times: D 40 M 32 96 to 111 s, M 48 310 to 341 s; D 58 M 32 109 to 130 s, M 48 578 to 847 s. Every run: M 48 floor check ok, the Newton solve stopped at the floor (D 40: 2 steps; D 58: 10), tails of both series 3.1e-48 (D 40) and 6.3e-42 (D 58) at most.

### D 40 (up7_D40.0201)

| bracket | λ(32) | λ(48) | n_det (M 32) | M 48 floor check | M 48 tails max | M 48 Newton steps | exit |
|---|---|---|---|---|---|---|---|
| b1 | 2.0627796726196306 | 2.0627796726196306 | 6 | ok | 3.1e-48 | 2 | 0 |
| b2 | 2.0627796726196306 | 2.062779672619631 | 7 | ok | 3.1e-48 | 2 | 0 |
| b3 | 2.0627796726196306 | 2.062779672619631 | 7 | ok | 3.1e-48 | 2 | 0 |
| b4 | 2.0627796726196306 | 2.0627796726196306 | 6 | ok | 3.1e-48 | 2 | 0 |
| b5 | 2.0627796726196306 | 2.0627796726196306 | 6 | ok | 3.1e-48 | 2 | 0 |
| b1r | 2.0627796726196306 | 2.0627796726196306 | 6 | ok | 3.1e-48 | 2 | 0 |
| none | None | None | 2 | - | - | - | 1 |

Spread over b1 to b5: λ(32) 0.000e+00 (min 2.0627796726196306, max 2.0627796726196306); λ(48) 4.441e-16 (min 2.0627796726196306, max 2.062779672619631). #273 kf 13: λ(32) 2.0627796726196337, λ(48) 2.062779672619633; b1 to b5 against #273: λ(48) -2.22e-15 to -1.78e-15.
Control b1r vs b1: λ(32) bit for bit equal, λ(48) bit for bit equal. Control none: exit 1, lam None.

### D 58 (up12_D58.0060)

| bracket | λ(32) | λ(48) | n_det (M 32) | M 48 floor check | M 48 tails max | M 48 Newton steps | exit |
|---|---|---|---|---|---|---|---|
| b1 | 2.0455297614777743 | 2.0455297614776238 | 6 | ok | 6.3e-42 | 10 | 0 |
| b2 | 2.045529761477775 | 2.045529761477577 | 7 | ok | 6.3e-42 | 10 | 0 |
| b3 | 2.045529761477775 | 2.0455297614778325 | 7 | ok | 6.3e-42 | 10 | 0 |
| b4 | 2.0455297614777765 | 2.0455297614777126 | 8 | ok | 6.3e-42 | 10 | 0 |
| b5 | 2.0455297614777748 | 2.045529761477681 | 7 | ok | 6.3e-42 | 10 | 0 |
| b1r | 2.0455297614777743 | 2.0455297614776238 | 6 | ok | 6.3e-42 | 10 | 0 |
| none | None | None | 2 | - | - | - | 1 |

Spread over b1 to b5: λ(32) 2.220e-15 (min 2.0455297614777743, max 2.0455297614777765); λ(48) 2.554e-13 (min 2.045529761477577, max 2.0455297614778325). #273 kf 13: λ(32) 2.045529761477777, λ(48) 2.0455297614777623; b1 to b5 against #273: λ(48) -1.85e-13 to +7.02e-14.
Control b1r vs b1: λ(32) bit for bit equal, λ(48) bit for bit equal. Control none: exit 1, lam None.

Reading (the issue's, fixed before the run). The spread of lambda(48) over b1 to b5 is the root's resolution at that D: D 40 4.4e-16 (at or below 2e-15, so brentq's tolerance, not det M's noise, set it); D 58 2.55e-13, within a factor 3 of #266's 5e-13 (ratio 0.51, the window 1.7e-13 to 1.5e-12). The D 55.04 at M 64 extension of the coordinator's comment of 2026-11-10 21:03 UTC was not run: its commands (comment of 2026-11-12) are for D 40 and D 58 at M 32 and M 48, the bracket option works at those M only.
