"""#1021: which of dh610's b21-25-fu retest controls fired in each pass, and whether each could. Reads the pass's rows
(rows_STEP_passN.jsonl) and recomputes, without fu_value.py's code, how many rows each mutation would change:
  f3        F_3 + 0.3i: the plain-accepted rows whose shifted F_3 is more than 0.1 from the nearest valued neighbour's;
  lowguard  guard 1 sigma: the rows that pass every test but the 10 sigma guard and have |R| >= 1 sigma.
A control that can change no row cannot fire: its exit 0 is vacuous. The script compares the exit that follows from the
rows (1 when some row changes, else 0) with the exit in exits_fu.txt, for every pass and mutation.
--mutate=exits flips the first reported exit: the comparison must then fail.
    python fu_controls.py FU_DIR [--mutate=exits]       exit 1 when a reported exit disagrees with the rows"""
import glob, json, math, os, re, sys

d = sys.argv[1]
mutate = "--mutate=exits" in sys.argv
GUARD, LOW, STEP = 10.0, 1.0, 0.1
rep = {}
for l in open(os.path.join(d, "exits_fu.txt")):
    m = re.match(r"(step\d_pass\d) retest --mutate=(\w+) exit (\d)", l)
    if m:
        rep[(m.group(1), m.group(2))] = int(m.group(3))
if mutate:
    k = sorted(rep)[0]
    rep[k] = 1 - rep[k]
    print(f"mutate=exits: reported exit of {k} flipped to {rep[k]}")


def tests(r, shift=0j):
    ok_val = bool(r["valued3"]) and math.isfinite(r["re"]) and math.isfinite(r["im"])
    ratio = math.hypot(r["re"], r["im"]) / r["sig"] if ok_val and r["sig"] else float("nan")
    f3 = complex(r["F3re"], r["F3im"]) + shift
    ok_sheet = bool(r["nbrs"]) and abs(f3 - complex(r["nbrs"][0][2], r["nbrs"][0][3])) <= STEP
    return ok_val, ok_val and r["ymax"] <= 1e2, ratio, ok_sheet


bad = 0
print("pass          rows  accepted  f3: rows changed, exit (rows -> reported)  lowguard: rows changed, exit (rows -> reported)")
for f in sorted(glob.glob(os.path.join(d, "rows_step*_pass*.jsonl"))):
    T = os.path.basename(f)[5:-6]
    rows = [json.loads(l) for l in open(f)]
    acc = ch_f3 = ch_low = 0
    for r in rows:
        ok_val, ok_y, ratio, ok_sheet = tests(r)
        a = ok_y and ratio >= GUARD and ok_sheet
        acc += a
        ch_f3 += a and not tests(r, 0.3j)[3]
        ch_low += (ok_y and ok_sheet and LOW <= ratio < GUARD)
    out = []
    for m, n in (("f3", ch_f3), ("lowguard", ch_low)):
        want, got = int(n > 0), rep.get((T, m))
        bad += got != want
        out.append(f"{n:>3}, {want} -> {got}{'' if got == want else ' DISAGREE'}{' (vacuous)' if n == 0 else ''}")
    print(f"{T:<13} {len(rows):>4}  {acc:>8}  f3: {out[0]:<36}  lowguard: {out[1]}")
    if ch_low == 0:                                      # vacuous lowguard: the causes of the rejected rows
        why = {}
        for r in rows:
            ok_val, ok_y, ratio, ok_sheet = tests(r)
            if not (ok_y and ratio >= GUARD and ok_sheet):
                w = re.sub(r" (at xi1|after) .*", "", r["why"])[:48] if not ok_val else f"valued, |R|/sigma {ratio:.3g}"
                why[w] = why.get(w, 0) + 1
        print("    rejected rows: " + "; ".join(f"{n} {w}" for w, n in sorted(why.items(), key=lambda x: -x[1])))
print(f"fu controls: {'PASS' if not bad else 'FAIL'} ({bad} reported exits disagree with the rows)")
sys.exit(1 if bad else 0)
