#!/usr/bin/env python3
"""#1025 D 17 k_c 71 dd check: the cap (10800 s) killed both det processes after their last noise line and before `ell_ddm.py det` wrote its record (detcmd writes the record
after the float64 slogdet, which follows the noise loop). The dd signs are in the logs. This script turns a det log into a record with the keys the readers use
(D, kc, lam, dd, dd_agree, noise, noise_robust, f64_sign = NaN because it did not finish), marked "source": "log". The record is the log's content and nothing else.
usage: det_log_to_jsonl.py LOG D KC OUT   |   det_log_to_jsonl.py selftest   (selftest: planted logs through read_d17_dd.py)"""
import json, math, os, re, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
RX_DD = re.compile(r"lambda (\S+): dd M built in (\d+) s; dd LU signs \[([^\]]*)\], ln\|det\| (\S+) \(spread over variants (\S+)\), (\S+) s per LU")
RX_NZ = re.compile(r"lambda (\S+): relative noise (\S+) on the dd propagator entries: dd signs \[([^\]]*)\]")


def parse(text, D, kc):
    dd, lam, noise = None, None, []
    for line in text.replace("\r", "").splitlines():
        m = RX_DD.search(line)
        if m:
            if dd is not None:
                raise SystemExit("two 'dd LU signs' lines in one log")
            lam = float(m.group(1))
            sg = [float(x) for x in m.group(3).split(",")]
            dd = [dict(sign=s, ln=(float(m.group(4)) if i == 0 else None), sec=None) for i, s in enumerate(sg)]
            continue
        m = RX_NZ.search(line)
        if m:
            if float(m.group(1)) != lam:
                raise SystemExit("a noise line for another lambda")
            noise.append(dict(eps=float(m.group(2)), signs=[float(x) for x in m.group(3).split(",")]))
    if dd is None:
        raise SystemExit("no 'dd LU signs' line in the log")
    return dict(D=D, kc=kc, lam=lam, mutate=None, dd=dd, dd_agree=len({x["sign"] for x in dd}) == 1, f64_sign=float("nan"), f64_ln=float("nan"), noise=noise,
                noise_robust=all(s == dd[0]["sign"] for e in noise for s in e["signs"]), source="log (the record was not written: the cap killed the process after the noise lines)")


def read_with(lo_text, hi_text):
    d = tempfile.mkdtemp(prefix="d17log_")
    fs = []
    for i, t in enumerate((lo_text, hi_text)):
        f = os.path.join(d, f"r{i}.jsonl")
        open(f, "w").write(json.dumps(parse(t, 17.0, 71)) + "\n")
        fs.append(f)
    p = subprocess.run([sys.executable, os.path.join(HERE, "read_d17_dd.py"), fs[0], fs[1]], capture_output=True, text=True)
    return p.stdout.strip().splitlines()[-1], p.returncode


if len(sys.argv) > 1 and sys.argv[1] == "selftest":
    lo = open(os.path.join(HERE, "det_lo.log")).read()
    hi = open(os.path.join(HERE, "det_hi.log")).read()
    flip = lambda t, a, b: (t.replace(a, b) if a in t else sys.exit(f"planted edit '{a}' not found"))
    cases = [("the real logs", lo, hi, "ROOT PASSES"),
             ("a variant of the upper flipped", lo, flip(hi, "dd LU signs [1.0, 1.0, 1.0, 1.0, 1.0]", "dd LU signs [1.0, 1.0, -1.0, 1.0, 1.0]"), "NO READING"),
             ("1e-24 noise flips the lower", flip(lo, "1e-24 on the dd propagator entries: dd signs [-1.0, -1.0]", "1e-24 on the dd propagator entries: dd signs [-1.0, 1.0]"), hi, "NO READING"),
             ("the 1e-24 line of the upper is missing", lo, "\n".join(l for l in hi.splitlines() if "noise 1e-24" not in l), "NO READING"),
             ("upper sign minus (all variants and noise)", lo, hi.replace("1.0", "-1.0"), "NO ROOT"),
             ("lower sign plus (all variants and noise)", lo.replace("-1.0", "1.0"), hi, "NO ROOT"),
             ("lower and upper swapped", hi, lo, "OPPOSITE")]
    bad = 0
    for name, a, b, want in cases:
        got, rc = read_with(a, b)
        ok = got.startswith(want)
        bad += not ok
        print(f"selftest {name}: {got[:72]} (want {want}) {'ok' if ok else 'WRONG'}")
    print("selftest", "passes" if bad == 0 else f"FAILS ({bad} wrong)")
    sys.exit(1 if bad else 0)
rec = parse(open(sys.argv[1]).read(), float(sys.argv[2]), int(sys.argv[3]))
open(sys.argv[4], "a").write(json.dumps(rec) + "\n")
print(f"wrote {sys.argv[4]}: lam {rec['lam']!r}, dd signs {[x['sign'] for x in rec['dd']]}, agree {rec['dd_agree']}, noise {[(e['eps'], e['signs']) for e in rec['noise']]}")
