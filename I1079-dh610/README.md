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
- 2026-11-23 17:34 UTC: folder, scripts, pins and criteria written before any run (raw ada1acba); commands posted on #1079 (comment 7108847808).
- 17:34:08 UTC: stage 1 started (unit i1079dh). 17:47:30 exc2's Krawczyk test passed; 17:47:37 exc1's passed but its controls came out UNEXPECTED at C6 (STOP line); 17:48 the coordinator resolved it (the documented case) and exc1 was resumed from H1 (`chain_h1.sh`); stage 1 ended 18:05:33 (all scripts done).
- 18:06 UTC: stage 2 (inclusion, cross-load of macm3's files) run by hand by the coordinator's order (`steps.txt` has the NOTE line; `stage2.sh`'s wait pattern never matched, a mistake of mine, so the four scripts were started directly). Nothing was stopped or changed in a finished run.

## Result (all numbers from the files; `compare_macm3.py` > `compare_macm3.txt`, `compare_json.py` > `compare_json.txt`, `steps.txt`)

**Every step passes on its own bounds at both zeros, and every control fires as on macm3, with one exception that the coordinator resolved: exc1's controls C6.**

| step | x1 (box 1e-12, 1e-13) | x2 (box 1e-12, 1e-12) |
|---|---|---|
| point run (s) | 404, g_rad 1.571e-21 | 400, g_rad 6.113e-23 |
| box run (s) | 405 | 401 |
| `krawczyk --point` | K(X) in int X True, relative margins +0.468, +0.619, +0.997, +0.998 | True, +0.711, +0.528, +0.981, +0.992 |
| `controls --point` | exit 1, C6 UNEXPECTED (below), the other nine as expected | exit 0, ALL AS EXPECTED |
| `certify_M_recheck.py`; `--mutate` | exit 0; exit 1 | exit 0; exit 1 |
| H1 `lemma6_sector_M.py` | ALL CHECKS PASS; lemma S 0.6961, old sector 0.6839; `--mutate=series` caught | PASS; 0.6782, 0.7008; caught |
| H3 `export6a`, lemma 6a | rho_6a 1.3652e-02 (macm3 1.3652e-02, 3e-7 apart); `partial` and `swap` caught (197, 228 s) | rho_6a 1.2590e-02 (5e-7 apart); caught (173, 247 s) |
| H2 `ray --c1`, `row --j=11`, rows (A, B) | 104, 97, 778, 743 s; 183 discs all `ok True`, `check --json` PASS, `c1check` True, `mutate --j=11` 0 of 12 | 97, 86, 732, 629 s; same |
| inclusion `theorem_A_sets_M.py --cert --ray`; `--selftest` | HOLD, slack +8.359e-12 at B3; PASS | HOLD, slack +8.278e-12; PASS |
| cross-load: macm3's box and point here | krawczyk exit 0, margins +0.702, +0.758, +0.997, +0.998 (macm3's own); controls exit 0 (ALL AS EXPECTED, C6 included); recheck exit 0; `--mutate` exit 1 | exit 0, +0.943, +0.945, +0.988, +0.995; controls ALL AS EXPECTED; recheck 0; `--mutate` 1 |

**The unexpected control (exc1):** C6, "zero planted inside, moved by (h/2, -3h/10, w/4, ...): expected pass, got fail", relative margins -3.17e-02, +0.319, +0.747, +0.748. The clean A margin is +0.468, below 0.5, so a zero moved by h/2 in A is no longer inside X: the documented case (A_M.md 6.2; macm3 saw it at x1's (1e-12, 1e-12) box). It is not a defect of the code. The coordinator's word at 17:48 UTC: resume from H1 (H1, H3 and H2 do not depend on the margins). C0 to C5, C6b, C7, C8 as expected. Exc2: all as expected.

### The discrepancy against macm3's margins (reported to the coordinator at 17:50 UTC; the diagnosis accepted by the coordinator)
Both zeros pass the Krawczyk test here, but the first two relative margins (A and w/w_inf) are far from macm3's at the same box (the order's 1% bar; `compare_macm3.txt`: 4 margins REPORTED):

| margin | x1 mine | x1 macm3 | x1 relative difference | x2 mine | x2 macm3 | x2 relative difference |
|---|---|---|---|---|---|---|
| A | +0.468 | +0.702 | -33% | +0.711 | +0.943 | -25% |
| w/w_inf | +0.619 | +0.758 | -18% | +0.528 | +0.945 | -44% |
| B3 | +0.997 | +0.997 | 0 | +0.981 | +0.988 | -0.7% |
| C3 | +0.998 | +0.998 | 0 | +0.992 | +0.995 | -0.3% |

Everything downstream agrees: rho_6a to 3e-7 and 5e-7, the lemma S, old-sector and flat estimates to the digits printed, the covering (183 tiles, 579 pieces, 461 links) and the C1 set radii to the digits printed (one 3.5e-3 at x2 row 11), the inclusion's slack to four digits. Bounds assembled from upper bounds (the slack, the radii) move with every radius and pass on their own (AGENTS.md, #111).

**Reading (`compare_json.txt`, the comparison the coordinator asked for; its control recomputes krawczyk_test's margins exactly, max difference 0, and fails under `--mutate`):**
- The box run was started the same way on both machines: `certify_M.py box 3 --centre=data/A_M_refine_M3_<T>.json --use_out --h --w` (no `--point`), the same refine file by blob; the charts `bx['C']`, the box centre p, the path and the steps ([726, 397, 57] and [718, 394, 64]) are identical. `certify_M.py` is the same file at macm3's 1addcada and at c40fbc77.
- The orders of the Taylor expansions: the box processes had ended when asked; the header of the box log does not print them; the processes of the same chain that were alive (the H2 rows) had `CERTIFY_M_NTAY=28 CERTIFY_M_NJAC=16` (and one BLAS/OMP thread) in `/proc/<pid>/environ`; the `ray` lines (28 at x2, 29 at x1: step size h, radii) are identical to every printed digit on both machines, as are the `arc` lines to step 325 (x2) and to the end (x1) except the seconds.
- The gap is in the box run's variational columns: the box Jacobian columns' max radii at x2 are [1.05e-4, 4.20e-4, 1.06e-4, 1.05e-4] here against [6.33e-5, 2.52e-4, 6.48e-5, 6.37e-5] (x1 within 2%), YJ's max radius 0.271 against 0.032 (x1 0.407 against 0.228); the (I - YJ)X term per row [2.89e-13, 4.72e-13, 1.88e-14, 7.8e-15] against [5.7e-14, 5.5e-14, 1.23e-14, 4.9e-15]. g and Y do not carry it: |Yg| midpoints are identical per row, the g radius is identical at x1 and 6.14e-23 against 7.44e-23 at x2, the point's Jacobian radii agree within 5%.
- Where it starts: in the last leg ("real", 64 and 57 steps) the derivative radius grows by three orders (x2: 1.04e-7 to 1.05e-4 here, 7.51e-8 to 5.66e-5 for macm3), and differs from the first steps of that leg; the first differing printed number is at x2's arc step 350 (3.00e-8 against 2.99e-8). The start data's float64 entries already differ in the last digits (x1 `eta` 1.508016533037434e-72 against 1.508016533037432e-72, `eta_der` 1.4322243334663837e-17 against 1.432224333466384e-17; x2 `eta_der` 2.265122423158685e-18 against ...682e-18).
- **Cause (the coordinator's diagnosis, accepted: no perturbation test needed):** last-digit differences of float64 quantities in the start data between the machines (macOS and Linux; AGENTS.md #111 records the same kind of difference for the integration path), amplified on the real leg by the growth of the variational radius. Both enclosures are valid; they differ in size, and the Krawczyk margins move with the box run's Jacobian enclosure.

### Pass criteria (fixed before the run) and what came out
| criterion | result |
|---|---|
| every step passes on its own bounds, every control fires as on macm3 | yes, except exc1's C6, the documented case, resolved by the coordinator |
| each machine's files pass on the other | macm3's box and point pass here (both zeros, all four steps, with macm3's own margins reproduced to the digit); this machine's files (`out/data/A_M_box_M3x?E2_*.json`, `A_M_point_M3x?E2.json`) are for the Mac: the coordinator runs them |
| margins and rho_6a may differ in late digits; above 1% in a margin is reported | rho_6a differs in the 7th digit; the A and w/w_inf margins differ by 18 to 44% at both zeros: reported, with the cause above |

### Predictions scorecard (written before the run)
| prediction | result |
|---|---|
| every step passes and every control fires as on macm3 (80%) | wrong in the strict reading: exc1's C6 (the other controls as expected) |
| the cross-load of macm3's files passes (88%) | right |
| the four margins within 1% of macm3's (85%) | wrong (A and w/w_inf 18 to 44%) |
| rho_6a within 1% (88%); lemma S contractions within 1% (90%) | right (3e-7 to 5e-7; identical) |
| the whole rerun 1 to 2.5 h (65%) | wrong (shorter): stage 1 took 31 min, stage 2 seconds (the 4 processes ran at nice 15 beside a leg lane that was still waiting for its first state) |
| point and box runs 150 to 450 s each (70%) | right (400 to 405 s) |
| no step needs a change of the code or of a parameter (85%) | right (exc1 was resumed from H1 with the same command lines) |

Files: `steps.txt` (every command, exit and last line), `out/` (copies of the worktree's data, logs, lemmas_M_runs and the two coverings `lemma6b1_runs_M3_exc?_linux`), `compare_macm3.txt`, `compare_json.txt`, `in/macm3_ref/` (macm3's logs and JSONs used for the comparison, blobs in `in_blobs_macm3_ref.txt`). Python-flint 0.9.0, FLINT 3.6.0, Python 3.14.10, numpy 2.5.4 (macm3: Python 3.14.3).
