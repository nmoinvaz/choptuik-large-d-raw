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
