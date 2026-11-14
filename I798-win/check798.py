#!/usr/bin/env python3
"""#798: the planted case and the table from lowD_plan_probe.py's probe.jsonl.
    python -I check798.py PROBE.jsonl        exit 0 when the planted case holds
    python -I check798.py --selftest
Planted truth (fixed before the run): (3.0425, order 3) capped, its last trace at x within 1e-9 of T135's 0.013725225625.
Then the table: per target and order, done with its seconds, or capped with its frozen x."""
import json
import sys

REF_X = 0.013725225625


def planted_ok(cases):
    c = [r for r in cases if abs(r["D"] - 3.0425) < 1e-9 and r["order"] == 3]
    return bool(c) and c[0]["status"] == "capped" and c[0].get("x") is not None and abs(c[0]["x"] - REF_X) <= 1e-9


def main(path):
    cases = [r for r in (json.loads(x) for x in open(path) if x.strip()) if r.get("stage") == "case"]
    ok = planted_ok(cases)
    print(f"planted (3.0425, n 3): {'met' if ok else 'NOT MET'}")
    targets = sorted({r["D"] for r in cases}, reverse=True)
    print("| target (h) | n 0 | n 1 | n 2 | n 3 |\n|---|---|---|---|---|")
    for D in targets:
        row = {r["order"]: r for r in cases if r["D"] == D}
        h = next(iter(row.values()))["h"]
        cells = [(f"plans, {row[n]['seconds']:.0f} s" if row[n]["status"] == "done" else f"capped at x {row[n]['x']:.12f}")
                 if n in row else "-" for n in range(4)]
        print(f"| {D:g} ({h:+.5f}) | " + " | ".join(cells) + " |")
    return 0 if ok else 1


def selftest():
    good = [dict(stage="case", D=3.0425, h=-0.00125, order=3, status="capped", seconds=900.0, x=REF_X)]
    off = [dict(good[0], x=REF_X + 2e-9)]
    done = [dict(good[0], status="done", x=None)]
    cases = [("exact", planted_ok(good), True), ("x off by 2e-9", planted_ok(off), False), ("planned", planted_ok(done), False)]
    bad = sum(got != want for _, got, want in cases)
    for label, got, want in cases:
        print(f"  {label}: {got} (expected {want}) {'ok' if got == want else 'WRONG'}")
    print("selftest", "passed" if not bad else "FAILED")
    return 1 if bad else 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    sys.exit(main(sys.argv[1]))
