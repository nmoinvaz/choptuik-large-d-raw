import re, math, sys
fam=None; d={}
for line in open('table_1b.md'):
    m=re.match(r'\*\*k_c (\d+)\*\*',line)
    if m: fam=int(m.group(1)); d[fam]={}; continue
    m=re.match(r'\| ([\d.]+) \|.*\*\*([+-][\d.e+-]+)\*\* \|',line)
    if m and fam: d[fam][float(m.group(1))]=float(m.group(2))
print({k:len(v) for k,v in d.items()})
def pair(a,b):
    for D in sorted(set(d[a])&set(d[b])):
        x,y=d[a][D],d[b][D]
        print(f"k{a} vs k{b} D {D}: {x:+.4e} {y:+.4e} ratio |{b}|/|{a}| {abs(y)/abs(x):.3f} diff {100*(abs(y)-abs(x))/abs(x):+.1f}%")
pair(31,47); pair(47,55)
for k in (31,47):
    Ds=sorted(d[k])
    print('k',k,'orders/unit D between consecutive scanned D:')
    for a,b in zip(Ds,Ds[1:]):
        print(f"  {a}->{b}: {(math.log10(abs(d[k][b]))-math.log10(abs(d[k][a])))/(b-a):.2f}")
    below=[D for D in Ds if abs(d[k][D])<=1e-6]; above=[D for D in Ds if abs(d[k][D])>1e-6]
    lo,hi=max(below),min(above)
    x=lo+(hi-lo)*(-6-math.log10(abs(d[k][lo])))/(math.log10(abs(d[k][hi]))-math.log10(abs(d[k][lo])))
    print(f"  k{k}: last below {lo}, first above {hi}, log-linear 1e-6 crossing D {x:.2f}")
