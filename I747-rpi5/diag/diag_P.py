# diagnostics on the planted-truth control only (point masses at REF541), no scan plant
import sys
sys.path.insert(0, "/home/nathan/Source/choptuik-large-d-747/solver/inner_amp")
import pade_far_poles as PF
ss, mp, pg, KS = PF.ss, PF.mp, PF.pg, PF.KS
wf = 1.0
node = PF.FNode(wf)
ref = ss.REF541[wf]
pts = [ref[k] for k in KS]
print("REF541", [f"{complex(p):.4f}" for p in pts])
# 1: pure poles, no main (exact rational): sigma_k = (1/3) sum t^k/k!
mom = PF.pole_moments(pts)
sig = [m / mom[0] for m in mom]
pl = PF.poles(sig, wf)
print("pure 3 point masses, no main:", {k: f"{pl[k]['dist']:.2e}" for k in KS})
# 2: main + point masses, large rungs
for kind in ("chord2",):
    main = node.mains[kind]
    w = PF.pole_part(main, pts)
    for eta in (1, 3, 10, 30, 100, 1e3, 1e4, 1e6):
        sig, info = ss.make_plant(main, w, eta, 0)
        pl = PF.poles(sig, wf)
        print(f"{kind} eta_P {eta:g}: d_8,9,10 = " + ", ".join(f"{pl[k]['dist']:.4f}" for k in KS)
              + f"; fit_resid {info['fit_resid']:.1e} M {info['M']}; share22 {info['share'][22]:.2f}")
# 3: one point mass at a time, eta_P = 1
main = node.mains["chord2"]
for j, k0 in enumerate(KS):
    w = PF.pole_part(main, [pts[j]])
    for eta in (1e-2, 1):
        sig, info = ss.make_plant(main, w, eta, 0)
        pl = PF.poles(sig, wf)
        print(f"single mass at REF541[{k0}] eta {eta:g}: d_8,9,10 to ITS OWN place " + ", ".join(
            f"{abs(pl[k]['nearest']-pts[j]) if False else 0:.0f}" for k in KS) if False else "", end="")
        import mpmath
        sig2 = sig
        with mp.workdps(pg.DPS_PADE):
            s = [mp.mpc(z) for z in sig2[:PF.N23]]
            out = []
            for k in KS:
                a = [mp.factorial(i) * s[i] for i in range(2*k+1)]
                _, q = mp.pade(a, k, k)
                us = mp.polyroots(q[::-1], maxsteps=500, extraprec=2*mp.mp.prec)
                ts = [complex(1/u) for u in us]
                out.append(min(abs(t - complex(pts[j])) for t in ts))
        print(f"single mass at REF541[{k0}] eta {eta:g}: distance of [8/8],[9/9],[10/10]'s nearest pole to it: " + ", ".join(f"{x:.4f}" for x in out))
