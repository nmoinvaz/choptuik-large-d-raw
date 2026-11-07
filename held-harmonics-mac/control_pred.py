import sys
sys.path.insert(0, '/Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-a28bee1f4ff612f8d/hp')
import mpmath as mp
from pinning import HeldFit
H = '/Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-a28bee1f4ff612f8d/hp/data/'
OUT = '/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/43f19197-40d3-4ad8-aa26-db5322fa8689/scratchpad/held_harmonics/'
good, bad = HeldFit(H + 'held_fit_deg8.json'), HeldFit(OUT + 'fit_wrong5.json')
D0, D1 = mp.mpf('73.0'), mp.mpf('73.8108651627')
s73 = {'5a': 8.4896e-03, '5b': 7.1471e-03}
ig, ib = good.increment(D0, D1, [5])[0], bad.increment(D0, D1, [5])[0]
d = [ib[0] - ig[0], ib[1] - ig[1]]
print('increment good', [mp.nstr(v, 6) for v in ig], 'wrong - good', [mp.nstr(v, 4) for v in d])
print('predicted control bias s(73) . dh =', mp.nstr(s73['5a'] * d[0] + s73['5b'] * d[1], 4))
