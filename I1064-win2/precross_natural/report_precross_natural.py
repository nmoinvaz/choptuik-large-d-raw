#!/usr/bin/env python3
"""report_precross_natural.py [DIR]: #1064's precross_natural arm on win2 (the precross rungs with --od_accept natural): for each of the two states (D 260.0073 and D 259.4568 of leg 10 of ks_chain3b), the ks 293 control and the ks 315 rung:
the gate's verdict, the start |F| (the first |F| of the log's step 0 line, octo-double max|F| of the base at that order), the octo-double steps, the last octo-double Newton line's max|F|,
the seconds, how the run stopped. Beside them: the start |F| at order 315 of dh610's D 261.0721 (I1064-dh610/ks315.log) and of D 261.6229 (../ks315.log, the first arm), read from those files.
The coordinator's reading (fixed before the runs): a rung that converges under natural means the chain can rerun from that state at order 315 with the natural test for the raise; both failing means neither test carries the raise from a start of about 1e-11.
(The own test's run of the same state is read from ../precross/D<D>_ks315.log and printed beside.)"""
import glob
import json
import os
import re
import sys

H = (sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.abspath(__file__))).replace("\\", "/").rstrip("/") + "/"
RAW = "D:/choptuik-large-d-raw-push/"
STEP = re.compile(r"^\s+on (\d+): \|F\| ([0-9.eE+-]+)(?: -> ([0-9.eE+-]+))?")
LAST = re.compile(r"octo-double Newton: (\d+) steps, max\|F\| ([0-9.eE+-]+|nan|inf), (not converged|converged)")


def read(path):
    return open(path, errors="replace").read() if os.path.exists(path) else None


def info(path):
    t = read(path)
    if t is None:
        return None
    steps = [m for m in (STEP.match(x) for x in t.splitlines()) if m]
    last = LAST.findall(t)
    stop = [x.strip() for x in t.splitlines() if re.match(r"^\s+on \d+: ", x) and ("stopping" in x or "converged" in x)]
    return dict(start=steps[0].group(2) if steps else None, nsteps=len(steps), last=last[-1] if last else None, stop=stop[-1] if stop else None)


def first_start(path):
    i = info(path)
    return i["start"] if i else None


exits = read(H + "exits_1064.txt") or ""
summ = read(H + "summary_1064.txt") or ""


def run(N):
    m = re.search(r"1064 %s exit (\S+) \(want 0\) wall (\d+) s capped (\d)" % re.escape(N), exits)
    g = read(H + "gate_%s.txt" % N)
    rc = read(H + "gate_rc_%s.txt" % N)
    i = info(H + N + ".log")
    return dict(exit=m.group(1) if m else None, wall=int(m.group(2)) if m else None, capped=m.group(3) if m else None,
                gate=(g or "").strip(), ok=(rc or "").strip() == "0", ran=i is not None and m is not None, i=i)


print("| state | order | exit, wall | gate | start max\\|F\\| (step 0) | od steps | last od line max\\|F\\| | how it stopped |")
print("|---|---|---|---|---|---|---|---|")
res = {}
for D in ("260.0073", "259.4568"):
    for K in (293, 315):
        N = "D%s_ks%d" % (D, K)
        r = run(N)
        res[(D, K)] = r
        if not r["ran"]:
            print("| D %s | %d | not run | | | | | |" % (D, K))
            continue
        i = r["i"]
        print("| D %s | %d | exit %s, %d s%s | %s | %s | %d | %s | %s |" % (
            D, K, r["exit"], r["wall"], ", CAPPED" if r["capped"] == "1" else "", "converged" if r["ok"] else "failed",
            i["start"] or "no step line", i["nsteps"], ("%s, %s" % (i["last"][1], i["last"][2])) if i["last"] else "no od Newton line",
            (i["stop"] or "")[:110]))
print()
print("gate lines:")
for D in ("260.0073", "259.4568"):
    for K in (293, 315):
        r = res[(D, K)]
        if r["ran"]:
            print("- D %s ks %d: %s" % (D, K, r["gate"]))
print("the own test's run of the same state (../precross, information):")
for D in ("260.0073", "259.4568"):
    o = info(H + "../precross/D%s_ks315.log" % D)
    n = res[(D, 315)]["i"]
    if o:
        print("- D %s: own: start %s, %d od steps, last od line %s, stop: %s" % (D, o["start"], o["nsteps"], ("%s, %s" % (o["last"][1], o["last"][2])) if o["last"] else "none", (o["stop"] or "")[:90]))
    if n:
        print("  D %s: natural: start %s, %d od steps, last od line %s" % (D, n["start"], n["nsteps"], ("%s, %s" % (n["last"][1], n["last"][2])) if n["last"] else "none"))
print()
ref = [("D 261.0721 (dh610's ks 315, `I1064-dh610/ks315.log`)", first_start(RAW + "I1064-dh610/ks315.log")),
       ("D 261.0721 (dh610's ks 295, `I1064-dh610/ks295.log`; the figure in the hc)", first_start(RAW + "I1064-dh610/ks295.log")),
       ("D 261.6229 (the first arm on win2, `../ks315.log`)", first_start(H + "../ks315.log"))]
print("start max|F| at order 315 for comparison:")
for k, v in ref:
    print("- %s: %s" % (k, v))
print()
conv = [D for D in ("260.0073", "259.4568") if res[(D, 315)]["ran"] and res[(D, 315)]["ok"]]
ran = [D for D in ("260.0073", "259.4568") if res[(D, 315)]["ran"]]
if conv:
    print("READING: ks 315 converged under natural from D %s: the chain can rerun from that state at order 315 with the natural test for the raise (the coordinator's reading)" % ", D ".join(conv))
if ran and not conv:
    print("READING: no ks 315 converged under natural: neither test carries the raise from a start of about 1e-11 (the coordinator's reading; the own test failed at both states in ../precross)")
if not ran:
    print("READING: no ks 315 rung ran (a control did not converge)")
missing = [D for D in ("260.0073", "259.4568") if not res[(D, 293)]["ok"]]
if missing:
    print("CONTROL: the ks 293 control did not converge at D %s" % ", D ".join(missing))
print()
print("delta information (Delta(b) - Delta(a)):")
for f in sorted(glob.glob(H + "delta1064_*.json")):
    j = json.load(open(f))
    print("- %s: %s (same D %s, ok %s)" % (os.path.basename(f)[9:-5], j.get("change"), j.get("same_D"), j.get("ok")))
for line in summ.splitlines():
    if line.startswith("delta1064_"):
        print("  " + line[:200])
