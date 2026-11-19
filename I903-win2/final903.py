# glue (read only, no computation): the accepted re-seeds of ks_chain2 since its restart on venv-i962 (leg 1 at ks 291 with --reseed_qd_bar 1e-21, leg 3 at ks 299 with 1e-15) from their
# anm_run.log and anm_run.jsonl: per accepted state the attempt's a, the quad-double polish (steps, |R|), the refinement's rung max|R| (first, last, maximum over its corrections), the re-seed
# and corrector wall, the octo-double steps, the exact Delta of the saved state and the p_min of its base. usage (raw repository root): python -I I903-win2/final903.py > I903-win2/final903.txt
import glob, json, os, re, datetime
import numpy as np
from mpmath import mp, mpf
mp.dps = 60
K = ['zh', 'zl', 'z2', 'z3', 'z4', 'z5', 'z6', 'z7']
LEGS = (('ks 291, bar 1e-21', 'I903-win2/ks_chain2/leg01_D238.1789_ks291/'), ('ks 299, bar 1e-15', 'I903-win2/ks_chain2/leg03_D242.0000_ks299/'))
for tag, leg in LEGS:
    rows = [json.loads(l) for l in open(leg + 'anm_run.jsonl')]
    pmin = {round(float(r['D0_str']), 4): r['pivots'][0] for r in rows}
    ok_att = []
    for r in rows:
        for a in r['attempts']:
            rs = a.get('reseed') or {}
            if rs.get('ok') and a['accepted']:
                pre = rs['rungs'][0]
                ok_att.append((round(a['D'], 4), a['a'], pre['its'], pre['R'], rs['seconds'], a['steps'], a['t_corr']))
    ref = []
    cur = None
    for l in open(leg + 'anm_run.log', errors='replace'):
        if 're-seeded (ok)' in l:
            cur = []
        m = re.search(r'refined in octo-double, rung max\|R\| (.*)$', l)
        if m and cur is not None:
            cur = [float(x) for x in m.group(1).split(' -> ')]
        if re.match(r'\s+a [\d.]+ -> D .*stall accepted', l) and cur is not None:
            ref.append(cur)
            cur = None
        elif re.match(r'\s+a [\d.]+ -> D ', l):
            cur = None
    print('=====', tag, '|', len(ok_att), 'accepted re-seeds,', len(ref), 'refinement lists')
    print('D | a | polish steps, |R| | refinement first, last, max | re-seed s | od steps | corrector s | saved UTC | Delta | p_min of base')
    for i, (D, a, its, R, rsec, st, tc) in enumerate(ok_att):
        f = glob.glob(leg + 'anm_pin3_D%.4f.npz' % D)
        d = t = ''
        if f:
            z = np.load(f[0], allow_pickle=True)
            d = mp.nstr(sum(mpf(float(z[k][-1])) for k in K), 30)
            t = datetime.datetime.fromtimestamp(os.path.getmtime(f[0]), datetime.timezone.utc).strftime('%H:%M:%S')
        rf = ref[i] if i < len(ref) else []
        rfs = ('%.2e, %.2e, %.2e' % (rf[0], rf[-1], max(rf))) if rf else 'n/a'
        print('%.4f | %.4f | %d, %.2e | %s | %.0f | %d | %.0f | %s | %s | %s' % (D, a, its, R, rfs, rsec, st, tc, t, d, ('%.4e' % pmin[D]) if D in pmin else 'not written'))
