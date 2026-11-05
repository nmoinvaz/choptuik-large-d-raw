import glob, json, numpy as np
R='/Users/nathan/Source/choptuik-large-d-raw/'; H='/Users/nathan/Source/choptuik-large-d/hp/data/states/'
for p in [H+'up13_D60.0020.npz', R+'T13-win/scratch/t13/up17_D60.9618.npz', R+'T73/t73/full1_D67.7422.npz']:
    d=np.load(p); m=json.loads(str(d['meta']))
    print(p, json.dumps(m)[:1500]); print()
