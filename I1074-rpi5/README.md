# I1074-rpi5: the +2.5e-6 step between Ecker et al.'s 512-mode Delta and ours at D 3.2: theirs or ours?

Machine: rpi5 (aarch64, one process, nice 10, analysis only). Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1074
Started: 2026-11-22 21:18 UTC. Code: main bd34b720 (worktree `choptuik-large-d-1074`). Their repository, data only (none of its code is run), the
#1073 clone at commit `f002d0af1680abb967e694a121cb2a8de2984b5d`. Follows I1073-rpi5 (raw d481a3a3).

## What is computed (written before the tables are printed)

1. **Their side**, every D in 3.1 to 3.3 in `complete_data/FortranData/dim<D>/<res>/`: Delta from `Delta.out` at 128/256/512, the run's
   `shoot_inner.par` (ny, xleft, xmid, nleft, nright, eps, tstep, crit, debug), the 512-mode differences between neighbouring D, and the
   divided second differences of the 512 series.
2. **Our side**, `hp/data/delta_all.csv` and `delta_dd.csv` (value, M, run, stored M difference, F) in 3.1 to 3.3, and every other
   record of Delta at those D in `hp/data/**/*.jsonl` (the M sequence at each D, its F).
3. **Location.** Three tests, any one of which can point to a side:
   - (a) settings: the D at which their 512 runs' settings change, against the D at which `d(D) = theirs512 - ours` jumps.
   - (b) trend of `d`: fit ln d against D (quadratic) through D 3.25 to 3.45 (5 points, theirs and ours both present), extrapolate to 3.2.
     d(3.2) is "on trend" if the extrapolation is within a factor 1.5 of it. An isolated error in one of our values would not be on the
     trend of their errors at other D. Control: d(3.2) multiplied by 3 must fail the test.
   - (c) second differences inside each series (leave-one-out cubic residual of the 4 nearest other points of the same series), with a
     planted step of 2.5e-6 at each point to give the detection floor. If a series' residuals exceed 2.5e-6 at the sparse D around 3.2,
     that test cannot see the step and says so.
   - (d) our M sequence at D 3.2 (128 / 160 / 192): its steps against the neighbours' and its F.

**Verdict rule.** "Theirs" if (a) their settings change at the D where d jumps and (b) d(3.2) is on the trend of d(D >= 3.25) and (d) our
3.2 is converged in M like its neighbours. "Ours" if d(3.2) is off the trend of d(D >= 3.25) and their settings at 3.2 equal those at 3.25.
Otherwise "undecided", with what would decide it.

## Acceptance (written before the tables)

1. D 3.7: their 512-mode Delta (read from `dim3.7000/512/Delta.out`) within 1e-7 of ours (M 80, `delta_dd_lowD.csv`).
2. The table reproduces #1073's +2.5e-6 at D 3.2: theirs - ours in [2.45e-6, 2.55e-6).
Either fails: stop and report. `analyze1074.py --mutate=shift` moves ours by 1e-6 and must fail check 1 (exit 1).

## Seen before this README was written (disclosed)

While checking the layout I had listed their runs' `shoot_inner.par` for 3.1 to 3.35: the 512 runs at D <= 3.18 have xleft 1e-4, xmid
0.03 to 0.05, nleft 7500, nright 6500, eps 1e-6, and those at D >= 3.2 have xleft 1e-3, xmid 0.1, nleft 4000, nright 4000, eps 1e-8. The
128 and 256 runs have the same settings at all D. I also saw our M sequence at 3.2 (3.0947374390 at M 128, 3.0947374327 at M 160 and 192).
Tests (b) and (c) were defined after that but before their numbers were computed.

## Result (run 2026-11-22 21:16 to 21:20 UTC; exits.txt, sha256.txt)

**The step is theirs: their 512-mode runs change grid settings between D 3.18 and 3.2, and our D 3.2 is converged and on its own curve.**
Acceptance passes: D 3.7 theirs 3.465200504469, ours (M 80) 3.465200483544, +2.09e-8 (bar 1e-7); D 3.2 theirs - ours +2.470e-6. Controls:
`--mutate=shift` fails acceptance 1 (exit 1), `--mutate=trend` (d(3.2) x 3) makes the verdict "not theirs" (exit 1).

**(a) Their settings** (`shoot_inner.par` of the 512-mode runs; D 3.1 to 3.35: 44 runs at 3.1 to 3.18, then 3.2, 3.25, 3.3, 3.35):

