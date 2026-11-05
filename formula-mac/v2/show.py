# Print the per-choice rows of a planted_<P>.json or real.json: full max|r|/s, hi/lo residual, Dinf, D3, ns, H1/H2/H3.
import json, sys
J = json.load(open(sys.argv[1])); cands = sys.argv[2].split(',') if len(sys.argv) > 2 else None
tr = J.get('truth', {}); print('truth', {k: v for k, v in tr.items() if k != 'poles_D'})
f = lambda v, fmt='.1e': ('%' + fmt) % v if isinstance(v, (int, float)) else str(v)
for cn, c in J['cands'].items():
    if cands and cn not in cands: continue
    for r in c['rows']:
        fu = r['full']
        if 'error' in fu: print(cn, r['choice'], r['kw'], 'ERROR', fu['error']); continue
        Dinf = fu['Dinf'] - (tr['Dinf'] if tr else 0.0)
        line = (f"{cn:7s} {r['choice']:10s} {str(r['kw']):16s} max|r|/s {f(fu['maxrs'])} hi {f(fu['maxr_hi'])} lo {f(fu.get('maxr_lo'))}"
                f" chi2 {f(fu['chi2dof'])} Dinf{'-true' if tr else ''} {Dinf:+.2e} D3 {f(fu.get('D3'), '.4f')} ns {f(fu.get('ns'), '.2f')}")
        for h in ('H1', 'H2', 'H3'):
            if h in r: line += f" {h} {f(r[h].get('max'))}" + (f"/{f(r[h].get('thin_max'))}" if h == 'H3' else '')
        print(line)
