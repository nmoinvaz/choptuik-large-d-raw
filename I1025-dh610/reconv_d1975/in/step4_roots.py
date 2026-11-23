#!/usr/bin/env python3
"""#1025 reconv_d1975 (dh610) step4_roots.py: reads the printed output of read_lower.py (dh170's, blob 89309d3c) for the step 4 scans.
  step4_roots.py check READ_DH.txt READ_MAC.txt [--mutate]   the reader on the reference rows must give dh170's 1.325410 and macm3's 1.338993 (det-linear, 1e-6); exit 1 otherwise
  step4_roots.py result READ_LIN.txt READ_MAC.txt DZ          both roots (the one robust change of each) beside the references, their difference, the difference per |dz|, beside the before value
  step4_roots.py selftest [--mutate]                          planted texts: a match passes, a root moved by 0.003 fails, the parse reads the planted fields; exit 0 only if all as written
--mutate (check, selftest) widens the bar from 1e-6 to 1e-2, which the 0.003 case must then fail to catch (selftest exits 1)."""
import sys, re

DH, MAC, BEFORE_DZ, BAR = 1.325410, 1.338993, 7.9032e-06, 1e-6
RC = re.compile(r"robust change \((\d\.\d+), (\d\.\d+)\), (.+?), det-linear (\d\.\d+), range \[(\d\.\d+), (\d\.\d+)\]")


def parse(text):
    ch = [dict(lo=float(m[0]), hi=float(m[1]), orient=m[2], det=float(m[3]), r0=float(m[4]), r1=float(m[5])) for m in RC.findall(text)]
    sg = re.search(r"hybrid signs: (.*)", text)
    npts = re.search(r"points (\d+) in", text)
    return dict(changes=ch, signs=sg.group(1).strip() if sg else None, npts=int(npts.group(1)) if npts else None)


def check(tdh, tmac, bar=BAR, shift=0.0):
    a, b = parse(tdh), parse(tmac)
    ok = len(a["changes"]) == 1 and len(b["changes"]) == 1
    if ok:
        ok = abs(a["changes"][0]["det"] - (DH + shift)) <= bar and abs(b["changes"][0]["det"] - (MAC + shift)) <= bar
    return ok, (a["changes"], b["changes"])


def result(tlin, tmac, dz):
    a, b = parse(tlin), parse(tmac)
    out = []
    for name, p in (("linRe", a), ("macRe", b)):
        out.append(f"{name}: points {p['npts']}, hybrid signs {p['signs']}, robust changes {len(p['changes'])}")
        for c in p["changes"]:
            out.append(f"   change ({c['lo']:.3f}, {c['hi']:.3f}), {c['orient']} (as the reader prints it), det-linear {c['det']:.6f}, estimator range [{c['r0']:.6f}, {c['r1']:.6f}]")
    if len(a["changes"]) == 1 and len(b["changes"]) == 1:
        ra, rb = a["changes"][0]["det"], b["changes"][0]["det"]
        out.append(f"reference roots: dh170 {DH:.6f}, macm3 {MAC:.6f}; before: difference {MAC - DH:.6f} at |dz| {BEFORE_DZ:.4e} = {(MAC - DH) / BEFORE_DZ:.0f} per unit")
        out.append(f"linRe {ra:.6f} (minus dh170's {ra - DH:+.6f}); macRe {rb:.6f} (minus macm3's {rb - MAC:+.6f}); macRe minus linRe {rb - ra:+.6f}")
        out.append(f"|dz| {dz:.4e}: difference per unit {(rb - ra) / dz:.0f}; the coordinator's expectation {(MAC - DH) * dz / BEFORE_DZ:.4f}; the ratio of the difference to it {(rb - ra) / ((MAC - DH) * dz / BEFORE_DZ):.2f}")
    else:
        out.append("not exactly one robust change for each state: no root difference is formed")
    return "\n".join(out)


def planted(det, lo=1.320, hi=1.330, extra=""):
    return (f"points 3 in 1.320-1.340; not noise-robust: none\nhybrid signs: 1.320- 1.330+ 1.340+\nrepeated points: none\n"
            f"  robust change ({lo:.3f}, {hi:.3f}), - to +, det-linear {det:.6f}, range [{det - 0.001:.6f}, {det:.6f}]\nrobust changes: 1; touching a non-robust point (not counted): none\n{extra}")


def selftest(mutate):
    bar = 1e-2 if mutate else BAR
    bad = 0
    p = parse(planted(1.325410))
    cases = [("parse reads the change", p["changes"] == [dict(lo=1.32, hi=1.33, orient="- to +", det=1.32541, r0=1.32441, r1=1.32541)] and p["signs"] == "1.320- 1.330+ 1.340+" and p["npts"] == 3, True),
             ("check passes on the reference values", check(planted(DH), planted(MAC, 1.330, 1.340), bar)[0], True),
             ("check passes within 5e-7", check(planted(DH + 5e-7), planted(MAC - 5e-7, 1.330, 1.340), bar)[0], True),
             ("check fails when both roots are moved by 0.003", check(planted(DH + 0.003), planted(MAC + 0.003, 1.330, 1.340), bar)[0], False),
             ("check fails when one root is moved by 0.003", check(planted(DH), planted(MAC + 0.003, 1.330, 1.340), bar)[0], False),
             ("check fails with two changes", check(planted(DH) + planted(DH), planted(MAC, 1.330, 1.340), bar)[0], False),
             ("check fails with no change", check("points 3 in 1.320-1.340\nhybrid signs: 1.320- 1.330- 1.340-\nrobust changes: 0\n", planted(MAC, 1.330, 1.340), bar)[0], False)]
    r = result(planted(1.325410), planted(1.327592), 1.2693059e-06)
    cases.append(("result prints the planted difference +0.002182 and the ratio 1.00", "macRe minus linRe +0.002182" in r and "the ratio of the difference to it 1.00" in r, True))
    cases.append(("result with two changes forms no difference", "no root difference is formed" in result(planted(DH) + planted(DH), planted(MAC), 1e-6), True))
    for name, got, want in cases:
        ok = bool(got) == want
        bad += not ok
        print(f"  {name}: {'yes' if got else 'no'} (wanted {'yes' if want else 'no'}): {'ok' if ok else 'WRONG'}")
    print("selftest" + (" --mutate" if mutate else ""), "FAIL" if bad else "PASS")
    return 1 if bad else 0


if __name__ == "__main__":
    mutate = "--mutate" in sys.argv
    a = [x for x in sys.argv[1:] if not x.startswith("--")]
    if a[0] == "selftest":
        sys.exit(selftest(mutate))
    if a[0] == "check":
        ok, ch = check(open(a[1]).read(), open(a[2]).read(), 1e-2 if mutate else BAR)
        print(("PASS" if ok else "FAIL") + f": the reader on the reference rows: dh170 {ch[0]}, macm3 {ch[1]}; wanted {DH:.6f} and {MAC:.6f} to {1e-2 if mutate else BAR:g}")
        sys.exit(0 if ok else 1)
    if a[0] == "result":
        print(result(open(a[1]).read(), open(a[2]).read(), float(a[3])))
        sys.exit(0)
