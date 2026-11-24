import sys, numpy as np
sys.path.insert(0, "D:/choptuik-i1080main/solver/inner_stokes")
import inner_nb; inner_nb.install()
import hier as H
A,wf=3.526473056695715,0.211497981391215
pts={"M3 harmonics, B5=C5=0":[0.9765085452,-0.0017633195,0,0],
     "M3 harmonics, seed B5,C5":[0.9765085452,-0.0017633195,0.026652899,0.003934666],
     "win2 hier stall":[0.976508545,-0.00176332,-0.52,-0.1],
     "continued (t=1)":[1.06489,-0.02329,0.48805,0.01148]}
for k,v in pts.items():
    x=np.array([A,wf]+v); r0=H.demixed_multi(x,5,[0.2])[0.2]
    cols=[]
    for j in (4,5):
        h=1e-6*max(abs(x[j]),1e-3*A); xp=x.copy(); xp[j]+=h; xm=x.copy(); xm[j]-=h
        cols.append((H.demixed_multi(xp,5,[0.2])[0.2]-H.demixed_multi(xm,5,[0.2])[0.2])/(2*h))
    J=np.array(cols).T; s=np.linalg.svd(J[4:6],compute_uv=False)
    print(f"{k:28s} |r3| {np.hypot(*r0[2:4]):.2e} |r5| {np.hypot(*r0[4:6]):.2e}  d r5/d(B5,C5) sv {s[0]:.2e} {s[1]:.2e} cond {s[0]/s[1]:.1e}")
