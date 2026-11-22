# I997-dh610/series_D304315_r2: rerun of Delta's Taylor series at D 3.04315, M 320, N 8, with the rules counted from the base line (#997)

Machine dh610 (Fedora 45, i7-12700, 20 threads, 62 GB). Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/997. Rerun ordered by the coordinator (hc t2j, 22 Nov 2026, `ref/rerun_rules_hc.txt`) after the first run (`../series_D304315/`, its files unchanged) was stopped at 05:58:34 UTC by the 3 h-from-the-start rule with no `base` line written. Same command and readings (`ref/commands_hc_997.txt`, `ref/comment_7073219529.md`), on the 10 threads beside #1067, nice 10; only the output folder carries the run tag `_r2`. Worktree `~/Source/choptuik-large-d-997c` at origin/main ab0ddb8c (clean), venv-i1058, base state `I945-win2/leg/states/lowD343_D3.043150_M320.npz` (blob c23b9cb3, checked by `run997d.sh`).

Rules (`run997d.py`; the clock for each is named):
- base cap 8 h, from the process start: no `base` line within 8 h: TERM to the exact pid, report. The base line's landing is reported at once with its own seconds and the seconds since the start ("the base time", which decides whether M 320 at this base is affordable);
- after the base line, from the time the monitor first sees it (20 s polling): order 2 not done within 3 h, or any order's solve with `converged False`: TERM to the exact pid, report. Each order's time is reported;
- the series file is saved before the target stage: past 30 min after it appears, TERM to the exact pid;
- readings, fixed by the coordinator before the data: radius 0.03 or more over the converged orders is "not a singularity of Delta", 0.001 or less is "a singularity", between is no reading (`read997c.py`).
No other cap: the run has none on total wall time.

## Before the launch (22 Nov)

Command diff (`cmddiff_prelaunch.txt`, run by `run997d.py` again at the launch, which stops on a difference): the two output paths carry `_r2`; the gate removes the tag, requires it on exactly two tokens, and compares the rest:

```
raw diff (the run tag shows):
@@ -2 +2 @@
-.../I997-dh610/series_D304315
+.../I997-dh610/series_D304315_r2
@@ -14 +14 @@
-.../I997-dh610/series_D304315/series_D3.04315_M320_N8.npz
+.../I997-dh610/series_D304315_r2/series_D3.04315_M320_N8.npz
cmddiff997: EMPTY after the run tag is removed
```

Selftests: `run997d.py --selftest` (13 cases: the order parser, the base parser, no stop at 3.5 h without a base line, the stop at 8.1 h without one, no stop once the base line landed at 7.5 h, the stop at 3 h plus 100 s after the base line without order 2 and none 100 s before, a not-converged order) pass; `--mutate` (base cap and order-2 bar raised to 1000 h, the convergence check off) exits 1 with 3 cases failing, as it must. `cmddiff997.py --selftest` (the same command and eight slips: `--N 9`, `--target 3.0432`, `--threads 6`, a wrong state, a dropped `--checks ''`, the stopped run's folder without the tag, the tag on one output path only, the tag on the state path) pass; `--break` exits 1. Plants of the readings (`read997c.py plants`, `plants_997d.txt`, the same code and criteria as the first run's): PASS; `plants --mutate` exits 1 as it must.

Launch: `start997d.sh` (unit `i997t`, under `systemd-inhibit`, memory log `memlog_i997t.log`: alert only), then `run997d.sh`, `run997d.py`. Logs as they come: `exits_997d.txt` (decisions with times), `anm_lowd.log`, `rss_997d.log` (RSS, CPU, MemAvailable, load every 60 s).

Written as the run goes.
