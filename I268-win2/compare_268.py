#!/usr/bin/env python3
"""I268-win2: the octo-double load check of anm_run.py on the I19-win2 crawl states, against what the crawl log recorded (issue #268).

    python -I compare_268.py [DIR]
        DIR holds load_D<D>.log for D in 214.6000 ... 215.0312 (default: this folder). For each state the crawl log
        (../I19-win2/crawl.log) is searched for the block of the accepted step into that D (the attempt line `a ... -> D <D>:` that is followed by
        `step k: D <D>,`), and three things are taken from the block and from this folder's log:
          - the converged line `on k: |F| X converged, Delta <18 digits> <correction>`: X, the Delta and the correction
            (the junk-projected correction of the converged Newton, hp/octo_corrector.py);
          - the line `octo-double Newton: n steps, max|F| X, converged; double-double |F| of its first two parts Y`;
          - the number of Newton iterations (the `on k:` lines).
        Prints a table per state: recorded, this run, and whether the printed digits agree. Exit 0: every state agrees in every field.
        Exit 1: some field differs (printed). Exit 2: a log is missing or has no converged line.
    python -I compare_268.py --selftest
        the crawl log's own block, used as 'this run', agrees in every field; a changed digit of Delta, a changed |F| exponent and a
        changed correction are each found at their field (exit 1 inside if any of these fails)."""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.dirname(HERE)
CRAWL = os.path.join(RAW, "I19-win2", "crawl.log")
STATES = ["214.6", "214.7", "214.8", "214.9", "215.0", "215.025", "215.03125"]
FILES = {"214.6": "214.6000", "214.7": "214.7000", "214.8": "214.8000", "214.9": "214.9000", "215.0": "215.0000", "215.025": "215.0250",
         "215.03125": "215.0312"}
CONV = re.compile(r"^\s+on (\d+): \|F\| ([\d.]+e[+-]\d+) converged, Delta ([\d.]+) ([+-][\d.]+e[+-]\d+)")
OCTO = re.compile(r"octo-double Newton: (\d+) steps, max\|F\| ([\d.]+e[+-]\d+), (converged|not converged); double-double \|F\| of its first two parts ([\d.]+e[+-]\d+)")
ITER = re.compile(r"^\s+on \d+: \|F\|")


def fields(lines):
    d = {"iterations": sum(1 for l in lines if ITER.match(l)), "converged_line": None, "octo": None}
    for l in lines:
        m = CONV.match(l)
        if m:
            d["converged_line"] = dict(on=int(m.group(1)), F=m.group(2), Delta=m.group(3), correction=m.group(4))
        m = OCTO.search(l)
        if m:
            d["octo"] = dict(steps=int(m.group(1)), maxF=m.group(2), status=m.group(3), ddF=m.group(4))
    return d


def crawl_block(lines, D):
    """the lines of the accepted attempt into D (from its re-seeded line to its `a ... -> D` line)"""
    pat = re.compile(rf"^    a [\d.]+ -> D {re.escape(D)}: ")
    for i, l in enumerate(lines):
        if pat.match(l) and i + 1 < len(lines) and re.match(rf"^step \d+: D {re.escape(D)},", lines[i + 1]):
            j = i
            while j > 0 and not re.match(r"^    a [\d.]+: re-seeded", lines[j]):
                j -= 1
            return lines[j:i + 1]
    return None


def compare(rec, ours, out=print, name=""):
    """returns the list of fields that differ"""
    bad = []
    for key, sub in (("converged_line", ("on", "F", "Delta", "correction")), ("octo", ("steps", "maxF", "status", "ddF"))):
        a, b = rec[key], ours[key]
        if a is None or b is None:
            bad.append(key + (" (missing in the crawl block)" if a is None else " (missing in this run)"))
            continue
        for f in sub:
            if a[f] != b[f]:
                bad.append(f"{key}.{f}: recorded {a[f]} this run {b[f]}")
    if rec["iterations"] != ours["iterations"]:
        bad.append(f"iterations: recorded {rec['iterations']} this run {ours['iterations']}")
    return bad


def selftest():
    crawl = open(CRAWL, encoding="utf-8", errors="replace").read().splitlines()
    ok = True
    for D in STATES:
        blk = crawl_block(crawl, D)
        ok &= blk is not None
        if blk is None:
            continue
        rec = fields(blk)
        ok &= compare(rec, fields(list(blk))) == [] and rec["converged_line"] is not None and rec["octo"] is not None
    blk = crawl_block(crawl, "214.6")
    e = [l.replace("Delta 1.69164734103273950", "Delta 1.69164734103273951") for l in blk]
    ok &= any("converged_line.Delta" in x for x in compare(fields(blk), fields(e)))
    e = [re.sub(r"(on \d+: \|F\| )5\.66e-48", r"\g<1>5.66e-47", l) for l in blk]
    ok &= any("converged_line.F" in x for x in compare(fields(blk), fields(e)))
    e = [l.replace("-9.3636e-17", "-9.3637e-17") for l in blk]
    ok &= any("converged_line.correction" in x for x in compare(fields(blk), fields(e)))
    print("selftest:", "ok" if ok else "FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    if sys.argv[1:2] == ["--selftest"]:
        sys.exit(selftest())
    d = sys.argv[1] if len(sys.argv) > 1 else HERE
    crawl = open(CRAWL, encoding="utf-8", errors="replace").read().splitlines()
    rc = 0
    for D in STATES:
        p = os.path.join(d, f"load_D{FILES[D]}.log")
        blk = crawl_block(crawl, D)
        print(f"== D {D}")
        if not os.path.exists(p) or blk is None:
            print("   MISSING", p if not os.path.exists(p) else "crawl block")
            rc = max(rc, 2)
            continue
        rec, ours = fields(blk), fields(open(p, encoding="utf-8", errors="replace").read().splitlines())
        if ours["converged_line"] is None:
            print("   this run has no converged line:")
            rc = max(rc, 2)
        for tag, f in (("recorded", rec), ("this run ", ours)):
            c, o = f["converged_line"], f["octo"]
            print(f"   {tag}: {f['iterations']} iterations; " + (f"last on {c['on']}: |F| {c['F']} converged, Delta {c['Delta']} {c['correction']}; " if c else "no converged line; ")
                  + (f"octo-double Newton {o['steps']} steps, max|F| {o['maxF']}, {o['status']}, dd |F| of its first two parts {o['ddF']}" if o else "no octo-double line"))
        bad = compare(rec, ours)
        print("   agree in every printed field" if not bad else "   DIFFERENCES:\n      " + "\n      ".join(bad))
        if bad:
            rc = max(rc, 1)
        a, b = rec["converged_line"], ours["converged_line"]
        if b is None and ours["octo"] is None:
            print("   VERDICT: not finished (no octo-double Newton line yet)")
        elif b is None:
            print(f"   VERDICT: not reproduced, the load check does not reach convergence (max|F| {ours['octo']['maxF']} after {ours['octo']['steps']} steps)")
        elif (a["Delta"], a["correction"]) == (b["Delta"], b["correction"]):
            print("   VERDICT: converged, Delta and its junk-projected correction equal the crawl's to the printed digits; |F|, steps and dd |F| differ only as listed")
        else:
            print(f"   VERDICT: converged, but Delta/correction differ: recorded {a['Delta']} {a['correction']}, this run {b['Delta']} {b['correction']}")
    sys.exit(rc)
