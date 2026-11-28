# I1109-macm3: stage 1c roots of #1109 by Rust block 12 (R0 control, w01, w10) on macm3

Machine: macm3 (MacBook Air M3, 8 threads, 24 GB), runner t5-macm3, account claude-me2, started 2026-11-28 06:18 UTC.
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1109 (stage 1c, comments from 7232733432 on).
Order: the coordinator's hc task t5 (2026-11-28 06:18 UTC). Budget 6 of 8 threads, nice 10.
Git over SSH and gh do not work on this Mac (Keychain locked over SSH): code and raw inputs by anonymous HTTPS fetch, nothing pushed,
no gh; the coordinator pushes and posts from the bundle and the post file.

Code: worktree ~/Source/choptuik-ell1fast at 693a4d79 (wip/i1101-weakdir), work from solver/matter.
Venv: ~/Source/venv-macm3-1058b (Python 3.14.3, numpy 2.5.4, scipy 1.18.1, mpmath 1.3.0, multidouble 5.1.0 with dd_logdet, maturin 1.16.0).
Raw inputs: choptuik-large-d-raw main c16a07b6 (worktree ~/Source/choptuik-large-d-raw-1109, sparse), blobs checked with
git hash-object --no-filters: R0 = I1101-dh170/in/sol_l1kc127k070w2_D23.0000.npy (90d3e655) and l1kc127k070w2.jsonl (d1a3a641);
w01 = I1109-mm5/c/sol_w01_D23.0000.npy (458d9026) and .jsonl (3410f1e5); w10 = I1109-mm5/c/sol_w10_D23.0000.npy (9947a645) and .jsonl (eb52631f).

## Step 1: ellrs (block 12 in Rust)

With the venv active and cargo on PATH: ellrs/build.sh (prints "ellrs <isa> <products>"), then with OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1:
- python ell_b12rs.py selftest (exit 0)
- python ell_b12rs.py selftest --mutate=nolam (exit 1)
- python ell_b12rs.py selftest --mutate=harm (exit 1)
- python ell_b12rs.py check <raw>/I1102-mac/in/l1kc31r1025.jsonl <raw>/I1102-mac/in/sol_l1kc31r1025_D10.5000.npy 10.5 2.87 --threads=2 --controls=1
  (exit 0: 15010 of 15010 bit for bit, both controls FAIL)
Any other outcome: stop and report.

## Step 2: the roots

OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 RAYON_NUM_THREADS=2, three at once, each detached (nohup), 14400 s cap each:
- python d18_secant.py run <R0 jsonl> <R0 npy> 23.0 0.0440 0.0470 r0.jsonl --tol=1e-6 --maxev=20 --b12=rust --b12_threads=2 --pin=90d3e655,d1a3a641
- python d18_secant.py run <w01 jsonl> <w01 npy> 23.0 0.0400 0.0500 w01.jsonl --tol=1e-6 --maxev=20 --b12=rust --b12_threads=2
- python d18_secant.py run <w10 jsonl> <w10 npy> 23.0 0.0350 0.0550 w10.jsonl --tol=1e-6 --maxev=20 --b12=rust --b12_threads=2
Exit 2 (an end not robust, or no sign change): widen that bracket once by 2x about its centre and say so.

