#!/usr/bin/env python3
"""Compare one round of the I146 loop with round 1, #140's run and #104 (issue #146).

    python compare_round.py ROUND [ROOT]    ROOT defaults to the folder of this file; ROUND is the round number k.
                                            Prints and writes round<k>/compare.txt; appends a line to rounds.csv.
                                            Exit 0: nothing anomalous. Exit 1: an anomaly (a crash, a missing JSON, copies
                                            that differ, a hash that differs from round 1, #140's or #104's, or a control
                                            that hashes like the copies); the anomaly is listed.
    python compare_round.py --selftest      a planted changed digit in a copy is flagged, a clean round is not

Hashes are compare.py's (SHA-256 of the JSON without timing keys). Per round: the three lemma copies' rho_6a JSON and
stored B, the rp = 0.081 control's JSON and B, and the three amplitude copies' JSON.
"""
import csv, datetime as dt, json, os, re, shutil, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import compare as C

LEMMA = [("l6a_copy%d.json" % i) for i in (1, 2, 3)]
BCOPY = [("B_copy%d.json" % i) for i in (1, 2, 3)]
AMP = [("amp_copy%d.json" % i) for i in (1, 2, 3)]
CTL = ["l6a_control.json", "B_control.json"]


def hashes(d):
    h = {}
    for f in LEMMA + BCOPY + AMP + CTL:
        p = os.path.join(d, f)
        h[f] = C.canon(p)[1] if os.path.exists(p) else None
    return h


def check(root, k, out=print):
    d = os.path.join(root, f"round{k}")
    r1 = os.path.join(root, "round1")
    i140, i104 = os.path.join(root, "..", "I140-win2"), os.path.join(root, "..", "I104-win2")
    h = hashes(d)
    bad = []
    for f, v in h.items():
        out(f"  {f:18s} {v or 'NO JSON'}")
        if v is None:
            bad.append(f"{f}: no JSON (crash?)")
    for name, group in (("lemma copies", LEMMA), ("B copies", BCOPY), ("amp copies", AMP)):
        if len({h[f] for f in group}) > 1:
            bad.append(f"{name} differ within the round")
    # against round 1 (skipped for round 1 itself), #140's round and #104's files
    refs = {"round 1": (r1, "same"), "I140-win2": (i140, "same")}
    for lab, (rd, _) in refs.items():
        if lab == "round 1" and k == 1:
            continue
        rh = hashes(rd)
        for f in LEMMA + BCOPY + AMP + CTL:
            if rh.get(f) is None:
                out(f"  (no {f} in {lab})")
            elif h[f] is not None and h[f] != rh[f]:
                bad.append(f"{f} differs from {lab}")
    for f, ref in (("l6a_copy1.json", "lemma6a_M5_sub1e-18.json"), ("B_copy1.json", "B_M5_sub1e-18.json")):
        p = os.path.join(i104, ref)
        if os.path.exists(p) and h[f] is not None and C.canon(p)[1] != h[f]:
            bad.append(f"{f} differs from I104-win2's {ref}")
    if h["l6a_control.json"] and h["l6a_control.json"] == h["l6a_copy1.json"]:
        bad.append("the rp control's JSON hashes like the copies (comparison cannot fail)")
    ex = os.path.join(d, "exits.txt")
    codes = {}
    if os.path.exists(ex):
        for l in open(ex).read().splitlines():
            m = re.match(r"^(\S+) exit (\d+) wall (\d+)s", l)
            if m:
                codes[m.group(1)] = int(m.group(2))
                if m.group(2) != "0":
                    bad.append(f"{m.group(1)} exit {m.group(2)}")
    for f in sorted(os.listdir(d)):
        if f.endswith(".log") and "Traceback" in open(os.path.join(d, f), errors="replace").read():
            bad.append(f"{f} holds a traceback")
    return h, codes, bad


def main(k, root):
    lines = []
    out = lambda s: (print(s), lines.append(s))
    out(f"round {k} compare at {dt.datetime.now(dt.timezone.utc):%Y-%m-%d %H:%M:%S} UTC")
    h, codes, bad = check(root, k, out)
    d = os.path.join(root, f"round{k}")
    out("anomalies: " + ("; ".join(bad) if bad else "none"))
    with open(os.path.join(d, "compare.txt"), "w") as f:
        f.write("\n".join(lines) + "\n")
    new = not os.path.exists(os.path.join(root, "rounds.csv"))
    with open(os.path.join(root, "rounds.csv"), "a", newline="") as f:
        w = csv.writer(f)
        if new:
            w.writerow(["round", "utc", "processes_exit0", "anomalies", "l6a_hash16", "B_hash16", "amp_hash16",
                        "control_hash16"])
        w.writerow([k, f"{dt.datetime.now(dt.timezone.utc):%Y-%m-%d %H:%M:%S}", sum(v == 0 for v in codes.values()),
                    "; ".join(bad) or "none", (h[LEMMA[0]] or "-")[:16], (h[BCOPY[0]] or "-")[:16],
                    (h[AMP[0]] or "-")[:16], (h["l6a_control.json"] or "-")[:16]])
    return 1 if bad else 0


def selftest():
    root = tempfile.mkdtemp()
    os.makedirs(os.path.join(root, "I140-win2")); os.makedirs(os.path.join(root, "I104-win2"))
    sub = os.path.join(root, "I146-win2"); os.makedirs(sub)
    base = {"M": 5, "sec": 1.0, "rho6a": "[0.2 +/- 1e-9]", "B": [["1.5", "1e-5"]]}
    def write(d, tweak=None):
        os.makedirs(d, exist_ok=True)
        for f in LEMMA + BCOPY + AMP + CTL:
            o = json.loads(json.dumps(base))
            if f.startswith("l6a_control"):
                o["rho6a"] = "[0.3 +/- 1e-9]"
            if tweak and tweak == f:
                o["B"][0][0] = "1.5000000001"
            json.dump(o, open(os.path.join(d, f), "w"))
        open(os.path.join(d, "exits.txt"), "w").write("l6a_copy1 exit 0 wall 5s x\n")
    write(os.path.join(sub, "round1")); write(os.path.join(sub, "round2")); write(os.path.join(root, "I140-win2"))
    for f in ("lemma6a_M5_sub1e-18.json",):
        json.dump(base, open(os.path.join(root, "I104-win2", f), "w"))
    json.dump(base, open(os.path.join(root, "I104-win2", "B_M5_sub1e-18.json"), "w"))
    clean = check(sub, 2, out=lambda s: None)[2]
    write(os.path.join(sub, "round3"), tweak="amp_copy2.json")
    planted = check(sub, 3, out=lambda s: None)[2]
    ok = clean == [] or all("I104" in b for b in clean)
    ok = ok and any("amp_copy2.json" in b for b in planted)
    print("selftest", "ok" if ok else "FAILED", "| clean:", clean[:2], "| planted:", planted[:2])
    shutil.rmtree(root)
    return 0 if ok else 1


if __name__ == "__main__":
    if sys.argv[1:] == ["--selftest"]:
        sys.exit(selftest())
    sys.exit(main(int(sys.argv[1]), sys.argv[2] if len(sys.argv) > 2 else HERE))
