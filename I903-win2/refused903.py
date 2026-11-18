# glue (read only, no computation): the re-seed rung lists of the attempts of leg 0 of ks_chain2 (ks 291) and leg 8 of ks_chain (ks 250) from their anm_run.jsonl, for the
# coordinator's request of 2026-11-18 ~20:30 UTC (#903): for each attempt since D 236.7 the base, its smallest pivot, a, the re-seed's rungs with |R| and whether converged.
# usage (from the raw repository root): python -I I903-win2/refused903.py > I903-win2/refused903.txt
import json, sys
RUNS = (('ks291 leg0', 'I903-win2/ks_chain2/leg00_D232.0000_ks291/anm_run.jsonl'),
        ('ks250 leg8', 'I903-win2/ks_chain/leg08_D232.0000_ks250/anm_run.jsonl'))
def rungs(rs):
    return ["u%.4g:%d its R %.2e %s" % (r['u'], r['its'] or 0, r['R'] if r.get('R') is not None else float('nan'), 'conv' if r.get('conv') else 'NOT')
            for r in rs['rungs']]
for tag, f in RUNS:
    print('=====', tag, '(failed re-seeds)')
    for r in map(json.loads, open(f)):
        if 'attempts' not in r:
            continue
        D0 = float(r['D0_str'])
        if D0 < 236.7:
            continue
        for a in r['attempts']:
            rs = a.get('reseed')
            if not rs or rs['ok']:
                continue
            print("base D %.4f p_min %.4e | a %.4f -> D %.4f | accepted %s od steps %s F_final %.2e | reseed %.0f s"
                  % (D0, r['pivots'][0], a['a'], a['D'], a['accepted'], a['steps'], a['F_final'], rs['seconds']))
            for s in rungs(rs):
                print("     ", s)
    print('=====', tag, '(successful re-seeds from D 236.7: first rung record = the quad-double polish of u 0.3 from the point\'s own data)')
    for r in map(json.loads, open(f)):
        if 'attempts' not in r:
            continue
        D0 = float(r['D0_str'])
        if D0 < 236.7:
            continue
        for a in r['attempts']:
            rs = a.get('reseed')
            if not rs or not rs['ok']:
                continue
            p = rs['rungs'][0]
            print("base D %.4f p_min %.4e | a %.4f -> D %.4f | accepted %s | pre-polish u%.4g: %d its R %.2e %s | reseed %.0f s"
                  % (D0, r['pivots'][0], a['a'], a['D'], a['accepted'], p['u'], p['its'] or 0, p['R'], 'conv' if p.get('conv') else 'NOT', rs['seconds']))
