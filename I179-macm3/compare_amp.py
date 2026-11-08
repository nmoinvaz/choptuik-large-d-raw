"""I179-macm3: the amplitude JSON of macm3 against win2's (#140 and #146), by #140's own hash.
    python3 compare_amp.py        (from this folder; imports ../I140-win2/compare.py)
Exit 0: macm3 equals win2's hash and the changed-digit control differs. Exit 1: macm3 differs (first differing entry printed).
Exit 2: the control hashes like the original (the comparison could not fail).
"""
import copy, hashlib, importlib.util, json, os, sys

here = os.path.dirname(os.path.abspath(__file__))
raw = os.path.dirname(here)
spec = importlib.util.spec_from_file_location("i140compare", os.path.join(raw, "I140-win2", "compare.py"))
cmp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cmp)

mine_o, mine_h, dropped = cmp.canon(os.path.join(here, "amp_314_macm3.json"))
print(f"macm3 {mine_h}  dropped keys: {', '.join(dropped)}")
theirs = {}
for lab, p in [(f"I140 copy{i}", os.path.join(raw, "I140-win2", f"amp_copy{i}.json")) for i in (1, 2, 3)] + \
             [(f"I146 round1 copy{i}", os.path.join(raw, "I146-win2", "round1", f"amp_copy{i}.json")) for i in (1, 2, 3)] + \
             [("I161 macm3 py3.13", os.path.join(raw, "I161-macm3", "amp_macm3.json"))]:
    o, h, _ = cmp.canon(p)
    theirs[lab] = (o, h)
    print(f"{lab:20s} {h}   {'EQUAL' if h == mine_h else 'DIFFERS'}")
code = 0 if all(h == mine_h for _, h in theirs.values()) else 1
if code:
    lab = next(l for l, (_, h) in theirs.items() if h != mine_h)
    print("first differing entry against", lab, ":", cmp.first_diff(mine_o, theirs[lab][0]))
# control: change the last digit of the last sigma string (sigma_str is a list of [re, im] strings)
ctl = copy.deepcopy(mine_o)
last = ctl["sigma_str"][-1][1]
assert isinstance(last, str)
ctl["sigma_str"][-1][1] = last[:-1] + ("1" if last[-1] != "1" else "2")
ch = hashlib.sha256(json.dumps(ctl, sort_keys=True).encode()).hexdigest()
print(f"control (last digit of sigma_str[-1][1] changed) {ch}  {'differs from' if ch != mine_h else 'EQUALS'} macm3's hash")
print("first entry where the control differs:", cmp.first_diff(mine_o, ctl))
if ch == mine_h:
    code = 2
print("exit", code)
sys.exit(code)
