"""#1080 walk d restart at iteration 1's point: is the float64 M = 5 start on row 0's branch?

    python check_d2_start.py ROW0.jsonl DIRECT.log DIRECT.json PATH20.jsonl PATH40.jsonl PATHMUT.jsonl
    python check_d2_start.py selftest

DIRECT = hier_nb at the new point, started from row 0's harmonics (log, and the solved x [A, w, B3, C3, B5, C5] in full digits);
PATH20, PATH40 = start_path.py from row 0's point to the new point in 20 and 40 steps, from row 0's harmonics; PATHMUT = the
20-step path ending at A + 0.01. Exit 0 iff all four hold:
  C0  the solved (A, w/w_inf) is the new point (row 0's (A + dA, w/w_inf + dw)), bit for bit
  C1  the direct solve's |r_3| and |r_5| are below 1e-6 (#1026's bar)
  C2  the same root: every component of the direct v is within 1e-6 of the 20-step and of the 40-step path's end
  C3  the control: the path that ends 0.01 in A off lands more than 1e-6 from the direct v (it must read as a different point)
The distance of the direct v from row 0's F3 is printed, and is not a criterion."""
import json
import re
import sys

TOL = 1e-6


def last_row(path):
    rows = [json.loads(l) for l in open(path) if l.strip()]
    return rows[-1]


def check(row0, log_text, x, p20, p40, pmut):
    A1, w1 = row0["A"] + float(row0["dA"]), row0["wf"] + float(row0["dwf"])
    v0 = [float(s) for s in row0["F3"]]
    r3 = re.findall(r"F_3/F_1 .*? r_3 ([0-9.eE+-]+)", log_text)
    r5 = re.findall(r"F_5/F_1 .*? r_5 ([0-9.eE+-]+)", log_text)
    v = x[2:6]
    d = lambda a, b: max(abs(s - t) for s, t in zip(a, b))
    res = {"C0": (x[0], x[1]) == (A1, w1),
           "C1": bool(r3 and r5) and float(r3[-1]) < TOL and float(r5[-1]) < TOL,
           "C2": d(v, p20) <= TOL and d(v, p40) <= TOL,
           "C3": d(v, pmut) > TOL}
    msg = (f"point ({A1!r}, {w1!r}); |r_3| {r3[-1] if r3 else None}, |r_5| {r5[-1] if r5 else None}; "
           f"direct v {v}; max|direct - 20-step| {d(v, p20):.2e}, max|direct - 40-step| {d(v, p40):.2e}, "
           f"max|direct - mutated path| {d(v, pmut):.2e}; max|direct - row 0's F3| {d(v, v0):.2e} (not a criterion)")
    return res, msg


def selftest():
    row0 = dict(A=2.7, wf=1.0, dA=-0.004, dwf=-0.01, F3=["0.1", "0.01", "0.008", "0.001"])
    A1, w1 = row0["A"] + row0["dA"], row0["wf"] + row0["dwf"]
    log = "F_3/F_1 = +0.05+0.005i   |.| 0.05  arg +0.09   r_3 3.8e-08\n      F_5/F_1 = +0.003+0.0005i   |.| 0.003  arg +0.17   r_5 2.6e-10\n"
    x = [A1, w1, 0.11, 0.012, 0.0081, 0.0011]
    ok = (log, x, list(x[2:]), list(x[2:]), [0.12, 0.012, 0.0081, 0.0011])
    cases = {"pass": (ok, True),
             "r3_1e-5": ((log.replace("3.8e-08", "1.0e-05"),) + ok[1:], False),
             "other_root": ((log, x, [0.2, 0.012, 0.0081, 0.0011], ok[3], ok[4]), False),
             "control_cannot_fire": ((log, x, ok[2], ok[3], list(x[2:])), False),
             "wrong_point": ((log, [A1 + 1e-9] + x[1:], ok[2], ok[3], ok[4]), False)}
    bad = [k for k, (a, want) in cases.items() if all(check(row0, *a)[0].values()) != want]
    print("selftest: " + ", ".join(f"{k} {'PASS' if k not in bad else 'FAIL'}" for k in cases))
    return 1 if bad else 0


def main():
    if sys.argv[1:2] == ["selftest"]:
        return selftest()
    if len(sys.argv) != 7:
        print(__doc__)
        return 2
    row0 = json.loads(open(sys.argv[1]).readline())
    res, msg = check(row0, open(sys.argv[2]).read(), json.load(open(sys.argv[3])),
                     last_row(sys.argv[4])["v"], last_row(sys.argv[5])["v"], last_row(sys.argv[6])["v"])
    print(msg)
    print(" ".join(f"{k} {'PASS' if v else 'FAIL'}" for k, v in res.items()))
    ok = all(res.values())
    print("PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