Bars (written before the runs):
1. Control: r0's root within 1e-5 of mm5's refined 0.0455917189 (#1109 comment 7233613794, stage 1c2 B, --b12=rust);
   otherwise stop the other two and report.
2. Report w01's and w10's roots and root - root(r0). For reading: w01 moved Delta by -1.957e-4 and w10 by -1.956e-3
   along R0's weak vector; w01 keeps R0's 4179 steps, w10 has 4182.

## Log
- 2026-11-28 06:26 UTC: README written, before step 1's checks and the roots.
- 2026-11-28 06:25 UTC: ellrs/build.sh in venv-macm3-1058b (cargo from ~/.cargo/bin): "ellrs neon accelerate" (maturin build 17 s).
- 2026-11-28 06:26-06:27 UTC step 1 (OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1, caffeinate -is nice -n 10; logs selftest*.log, check_kc31.log):
  selftest exit 0 (3666 of 3666 entries bit for bit); selftest --mutate=nolam exit 1 (0 of 3666, FAIL); selftest --mutate=harm exit 1 (0 of 3666, FAIL);
  check kc31 (D 10.5, lambda 2.87, --threads=2 --controls=1) exit 0: 15010 of 15010 entries bit for bit, Rust 2.27 s against DDEll 22.5 s, controls nolam and harm 0 of 15010 FAIL.
- 2026-11-28 06:27:28 UTC step 2 launched, detached by common/launch_1070.py (double fork, from the #1025 runs: a copy), each through run_case.sh
  (caffeinate -is nice -n 10, common/capped_run.py 14400 s, RAYON_NUM_THREADS=2): r0 (0.0440, 0.0470, --pin=90d3e655,d1a3a641, pins matched),
  w01 (0.0400, 0.0500), w10 (0.0350, 0.0550). Records r0.jsonl, w01.jsonl, w10.jsonl, stdout r0.out, w01.out, w10.out, exit codes r0.exit, w01.exit, w10.exit.
  All three print the record system at start: |F| 3.1959e-10 / 3.1878e-10 / 3.1673e-10, steps 4179 / 4179 / 4182.
- 2026-11-28 07:24:50 UTC r0 ended exit 0 (status tol, 6 evaluations, 3435 s): bracket [0.045591589325629484, 0.045592089325629484], det-linear root 0.04559171900836614; bar 1 PASS (+1.0837e-10 from 0.0455917189).
- 2026-11-28 07:31:51 UTC w10 ended exit 4 (nonrobust, 7 evaluations, 3858 s); 07:35:21 UTC w01 ended exit 4 (nonrobust, 8 evaluations, 4067 s). No exit 2, no bracket widened.
  Roots and shifts: roots_summary.txt (python3 roots_summary.py; --selftest passes). RSS sample 9 min in: 2.8 to 3.0 GiB per process; 532 to 625 s per evaluation with three at once.
- Files: r0/w01/w10 .jsonl (records), .out (stdout), .exit (exit code), selftest*.log, check_kc31.log, run_case.sh, wait_r0.sh, common/, roots_summary.py/.txt, make_post.py, post_started.md, post_result.md.

## Stage 1e: nonlinear elimination at k_c 127, D 23.0 (t5's order, 2026-11-28 07:38 UTC; written 2026-11-28 07:39 UTC before the run)

The linear estimate says R0's discrete zero along its weak vector lies at dDelta -0.0196 and would move lambda_1 by about -0.015.
Test it with #1105's nonlinear elimination at k_c 127, D 23.0 (at D 16 it found the zero receding). Same worktree (693a4d79), venv, budget (6 threads, nice 10).
1. OPENBLAS_NUM_THREADS=6 VECLIB_MAXIMUM_THREADS=6, detached (common/launch_1070.py), 21600 s cap (common/capped_run.py), run_ne.sh:
   python i1101_weakdir.py ne <R0 jsonl> <R0 npy> 23.0 <this folder>/ne/ --outer=6
   (fresh J and SVD per outer step, Gauss-Newton step on the weak vector at fractions 1 to 1/8, re-frozen steps and chord steps on the strong band;
   stops when an outer step cuts |U_w^T F| by less than 2x; every iterate saved with a stub record.)
2. Then the root of the last saved iterate (Rust block 12, RAYON_NUM_THREADS=2, 14400 s cap):
   python d18_secant.py run <iterate jsonl> <iterate npy> 23.0 LO HI ne_root.jsonl --tol=1e-6 --maxev=20 --b12=rust --b12_threads=2
   with (LO, HI) = (0.0455917 + 0.785 dDelta) -+ 0.004, dDelta of that iterate against R0 (the linear slope), widened once by 2x on exit 2.
Bars (the order's, written before the run): report per outer step |U_w^T F|, Delta, dDelta from R0, |F|, steps, seconds. Reading:
(a) |U_w^T F| falls at least 2x per step to <= 1e-12: the zero is reachable; its root is the k_c 127 root at the discrete zero; compare root - 0.0455917 with -0.785 x dDelta.
(b) it stops (the elimination's rule): the zero recedes, as at D 16; report the last iterate's root as the root along the valley at that dDelta.
Either way, post via files, bundle, report to t5.
- 2026-11-28 07:39:05-08:00:46 UTC stage 1e step 1 (ne.out, ne/): exit 0, 1301 s, stopped by the elimination's rule at outer 1 (|U_w^T F| 1.0453e-10 -> 1.0420e-10, less than 2x): reading (b).
  Saved iterate ne/sol_ne1_D23.0000.{npy,jsonl} (fraction 0.125 taken, |F| 3.1513e-10, 4183 steps). dDelta from R0 = -2.4468301010811544e-3 (z[-1] of the two npy files).
- 2026-11-28 08:01 UTC step 2: bracket centre 0.0455917 + 0.785 dDelta = 0.043670938370651294, LO 0.0396709, HI 0.0476709 (+-0.004, rounded to 7 decimals); run_case.sh ne_root LO HI <ne jsonl> <ne npy> (same flags as r0), records ne_root.jsonl.
- 2026-11-28 08:01:33-08:33:45 UTC step 2 (ne_root.out, ne_root.jsonl): exit 4 (nonrobust last point, dln 2.54), 6 evaluations, 1922 s, det-linear root 0.04031747487157126,
  robust bracket [0.0396709, 0.04032159856405092]; root - 0.0455917 = -5.2742e-3 against +0.785 dDelta = -1.9208e-3 (the order's text has -0.785 dDelta: sign noted in post_1e.md). Reading (b).
- 2026-11-28 08:35 UTC files added: ne.out, ne/ (sol_ne1_D23.0000.{npy,jsonl}), ne.exit, ne_root.{out,jsonl,exit}, run_ne.sh, ne_summary.py (--selftest passes) and ne_summary.txt, make_post_1e.py, post_1e.md.
