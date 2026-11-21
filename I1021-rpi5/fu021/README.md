# fu021: #1021's record leftovers (11 unresolved cells at xi1 0.17) valued again from other starts and seeds (xfchecks' driver run_fu021.sh), then recounted

Part of `I1021-rpi5`. Machine: rpi5, Raspberry Pi 5, aarch64, 4 cores, 8 GB, Linux 6.17.0-1021-raspi, agent claude-me2.
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1021. Started 2026-11-21 21:09:37 UTC on the coordinator's word
(hc of 21 Nov: "Your next task, now, #1021 fu021: the record's leftovers at xi1 0.17, with xfchecks' driver at raw f3018a8e").

## Plan and criteria (xfchecks', fixed before the run)
`I1021-mac/rpi5_fu021/` (raw f3018a8e) holds the driver `run_fu021.sh`, its README (the leftovers, the passes, criteria
1 to 6, the Mac's pilot), `fu_value.py` (dh610's, sha256 b36fb3e9..., unchanged), `select_points.py`, `prefix_keys.py`,
`SHA256SUMS` and `in/` (`SHA256SUMS_record`, `cells_unresolved11.jsonl`, `select_dry.txt`). The record is
`I1021-mac/final/record/` (raw 7dac2e32; 3229-line 0.17 cache, 1151-line 0.2 seed file). In short:
- 20 points: the record's 16 named blockers (7 without value, 9 guard-blocked at 4.65 to 9.86 sigma) and 4 guard-blocked
  points inside cell 25's unresolved leaf. Each is valued again in 6 variants (default, rhs1e7, s0.2, seed2, seed3,
  s0.2seed2; 3600 s each), 120 runs per pass, 4 processes at nice 10, 12 h cap. A row is accepted only by fu_value.py's
  tests (valued, max|Y| <= 100, |R| >= 10 sigma, |dF3| to the nearest valued neighbour <= 0.1), and the first accepted
  row of a point is appended to the cache with `"fu": variant`.
- Each pass: value step, retests (`--mutate=f3` must fire in a pass that accepted a row, `--mutate=lowguard` where the
  guard alone blocked a row, else vacuous), end if nothing accepted, then the recount of the 11 cells (`--M=3 --r1=0.17
  --r1b=0.2 --m3fix --m3maxrhs=2.4e6 --m3wall=3600 --m3noisecap=1e7 --procs=4 --retry`, 16 h cap), end at 0 unresolved
  leaves. At most 2 passes; pass 2 values only the points without value that pass 1 had not run.
- At the end `prefix_keys.py` record -> fu021 (must exit 0) and `argcount_samebits.py` (reported only: it exits 1
  whenever a guard-blocked point is lifted, as in recount4).
- Criteria: (1) argcount selftest and 5 mutations `0 1 1 1 1 1`; fu_value selftest, `--break`, `prefix_keys.py
  --mutate=edit` `0 1 1`; (2) acceptance only by those tests; (3) the retests as above; (4) prefix_keys exit 0 (the record's
  3229 lines are the first lines byte for byte, every later record of an old key is an accepted fu row or a `--retry`
  record); (5) counts on hold until xfchecks' sheet check of fu021's new points; (6) accepted at 0 unresolved leaves, or
  each unresolved leaf named with its blocking points and each variant's cause (`../../I1021-mac/final/leftovers/leftovers.py`
  on fu021's cache and last leaves).

## Command and setup
From the live raw clone's root (`$PWD` as RAW), in the background:
`bash I1021-mac/rpi5_fu021/run_fu021.sh ~/Source/cl-1013fix ~/Source/venv-choptuik/bin/python "$PWD" > I1021-rpi5/fu021_driver.out 2>&1`
(`I1021-rpi5/fu021_driver.start` has the start and `driver exit` lines).
- Code: worktree `~/Source/cl-1013fix` at `wip/argcount-m3-bounds` 6da7da7b, no local changes (the driver checks).
  Python 3.13.7, numpy 2.5.4, scipy 1.18.1, mpmath 1.3.0.
- Deviations: (a) the live clone is not sparse and cannot pull, so I copied `I1021-mac/final/record/` and
  `I1021-mac/rpi5_fu021/` from the push worktree (`~/Source/choptuik-large-d-raw-964`, f3018a8e is an ancestor of its HEAD
  d99383d1) with `cp -a`, `diff -r` identical, the driver's sha256 checks pass; (b) the coordinator's command wrote the
  driver's stdout to `I1021-rpi5_fu021_driver.out` in the raw root, which I put inside `I1021-rpi5/` so no stray file
  sits at the repository root.
- Pushes during the run come only from the push worktree (rsync of `I1021-rpi5/`), never from the live clone.
- The `running` label on #1021 was already set when I started; I leave it as it is.

## Runs
(filled in as the run goes)
