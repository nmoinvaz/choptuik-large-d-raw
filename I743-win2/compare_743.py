#!/usr/bin/env python3
"""#743: the first Newton step of the --log_proj 1 rerun against s132's, and the rerun's projection lines.

    python3 -I compare_743.py S132_LOG NEW_LOG [--mutate=drop|count]   exit 0 when every check passes, 1 otherwise

Checks (each can fail):
  1. The step-0 lines ("on 0 chord", "on 0 trial", "on 0:"), with the timings cut, are equal in the two logs.
  2. The number of "projection failed (" lines equals the 'failed' count of the rerun's "elim projections" line.
  3. Every such line names a stage that failed (NOT converged, FAILED or not finite), and none says "no stage record".
It then tallies the failed lines by stage and prints each one's point max|F|.
Controls: --mutate=drop deletes the rerun's last step-0 trial line, so check 1 must fail; --mutate=count adds 1 to the
'failed' count, so check 2 must fail.
"""
import ast
import re
import sys

TIMING = re.compile(r", [0-9.]+ s$")


def step0(lines):
    """the step-0 lines, stripped, without their trailing timing"""
    return [TIMING.sub("", s.strip()) for s in lines if re.match(r"\s*on 0[ :]", s)]


def main(argv):
    args = [a for a in argv if not a.startswith("--")]
    mutate = next((a.split("=", 1)[1] for a in argv if a.startswith("--mutate=")), None)
    if len(args) != 2 or mutate not in (None, "drop", "count"):
        print(__doc__)
        return 2
    old = open(args[0], encoding="utf-8").read().splitlines()
    new = open(args[1], encoding="utf-8").read().splitlines()
    a, b = step0(old), step0(new)
    if mutate == "drop":
        i = max(k for k, s in enumerate(b) if s.startswith("on 0 trial"))
        b = b[:i] + b[i + 1:]
    ok1 = len(a) > 0 and a == b
    print(f"1. step-0 lines: s132 {len(a)}, rerun {len(b)}, {'equal' if ok1 else 'DIFFER'}")
    if not ok1:
        for k in range(max(len(a), len(b))):
            x, y = (a[k] if k < len(a) else "-"), (b[k] if k < len(b) else "-")
            if x != y:
                print(f"   first difference at line {k}:\n     s132:  {x}\n     rerun: {y}")
                break
    fails = [s.strip() for s in new if s.strip().startswith("projection failed (")]
    counts = [ast.literal_eval(m.group(1)) for s in new
              for m in [re.search(r"elim projections (\{.*\})", s)] if m]
    nfail = counts[-1]["failed"] + (1 if mutate == "count" else 0) if counts else None
    ok2 = nfail is not None and len(fails) == nfail
    print(f"2. projection lines {len(fails)}, the counts line's failed {nfail}: {'equal' if ok2 else 'DIFFER'}")
    named = [("NOT converged" in s or "FAILED" in s or "not finite" in s) and "no stage record" not in s for s in fails]
    ok3 = all(named)
    print(f"3. lines naming a failed stage: {sum(named)} of {len(fails)}: {'ok' if ok3 else 'NOT ALL'}")
    tally = {}
    for s in fails:
        for st in ("u0 rung", "u0 quad-double", "ladder"):
            part = next((p for p in s.split("; ") if p.startswith(st)), "")
            if "NOT converged" in part or "FAILED" in part or "not finite" in part:
                tally[st] = tally.get(st, 0) + 1
    print("failed stages:", ", ".join(f"{k} {v}" for k, v in tally.items()) or "none")
    for s in fails:
        m = re.search(r"point max\|F\| ([0-9.e+-]+)", s)
        print("  ", m.group(1) if m else "?", "|", s[:160])
    ok = ok1 and ok2 and ok3
    print(("PASS" if ok else "FAIL") + (f" (mutate={mutate})" if mutate else ""))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
