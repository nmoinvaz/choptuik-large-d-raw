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
