import json
OUT = '/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/43f19197-40d3-4ad8-aa26-db5322fa8689/scratchpad/held_harmonics/'
q = [r for r in json.load(open(OUT + 'sens_chain.json')) if float(r['D']) < 190]
o = [r for r in json.load(open(OUT + 'sens_octo.json')) if float(r['D']) > 190]
json.dump(q + o, open(OUT + 'sens_all.json', 'w'), indent=1)
print([(r['state'], r['piv']) for r in q + o])
