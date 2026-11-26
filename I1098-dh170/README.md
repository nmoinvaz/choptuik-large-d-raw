# I1098-dh170: the fastmul6 kernel built for the Skylake instruction set, and dh170's ladder point (#1098)

Machine: dh170 (Fedora, i7-7700, 8 threads, 31 GB; a #1025 lane runs beside). Issue:
https://github.com/nmoinvaz/choptuik-large-d/issues/1098

- `fastmul6_sky/`: dh610's cross-build of wip/large-d-fastmul6 at e1cd7a84 with -C target-cpu=skylake. The wheel's sha256
  is 9c4d41e97df63f3f867997e28cbf626af8e152525111e61b8b001f455b18ffef, and it has no GFNI instructions. Its AVX-512 code
  sits only in multidouble's runtime-dispatched SIMD backend. It is installed into site_sky by `install_sky.sh`, with
  the Python of f398e829, and checked here. All six checks exit 0 with the same figures as dh610's and mm5's builds:
  - relaxed_build_check: 4.53e-57, control 3.69e-05
  - recip_check: D 300 and D 1000, step-plan change 0, controls 1.72e-36 and 5.06e-37
  - dmat_check: 5.21e-6 and 2.72e-6, controls 1.0
  - taylor_mp_check: 1.1e-124, control 2.36e-31
- The ladder point D 1549 (ladder_point2.sh, kc 230, kmax 31, KSBAR 1e-70, 6 threads) started after the checks, at
  19:00 UTC. That first run (install_sky.sh) stopped at its ks gate on the gate's parse bug.
- `ladder/restart1549.sh` (unit i1088a-ladder1549b) restarted it at 19:43 UTC with the fixed ladder_point2.sh (raw blob
  651bb75f), keeping the converged jump. The gate chose ks 2941 (an octo-double residual change of 1.39e-101 at ks 3141).
  - It runs h5..h11 and h13 at M 32 only (STOP_AFTER=rls13). The h13 state goes to raw, and the M 48 tail h13..h31 runs
    on mm5 from it.
- **The D 1549 run's commit field.** The jump (in `jump/`) was run by the first script, which passed a hard-coded
  --commit 478e9d86. The restarted stages pass COMMIT=f398e829. The Python every stage runs is f398e829's (hp_y from that
  commit's archive), and the kernel is the Skylake wheel of e1cd7a84 (d368a0c0's Rust). So the jump's records name
  478e9d86 where they mean f398e829.
  - f398e829 makes the inner held solves take chord steps by default (--inner_chord 1, from e1cd7a84). The point
    converges to the same 1e-48 tolerance as D 432-1291, though not to the same bits. The ladder record will give
    f398e829.
- **D 519 machine check** (`ladder/after1549.sh`, unit i1088a-d519x). It starts when D 1549's unit ends. It runs D 519's
  Moebius M 32 tail (ladder_tail.sh mob, ks 1196, kmax 23, 6 threads) from mm5's h13 state, to compare with mm5's tail
  (I1098-mm5/ladder/D519/tail_mob).
  - What differs: the machine (dh170's i7-7700 against mm5's M5 Pro) and the kernel's build (the Skylake wheel of
    e1cd7a84 against mm5's native build). The Python is f398e829 against 478e9d86. With --inner_chord 0 (below) their
    release_ls takes the same path: their form_s.py differ only in the chord option and a rewritten floor test with
    the same logic.
  - What the two runs share: the kernel source (d368a0c0's Rust), the input state
    (I1098-mm5/ladder/D519/rls/release_ls_h13_D519.0000.npz, blob b5a40765, the same blob as `inputs/D519_rls_h13.npz`
    here), ladder_tail.sh (sha256 12055ac1..., I1098-mac-a/tools), and its settings.
  - So a difference measures the machine and the build together.
- **h13 chord-free, and the D 519 check too.** mm5's D 747 on f398e829 stopped at h13 outer 1. Its qq inner solve with
  chord steps reached 1.75e-45 in 10 steps against tol 1e-48, where the chord-free solves of D 519 and 622 reached about
  1e-77 in 4.
  - Unit i1088a-d519x was stopped before it ran anything. `ladder/restart1549c.sh` (unit i1088a-r1549c, started 20:06
    UTC) takes both jobs.
  - It waits for D 1549's h5-h11 release to end and stops i1088a-ladder1549b. It moves the half-begun rls13/ to
    rls13_<UTC time> and runs h13 at M 32 with --inner_chord 0 and --commit f398e829 (I1098-mac-a/tools/
    ladder_from_h11.sh, blob 780ba729, STOP_AFTER=rls13). Then it runs the D 519 check with --inner_chord 0.
  - The h5-h11 stage keeps its chord steps (tol 1e-36). The h13 inner system re-solves every unknown below harmonic 13
    to 1e-48, so that state serves only as the starting point.
- `ladder/D1549/` and `ladder/D519x/`: the run folders (dh170's out/ladder), copied here and pushed at each stage's end
  by `push_ladder.sh` (unit i1088a-push1549) from a sparse worktree of dh170's raw clone. The runs themselves write
  outside this repository (--allow_unraw); later points write into their raw folder directly.
