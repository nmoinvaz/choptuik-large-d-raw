"""#1080 control walk: does zero_mp.py's walk from the fundamental's M = 3 zero end 'located' at Theorem A(5)'s box centre?

    python3 control_check.py control_walk.log control_walk.jsonl     exit 0 iff the log's verdict is 'located' and the last row's (A, wf) is within 1e-10 of
                                                                     (2.71857918921174, 0.999228403206568) in each coordinate
    python3 control_check.py selftest                                planted logs and rows: the pass case and three mutations (NOT located, A 2e-10 off,
                                                                     no verdict line), each of which must exit 1

The point is the last row's (A, wf) (the point zero_mp's 'located' line prints); the step it did not apply is printed beside it."""
import json
import re
import sys

TARGET = (2.71857918921174, 0.999228403206568)
TOL = 1e-10


def check(log_text, rows):
    verdicts = [l for l in log_text.splitlines() if re.match(r"(NOT )?located:", l)]
    if len(verdicts) != 1 or not rows:
        return 1, f"verdict lines {len(verdicts)}, rows {len(rows)}: no verdict"
    last = rows[-1]
    dA, dw = last["A"] - TARGET[0], last["wf"] - TARGET[1]
    near = abs(dA) <= TOL and abs(dw) <= TOL
    located = verdicts[0].startswith("located:")
    msg = (f"{verdicts[0].split(':')[0]}; last point A {last['A']!r} wf {last['wf']!r}, minus the target ({dA:+.3e}, {dw:+.3e}) (bar {TOL:g} each); "
           f"unapplied step ({last['dA']:+.2e}, {last['dwf']:+.2e}); |R|/sigma_mp {last['R_over_sig']:.2e}; iterations {len(rows)}")
    return (0 if located and near else 1), msg


def selftest():
    row = dict(A=TARGET[0] + 3e-12, wf=TARGET[1] - 2e-12, dA=1e-13, dwf=-1e-13, R_over_sig=5.0)
    ok_log = "it 0: ...\nlocated: A 2.7 wf 0.99 ...\n"
    cases = {"pass": (ok_log, [row], 0),
             "not_located": (ok_log.replace("located:", "NOT located:"), [row], 1),
             "A_2e-10_off": (ok_log, [dict(row, A=TARGET[0] + 2e-10)], 1),
             "no_verdict": ("it 0: ...\n", [row], 1)}
    res = {k: check(t, r)[0] == want for k, (t, r, want) in cases.items()}
    print("selftest: " + ", ".join(f"{k} {'PASS' if v else 'FAIL'}" for k, v in res.items()))
    return 0 if all(res.values()) else 1


if __name__ == "__main__":
    if sys.argv[1:2] == ["selftest"]:
        sys.exit(selftest())
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(2)
    rc, msg = check(open(sys.argv[1]).read(), [json.loads(l) for l in open(sys.argv[2]) if l.strip()])
    print(msg)
    print("PASS" if rc == 0 else "FAIL")
    sys.exit(rc)
