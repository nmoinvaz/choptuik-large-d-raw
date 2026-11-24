import json,sys,numpy as np
rows=[json.loads(l) for l in open(sys.argv[1])]
r=sys.argv[2]; lev=int(sys.argv[3])
B=sorted(set(x["B5"] for x in rows)); C=sorted(set(x["C5"] for x in rows))
Z=np.full((len(B),len(C)),np.nan)
for x in rows:
    if isinstance(x["R"],dict):
        v=x["R"][r]; i=lev-1 if lev>1 else 0
        Z[B.index(x["B5"]),C.index(x["C5"])]=np.log10(np.hypot(v[i],v[i+1]))
print("rows B5, cols C5 from",C[0],"to",C[-1],": log10|r_%d| at %s"%(lev,r))
step=int(sys.argv[4]) if len(sys.argv)>4 else 2
for i in range(0,len(B),step):
    print("%6.2f "%B[i]+" ".join("%3.0f"%z if np.isfinite(z) else "nan" for z in Z[i,::step]))
k=np.nanargmin(Z); print("min", np.nanmin(Z), "at B5 %.3f C5 %.3f"%(B[k//len(C)],C[k%len(C)]))
