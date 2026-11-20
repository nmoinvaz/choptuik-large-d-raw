#!/usr/bin/env python3
"""classify.py LOG [LOG ...] [--json]: the reading of notes/EXACT_RECIP.md 3.5 and 3.6 for an anm_run.py base polish log (--log_proj 1):
converged       the log's "octo-double Newton: K steps, max|F| X" has X <= 1e-50 and "base polish saved as" follows it;
stopped at start "the start's projection failed, attempt stopped": the start's pinned max|F| is the first "projection failed (1)" line's;
not converged   a Newton line with X > 1e-50 (a stall, or the --qd_it cap of 40 steps): its steps K, last max|F| X, the first step's |F| and |dz| ("on 0:"),
                the number of "projection failed (n)" lines, and whether a base was saved or "not adopted".
classify.py --selftest: five logs of this raw folder with known readings (converged: resolve251_r0, resolve241_r1; stopped at start: resolve251_r1, resolve246.4399_r1;
not converged: resolve251_r1b); --selftest --mutate expects one wrong reading and must exit 1."""
import json
import re
import sys


def classify(path):
    L = open(path).read().splitlines()
    stop = any("attempt stopped" in ln for ln in L)
    pf = [ln for ln in L if re.search(r"projection failed \(\d+\)", ln)]
    npf = max([int(re.search(r"projection failed \((\d+)\)", ln).group(1)) for ln in pf] or [0])
    start = None
    for ln in pf:
        if "projection failed (1)" in ln:
            m = re.search(r"point max\|F\| ([0-9.]+e[-+]?\d+|nan)", ln)
            start = m.group(1) if m else None
            break
    newton = [(i, ln) for i, ln in enumerate(L) if "octo-double Newton:" in ln]
    saved = [i for i, ln in enumerate(L) if ln.startswith("base polish saved as")]
    notadopted = any(ln.startswith("base polish not adopted") for ln in L)
    first = None
    for ln in L:
        m = re.match(r"\s+on 0: \|F\| ([0-9.e+-]+)(?: -> [0-9.e+-]+)?, \|dz\| ([0-9.e+-]+)", ln)
        if m:
            first = (m.group(1), m.group(2))
            break
    r = dict(log=path.split("/")[-1], projection_failed_lines=npf, start_maxF=start, first_step=first, saved=bool(saved), not_adopted=notadopted)
    if stop:
        r["reading"] = "stopped at start"
        return r
    if not newton:
        r["reading"] = "no Newton line"
        return r
    m = re.search(r"octo-double Newton: (\d+) steps, max\|F\| ([0-9.]+e[-+]?\d+)", newton[-1][1])
    K, X = int(m.group(1)), float(m.group(2))
    r.update(steps=K, last_maxF=X, qd_it_cap=K >= 40)
    r["reading"] = "converged" if (X <= 1e-50 and saved and saved[-1] > newton[-1][0]) else "not converged"
    return r


def selftest(mutate):
    D = "/home/nathan/Source/choptuik-large-d-raw/I1054-dh610/"
    want = {"resolve251_r0.log": "converged", "resolve241_r1.log": "converged", "resolve251_r1.log": "stopped at start",
            "resolve246.4399_r1.log": "stopped at start", "resolve251_r1b.log": "not converged"}
    if mutate:
        want["resolve251_r1b.log"] = "converged"
    bad = 0
    for f, w in want.items():
        got = classify(D + f)["reading"]
        print(f"  {f}: {got} (expected {w}) {'ok' if got == w else 'MISMATCH'}")
        bad += got != w
    print(f"classify selftest{' --mutate' if mutate else ''}: {'PASS' if not bad else 'FAIL'}")
    return 1 if bad else 0


def main():
    a = sys.argv[1:]
    if "--selftest" in a:
        return selftest("--mutate" in a)
    for f in [x for x in a if not x.startswith("--")]:
        r = classify(f)
        print(json.dumps(r) if "--json" in a else f"{r['log']}: {r['reading']}" + "".join(f", {k} {v}" for k, v in r.items() if k not in ("log", "reading") and v not in (None, False, 0)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
