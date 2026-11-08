#!/usr/bin/env python3
"""Compare one round of the I177 loop (amplitude copies on Python 3.14) with #161's hash (issue #177).

    python compare_amp.py ROUND [ROOT]   ROOT defaults to the folder of this file. Prints and writes round<k>/compare.txt and
                                         appends a line to rounds.csv. Exit 0: every copy exited 0, has a JSON, and hashes to
                                         REF_HASH. Exit 1: an anomaly (a crash, a missing JSON, a traceback, a different hash,
                                         copies that differ), listed with the first differing entry against #146's round 1.
                                         Exit 2: the reference itself does not hash to REF_HASH, so nothing could be compared.
    python compare_amp.py --selftest     a clean round passes; a changed digit, a missing JSON and a non-zero exit are flagged

The hash is I140-win2/compare.py's: SHA-256 of the JSON without its timing keys."""
import csv, datetime as dt, glob, json, os, re, shutil, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(RAW, "I140-win2"))
import compare as C

REF_HASH = "fd6b5ef2f90d4f559a1a1ab68a7e85fe7c9b8538cc7e50ac41d2fb5510eb47d8"
REF_JSON = os.path.join(RAW, "I146-win2", "round1", "amp_copy1.json")
EXIT = re.compile(r"^([^ ]+) exit ([0-9]+) wall ([0-9]+)s")


def check(root, k, out=print):
    d = os.path.join(root, f"round{k}")
    bad, hashes, codes = [], {}, {}
    ex = os.path.join(d, "exits.txt")
    names = []
    if os.path.exists(ex):
        for line in open(ex).read().splitlines():
            m = EXIT.match(line)
            if m:
                names.append(m.group(1))
                codes[m.group(1)] = int(m.group(2))
                if m.group(2) != "0":
                    bad.append(f"{m.group(1)} exit {m.group(2)}")
    else:
        bad.append("no exits.txt")
    ref_obj = C.canon(REF_JSON)[0]
    for n in sorted(set(names) | {os.path.basename(p)[:-5] for p in glob.glob(os.path.join(d, "amp_copy*.json"))}):
        p = os.path.join(d, n + ".json")
        if not os.path.exists(p):
            out(f"  {n:12s} NO JSON")
            bad.append(f"{n}: no JSON (crash?)")
            continue
        obj, h, _ = C.canon(p)
        hashes[n] = h
        out(f"  {n:12s} {h}")
        if h != REF_HASH:
            bad.append(f"{n}: hash differs from #161's; first differing entry {C.first_diff(ref_obj, obj)}")
    if len(set(hashes.values())) > 1:
        bad.append("copies differ within the round")
    for f in sorted(glob.glob(os.path.join(d, "*.log"))):
        if "Traceback" in open(f, errors="replace").read():
            bad.append(f"{os.path.basename(f)} holds a traceback")
    return hashes, codes, bad


def main(k, root):
    if C.canon(REF_JSON)[1] != REF_HASH:
        print("exit 2: the reference JSON does not hash to REF_HASH")
        return 2
    lines = []
    out = lambda s: (print(s), lines.append(s))
    out(f"round {k} compare at {dt.datetime.now(dt.timezone.utc):%Y-%m-%d %H:%M:%S} UTC")
    hashes, codes, bad = check(root, k, out)
    d = os.path.join(root, f"round{k}")
    out("anomalies: " + ("; ".join(bad) if bad else "none"))
    with open(os.path.join(d, "compare.txt"), "w") as f:
        f.write("\n".join(lines) + "\n")
    path = os.path.join(root, "rounds.csv")
    new = not os.path.exists(path)
    with open(path, "a", newline="") as f:
        w = csv.writer(f)
        if new:
            w.writerow(["round", "utc", "copies", "exit0", "anomalies", "hash16"])
        w.writerow([k, dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d %H:%M:%S"), len(hashes),
                    sum(1 for c in codes.values() if c == 0), "; ".join(bad) or "none",
                    ",".join(sorted({h[:16] for h in hashes.values()}))])
    return 1 if bad else 0


def mutate_digit(o):
    """change the last digit of the first string that holds a digit; True when one was changed"""
    items = list(o.items()) if isinstance(o, dict) else list(enumerate(o)) if isinstance(o, list) else []
    for key, v in items:
        if isinstance(v, str) and re.search("[0-9]", v):
            i = max(j for j, ch in enumerate(v) if ch.isdigit())
            o[key] = v[:i] + str((int(v[i]) + 1) % 10) + v[i + 1:]
            return True
        if mutate_digit(v):
            return True
    return False


def selftest():
    tmp = tempfile.mkdtemp()
    try:
        def make(k, mut=False, drop=False, code=0):
            d = os.path.join(tmp, f"round{k}")
            os.makedirs(d)
            with open(os.path.join(d, "exits.txt"), "w") as ex:
                for i in (1, 2, 3):
                    obj = json.load(open(REF_JSON))
                    if i == 2 and mut:
                        assert mutate_digit(obj)
                    if not (i == 3 and drop):
                        json.dump(obj, open(os.path.join(d, f"amp_copy{i}.json"), "w"))
                    ex.write(f"amp_copy{i} exit {code if i == 1 else 0} wall 1s\n")
        make(1)
        make(2, mut=True)
        make(3, drop=True)
        make(4, code=9)
        res = {k: check(tmp, k, lambda s: None)[2] for k in (1, 2, 3, 4)}
        ok = (res[1] == [] and any("hash differs" in b for b in res[2]) and any("no JSON" in b for b in res[3])
              and any("exit 9" in b for b in res[4]))
        print("selftest", "ok" if ok else f"FAILED {res}")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    return 0 if ok else 1


if __name__ == "__main__":
    if sys.argv[1:] == ["--selftest"]:
        sys.exit(selftest())
    sys.exit(main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else HERE))
