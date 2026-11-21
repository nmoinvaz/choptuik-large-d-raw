#!/usr/bin/env python3
"""#1025 D 17 k_c 71: the verdict of the hybrid row. The pass rules of the README (P4 rules and the outer-grid-point edge rule by raw I1025-mac/d18/d18_check.py,
run as a subprocess) plus the signtest at lambda -/+ 0.02 (both lines agree, opposite signs, lam values as asked, system line same true), then the k_c error.
usage: d17_verdict.py HYBRID.jsonl D SIGNTEST.log D18_CHECK.py PYTHON   |   d17_verdict.py selftest"""
import json, os, subprocess, sys, tempfile
REF63, OFF165 = 2.0399399392, 2.1459968362025212 - 2.1466599631271923    # xfkappa's k_c 63 hybrid root at D 17; D 16.5 hybrid k_c 71 minus k_c 63


def signtest_ok(stlog, lam):
    sysl, sts = None, []
    for l in open(stlog, errors="replace"):
        l = l.strip()
        if l.startswith('{"system_check"'): sysl = json.loads(l)
        elif l.startswith('{"state"'): sts.append(json.loads(l))
    ok = (sysl is not None and bool(sysl.get("same")) and len(sts) == 2 and all(s["agree"] for s in sts)
          and sts[0]["signs"][0] * sts[1]["signs"][0] < 0 and abs(sts[0]["lam"] - (lam - 0.02)) < 1e-9 and abs(sts[1]["lam"] - (lam + 0.02)) < 1e-9)
    return ok, sysl, sts


if sys.argv[1] == "selftest":
    d = tempfile.mkdtemp(prefix="d17st_")
    sysl = '{"system_check": "x", "same": true}'
    def line(l, sg, ag=True): return json.dumps(dict(state="s", lam=l, signs=sg, agree=ag, n_below_1e_12=3, sec=1))
    cases = [("pass", [sysl, line(1.98, [-1, -1, -1, -1]), line(2.02, [1, 1, 1, 1])], True),
             ("same signs", [sysl, line(1.98, [1, 1, 1, 1]), line(2.02, [1, 1, 1, 1])], False),
             ("one line disagrees", [sysl, line(1.98, [-1, 1, -1, -1], False), line(2.02, [1, 1, 1, 1])], False),
             ("wrong lam", [sysl, line(1.90, [-1, -1, -1, -1]), line(2.02, [1, 1, 1, 1])], False),
             ("system line says same false", [sysl.replace("true", "false"), line(1.98, [-1] * 4), line(2.02, [1] * 4)], False),
             ("no system line", [line(1.98, [-1] * 4), line(2.02, [1] * 4)], False), ("one line only", [sysl, line(1.98, [-1] * 4)], False)]
    bad = 0
    for i, (name, ls, want) in enumerate(cases):
        f = os.path.join(d, f"c{i}.log"); open(f, "w").write("\n".join(ls) + "\n")
        got = signtest_ok(f, 2.0)[0]; bad += got != want
        print(f"selftest {name}: {'pass' if got else 'FAIL'} (want {'pass' if want else 'FAIL'}) {'ok' if got == want else 'WRONG'}")
    print("selftest", "passes" if bad == 0 else f"FAILS ({bad} wrong)"); sys.exit(1 if bad else 0)
js, D, stlog, chk, py = sys.argv[1], float(sys.argv[2]), sys.argv[3], sys.argv[4], sys.argv[5]
rec = [json.loads(l) for l in open(js) if l.strip() and abs(json.loads(l)["D"] - D) < 1e-9][-1]
lam = rec["lam"]
p = subprocess.run([py, chk, js, str(D)], capture_output=True, text=True); print(p.stdout.rstrip())
rules = p.returncode == 0
ok_st, sysl, sts = signtest_ok(stlog, lam) if lam is not None else (False, None, [])
print("signtest: " + ("; ".join(f"lam {s['lam']:.9f} signs {s['signs']} agree {s['agree']} ({s['n_below_1e_12']} sv below 1e-12, {s['sec']} s)" for s in sts) if sts else "no result lines")
      + f"; system line same {None if sysl is None else sysl.get('same')} -> {'pass' if ok_st else 'FAIL'}")
print(f"hybrid minus the Mac's float64 record 2.0379024670520076: {lam - rec['lam_record']:+.6e}" if lam is not None else "no root")
if lam is not None:
    print(f"k_c ERROR at D 17: lambda_71(17) - {REF63} = {lam - REF63:+.6e} (D 16.5: {OFF165:+.6e}; the guess assumed -6.6e-4: guess {rec['lam_guess']} -> root minus guess {lam - rec['lam_guess']:+.6e})")
print(f"VERDICT D {D} k_c {rec['kc']}: {'PASS' if rules and ok_st else 'FAIL'} (rules {'pass' if rules else 'FAIL'}, signtest {'pass' if ok_st else 'FAIL'}) lam {lam!r}")
sys.exit(0 if rules and ok_st else 1)
