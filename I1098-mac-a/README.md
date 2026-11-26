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
