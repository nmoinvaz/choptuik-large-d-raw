# I1098-dh370: the fastmul6 build attempt on dh370 (#1098)

Machine: dh370 (Fedora 45, i7-8700, 12 threads, 31 GB, 8 GB swap; a #1025 lane holds about 6 GB). Issue:
https://github.com/nmoinvaz/choptuik-large-d/issues/1098

- `fastmul6_build/`: the release build of wip/large-d-fastmul6 at e1cd7a84 (`rebuild_y.sh`: the low-memory recipe with 3
  jobs). Started at 16:51:41 UTC and stopped by hand at 16:59:45 UTC, before the #1025 lane could run short of memory.
  Eight minutes into the hpkernel crate its rustc was at 25.0 GB, and available memory fell to 1.7 GB with swap at
  3.2 GB (`mem.log`, every 30 s). The ladder queue behind it (`after_y.sh`: D 622, 747 and 896 by ladder_point2.sh) was
  stopped with it and never ran.
- dh610's fastmul6 wheel (target-cpu=native on an i7-12700) cannot serve here. objdump finds 60 gf2p8affineqb (GFNI)
  instructions in it, which the i7-8700 lacks.
- The D 2828 release on the old kernel (I1088-dh370's rls2828) was stopped at 16:50 UTC on the coordinator's order.
  Its h5, h7 and h9-step states are kept on dh370 in out/rls2828/.
- `fastmul6_sky/`: dh610's Skylake cross-build of fastmul6 (e1cd7a84; wheel sha256 9c4d41e9..., no GFNI; its AVX-512
  code sits only in multidouble's runtime-dispatched SIMD backend), installed into site_sky with the Python of f398e829
  by `install_sky.sh`. All six checks exit 0 with the same figures as dh610's and mm5's builds. The ladder point D 896
  (ladder_point2.sh, kc 200, M 48 tail, kmax 23, KSBAR 1e-64, 6 threads) started after the checks, at 18:58 UTC.
- **The D 896 run's commit field:** ladder_point2.sh (blob ed177006 for the first try, 8e6779cf for the restart at 19:05
  UTC after the ks-gate parse fix) passes a hard-coded --commit 478e9d86. The Python it runs is f398e829's (hp_y from
  that commit's archive), and its kernel is the Skylake wheel of e1cd7a84 (d368a0c0's Rust). So its records name
  478e9d86 where they mean f398e829. f398e829 also makes the inner held solves take chord steps by default
  (--inner_chord 1, e1cd7a84). The points converge to the same 1e-48 tolerance as D 432-1291, though not to the same
  bits. The ladder record will give f398e829.
- **h13 and the tail chord-free.** mm5's D 747 on f398e829 stopped at h13 outer 1. Its qq inner solve with chord steps
  reached 1.75e-45 in 10 steps against tol 1e-48, where the chord-free solves of D 519 and 622 reached about 1e-77 in 4.
  - `ladder/restart896c.sh` (unit i1088a-r896c, started 20:06 UTC) waits for D 896's h5-h11 release to end and stops
    i1088a-ladder896b. It moves the half-begun rls13/ to rls13_<UTC time> and runs h13 and the M 48 tail (kmax 23) with
    --inner_chord 0 and --commit f398e829 (I1098-mac-a/tools/ladder_from_h11.sh, blob 780ba729).
  - With --inner_chord 0, f398e829's release_ls takes the same path as 478e9d86's: their form_s.py differ only in the
    chord option and a rewritten floor test with the same logic.
  - The h5-h11 stage keeps its chord steps (tol 1e-36). The h13 inner system re-solves every unknown below harmonic 13
    to 1e-48, so that state serves only as the starting point.
- `ladder/D896/`: the run folder (dh370's out/ladder/D896), copied here and pushed at each stage's end by
  `push_ladder.sh` from a sparse worktree of dh370's raw clone (unit i1088a-push896 until 20:36 UTC, then
  i1088a-push370, which also takes D519x). The run itself writes outside this repository (--allow_unraw); later points
  write into their raw folder directly.
- **D 519 machine check** (`ladder/d519x_370.sh`, unit i1088a-d519x370, started 20:36 UTC, 5 threads). It moved here
  from dh170's queue on the coordinator's order. It runs D 519's Moebius M 32 tail (ladder_tail.sh mob, ks 1196,
  kmax 23) from mm5's h13 state, chord-free (--inner_chord 0), to compare with mm5's tail
  (I1098-mm5/ladder/D519/tail_mob).
  - It writes into `ladder/D519x/` of a second sparse worktree of dh370's raw clone
    (~/Source/choptuik-large-d-raw-1088a-live, never pulled while a run writes there), without --allow_unraw.
    i1088a-push370 copies it into the push worktree.
  - What differs: the machine (dh370's i7-8700 against mm5's M5 Pro) and the kernel's build (dh610's Skylake wheel of
    e1cd7a84 against mm5's native build). The Python is f398e829 against 478e9d86. With --inner_chord 0 their
    release_ls takes the same path: their form_s.py differ only in the chord option and a rewritten floor test with
    the same logic.
  - What the two runs share: the kernel source (d368a0c0's Rust), the input state
    (I1098-mm5/ladder/D519/rls/release_ls_h13_D519.0000.npz, blob b5a40765, written to `ladder/inputs/` by the job and
    checked by its blob), ladder_tail.sh (sha256 12055ac1..., the version before the inner_chord and k* changes), and
    its settings.
  - So a difference measures the machine and the build together.
