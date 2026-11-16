# I906-rpi5: two checks of Delta_inf (Bulirsch-Stoer and Akaike-averaged fits) on the Raspberry Pi 5

Machine rpi5 (Raspberry Pi 5 Model B, aarch64 Linux, 4 cores, 8 GB), issue
https://github.com/nmoinvaz/choptuik-large-d/issues/906 (`hp/dinf_check.py`, the six plants of `hp/planted_dinf.py`, then
the real double-double points). Script `run906.sh` (the coordinator's, md5 7ae710395fc4dddaf1bd0fe078f6ece2, unedited):
`bash run906.sh <venv python> <worktree> <raw clone root>`, run from the raw clone's root with the worktree
`~/Source/choptuik-large-d-906` (wip/i906-rpi5 at origin/main 49bfccec, never committed). It runs four commands of
`dinf_check.py` one after another at nice 10: `bst`, `bst --mutate omega2`, `aic`, `aic --mutate noweight`, with the
required exit status 0, 1, 0, 1. Each command's output is `<name>.log`, `exits_906.txt` has its start, its exit status
against the required one and its wall time, `env.txt` the commit and the versions.

Started 2026-11-16 05:19:29 UTC, `906 done` 06:16:17 UTC (57 min, the issue estimated 2 to 3 h). mpmath 1.3.0, python 3.13.7,
aarch64 glibc 2.42 (`env.txt`), worktree commit 49bfccec, never committed (`git status` clean).

## Result

All four exit statuses are the required ones (0, 1, 0, 1). `bst` passes the five graded plants and its real median is
1.64389374643, 4.25e-10 from the README's 1.643893746 (inside the bar). `aic` passes the five graded plants with no
offset, but on the real points its mean is 1.64389620925, 2.46e-6 from the README's value and outside its ±1.5e-8 bar,
with one fit carrying the whole weight (largest weight 1.0). The disagreement is reported, not fixed.

| command | required exit | exit | wall | graded plants passed | verdict |
|---|---|---|---|---|---|
| `bst` | 0 | 0 | 271 s | 5 of 5 | as required |
| `bst --mutate omega2` | 1 | 1 | 240 s | 0 of 5 (median off by 0.0322 on each) | the control fires |
| `aic` | 0 | 0 | 1555 s | 5 of 5 | as required |
| `aic --mutate noweight` | 1 | 1 | 1342 s | 0 of 5 (mean off by 2.14e-8 to 2.16e-8) | the control fires |

Each log below is `<name>.log` verbatim from its first line; the planted limit is P(0) = 1.64389374467885 in all four.
T1 to T5 are graded, T6 (non-analytic at 1/D = 0) is reported only (`info`).

### bst (`bst.log`)

| plant | median of 54 tables off by | middle-half spread | verdict |
|---|---|---|---|
| T1 | 1.12e-9 | 1.2e-8 | pass |
| T2 | 1.07e-9 | 1.2e-8 | pass |
| T3 | 4.81e-9 | 2.4e-8 | pass |
| T4 | 1.05e-9 | 1.2e-8 | pass |
| T5 | 1.11e-9 | 1.2e-8 | pass |
| T6 | 1.19e-9 | 1.2e-8 | info |

`real: median of 54 tables 1.64389374643, middle-half spread 1.2e-8`, and `against the README's 1.643893746 +- 1.5e-8:
4.25e-10 (inside the bar)`.

### bst --mutate omega2 (`bst_omega2.log`)

| plant | median of 54 tables off by | middle-half spread | verdict |
|---|---|---|---|
| T1 to T5 | 0.0322 | 0.0065 (0.0066 at T4) | FAIL (5) |
| T6 | 0.0322 | 0.0065 | info |

`0 of 5 graded plants passed`. The log has no `real:` line.

### aic (`aic.log`)

| plant | fits | mean off by | sd | in sd | largest weight | verdict |
|---|---|---|---|---|---|---|
| T1 | 120 | -1.21e-10 | 7.0e-10 | -0.17 | 0.408 | pass |
| T2 | 120 | -1.21e-10 | 7.0e-10 | -0.17 | 0.408 | pass |
| T3 | 120 | -2.29e-10 | 7.8e-10 | -0.3 | 0.552 | pass |
| T4 | 120 | -1.21e-10 | 7.0e-10 | -0.17 | 0.408 | pass |
| T5 | 120 | -1.23e-10 | 7.3e-10 | -0.17 | 0.439 | pass |
| T6 | 120 | -9.72e-11 | 7.2e-10 | -0.14 | 0.428 | info |

`real: 120 fits, mean 1.64389620925, sd 9.4e-8, largest weight 1.0`, and `against the README's 1.643893746 +- 1.5e-8:
2.46e-6 (OUTSIDE the bar)`.

### aic --mutate noweight (`aic_noweight.log`)

| plant | fits | mean off by | sd | in sd | largest weight | verdict |
|---|---|---|---|---|---|---|
| T1 | 120 | 2.14e-8 | 5.1e-8 | 0.42 | 0.00833 | FAIL |
| T2 | 120 | 2.14e-8 | 5.1e-8 | 0.42 | 0.00833 | FAIL |
| T3 | 120 | 2.15e-8 | 4.9e-8 | 0.44 | 0.00833 | FAIL |
| T4 | 120 | 2.14e-8 | 5.1e-8 | 0.42 | 0.00833 | FAIL |
| T5 | 120 | 2.16e-8 | 5.2e-8 | 0.42 | 0.00833 | FAIL |
| T6 | 120 | 2.14e-8 | 5.1e-8 | 0.42 | 0.00833 | info |

`0 of 5 graded plants passed`. The mean is within 1 sd on every plant, so the failure is the 0.3e-8 bar (mean within
0.3e-8 of the truth), not the 2 sd line. The log has no `real:` line.

### Discrepancy

On the real points `aic` gives 2.46e-6 from the README's Delta_inf (26 times its own sd of 9.4e-8) and puts the whole
weight on one fit of the 120 (largest weight 1.0), while `bst` agrees to 4.25e-10. The planted-data weights
are spread (largest 0.41 to 0.55). The code applies the planted noise (1e-16 for D <= 60.1, 7e-16 above) to the real
points too, so the real chi^2 enters the AIC at that scale; whether that is why one fit takes all the weight was not
tested here. This run did not look inside the fits.

### Recommended tasks

- **Which fit carries the weight at the real points.** Print the `aic` table for the real points (the 120 fits with
  model, degree, Dmin, cleaning, chi^2, N_cut, AIC, weight, limit), and rerun it with the real points' own scatter as
  the noise (the per-point residual of a reference fit) in place of the planted noise. Acceptance: the table names the
  fit with weight 1.0 and its limit, and the rerun either spreads the weight over several fits with a mean inside
  1.5e-8 of 1.643893746 or shows it does not. Depends on #906.
