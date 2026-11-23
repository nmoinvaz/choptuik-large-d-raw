# I1079-dh610: Linux rerun of the excited M = 3 zeros' certificates (Krawczyk point and box, H1, H2, H3, the inclusion) from macm3's command lines, and the cross-load of macm3's box and point files

Machine dh610 (Fedora 45, i7-12700, 20 logical CPUs, 64 GB RAM, Linux). Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1079. Written 2026-11-23 17:33 UTC, before any run of this folder. Status words: numerical evidence until the coordinator rules; nothing here asserts Theorem A(3).

## Order (coordinator t5, hc and the #1079 comment of "18:10", posted 17:30Z), in part
"Task for dh610: rerun the excited certificates on Linux (AGENTS.md "Reproducing a certificate on another machine", #111). Checkout: a new worktree of feat/certify-excited at c40fbc77, with main's venv (python-flint 0.9.0; record python-flint and FLINT). Threads: 4, nice 10, beside the recount and the leg lane. Raw: I1079-dh610/, README first. Take the command lines from macm3's scripts in raw I1079-macm3/ (levers/runner/levers.sh, hyp.sh, hyp1.sh, h2/runner/h2.sh, incl.sh), without their macOS wrappers, and post them here before running. For each zero, at CERTIFY_M_NTAY=28 CERTIFY_M_NJAC=16, xi_1 0.3, centres p^ from macm3's refine files (x1 box (1e-12, 1e-13), x2 box (1e-12, 1e-12)): 1. certify_M.py point and box runs; krawczyk --point, controls --point and certify_M_recheck.py, with its mutation. 2. H1: lemma6_sector_M.py --M=3 --rp=0.1 --k=20 --box=1e-6 --Z=0.004489 --x=p^, with --mutate=series. 3. H3: the 6a export, then lemma6_jump_M.py, with the partial and swap controls. 4. H2: lemma6b1_cover_M.py: ray --c1, rows, check, c1check, mutate --j=11 at --h=1e-11 --tag=_excN_linux. Then theorem_A_sets_M.py --M=3 --cert --ray, and its --selftest. Cross-load: certify_M.py krawczyk --box=<macm3's box> --point=<macm3's point> on this machine. The coordinator runs dh610's files on the Mac. Pass, fixed before the run: every step passes on its own bounds, with every control firing as on macm3; each machine's files pass on the other; the margins and rho_6a may differ from macm3's in late digits, and a difference above 1% in any margin is reported. Estimate: about 3 h."
t5's hc adds: "an added task beside the recount and the leg lane (4 threads, nice 10) ... Post the commands on #1079 first; raw I1079-dh610/, README first with the pass criteria. Report each step; the leg lane keeps priority." The commands are posted on #1079 (the comment's link is in the Status below).
Memory alerts only (standing rule).

## Checkout and environment
- Worktree `~/Source/choptuik-large-d-1079a`: `feat/certify-excited` at c40fbc77d8505d8838c2c0ecc51d3feaa5d7a340 (detached, clean, tracked files only; macm3 ran the boxes at 1addcada, H1 and H2 at 89553c6b and the inclusion at c40fbc77; the branch is linear, the changes after 1addcada are options whose defaults leave stored results unchanged). All steps in `solver/proof`.
- Python `~/Source/venv-i1058/bin/python`: Python 3.14.10, python-flint 0.9.0, FLINT 3.6.0 (macm3: Python 3.14.3, python-flint 0.9.0, FLINT 3.6.0). The steps print and record the versions in `steps.txt`.
- `CERTIFY_M_NTAY=28 CERTIFY_M_NJAC=16`, `CERTIFY_M_XI1` unset (xi_1 = 0.3), 1 BLAS/OMP thread per process, `nice -n 15`.
- Threads: 4 processes of 1 thread (zeros 1 and 2 side by side, each with a certificate chain and a covering). The leg lane (`../I1025-dh610/kc79_leg`, 8 threads at nice 10) has priority. Nominal total beside the #1076 recount's 12: 24 (the standing rule is at most 20); in fact the recount's batches use 2 processes now (`../I1021-dh610/fu022mp_m3mp/logs/sampler.log`), so the load is about 14 to 16 while a leg scan runs. Said to the coordinator with the start.

