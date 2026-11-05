"""The real data through exactly the planted path (planted.CANDS, forms.evaluate, the same splits): per candidate the
best full-fit max |r|/sigma, Dinf (centre +- half-range over fit choices: a spread over fit choices), Delta(3) likewise,
the free-n_s range, and the held-out maxima H1 (D > 45), H2 (D < 3.1), H3 (D = 5, 6, 8; and the M48 thin points in
units of their estimated error). Writes real.json; G5 is printed at the end with the plants' values.

    python3 real.py
"""
import json, time
import numpy as np
import common as C, forms as F
from planted import CANDS, D, H, L, s, TH

def main():
    T0 = time.time(); out = dict(cands={})
    for cn, lst in CANDS.items():
        rows = [dict(choice=str(ch), kw=dict(kw), **F.evaluate(fn, D, H, L, s, ch, thin=TH, **kw)) for fn, ch, kw in lst]
        full = [r['full'] for r in rows if 'error' not in r['full']]
        g = {}
        for key in ('Dinf', 'D3'):
            v = [r[key] for r in full if r.get(key) is not None]
            if v: g[key] = dict(centre=(min(v) + max(v)) / 2, half=(max(v) - min(v)) / 2)
        fr = [r['full']['ns'] for r, (fn, ch, kw) in zip(rows, lst) if kw.get('free')]
        if fr: g['ns_free'] = (min(fr), max(fr))
        g['best_full_maxrs'] = min(r['maxrs'] for r in full)
        for h in ('H1', 'H2', 'H3'):
            hv = [r[h]['max'] for r in rows if h in r and 'max' in r[h]]
            if hv: g['best' + h] = min(hv)
        tv = [r['H3']['thin_maxrs'] for r in rows if 'H3' in r and 'thin_maxrs' in r['H3']]
        if tv: g['bestH3thinrs'] = min(tv)
        out['cands'][cn] = dict(grade=g, rows=rows)
        line = f"real {cn:7s} Dinf {g['Dinf']['centre']:.11f} +- {g['Dinf']['half']:.1e}"
        if 'D3' in g and cn.startswith('Z-'): line += f" D3 {g['D3']['centre']:.4f} +- {g['D3']['half']:.4f}"
        if 'ns_free' in g: line += f" ns {g['ns_free'][0]:.2f}..{g['ns_free'][1]:.2f}"
        line += f" | best H1 {g['bestH1']:.1e}" + (f" H2 {g['bestH2']:.1e}" if 'bestH2' in g else '')
        line += (f" H3 {g['bestH3']:.1e} thin/sigma {g['bestH3thinrs']:.1e}" if 'bestH3' in g else '')
        print(line + f" | full max|r|/s {g['best_full_maxrs']:.1e}  ({time.time() - T0:.0f} s)", flush=True)
    json.dump(out, open('real.json', 'w'), indent=1, default=str)
    # G5: N-poly best H1 / W-poly (and Z-poly) best H1, real against each plant
    print('G5  A = best H1 of N-poly / best H1 of W-poly (and / Z-poly):')
    for pn in ('P0', 'Pe', 'P7', 'P8', 'Pz'):
        try: J = json.load(open(f'planted_{pn}.json'))['cands']
        except FileNotFoundError: continue
        a = J['N-poly']['grade']['bestH1'] / J['W-poly']['grade']['bestH1']
        b = J['N-poly']['grade']['bestH1'] / J['Z-poly']['grade']['bestH1'] if 'Z-poly' in J else float('nan')
        print(f'  {pn}: A_W = {a:.1f}  A_Z = {b:.1f}')
    g = out['cands']
    print(f"  real: A_W = {g['N-poly']['grade']['bestH1'] / g['W-poly']['grade']['bestH1']:.1f}"
          f"  A_Z = {g['N-poly']['grade']['bestH1'] / g['Z-poly']['grade']['bestH1']:.1f}")

if __name__ == '__main__':
    main()
