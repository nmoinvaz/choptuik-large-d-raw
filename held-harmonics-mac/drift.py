import sys
sys.path.insert(0, '/Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-a28bee1f4ff612f8d/hp')
import mpmath as mp
from held_fit import load, coeffs_of, KS, KEYS
from pinning import HeldFit
R = '/Users/nathan/Source/choptuik-large-d-raw/'
H = '/Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-a28bee1f4ff612f8d/hp/data/'
fits = {d: HeldFit(H + f) for d, f in ((6, 'held_fit_d6.json'), (8, 'held_fit.json'), (10, 'held_fit_d10.json'))}
for st in ['anm-mac/run_trend_pin3_qd3/anm_pin3_D79.7657.npz', 'anm-mac/run_trend_pin3_qd9/anm_pin3_D85.7473.npz',
           'T110-win/chain/anm_pin3_D100.1184.npz', 'T116-win2/chain/anm_pin3_D149.5559.npz', 'T129-win2/chain4/anm_pin3_D200.2746.npz']:
    D, z, m, dl = load(R + st)
    c = coeffs_of(z)
    out = []
    for d, hf in fits.items():
        h = dict(zip(KEYS, [v for ab in hf.values(D, KS) for v in ab]))
        out.append((d, h))
    print(f'{mp.nstr(D, 8)}: chain 5a {c["5a"]:+.6e} 5b {c["5b"]:+.6e} | ' + ' | '.join(
        f'deg{d}: 5a {h["5a"]:+.6e} 5b {h["5b"]:+.6e} 7a {h["7a"]:+.4e} 13a {h["13a"]:+.3e}' for d, h in out) + f' | chain 7a {c["7a"]:+.4e} 13a {c["13a"]:+.3e}')
