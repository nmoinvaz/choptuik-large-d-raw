import sys, os, numpy as np
sys.path.insert(0, "D:/choptuik-i1080x2/solver/inner_stokes")
import inner_nb; inner_nb.install()
import hier as H
A,wf,B3,C3,B5,C5=[float(t) for t in sys.argv[1].split(",")]
k=int(sys.argv[2]); r=float(sys.argv[3])
for h in [0]+[s*10.0**e for e in range(-9,0) for s in (1,-1)]:
    x=np.array([A,wf,B3,C3,B5,C5]); x[k]+=h
    R=H.demixed_multi(x,5,[r])[r]
    print(f"h {h:+.0e}  r1 {R[0]:+.4e}{R[1]:+.4e}i  r3 {R[2]:+.4e}{R[3]:+.4e}i  r5 {R[4]:+.4e}{R[5]:+.4e}i")
