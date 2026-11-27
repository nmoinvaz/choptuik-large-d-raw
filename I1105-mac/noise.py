import sys, numpy as np
sys.path.insert(0, ".")
import i1105_u0 as U
z = np.load(sys.argv[1]); D, kc = 23.0, 135
S0 = U.make(kc, D, z); base = S0.freeze_from(z, 0.7)
def h(u0):
    Sh = U.make(kc, D, z, u0=u0); return Sh.freeze_from(z, 0.7)[U.hkey(Sh)]
def last(zz, u0, eps_steps=0):
    S = U.make(kc, D, zz, u0=u0)
    st = {k: v for k, v in base.items() if k != U.hkey(S0)}; st[U.hkey(S)] = h(u0) + eps_steps
    S.steps_map = st
    return U.last_block(S, S.residual(zz[None])[0])
for seed in [None, 1, 2, 3, 4]:
    zz = z.copy()
    if seed is not None:
        r = np.random.default_rng(seed); zz[:-1] = z[:-1] * (1 + 1e-16 * r.standard_normal(len(z) - 1))
    d02 = np.linalg.norm(last(zz, 0.02) - last(zz, 0.04)); d03 = np.linalg.norm(last(zz, 0.03) - last(zz, 0.04))
    print(f"seed {seed}: |dz|/|z| {np.linalg.norm(zz - z) / np.linalg.norm(z):.1e}  dF_last(0.02) {d02:.4e}  dF_last(0.03) {d03:.4e}", flush=True)
