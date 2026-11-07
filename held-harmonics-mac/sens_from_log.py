import json, re
OUT = '/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/43f19197-40d3-4ad8-aa26-db5322fa8689/scratchpad/held_harmonics/'
rows, cur = [], None
for line in open(OUT + 'sens.log'):
    m = re.match(r'(\S+\.npz): D (\S+) newton_q', line)
    if m:
        cur = dict(state=m.group(1), D=m.group(2), sens={}, h={}, delta='0', piv=[0, 0])
        rows.append(cur)
        continue
    m = re.match(r'\s+k\s+(\d+): h = \((\S+), (\S+)\)\s+dDelta/dh = \((\S+), (\S+)\)', line)
    if m:
        k = m.group(1)
        cur['h'][k + 'a'], cur['h'][k + 'b'] = float(m.group(2)), float(m.group(3))
        cur['sens'][k + 'a'], cur['sens'][k + 'b'] = float(m.group(4)), float(m.group(5))
json.dump(rows, open(OUT + 'sens_prelim.json', 'w'), indent=1)
print(len(rows), [r['D'] for r in rows])
