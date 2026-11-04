# Cache the production cleaning (hp/dd_fits_mp.clean, 60 digits, 1/D degree 18, threshold 1e-15) of every
# continuation point D >= 10 into clean_drop.json; common.data() drops those points.
import sys, json, time
sys.dont_write_bytecode = True
sys.path.insert(0, '/Users/nathan/Source/choptuik-large-d/hp')
import dd_fits_mp as F
t = time.time(); pts, _ = F.load_points(); Ds = sorted(d for d in pts if d >= 10)
kept = F.clean(pts, Ds, verbose=True); drop = sorted(set(Ds) - set(kept))
json.dump({'drop': drop, 'n_in': len(Ds), 'n_kept': len(kept)}, open('clean_drop.json', 'w'))
print(len(Ds), 'in', len(kept), 'kept', f'{time.time() - t:.0f} s')
