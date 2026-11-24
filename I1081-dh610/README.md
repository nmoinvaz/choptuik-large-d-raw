# I1081-dh610: the second excited M = 3 zero's box run at three configurations (PREC, box size), six frame-perturbed reruns each, and the Krawczyk margins of every run

Machine dh610 (Fedora 45, i7-12700, 20 logical CPUs, 64 GB RAM, Linux). Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1081, item 1 (follow-up of #1079's review, finding 18). Written 2026-11-24 00:47 UTC, before any run of this folder. Status words: numerical evidence; nothing here asserts Theorem A(3).

## Order (coordinator t5, hc and the #1081 comment headed "2026-11-24 01:00 UTC", created 00:44Z per the API), in part
"pull main (9676d7c1: CERTIFY_M_PREC). At the second zero (macm3's A_M_refine_M3_x2E2.json centre, NTAY 28 NJAC 16), configs (a) h=w=1e-12 PREC 256, (b) h=w=1e-12 PREC 384, (c) h=w=1e-13 PREC 256: per config one point run, one unperturbed box run, six box runs under review_1079/perturb_box.py with REVIEW_PERTURB=qr REVIEW_SEED=1..6, and krawczyk --point=<that config's point file> --box=<each>. Written before (README): (a) reproduces the review (most perturbed runs fail); robust = all six perturbed pass with smallest margin > +0.2. Report every margin. Raw I1081-dh610/." Threads: 5 at nice 10, beside the recount and the leg lane. Estimate: 21 box runs and 3 point runs at about 7 to 10 min each, about 1 h at 5 processes.

## Checkout and environment
- Worktree `~/Source/choptuik-large-d-1081`: main of the code repository at 9676d7c11fa61af808031839b106a4d50fa69547 (detached, clean; `CERTIFY_M_PREC` unset gives 256 as before). All steps run in `solver/proof`; the lane refuses any other commit or tracked changes.
- Python `~/Source/venv-i1058/bin/python` (Python 3.14.10, python-flint 0.9.0, FLINT 3.6.0; the same as the #1079 rerun, raw I1079-dh610). `CERTIFY_M_NTAY=28 CERTIFY_M_NJAC=16`, `CERTIFY_M_XI1` unset, `CERTIFY_M_PREC` per configuration, one BLAS/OMP thread per process, `nice -n 10`.
- Centre: `in/A_M_refine_M3_x2E2.json` (macm3's refine file, `p_out`; blob c1c7bab0, `in_blobs.txt`; the lane refuses any other blob), the same file as the #1079 rerun's.
- Threads: 5 processes of 1 thread, nice 10. Beside them the #1076 recount (2 processes) and the k_c 79 leg lane (8, nice 10): 15 of the 20 allowed. Memory: alert-only log, no process is stopped for memory; the lane refuses to start with less than 24 GB available.

## Configurations and runs (per configuration, in `cfg_a/`, `cfg_b/`, `cfg_c/`)
| config | h, w | PREC | role |
|---|---|---|---|
| a | 1e-12, 1e-12 | 256 | the baseline: the review's setting |
| b | 1e-12, 1e-12 | 384 | higher working precision of the Lohner integration |
| c | 1e-13, 1e-13 | 256 | a smaller box |
- `point.json`: `certify_M.py point 3 --p=<p_out of the refine file> --out=... --log=...` at the configuration's PREC (one per configuration, as ordered; a and c have the same inputs, so their point files should agree, and I compare them).
- `box_U.json`: `certify_M.py box 3 --centre=in/A_M_refine_M3_x2E2.json --use_out --h=H --w=W --out=...`, unperturbed.
- `box_s1.json` to `box_s6.json`: the same command through `review_1079/perturb_box.py` with `REVIEW_PERTURB=qr REVIEW_SEED=k` (every entry of Q from `qr_pivot` times 1 +- 2^-52, seeded; the run stays a valid enclosure).
- `krawczyk_<run>.log`: `certify_M.py krawczyk --point=cfg_X/point.json --box=cfg_X/box_<run>.json` for each of the seven boxes, run with the configuration's `CERTIFY_M_PREC` (`exact_p` rounds the centre at PREC bits, so the assembly must use the PREC of the run files). Four relative margins are printed per run; a run passes when "K(X) in int X: True".
- `certify_M.py controls --box=box_U.json --point=point.json` per configuration (exit 0, "CONTROLS ALL AS EXPECTED", as in the #1079 rerun): it must be able to fail, and it is the control that the Krawczyk test can fail.
- Scheduling: 24 jobs, a pool of 5 processes, in the order b, c, a (the slowest first). The Krawczyk stage runs after the pool (seconds).
- Files: `lane_1081.sh` (pins, selftests, pool, Krawczyk stage, summary, push), `job.sh`, `common.sh`, `start_1081.sh` (systemd user unit `i1081`), `notify_1081.sh`, `summarize_1081.py` (tables, criterion, scorecard; selftest, `--mutate`), `steps.txt` (every command with its seconds and exit), `exits_1081.txt`.

## Acceptance (fixed before the run)
- Every job exits 0 and writes its file; every run file records `prec` = the configuration's PREC, `h` and `w` as set, and `orders` [28, 16]; the point files of a and c are equal in `g`, `steps` and `p` (their `sec` differs).
- The perturbation acted: each perturbed run prints "perturbed calls: qr_pivot N" with N > 0 and the unperturbed run N = 0; each perturbed box file differs from its configuration's `box_U.json` in its `sets`. Otherwise the lane's result is void and I report it.
- `certify_M.py controls` exits 0 on each configuration's unperturbed box; the summarizer's selftest exits 0, `selftest --mutate` exits 1, and `--mutate` on the real files exits 1 with "control FIRED" (3 if it does not fire).
- A step that fails or a control that fires stops the lane and is reported; nothing is loosened.
- **The order's criterion, fixed before the run:** a configuration is *robust* when all six perturbed runs pass (K(X) in int X: True) and the smallest of the 24 relative margins (four per run) is above +0.2. Margins of every run, the unperturbed ones included, are reported in a table; the unperturbed run is not part of the criterion. The configuration (a) is expected not to be robust (the order).

## Predictions, registered before the run (mine, information)
- The lane runs to its end with every job exit 0 and the acceptance holds (88%); the perturbation acted in all 18 perturbed runs (96%); the 18 perturbed box files all differ from their `box_U.json` (96%).
- The unperturbed boxes pass the Krawczyk test: a 90%, b 85%, c 90%. The unperturbed box of (a) gives the margins of my #1079 rerun at c40fbc77 (+0.711, +0.528, +0.981, +0.992) to the printed digits: 85%.
- (a): at least four of the six perturbed runs fail: 75% (all six fail 25%; all six pass 5%). (a) is not robust: 97%.
- (b), the higher precision: robust 25% (the mechanism of finding 18 is unknown, and a smaller roundoff floor at 384 bits is far below the box).
- (c), the smaller box: robust 70% (at the first zero, the box with w = 1e-13 passes 6 of 6).
- At least one of b and c robust: 75%; both: 20%.
- (Scoring of the time and memory predictions: on every job of the kind, minimum and maximum printed; "within" means all of them.)
- Seconds per run at PREC 256 (point and box, nice 10 beside 10 other threads): 300 to 650 s (70%; #1079 rerun 400 s at nice 15, macOS 205 s); the PREC 384 runs take 1.3 to 2.5 times the PREC 256 runs of the same kind (70%); the lane ends within 75 min of its start (70%); peak RSS per process below 3 GiB (80%).

## Status
- 2026-11-24 00:47 UTC: folder and README written; scripts and the summarizer next, nothing run.
- 2026-11-24 00:50 UTC: scripts written (`lane_1081.sh`, `job.sh`, `common.sh`, `start_1081.sh`, `notify_1081.sh`, `summarize_1081.py`). The lane's dry run passed at 00:49:21 UTC (pins, summarizer selftest 0 and `--mutate` 1; its two lines are the first of `exits_1081.txt`). The summarizer was tested on planted data in a scratch directory (test only: the real-file path, a planted missing perturbation and a planted equal box are caught, `--mutate` fires); a 3-step pilot of the perturbed box command at PREC 384 and h = w = 1e-13 ran (6.6 s per step at the start, perturbed calls 6; scratch, not a result). The unit `i1081` starts after this README is pushed.


## Result (`summarize_1081.py` > `summary_1081.txt` prints the tables from the files; its `--mutate` exit 1 with "control FIRED", `selftest` 0, `selftest --mutate` 1)
| config | run | exit | K(X) in int X | relative margins | smallest | box seconds (file) | perturbed calls | sets differ from U |
|---|---|---|---|---|---|---|---|---|
| a | U | 0 | True | +0.711, +0.528, +0.981, +0.992 | +0.528 | 369 | none | - |
| a | s1 | 1 | False | +0.031, -0.606, +0.979, +0.994 | -0.606 | 369 | 2352 | True |
| a | s2 | 1 | False | -0.081, -0.774, +0.985, +0.993 | -0.774 | 369 | 2352 | True |
| a | s3 | 1 | False | +0.311, -0.251, +0.973, +0.990 | -0.251 | 359 | 2352 | True |
| a | s4 | 0 | True | +0.696, +0.502, +0.988, +0.994 | +0.502 | 358 | 2352 | True |
| a | s5 | 0 | True | +0.559, +0.275, +0.981, +0.992 | +0.275 | 324 | 2352 | True |
| a | s6 | 1 | False | +0.255, -0.240, +0.984, +0.993 | -0.240 | 319 | 2352 | True |
| b | U | 0 | True | +0.711, +0.528, +0.981, +0.992 | +0.528 | 687 | none | - |
| b | s1 | 1 | False | +0.031, -0.606, +0.979, +0.994 | -0.606 | 1100 | 2352 | True |
| b | s2 | 1 | False | -0.081, -0.774, +0.985, +0.993 | -0.774 | 771 | 2352 | True |
| b | s3 | 1 | False | +0.311, -0.251, +0.973, +0.990 | -0.251 | 1104 | 2352 | True |
| b | s4 | 0 | True | +0.696, +0.502, +0.988, +0.994 | +0.502 | 709 | 2352 | True |
| b | s5 | 0 | True | +0.559, +0.275, +0.981, +0.992 | +0.275 | 762 | 2352 | True |
| b | s6 | 1 | False | +0.255, -0.240, +0.984, +0.993 | -0.240 | 942 | 2352 | True |
| c | U | 0 | True | +0.971, +0.953, +0.998, +0.999 | +0.953 | 634 | none | - |
| c | s1 | 0 | True | +0.903, +0.839, +0.998, +0.999 | +0.839 | 518 | 2352 | True |
| c | s2 | 0 | True | +0.892, +0.823, +0.999, +0.999 | +0.823 | 454 | 2352 | True |
| c | s3 | 0 | True | +0.931, +0.875, +0.997, +0.999 | +0.875 | 392 | 2352 | True |
| c | s4 | 0 | True | +0.970, +0.950, +0.999, +0.999 | +0.950 | 387 | 2352 | True |
| c | s5 | 0 | True | +0.951, +0.916, +0.998, +0.999 | +0.916 | 384 | 2352 | True |
| c | s6 | 0 | True | +0.926, +0.876, +0.998, +0.999 | +0.876 | 372 | 2352 | True |

| config | perturbed runs passing | smallest margin of the six perturbed runs | robust (all six pass, smallest > +0.2) | unperturbed run passes | unperturbed margins |
|---|---|---|---|---|---|
| a (h = w = 1e-12, PREC 256) | 2 of 6 | -0.774 | False | True | +0.711, +0.528, +0.981, +0.992 |
| b (h = w = 1e-12, PREC 384) | 2 of 6 | -0.774 | False | True | +0.711, +0.528, +0.981, +0.992 |
| c (h = w = 1e-13, PREC 256) | 6 of 6 | +0.823 | True | True | +0.971, +0.953, +0.998, +0.999 |

acceptance checks: 74 of 74 hold; failing: none; every job exit 0: True (24 jobs)
config a: seconds (wall, /usr/bin/time -v) point 368, box U 369, perturbed 319 to 370; peak RSS 0.06 to 0.06 GiB
config b: seconds (wall, /usr/bin/time -v) point 716, box U 687, perturbed 709 to 1105; peak RSS 0.06 to 0.06 GiB
config c: seconds (wall, /usr/bin/time -v) point 653, box U 634, perturbed 372 to 519; peak RSS 0.06 to 0.06 GiB
pool: 2026-11-24 00:50:32 to 2026-11-24 01:37:27 (47 min)
#1079 rerun, second zero, unperturbed (c40fbc77): (True, [0.711, 0.528, 0.981, 0.992]); this run's (a, U): (True, [0.711, 0.528, 0.981, 0.992]); equal to the printed digits: True
time ratios b over a per job kind: [1.94, 1.86, 2.98, 2.09, 3.07, 1.98, 2.35, 2.96]; PREC 256 seconds 319 to 653; peak RSS over all jobs 0.06 GiB

- **Config c is robust by the order's criterion:** all six perturbed runs pass, smallest margin +0.823 (seed 2); unperturbed +0.971, +0.953, +0.998, +0.999. **Config a is not** (2 of 6 pass: seeds 4 and 5; seeds 1, 2, 3 and 6 fail with a margin between -0.240 and -0.774). **Config b is not** (2 of 6 pass).
- **b equals a at every run:** the four relative margins of all seven boxes (U and seeds 1 to 6) are the same to the printed digits in a and b (compared run by run from the Krawczyk logs), although the b runs took 1.9 to 3.1 times longer, their run files record prec 384, and the 384-bit run files differ from the 256-bit ones in their `sets` at all seven runs (added check, below). The same seeds give the same frames Q (float64 from the QR of the midpoint, any PREC), so the same perturbation acts in a and b. What is measured: the margins do not move with the working precision between 256 and 384 bits, and move with the box size. The mechanism (the float64 frames) is the coordinator's reading; this folder shows the two levers, not the mechanism.
- **Acceptance:** all jobs exit 0; `prec`, `h`, `w`, `orders` [28, 16] recorded as set in all 24 files; the perturbation acted in 18 of 18 runs (`perturbed calls: qr_pivot 2352`) and in none of the unperturbed ones; the 18 perturbed boxes differ from their U; the point files of a and c agree in p, g and steps; `certify_M.py controls` on each U exit 0, CONTROLS ALL AS EXPECTED. 74 of 74 checks hold.
- **Time and memory:** pool 00:50:32 to 01:37:27 UTC (47 min); PREC 256 jobs 319 to 653 s, PREC 384 jobs 687 to 1105 s (a and c: the point and the unperturbed box 368 to 653 s); the sampled total RSS of the 5 processes at most 0.28 GiB (about 57 MB per process), MemAvailable at least 48.21 GiB, load median 13.08 (the leg lane's 8 and the recount's 2 beside), no alert line in `memlog_i1081.log`.
- **A correction of my own summarizer, made after the first read:** the lane's first summary (`summary_1081_lane_run.txt`, kept) took the #1079 rerun's reference margins from the *last* matching line of `../I1079-dh610/steps.txt`, which is the cross-load stage (+0.943, +0.945, +0.988, +0.995), not the chain stage (+0.711, +0.528, +0.981, +0.992), and scored the row "(a, U) equals the #1079 rerun" WRONG. The reference is now the anchored chain line, with a selftest case and its `--mutate` (the loose pattern must fail); the row is right. One check was added after the first read: that b's box differs from a's at the same run (7 of 7 hold), which changes no verdict. Nothing else was touched; the table above is the regenerated `summary_1081.txt`.

### Predictions scorecard (written before the run; "right" = the stated event happened)
| prediction (registered before the run; right = the stated event happened) | result | verdict |
|---|---|---|
| every job exit 0 and the acceptance holds (88%) | exit0 True, failing checks 0 | right |
| the perturbation acted in all 18 perturbed runs (96%) | 18 of 18 | right |
| the 18 perturbed box files all differ from their U (96%) | 18 of 18 | right |
| unperturbed box passes at a (90%) | True | right |
| unperturbed box passes at b (85%) | True | right |
| unperturbed box passes at c (90%) | True | right |
| (a, U) margins equal the #1079 rerun's to the printed digits (85%) | True | right |
| (a) at least four of six perturbed runs fail (75%) | 4 of 6 fail | right |
| (a) all six perturbed runs fail (25%) | 4 of 6 fail | WRONG |
| (a) all six perturbed runs pass (5%) | 2 of 6 pass | WRONG |
| (a) not robust (97%) | robust False | right |
| (b) robust (25%) | 2 of 6 pass, smallest -0.774 | WRONG |
| (c) robust (70%) | 6 of 6 pass, smallest +0.823 | right |
| at least one of b and c robust (75%) | b False, c True | right |
| both b and c robust (20%) | b False, c True | WRONG |
| PREC 256 jobs each 300 to 650 s (70%) | 319 to 653 | WRONG |
| PREC 384 jobs 1.3 to 2.5 times the PREC 256 (a) jobs of the same kind (70%) | 1.86 to 3.07 | WRONG |
| the pool ends within 75 min of its start (70%) | 47 min | right |
| peak RSS per job below 3 GiB (80%) | max 0.06 GiB | right |

The time predictions failed twice: the PREC 256 jobs ran 319 to 653 s (registered 300 to 650 s; the c point run took 653 s), and the PREC 384 jobs took 1.86 to 3.07 times the PREC 256 (a) jobs of the same kind (registered 1.3 to 2.5). (b) robust was registered at 25% and did not happen; (c) robust at 70% happened.

## Status after the pool
- 2026-11-24 01:39 UTC: pool and Krawczyk stage done (lane exit lines in `exits_1081.txt`), result and scorecard above. Next (t5's order, #1081 comment of 01:45 UTC): config c as the second zero's certificate of record, in `record_c/`.
