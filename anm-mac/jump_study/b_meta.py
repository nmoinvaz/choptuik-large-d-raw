import glob, json, numpy as np, sys
R='/Users/nathan/Source/choptuik-large-d-raw/'; H='/Users/nathan/Source/choptuik-large-d/hp/data/states/'
fs = sorted(glob.glob(H+'up*_D*.npz'))
fs += sorted(glob.glob(R+'T12-win/scratch/t12/up*_D*.npz'))[:3] + sorted(glob.glob(R+'T13-win/scratch/t13/up*_D*.npz'))[:3]
fs += [R+'T73/t73/full1_D67.7422.npz'] + sorted(glob.glob(R+'T84-mac/pin*_full.npz')) + [R+'T81/conv_pin7_D72.8000_D72.800000.npz', R+'T81/conv_pin5_D73.0000_D73.000000.npz']
for p in fs:
    d=np.load(p); m=json.loads(str(d['meta']))
    keys=list(d.keys())
    short={k:m[k] for k in m if k not in ('hist','segs')}
    print(p.replace(R,'R/').replace(H,'H/'), keys, json.dumps(short)[:400])
