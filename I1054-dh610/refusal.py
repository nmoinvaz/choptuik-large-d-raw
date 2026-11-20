#!/usr/bin/env python3
"""refusal.py LOG: reads anm_run.py's attempt lines ("    a A -> D X: predicted |F| P, od K steps -> FC (tol T[, stall accepted ...]), ...") and the
line "stopped: no convergence ...". An attempt is accepted when FC <= T or the line says "stall accepted" (anm_run prints that exactly when an
attempt is accepted above its tol); otherwise it is refused (its a halves). Exit 1 and one line naming the first refusal, 0 when there is none, 2 on an
unreadable log. refusal.py --selftest: two lines of a real log (raw I1034-dh610/step6c_chain_s0.log, a refused attempt and the accepted one after it),
an attempt that converged and a nan one; --selftest --mutate flips the acceptance test and must fail (exit 1)."""
import re
import sys

LINE = re.compile(r"^    a ([0-9.]+) -> D ([0-9.]+): predicted \|F\| \S+, \w+ (\d+) steps -> (\S+) \(tol ([0-9.e+-]+)(,[^)]*)?\)")


def attempts(text, mutate=False):
    """[(a, D, steps, Fc, tol, accepted)] for each attempt line, in order"""
    out = []
    for ln in text.splitlines():
        m = LINE.match(ln)
        if not m:
            continue
        a, D, k, fc, tol, tail = m.groups()
        fc, tol = float(fc), float(tol)
        acc = (fc <= tol) or bool(tail and "stall accepted" in tail)
        if mutate:
            acc = not acc
        out.append((a, D, int(k), fc, tol, acc))
    return out


def first_refusal(text, mutate=False):
    for n, (a, D, k, fc, tol, acc) in enumerate(attempts(text, mutate), 1):
        if not acc:
            return f"attempt {n} refused: a {a} -> D {D}, {k} steps -> {fc:.2e} (tol {tol:.1e})"
    m = re.search(r"^stopped: no convergence.*$", text, re.M)
    return m.group(0) if m else None


def selftest(mutate):
    refused = "    a 1.000 -> D 238.526970387: predicted |F| 8.62e+17, od 0 steps -> 8.62e+17 (tol 1.4e-20), Delta 1.686908837153 (formula diff -1.5e-06), moved 0.0e+00, 162 s"
    stall = "    a 0.500 -> D 238.026970387: predicted |F| 1.50e+17, od 3 steps -> 4.56e+17 (tol 1.2e-20, stall accepted, Delta correction +0.0e+00), Delta 1.686998214543 (formula diff -1.5e-06), moved 2.4e-35, 184 s"
    conv = "    a 0.250 -> D 242.210237122: predicted |F| 3.00e-05, od 4 steps -> 2.00e-84 (tol 1.0e-60), Delta 1.686998214543 (formula diff -1.5e-06), moved 2.4e-35, 184 s"
    nan = "    a 0.250 -> D 242.210237122: predicted |F| nan, od 0 steps -> nan (tol 1.0e-60), Delta nan (formula diff +nan), moved 0.0e+00, 1 s"
    ok = True
    for name, txt, want in (("refused first, then stall accepted", refused + "\n" + stall, True), ("stall accepted alone", stall, False),
                            ("converged alone", conv, False), ("nan", nan, True),
                            ("the stopped line", "stopped: no convergence after three halvings", True)):
        got = first_refusal(txt, mutate) is not None
        print(f"  {name}: refusal {got} (want {want}) {'ok' if got == want else 'FAIL'}")
        ok &= got == want
    print("selftest", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest("--mutate" in sys.argv))
    try:
        r = first_refusal(open(sys.argv[1]).read())
    except OSError as e:
        print(e)
        sys.exit(2)
    print(r or "no refusal")
    sys.exit(1 if r else 0)
