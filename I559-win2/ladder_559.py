#!/usr/bin/env python3
"""#559 (ladder_554.py of I554-win2 extended to x_last = 0.94, 0.96, 0.98): the last-node ladder at D 242.36 (layouts 0.3, 0.4, 0.5, 0.6, x_last), raw and equilibrated sigma_1..4 with each one's mode, and where the weakest equilibrated sigma peaks.
usage: python ladder_559.py [--selftest]       (run from I554-win2 after the lane; reads this folder's nn_/eq_ logs (0.94, 0.96, 0.98), ../I554-win2 (0.82 to 0.92), ../I543-win2 (0.74, 0.76, 0.80), ../I537-win2 (0.70, 0.72) and, if present, ../I553-win2 (0.73, 0.75, 0.77, 0.78, 0.79))
Modes. Raw (near_null.py): H3 (delta share < 0.01 and the top component harmonic 3), H1 (top harmonic 1, delta share below 0.9), D (delta share >= 0.9), as in I543-win2/modes_543.py. Equilibrated (near_null_eq.py, Curtis-Reid + Ruiz, section 'J,
Curtis-Reid + Ruiz'): the first 'scaled' top component of the scaled singular vector (block, harmonic) and the share of Delta in the vector in z (D_c v); 'Dz' when that share is >= 0.9.
Acceptance of #554: the weakest equilibrated sigma against x_last tabled with its mode; the x_last where it is largest located to within 0.02 (an interior maximum with both tabulated neighbours within 0.02) or reported at the end of the range (the
largest at 0.92, the last layout); renode checks and controls as in #543 (all check lines pass).
--selftest: a planted weakest-sigma series with an interior peak is located, a monotonic one is reported at the end of the range, and the log parser reads planted lines."""
import math, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
RAWPAT = re.compile(r"^\s+sigma_(\d) ([0-9.e+-]+) \(converged to [0-9e.+-]*\); delta share ([0-9.e+-]+); blocks .*?; top (\S+) k(\d+)", re.M)
EQHEAD = "J, Curtis-Reid + Ruiz ("
EQSIG = re.compile(r"^\s+Curtis-Reid \+ Ruiz sigma_(\d) ([0-9.e+-]+) \(converged to [0-9e.+-]*\)\n\s+scaled: delta share ([0-9.e+-]+); blocks [^;]*; top (\S+) k(\d+)[^\n]*\n\s+in z: delta share ([0-9.e+-]+);", re.M)


def read(p):
    return open(p, encoding="utf-8").read()


def classify_raw(share, kh):
    return "D" if share >= 0.9 else "H3" if (share < 0.01 and kh == 3) else "H1" if kh == 1 else "other"


def raw(path):
    s = read(path)
    rows = [(int(m.group(1)), float(m.group(2)), classify_raw(float(m.group(3)), int(m.group(5)))) for m in RAWPAT.finditer(s)]
    return rows, "check: pass" in s


def eq(path):
    s = read(path)
    i = s.index(EQHEAD)
    sec = s[i:i + 6000]
    rows = []
    for m in EQSIG.finditer(sec):
        dz = float(m.group(6))
        rows.append((int(m.group(1)), float(m.group(2)), ("Dz " if dz >= 0.9 else "") + f"{m.group(4)} k{m.group(5)}"))
    return rows[:4], bool(re.search(r"^check: pass", s, re.M))


def where():
    out = {}
    for x, d, tag in ((0.70, "I537-win2", "base"), (0.72, "I537-win2", "last072"), (0.73, "I553-win2", "last073"), (0.74, "I543-win2", "last074"), (0.75, "I553-win2", "last075"), (0.76, "I543-win2", "last076"),
                      (0.77, "I553-win2", "last077"), (0.78, "I553-win2", "last078"), (0.79, "I553-win2", "last079"), (0.80, "I543-win2", "last080")):
        out[x] = (os.path.join(HERE, "..", d), tag)
    for x in (0.82, 0.84, 0.86, 0.88, 0.90, 0.92):
        out[x] = (os.path.join(HERE, "..", "I554-win2"), f"last{int(round(x * 100)):03d}")
    for x in (0.94, 0.96, 0.98):
        out[x] = (HERE, f"last{int(round(x * 100)):03d}")
    return out


