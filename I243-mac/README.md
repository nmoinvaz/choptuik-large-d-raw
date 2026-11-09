# I243-mac: the earlier mode counts re-checked for hidden turns, with the alias rule of #242 and a second-scale check

Machine: mac (Apple M5, 10 cores, macOS 27, shared with #208's two CAPD processes), venv-314 (Python 3.14, hpkernel and
multidouble NEON, python-flint 0.9.0, modecount_cx cp314 build of 2026-11-08 16:26 from the main checkout). Issue:
https://github.com/nmoinvaz/choptuik-large-d/issues/243. Code: branch wip/i242 of the main repository (the #242 rule,
hp/modecount_wind.py 01f6c59). Inputs read from the raw-data repository by git archive into a scratch directory (nothing
pulled here): 6d8007f for every folder, 9ef605c for I241-macm3. All runs single-threaded under nice 10 and caffeinate -i,
at most two count processes at a time.

## Method

1. Scans, no determinants (scan.log, from scan_all.py): I230-mac/alias_scan.py, unchanged (copied as
   alias_scan_I230.py), and scan_rule.py (the #242 rule's first-pass flags, corners included) on the definitive record
   of every count (records/, listed with their sources in records/manifest.txt). Control first: #212's kf 23 record.
2. Re-evaluation (reeval.py, run_batch.py): each count's cache is copied into NAME/data/ and hp/modecount_wind.py
   reruns with the #242 rule and the record's own geometry (aLL, aL, a1, a2, aR, Im2, h0 and lam passed explicitly).
   It re-samples the flagged intervals (and whatever the rule's cascade reaches) to steps <= pi/4 with the repeated
   verification of steps > pi/8, and adds only the determinants it needs. NAME/cache_lines.txt has the line counts
   before and after and a check that the old lines are unchanged. The saved resampled states of the original runs
   (hp_data_after/ of each folder) were copied into the worktree's hp/data so that setup loaded them, not re-converged.
3. Second-scale check (offset_check.py, for the counts of 0 behind the README's statements): every interval gets one
   new sample at its golden-section point, and the two pieces must each be at most pi/4 and add up to the interval's
   step. It shares the determinant code, g's factors and the samples with the count, not the alias rule.
   planted_offset.py tests it on the synthetic det M of hp/modecount_planted.py, counted with the old rule.

## Results

(filled in at the end)
