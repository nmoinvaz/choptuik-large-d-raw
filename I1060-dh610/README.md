# I1060-dh610: leg 10's step 17 of ks_chain3b (D 260.6706 -> 260.8483) on main 8179068d, bit for bit and with --series_split 2

Machine dh610 (Fedora, i7-12700, 20 threads, AVX2). Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1060 (queued by the coordinator after #1043 job 6).

Code: worktree `~/Source/choptuik-large-d-1060` at main 8179068d, venv-i1058 (hpkernel built from main 8179068d, #1058). Input and references: `I966-dh370/ks_chain3b/leg10_D256.1776_ks293/` of the raw repository (blobs of origin/main a691fd7f, checked against their tree ids): `anm_pin3_D260.6706.npz` (the start), `anm_pin3_D260.8483.npz` (leg 10's step 17 state), `jet_pin3_D260.6706.npz`, `pred_pin3_D260.8483.npz`, `anm_run.jsonl`.

Leg 10's command line (dh370, build 1aa4a4fb in `choptuik-large-d-966g`, python of `choptuik-large-d-961/.venv`): the leg's `anm_run.log` has no header, so it is taken from `run966m.sh chainm` (F3m, T = 10 threads) as `ks_chain.py` prints it for leg 10 in `I966-dh370/ks_chain3b_m_dry.log` (the dry run of 20 Nov 07:08:25 UTC, `exits_966.txt`: "starting i966p (run966m.sh chainm ... PAD -300)"):

    anm_run.py RAW OUT --state I966-dh370/ks_chain3b/leg09_D255.0004_ks293/anm_pin3_D256.1776.npz --kfreeze 3 --held_fit data/held_fit.json --N 31 --eps 1e-14 --h_max 2 --threads 10 --corrector od --tol_od 2e-34 --qd_it 40 --lam_stall 0.04 --od_junk 0 --jet_o 1 --reseed 2 --reseed_q 1 --held_o 1 --reseed_o 3 --save_pred 1 --od_accept natural --save_jet 1 --od_strong 4 --reseed_start pred --a_rule reseed --a_scale 0.00715 --jet_tangent_from 1 --series_split 1 --a_rise 1 --proj_start pred --reseed_o_stop 1 --od_floor_delta 1e-30 --proj_o 1 --reseed_qd_bar 1e-13 --steps 400 --ks 293 --keep_plan 0 --D_max 266.1776

Here: the same with `--state I966-dh370/ks_chain3b/leg10_D256.1776_ks293/anm_pin3_D260.6706.npz`, `--steps 1`, `--D_max 300`, OUT absolute (`step17_s<S>/`), and `--series_split S` for S = 1 (leg 10's own), 2 (the A/B) and 0 (the issue's "split 0"). The issue says dh370's chain runs `--series_split 0`; the command line above says 1 (a discrepancy in the issue, reported). `run1060.sh` runs them in the order 1, 2, 0 and stops after S = 1 if its state's a or D differ from leg 10's (reading: report both logs' step lines).

`cmp1060.py` is the comparator: `bits` (eight parts byte for byte, D_str, a; `--mutate` flips one byte of z3 and must report a difference, exit 1), `files` (the series and prediction files), `close` (Delta, M1 per part and M2 on exact sums at 600 bits) and `plant` (a planted shift of the exact sums, re-split into eight parts). Criterion for the A/B, fixed before the runs: Delta and M2 at or below 1e-100. M1, the issue's literal "each part's max", cannot be the pass test: a planted 1e-120 shift reads Delta 6.7e-121, M2 1.0e-120 and, per part, z6 5.2e-22 and z7 7.7e-06 (a part's low words carry the representation, not the value; `comparator_controls_1060.txt`), so M1 is printed and not read. Times: series = the record's `t_coef`, corrector = the attempts' `t_corr`, step = the run's wall (it includes the start's base polish).

## Amendment (01:52 UTC, 21 Nov, coordinator's hc)

win2 takes the split-2 A/B (step 2). dh610 runs only step 1 after #1043 job 6: leg 10's step 17 at `--series_split 0` on venv-i1058, which must equal the stored D 260.8483 state bit for bit (and, as before, the same a and D_str), with the comparator control. `run1060.sh` now loops over S = 0 only and `report1060.py` reads `step17_s0/`; the S = 1, 2 and 0 plan above is superseded. Leg 10's own line has `--series_split 1`; the coordinator's S = 0 is run as asked, and S = 1 is not run unless asked.

## Second amendment (01:58 UTC, 21 Nov, coordinator's hc): leg 10's line exactly as it ran, `--series_split 1`

The first amendment's S = 0 is replaced: `run1060.sh` now runs S = 1 only (leg 10's own line, `--series_split 1`, `--steps 1`, `--D_max 300`, absolute OUT `step17_s1/`). The comparison with the stored D 260.8483 state is judged, as win2's comparator note says, on Delta and the exactly summed parts (`cmp1060.py bits`: each component's eight parts summed as exact rationals, Delta and every S_i equal, D_str and a equal); the bytes that differ per part and the per-part M1 are printed as information. Controls (`comparator_controls_1060_exact.txt`): the state against itself exits 0; one byte of z3 flipped, and one byte of z7 (a change of 4.4e-134 in a sum), each exit 1; a planted 1e-120 shift exits 1 with Delta difference -1.1e-120 while its z7 M1 reads 7.7e-06. `run1060.sh` reruns all of them before the step.

## Result (21 Nov, 03:18 UTC): step 1, leg 10's step 17 at its own `--series_split 1`

Unit `i1060` 02:57:05 to 03:18:22 UTC, `step17_s1` exit 0, 1275 s (cap 10800 s), venv-i1058, worktree `~/Source/choptuik-large-d-1060` clean at 8179068d, `nice -n 10`, alert-only memory log `memlog_1060.log`.
The comparator controls ran first and were as required (`ctl_*.txt`, `comparator_controls_1060*.txt`). `a` and D_str equal leg 10's, so the stop rule did not apply. The verdict of `cmp1060.py bits`
(Delta and every exactly summed part) is DIFFERENT: Delta of this run's state 1.683264757534070378573492007334915999511, leg 10's 1.683264757534070378561608147670576687234, difference 1.188e-20, and the largest
difference of any component's exact sum, max |dS_i|, is the same 1.188e-20. `cmp_s1_vs_leg10.txt` and `report_1060.md` have the full lines; `series_pred_by_order_1060.txt` the per-order series and prediction differences
(exact sums, information; its controls run first).

## Step 2 (coordinator's follow-on after #1064, 21 Nov): leg 10's step 17 at split 1 with `--base_polish 0`

`run1060b.sh` (step 1's script with the names changed and `--base_polish 0` added at the end of the command; OUT `step17_s1_nobp/`, log `step17_s1_nobp.log`, `exits_1060b.txt`, `summary_1060b.txt`,
`report_1060b.md` from `report1060b.py`, comparator controls rerun into `ctl_b/`, `cmp_s1_nobp_vs_leg10.txt`) and `seriesdiff1060.py` (the per-order series and prediction differences against leg 10's, by
exact sums, with its own controls). Reading, the coordinator's, fixed before the run: equal bits (D_str, `a`, Delta and the exactly summed parts) mean the 1.188e-20 of step 1 came from the base polish, so main's build
reproduces dh370's chain; unequal bits with the base unmoved (series row 0 equal to the stored base) mean the build (1aa4a4fb python on the 40f4b4a5 kernel, against main 8179068d) or the platform, and
the report says which if the logs tell. `report1060b.py --selftest` runs the three branches of that reading, `--break` must exit 1.