def locate(xs, ys):
    """x of the largest y and the verdict: 'within 0.02' for an interior maximum with both neighbours within 0.02, 'end of the range' if at the last x, else 'interior, neighbours farther than 0.02'"""
    i = max(range(len(ys)), key=lambda j: ys[j])
    if i == len(xs) - 1:
        return xs[i], "at the end of the range"
    if i == 0:
        return xs[i], "at the start of the range"
    if xs[i] - xs[i - 1] <= 0.0201 and xs[i + 1] - xs[i] <= 0.0201:
        return xs[i], "located to within 0.02"
    return xs[i], "interior maximum, a neighbour farther than 0.02"


def selftest():
    xs = [0.80, 0.82, 0.84, 0.86, 0.88, 0.90, 0.92]
    ok = locate(xs, [1, 2, 3, 5, 4, 2, 1])[1] == "located to within 0.02" and locate(xs, [1, 2, 3, 4, 5, 6, 7])[1] == "at the end of the range" and locate([0.7, 0.76, 0.8], [1, 5, 2])[1].startswith("interior maximum, a neighbour")
    line = "  J, Curtis-Reid + Ruiz (9 s):\n    Curtis-Reid + Ruiz sigma_1 1.4769e-56 (converged to 0e+00)\n        scaled: delta share 2.6e-05; blocks a_h 0.54, m_h 0.46, node4.m 0.00; top m_h k1 0.11, a_h k2 0.08\n        in z: delta share 1.0e+00; blocks m_h 0.00, node4.p 0.00\n"
    m = EQSIG.search(line)
    ok = ok and m and abs(float(m.group(2)) - 1.4769e-56) < 1e-60 and m.group(4) == "m_h" and m.group(5) == "1" and float(m.group(6)) == 1.0
    m = RAWPAT.search("  sigma_3 4.392e-26 (converged to 5e-16); delta share 7.0e-01; blocks p1 0.07, m_h 0.05, node4.p 0.03; top p1 k1 0.07, m_h k1 0.05")
    ok = ok and m and classify_raw(float(m.group(3)), int(m.group(5))) == "H1"
    print("selftest: ok" if ok else "selftest FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    lay = where()
    allok = True
    data = {}
    for x in sorted(lay):
        d, tag = lay[x]
        if not os.path.exists(os.path.join(d, f"eq_{tag}.log")) or "check:" not in read(os.path.join(d, f"eq_{tag}.log")):
            continue          # a layout whose near_null_eq has not finished
        nn = os.path.join(d, f"nnv_{tag}.log") if (not os.path.exists(os.path.join(d, f"nn_{tag}.log"))) else os.path.join(d, f"nn_{tag}.log")
        r, o1 = raw(nn)
        e, o2 = eq(os.path.join(d, f"eq_{tag}.log"))
        allok = allok and o1 and o2
        data[x] = (r, e)
    print("| x_last | raw sigma_1 (mode) | raw sigma_2 | raw sigma_3 | raw sigma_4 | equilibrated sigma_1 (top scaled component) | sigma_2 | sigma_3 | sigma_4 |\n|---|---|---|---|---|---|---|---|---|")
    for x, (r, e) in data.items():
        print(f"| {x:.2f} | " + " | ".join(f"{s:.3e} ({c})" for _, s, c in r) + " | " + " | ".join(f"{s:.3e} ({c})" for _, s, c in e) + " |")
    xs = list(data)
    print("\nthe weakest sigma at each layout")
    print("| x_last | weakest raw sigma | its mode | weakest equilibrated sigma | its mode (top scaled component) | ln of the equilibrated one |\n|---|---|---|---|---|---|")
    wr, we = [], []
    for x in xs:
        r, e = data[x]
        a = min(r, key=lambda t: t[1])
        b = min(e, key=lambda t: t[1])
        wr.append(a[1]); we.append(b[1])
        print(f"| {x:.2f} | {a[1]:.3e} | {a[2]} | {b[1]:.3e} | {b[2]} | {math.log(b[1]):.2f} |")
    xm, verdict = locate(xs, [math.log(v) for v in we])
    xr, vr = locate(xs, [math.log(v) for v in wr])
    print(f"\nthe weakest equilibrated sigma is largest at x_last = {xm:.2f} ({we[xs.index(xm)]:.3e}): {verdict}")
    print(f"(the weakest raw sigma is largest at x_last = {xr:.2f}: {vr})")
    print("all check lines pass" if allok else "a check line is not pass")
    sys.exit(0 if allok else 1)
