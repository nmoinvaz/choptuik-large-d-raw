"""#1024: each rpi5 log and record of this folder against the Mac's of the same run (I992-mac, I1017-mac, I1019-mac of the raw-data repository).
    python3 compare1024.py MAC_RAW_DIR [--mutate] [--list]   # --list prints every differing numeric leaf      # MAC_RAW_DIR = a checkout of choptuik-large-d-raw holding the three folders
Text logs: line by line with timings masked ("[12.3 s]", "(104 s)", "about N s", "(N s)"); a differing line is printed with both texts.
Records (.jsonl, .json): leaf by leaf (key 'sec' skipped); equal strings pass, otherwise the largest relative difference of the numbers is reported
(strings of digits are parsed with mpmath at 80 digits). --mutate changes one printed digit in the rpi5 disc_ray log and one float of the rpi5
p2c_disc_ray.jsonl by 1e-12 relative: both must be reported as differences."""
import json, os, re, sys
import mpmath as mp
mp.mp.dps = 80
HERE = os.path.dirname(os.path.abspath(__file__)); MAC = sys.argv[1]; MUT = "--mutate" in sys.argv; LIST = "--list" in sys.argv
LOGS = [  # (rpi5 log, Mac log)
    ("disc_checkint", "I992-mac/p2c_disc_checkint.log"), ("disc_ray", "I992-mac/p2c_disc_ray.log"),
    ("disc_K1_toolarge", "I992-mac/p2c_disc_K1_toolarge.log"), ("disc_K2_sign", "I992-mac/p2c_disc_K2_sign.log"),
    ("disc_all_infl2", "I992-mac/p2c_disc_all_infl2.log"),
    ("h8_centre", "I1017-mac/logs/centre.log"), ("h8_centre_mut_A", "I1017-mac/logs/centre_mut_A.log"),
    ("h8_d0_0", "I1017-mac/logs/box_d0_0.log"), ("h8_d0_1e7", "I1017-mac/logs/box_d0_1e7.log"),
    ("b5_model", "I1019-mac/b5/logs/model.log"), ("b5_phiz", "I1019-mac/b5/logs/phiz.log"),
    ("b5_phiz_mut_G0", "I1019-mac/b5/logs/phiz_mut_G0.log"), ("b5_residual", "I1019-mac/b5/logs/residual.log"),
    ("b5_residual_mut_offphi", "I1019-mac/b5/logs/residual_mut_offphi.log"),
    ("b5_sector_box_nr32_na64", "I1019-mac/b5/logs/sector_box.log")]
RECS = [("p2c_disc_ray.jsonl", "I992-mac/p2c_disc_ray.jsonl"), ("p2c_disc_all_infl2.jsonl", "I992-mac/p2c_disc_all_infl2.jsonl"),
        ("p2c_disc_11-0_r16.jsonl", "I992-mac/p2c_disc_11-0_r16.jsonl"), ("p2c_disc_ray_mut_sign.jsonl", "I992-mac/p2c_disc_ray_mut_sign.jsonl"),
        ("p2c_h8_d0_0.json", "I1017-mac/p2c_h8_d0_0.json"), ("p2c_h8_d0_1e7.json", "I1017-mac/p2c_h8_d0_1e7.json"),
        ("p2c_b5_box_nr32_na64.json", "I1019-mac/b5/p2c_b5_box_nr32_na64.json")]
MASK = [re.compile(p) for p in (r"\[\d+(\.\d+)? s\]", r"\(\d+ s\)", r"\d+ s\)", r"\(\d+ cells, \d+ s\)", r"records \S+")]  # timings and the output path


def mask(t):
    for m in MASK:
        t = m.sub("<t>", t)
    return t


def num(x):
    try:
        return mp.mpf(x) if isinstance(x, str) else mp.mpf(float(x))
    except Exception:
        return None


def leaves(o, path=""):
    if isinstance(o, dict):
        for k, v in o.items():
            if k != "sec":
                yield from leaves(v, f"{path}/{k}")
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from leaves(v, f"{path}[{i}]")
    else:
        yield path, o


def load(p):
    t = open(p).read()
    try:
        return [json.loads(t)]
    except ValueError:
        return [json.loads(l) for l in t.splitlines() if l.strip()]


bad = 0
print("== text logs (timings masked)")
for mine, mac in LOGS:
    a, b = f"{HERE}/logs/{mine}.log", f"{MAC}/{mac}"
    if not (os.path.exists(a) and os.path.exists(b)):
        print(f"{mine}: missing ({'rpi5' if not os.path.exists(a) else 'Mac'} side)"); continue
    ta, tb = mask(open(a).read()).splitlines(), mask(open(b).read()).splitlines()
    if MUT and mine == "disc_ray":                # the control: one printed Lambda digit changed on the rpi5 side
        i = next(i for i, l in enumerate(ta) if "Lambda " in l)
        ta[i] = re.sub(r"(Lambda \d\.)(\d)", lambda m: m.group(1) + str((int(m.group(2)) + 1) % 10), ta[i], count=1)
    diffs = [(i, x, y) for i, (x, y) in enumerate(zip(ta, tb)) if x != y]
    n = len(diffs) + abs(len(ta) - len(tb)); bad += n
    print(f"{mine}: {len(ta)} lines vs {len(tb)}; {n} differ" + ("" if not n else ""))
    for i, x, y in diffs[:6]:
        print(f"   line {i + 1}\n     rpi5: {x[:230]}\n     Mac:  {y[:230]}")
print("== records (leaf by leaf, 'sec' skipped)")
for mine, mac in RECS:
    a, b = f"{HERE}/{mine}", f"{MAC}/{mac}"
    if not (os.path.exists(a) and os.path.exists(b)):
        print(f"{mine}: missing ({'rpi5' if not os.path.exists(a) else 'Mac'} side)"); continue
    ra, rb = load(a), load(b)
    ndiff = nstr = 0; worst = mp.mpf(0); first = None
    if len(ra) != len(rb):
        print(f"{mine}: {len(ra)} records vs {len(rb)}"); bad += 1; continue
    for k, (x, y) in enumerate(zip(ra, rb)):
        lx, ly = dict(leaves(x)), dict(leaves(y))
        if MUT and k == 0 and mine == "p2c_disc_ray.jsonl":   # the control: one float of the rpi5 side moved by 1e-12 relative
            key = next(p for p, v in lx.items() if isinstance(v, float) and v != 0); lx[key] = lx[key] * (1 + 1e-12)
        for p in sorted(set(lx) | set(ly)):
            u, v = lx.get(p), ly.get(p)
            if u == v:
                continue
            nu, nv = num(u), num(v)
            if nu is not None and nv is not None and nv != 0:
                r = abs(nu - nv) / abs(nv)
                if r > worst:
                    worst, first = r, (k, p, u, v)
                ndiff += 1
                if LIST:
                    print(f"   {mine} record {k} (j {x.get('j')}, k {x.get('k')}) {p}: rpi5 {u} Mac {v} rel {mp.nstr(r, 3)}")
            else:
                nstr += 1; first = first or (k, p, u, v)
    bad += ndiff + nstr
    print(f"{mine}: {len(ra)} records; leaves that differ: {ndiff} numeric (largest relative {mp.nstr(worst, 3)}), {nstr} other"
          + (f"; e.g. record {first[0]} {first[1]}: rpi5 {str(first[2])[:60]} vs Mac {str(first[3])[:60]}" if first else ""))
print(f"TOTAL differing: {bad}")
