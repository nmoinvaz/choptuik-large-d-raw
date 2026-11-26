# I1098-dh610: the per-point error budget of full form-S solves on dh610 (Delta to 20 digits, part 1)

Machine: dh610 (Fedora 45, i7-12700, 20 threads; 2 threads per run, nice 10). Issue:
https://github.com/nmoinvaz/choptuik-large-d/issues/1098

Each folder is one full solve re-converged with one discretization parameter changed, by `form_s.py release_ls --harm 13
--kmax 13` from a variant state (`variant_state_dh.py`; `run_budget300v.sh`, `run_budget1000.sh`), the octo-double
residual, tol 1e-48; its rls.log ends with "h13's change", Delta's change against the state it started from.

- `budget1000/`: D 1000's full kfree-13 state (I1088-dh610/rls1000h13q; Moebius a 8, ks 1517, kc 200, kt 36, 186 steps).
  base (re-converged from |F| 5.4e-43 to 3.5e-49): -2.050e-23; ks+200, kc+20, kt+8: -2.050e-23 each, the same as the
  base to all digits (no effect); steps2 (all steps halved): -9.673e-23, so -7.62e-23 against the base; steps4 (quarter,
  from steps2's state): running.
- `budget300/`: D 300's full kfree-13 state (I1088-dh610/out/rls300; u horizon, ks 306, kc 146, kt 36, 78 steps). kc+20
  and kt+8: released at once (no change at 1e-48). seg0, seg1, seg2 (one segment's steps halved): +6.3e-26, +4.6e-26,
  +6.1e-26; seg3 (the last segment, 0.6 to x_l = 0.7): +4.959e-20, the whole of the halved-steps change (I1098-mac-a's
  steps2: +4.96e-20). steps4 (quarter steps from steps2's state): -6.227e-20, so the step term does not converge.
  mob8,ks=600 (the Moebius horizon, a 8, ks 600, base steps): Delta 1.678171015400871564600114080598, -3.13e-18 from the
  u horizon's 1.678171015400871567732214178494. mob_mob16, mob_ks=800, mob_steps2, mob_seg3 (from the Moebius state: a
  16, ks 800, halved steps, the last segment halved): running.
- `refine_test.py`, `after_ref.sh`, `rebuild_ref.sh`: the B slaving's refinement count against the residual
  (HP_SLAVE_REFINE_OD, 4a0409b5), on the kernel built into site_r (running).
