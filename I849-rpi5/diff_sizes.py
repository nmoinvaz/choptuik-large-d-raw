import json, re, subprocess, sys
WT = "/home/nathan/Source/choptuik-large-d-849"
D = "solver/proof/lemmas_M_runs/"
FILES = ["fixed_point_M_data_M3", "fixed_point_M_table_M3", "fixed_point_M_table_M5",
         "lemma6_sector_M3_rp0.1_1e-6", "lemma6_sector_M5_rp0.08_1e-6", "lemmaS_scan_M3", "mutations_M"]
TIME = re.compile(r"\(\s*\d+(\.\d+)?\s*s\)|\[\s*\d+(\.\d+)?\s*s\]|\b\d+(\.\d+)? s\b")
def leaves(x, p=""):
    if isinstance(x, dict):
        for k, v in x.items(): yield from leaves(v, p + "/" + k)
    elif isinstance(x, list):
        for i, v in enumerate(x): yield from leaves(v, p + f"[{i}]")
    else: yield p, x
def key(p): return re.sub(r"\[\d+\]", "", p).rsplit("/", 1)[-1]
for f in FILES:
    old = json.loads(subprocess.run(["git", "-C", WT, "show", f"HEAD:{D}{f}.json"], capture_output=True, text=True).stdout)
    new = json.load(open(f"{WT}/{D}{f}.json"))
    a, b = dict(leaves(old)), dict(leaves(new))
    assert a.keys() == b.keys(), (f, "structure differs")
    timing = 0; strchg = []; num = {}; bool_or_flag = []
    for p in a:
        x, y = a[p], b[p]
        if x == y: continue
        k = key(p)
        if k in ("sec", "time", "secs", "wall") : timing += 1; continue
        if isinstance(x, str) and isinstance(y, str):
            if TIME.sub("", x) == TIME.sub("", y): timing += 1; continue
            strchg.append(p); continue
        if isinstance(x, bool) or isinstance(y, bool): bool_or_flag.append((p, x, y)); continue
        if isinstance(x, (int, float)) and isinstance(y, (int, float)):
            rel = abs(x - y) / max(abs(x), abs(y), 1e-300)
            if k not in num or rel > num[k][0]: num[k] = (rel, x, y, p)
        else: strchg.append(p)
    n = sum(1 for p in a if a[p] != b[p])
    print(f"== {f}: {len(a)} leaves, {n} differ: {timing} timing, {sum(1 for _ in num)} numeric keys, {len(strchg)} other strings, {len(bool_or_flag)} flags")
    for k, (rel, x, y, p) in sorted(num.items(), key=lambda t: -t[1][0]):
        print(f"   {k:14s} max rel diff {rel:.2e}  ({x} -> {y})")
    for p in strchg[:4]: print("   string differs:", p, "|", str(a[p])[:90], "->", str(b[p])[:90])
    for t in bool_or_flag[:4]: print("   flag differs:", t)
