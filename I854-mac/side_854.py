#!/usr/bin/env python3
"""#854's steps of keep_s1 (keep_projected on) beside #839's A_s1 (off), from the two logs.

Per step: the accepted lam of each, |F| and |dz| before the step, and each refused trial's point max|F| with its ratio
to the step's lam-1 trial. Two checks (exit 0 when both pass):
  algebra: at lam 1 both variants evaluate zp + s, and the projection sets the same zp from the same bulk, so while
           every earlier accepted lam agrees, keep_s1's lam-1 trial line equals A_s1's (seconds removed).
  law:     keep_s1's shorter trials carry no displacement term, so their point max|F| is the lam-1 trial's times lam^4
           (#839's |dz|^4 law along the step), within 5%.
Controls (each must fail): --mutate=digit (one digit of keep_s1's first lam-1 trial changed), --mutate=power (the law
taken as lam^3).
usage: python3 side_854.py A_s1.log keep_s1.log [--mutate=digit|power]"""
import re
import sys

TRIAL = re.compile(r"^    on (\d+) trial lam (\S+): max\|F\| (\S+); raw \|dz_t\| (\S+) vs \|dz\| (\S+)")
STEP = re.compile(r"^  on (\d+): \|F\| (\S+) -> (\S+), \|dz\| (\S+) -> (\S+), lam (\S+), dDelta (\S+), piv (\S+)\.\.")
SEC = re.compile(r",? [0-9.]+ s$")


def parse(path, mutate=""):
    trials, steps, lam1 = {}, {}, {}
    for ln in open(path).read().splitlines():
        m = TRIAL.match(ln)
        if m:
            k, lam = int(m.group(1)), float(m.group(2))
            trials.setdefault(k, []).append((lam, float(m.group(3))))
            if lam == 1:
                lam1[k] = SEC.sub("", ln)
            continue
        m = STEP.match(ln)
        if m:
            steps[int(m.group(1))] = dict(F=m.group(2), dz=m.group(4), lam=float(m.group(6)), dDelta=m.group(7),
                                          piv=m.group(8))
    if mutate == "digit" and lam1:
        k = min(lam1)
        i = lam1[k].index("max|F| ") + 7
        lam1[k] = lam1[k][:i] + ("9" if lam1[k][i] != "9" else "8") + lam1[k][i + 1:]
    return trials, steps, lam1


def frac(lam):
    return "1" if lam == 1 else f"1/{round(1 / lam)}"


def main(argv):
    mut = next((a.split("=", 1)[1] for a in argv if a.startswith("--mutate=")), "")
    a_path, k_path = [a for a in argv if not a.startswith("--")][:2]
    At, As, A1 = parse(a_path)
    Kt, Ks, K1 = parse(k_path, mut)
    p = 3 if mut == "power" else 4
    print("| step | \\|F\\| before | \\|dz\\| before | A_s1 lam | keep_s1 lam | lam-1 trial (both) | "
          "A_s1 refused shorter trials | keep_s1 refused shorter trials, ratio to lam-1 × lam^4 |")
    print("|---|---|---|---|---|---|---|---|")
    ok_alg, ok_law, same = True, True, True
    for k in sorted(set(As) | set(Ks)):
        a, b = As.get(k), Ks.get(k)
        f1 = dict(Kt.get(k, [])).get(1.0)
        ash = ", ".join(f"{frac(l)}: {F:.2e}" for l, F in At.get(k, []) if l < 1 and (not a or l > a["lam"])) or "none"
        ksh = []
        for l, F in Kt.get(k, []):
            if l < 1 and (not b or l > b["lam"]):
                r = F / (f1 * l ** p) if f1 else float("nan")
                ksh.append(f"{frac(l)}: {F:.2e} ({r:.3f})")
                if not (0.95 <= r <= 1.05):
                    ok_law = False
        if same and k in A1 and k in K1:
            eq = A1[k] == K1[k]
            ok_alg &= eq
            tag = "equal" if eq else "DIFFER"
        else:
            tag = "after a departure" if not same else "n/a"
        print(f"| {k} | {(b or a)['F']} | {(b or a)['dz']} | {frac(a['lam']) if a else '–'} | "
              f"{frac(b['lam']) if b else '–'} | {f'{f1:.2e}' if f1 else '–'} ({tag}) | {ash} | {', '.join(ksh) or 'none'} |")
        if a and b and a["lam"] != b["lam"]:
            same = False
    print(f"algebra: keep_s1's lam-1 trial lines equal A_s1's while the accepted lam agree: {'pass' if ok_alg else 'FAIL'}")
    print(f"law: keep_s1's refused shorter trials at lam-1 × lam^{p} within 5%: {'pass' if ok_law else 'FAIL'}")
    ok = ok_alg and ok_law
    print(f"side_854{' --mutate=' + mut if mut else ''}: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