| | D 3.1 to 3.18 | D 3.2 to 3.35 |
|---|---|---|
| xleft | 1e-4 | 1e-3 |
| xmid | 0.03, 0.04, 0.05 | 0.1 |
| nleft, nright | 7500, 6500 | 4000, 4000 |
| eps | 1e-6 (1e-8 at 3.125) | 1e-8 |
| tstep, errmax, debug | vary from run to run (1 or 2; 1e-14 or 1e-13; T or F) | 2, 1e-14, F |

xleft, nleft and nright change only between D 3.18 and 3.2. The other fields vary below 3.18 (tstep, errmax, eps, debug, xmid); the four runs there that
have a value of ours (3.1, 3.125, 3.15, 3.175) differ in them and agree with ours to 5e-10 or better. Their 128 and 256 runs (D 3.145 to 3.3) have one setting at every D (xleft 1e-3, xmid
0.1, 3000/3000 points, eps 1e-8, tstep 2).

| D | 3.0475 | 3.05 | 3.075 | 3.1 | 3.125 | 3.15 | 3.175 | **3.2** | 3.25 | 3.3 | 3.35 | 3.4 | 3.45 | 3.5 | 3.55 | 3.6 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| theirs - ours | +6.9e-10 | +5.0e-10 | +2.9e-9 | +5.2e-10 | +2.2e-10 | -5.2e-11 | -2.1e-10 | **+2.47e-6** | +3.58e-7 | +6.59e-8 | +1.43e-8 | +3.5e-9 | +1.4e-9 | +1.9e-9 | +3.9e-9 | +7.5e-9 |

The largest jump in |d| is x1.15e4 between 3.175 and 3.2, the same interval as the settings change. The next is x5.7 (3.05 to 3.075).

**(b) Trend of d.** From D 3.2 up, d falls smoothly (x0.15, 0.18, 0.22, 0.25 per 0.05 step to 3.4). A quadratic in ln d through 3.25 to
3.45 (fit residual 0.09 in ln d) extrapolates to 2.71e-6 at 3.2; the value is 2.47e-6, ratio 0.91. An isolated error in our 3.2 would not
sit on that curve. The same trend continued to 3.175 would give 8.0e-6, and d(3.175) is -2.1e-10.

**(d) Our D 3.2.** Converged in M like its neighbours (M 128 -> 160 -> 192 at 3.2: -6.31e-9, -2.42e-11; at 3.175: -6.38e-9, -3.3e-10; at
3.25: -9.8e-10, -1.4e-11), F 7.0e-29 (neighbours 3e-29 to 8e-29). Our Delta at 3.2 is the M 192 value of `lowD-M192`, the same run family
as 3.175 and 3.25.

**(c) Second differences cannot decide.** Leave-one-out cubic residuals of the smooth curve at the sparse D around 3.2 are 1e-4 to
1e-3 in both series (theirs 512: 3.2 -9.5e-5, 3.25 -4.3e-4; ours: 3.175 -1.8e-4, 3.2 -2.7e-4, 3.25 -4.7e-4), against a 2.5e-6 step. Their
dense block (D 3.14 to 3.175, step 0.005) has a floor of 2e-7 to 4e-7 and no break, but it ends at 3.18. The sensitive instrument is
d(D), whose smooth part cancels.

**What is not shown.** Which of the changed fields (xleft 1e-4 -> 1e-3, the radial points, eps) makes the +2.5e-6 is not known: their code was
not run (read-only). After 3.45, d rises again (1.4e-9 at 3.45 to 7.5e-9 at 3.6): a second effect, in either set, not studied here.

**For notes/LOW_D.md 5:** call the 3.2 step theirs (their 512-mode runs at D >= 3.2 use xleft 1e-3 and 4000/4000 radial points, those
at D <= 3.18 use xleft 1e-4 and 7500/6500). No recomputation of our D 3.2 is needed. The 128/256 runs and the 512 runs at D >= 3.2 share
the coarser radial set, so their Delta at D >= 3.2 carries a radial error of about 2.5e-6 at 3.2 falling to 1e-9 at 3.45.
Optional, needs the coordinator's word (AGENTS.md: external code is not run): their Fortran code at D 3.2 with the D 3.18 settings, in
isolation, would say which field matters.

## Files

README.md, analyze1074.py (`python3 -I analyze1074.py ECC CODE [--mutate=shift|trend]`, stdlib only), analyze1074.txt (all tables),
analyze1074_mutate_shift.txt, analyze1074_mutate_trend.txt, exits.txt, sha256.txt.
