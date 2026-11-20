import json
J = "C:/Users/nathan/Source/signtest_lowD_1025/I1025-win/signtest_lowD/signtest_lowD.jsonl"
L = "C:/Users/nathan/Source/signtest_lowD_1025/I1025-win/signtest_lowD/signtest_lowD.log"
rs = [json.loads(l) for l in open(J) if l.strip()]
sc = {r["D"]: r for r in rs if "system_check" in r}
st = {}
for r in rs:
    if "state" in r:
        st.setdefault(r["D"], []).append(r)
# row start/end times from the log
import re
t = {}
for l in open(L):
    m = re.match(r"== (\S+ \S+) row D (\S+) k_c (\d+): (PASS|FAIL)", l)
    if m: t[float(m.group(2))] = m.group(1)
    m = re.match(r"== (\S+ \S+) row D (\S+) k_c (\d+): signtest.py", l)
    if m: t[("start", float(m.group(2)))] = m.group(1)
print("| D | k_c | system check (F, record F, steps) | lam - 0.02 | signs | lam + 0.02 | signs | agree | below 1e-12 / 1e-15 | s | verdict |")
print("|---|---|---|---|---|---|---|---|---|---|---|")
for D in sorted(st, reverse=True):
    a, b = st[D]
    c = sc[D]
    sg = lambda r: ", ".join(str(int(x)) for x in r["signs"])
    ok = a["agree"] and b["agree"] and a["signs"][0] != b["signs"][0]
    print(f"| {D:g} | {a['kc']} | F {c['F']:.3e}, record {c['F_record']:.3e}, {c['steps']} = {c['steps_record']} steps, same {str(c['same']).lower()} | {a['lam']:.7f} | {sg(a)} | {b['lam']:.7f} | {sg(b)} | {str(a['agree']).lower()}, {str(b['agree']).lower()} | {a['n_below_1e_12']} / {a['n_below_1e_15']} ; {b['n_below_1e_12']} / {b['n_below_1e_15']} | {a['sec']:.0f}, {b['sec']:.0f} | {'PASS' if ok else 'FAIL'} |")
