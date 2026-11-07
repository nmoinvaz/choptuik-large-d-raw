import sys
sys.path.insert(0, '/Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-a28bee1f4ff612f8d/hp')
import numpy as np
from held_fit import full_states
R = '/Users/nathan/Source/choptuik-large-d-raw/'
pts = [r for r in full_states(R) if r['D'] >= float(sys.argv[1])]
n = np.array([float(r['D']) - 2 for r in pts])
x = 1 / n
for key in ('11a', '11b', '13a', '13b'):
    y = np.sqrt(n) * np.array([r['c'][key] for r in pts])
    for deg in (4, 8):
        c = np.polynomial.chebyshev.Chebyshev.fit(x, y, deg)
        res = (y - c(x))
        idx = np.argsort(-np.abs(res))[:6]
        print(key, deg, 'median |res| (sqrt n units)', f'{np.median(np.abs(res)):.1e}', 'worst:',
              ', '.join(f'{float(pts[i]["D"]):.3f} {pts[i]["kind"]} {res[i]:+.1e}' for i in idx))