## Inputs (pinned by blob, copies in `in/macm3/`; `in_blobs_macm3.txt`; the scripts refuse any other blob)
| file (macm3, raw I1079-macm3/levers/data/, origin/main 143d4d5b) | blob | use |
|---|---|---|
| `A_M_refine_M3_x1E2.json`, `A_M_refine_M3_x2E2.json` | 482d4e3a, c1c7bab0 | the centres p^ (`p_out`), the box centre files |
| `A_M_box_M3x1E2_h1e-12_w1e-13.json`, `A_M_box_M3x2E2_h1e-12_w1e-12.json` | 1e643208, a1ae0391 | cross-load |
| `A_M_point_M3x1E2.json`, `A_M_point_M3x2E2.json` | 611a68c1, cd3cb7f8 | cross-load |
macm3's logs and result files (`I1079-macm3/levers/logs`, `levers/h1`, `levers/lemmas_M_runs`, `h2/`) are the reference for the comparison (`compare_macm3.py`, written before the runs end, reads both sets; no number is typed by hand).

## Commands (the comment on #1079 has the list; `common.sh`, `chain.sh`, `h2.sh`, `incl.sh`, `xload.sh`, `run_all.sh` are macm3's `levers.sh`, `hyp1.sh`, `hyp.sh h3`, `h2/runner/h2.sh`, `incl.sh` without the macOS wrappers; the command lines are unchanged)
Differences from macm3's runs, all deliberate: no refine step (the centre is macm3's refine file, pinned); one box per zero (not the 4-box matrix); no H0 (not in the order); one worktree (c40fbc77) for all steps; `--tag=_excN_linux`; nice 15; H2's rows run one after the other in one process per zero (A then B); the `probe` of H2 runs first (information, 20 s); caught mutations that the scripts return exit 0 for are read from their log lines (partial: "NOT established", swap: "backward integration failed", series: "lemma S holds: False (must be False)", `mutate --j=11`: "0 of 12 discs of row 11 certified (must be 0)").
Stage 1 (4 processes): `chain.sh N` (point, box, krawczyk --point, controls --point, recheck and its mutation; H1; export6a and H3) and `h2.sh N` (probe, ray --c1, row --j=11, rows, check, c1check, mutate --j=11), N = 1, 2. Stage 2 (4 processes): `incl.sh N` (the inclusion and its selftest) and `xload.sh N` (macm3's box and point through this machine's krawczyk, controls, recheck and its mutation). Each script stops at a failed step and writes a `STOP:` line to `steps.txt`; a failing control stops the work and is reported, no bar is loosened.

## Pass criteria (fixed before the run; the order's)
1. Every step passes on its own bounds and every control fires as on macm3: point, box, krawczyk, controls, recheck exit 0 and `recheck --mutate` exit 1; H1 "ALL CHECKS PASS (M = 3): True" and the series mutation caught; export6a and lemma 6a exit 0 with rho_6a below 1, and the partial and swap mutations caught; H2 every disc `ok True`, `check --json` PASS, `c1check` True, `mutate --j=11` 0 of 12 discs; the inclusion HOLD and its `--selftest` PASS.
2. Each machine's files pass on the other: macm3's box and point pass here (krawczyk exit 0, controls exit 0, recheck exit 0 and its mutation exit 1). The coordinator runs the files of this folder (`out/`) on the Mac.
3. The margins and rho_6a may differ from macm3's in late digits; a difference above 1% in any of the four relative margins (macm3: x1 +0.702, +0.758, +0.997, +0.998; x2 +0.943, +0.945, +0.988, +0.995) is reported with the number. Also compared, as information with the same 1% reading: rho_6a (macm3 0.01365237958 at x1, 0.01258978538 at x2), lemma S and old-sector contractions, the point runs' g_rad, the inclusion's slack (a bound assembled from upper bounds moves with every radius; it passes on its own, #111).

## Predictions, registered before the run (mine, information)
- Every step passes and every control fires as on macm3 (80%); the cross-load of macm3's files passes (88%).
- The four relative margins of each zero agree with macm3's within 1% (85%; they come from ball arithmetic, a different machine and Python changing at most late digits); rho_6a within 1% (88%); the lemma S contractions within 1% (90%).
- Time: the whole rerun, 2 stages, takes 1 to 2.5 h (65%; macm3's steps: point 216 to 248 s, box 217 to 231 s, H2 rows 400 to 510 s, row 11 about 50 s, H3 about 3 min; the coordinator's estimate is 3 h); the point and box runs take 150 to 450 s each (70%).
- No step needs a change of the code or of a parameter (85%).

## Status
- 2026-11-23 17:33 UTC: folder, scripts, pins and criteria written before any run; commands posted on #1079 next.
