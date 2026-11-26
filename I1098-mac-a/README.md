# I1098-mac-a: the per-point error budget of full form-S solves (Delta to 20 digits, part 1)

Machine: the Mac (macOS, M-series laptop, 2 threads at nice 10). Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1098

- `budget300/`: D 300's full solve (I1088-dh610/out/rls300/release_ls_h13_D300.0000.npz, u horizon, ks 306, kc 146,
  kt 36, 78 Taylor steps, kfreeze 13) re-solved with one discretization parameter changed (`variant_state.py`: every
  Taylor step halved, ks + 200, kc + 20, kt + 8), each by `form_s.py release_ls --harm 13 --kmax 13` from the full
  state (the inner held solves re-converge everything but harmonic 13 under the new discretization, the outer step
  harmonic 13), the octo-double residual, tol 1e-48, tol_h 1e-44 (`run_budget300.sh`); Delta's change against the
  base re-solve.
  Results so far: base (released at once, |F| 5.4e-50): Delta 1.678171015400871567732214178494; steps2 (5 outer steps
  to |F| 1.7e-61): 1.678171015400871567781806556988, the halved steps' change +4.96e-20.
- `resample_m.py`: a form-S state resampled from M to M' collocation points by each field's trigonometric series (odd
  fields p1, p, m, m_h; even c0, c), checked by a round trip 32 -> 48 -> 32 that reproduces the state exactly.
- `m48_300/` (running): mm5's kfree-31 state (I1098-mm5/kfree300) resampled to M 48 (residual there 1.9e-17: centre
  block 1.9e-17, steps about 1e-18, horizon 1.1e-17) and re-converged at M 48 (`run_m48_300.sh`, the dev-o1 kernel of
  b9a2954b, which instantiates form S at M 48).
- `gainq.py`: Delta's gain with the quad-double Jacobian solved in quad-double, for the residual bound.
  ks+200 (ks 306 -> 506, the u horizon): released in 4 outer steps, Delta -2.63e-23 from the base. kc+20 and kt+8 ran on
  dh610 (I1098-dh610 budget300): both released at once (target 5.4e-50 and 1.2e-49), no change at 1e-48.
- `m48_300/`, `m48_300b/`: the M 48 re-solve of mm5's kfree-31 state (resampled; 1.9e-17 at M 48), qd then qq
  (`m48_300b` restarts from m48_300's outer-1 state with the trial-acceptance fix dfccf920): released at |F| 1.9e-65;
  Delta 1.678171015400871524283476024308, -7.59e-25 from M 32's 1.678171015400871524283476783790; the Hamiltonian
  check's a rows 2.4e-26 at M 48 against 1.06e-20 at M 32 (kfree 31).
- `cont360/`, `cont360b/`: D 300 -> 360 by `release_joint` from guesses (linear in 1/n from D 250 and 300; interpolated
  from D 300 and 400), both stopped: the inner held solve at the guess's harmonics 5-25 stalled (1.5e-6 at a damped
  step, then 4.4e-10 at full steps with Delta swinging by 2.5e-4, `heldsolve.py`).
- `gains/gains.log`: Delta's gain of the full systems (`gainq.py`): D 1000 (rls1000h13q) 3.30e22, so its record's
  |F| 5.4e-43 is a first-order bound of 1.8e-20.
- `budget.py`, `extrap_state.py`, `heldsolve.py`: the direct full-system Newton (it stalls, the full system being
  near-singular along the free top harmonic), the guess by 1/n, the held solve step by step.
- `tools/variant_state.py`, `tools/horizon300.sh`: the variant-state tool, with the hp directory as its first argument
  so that it runs on any machine, and the D 300 horizon runs on the fastmul5 kernel (f350aa62). The runs are u
  ks + 200 and ks + 400; Moebius ks 800; a 16 and a 4, each at ks 600 and ks 800; and Moebius with the relaxed products
  off. Each starts from one of mm5's wave-1 states (I1098-mm5/fix).
