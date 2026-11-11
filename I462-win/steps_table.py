"""#462: the verdict-first report of the steps, from the chains' logs and saved states, in the coordinator's line shape.

    python3 steps_table.py [--since-d10 D] [--since-d6 D]      run from the I462-win folder
    python3 steps_table.py --selftest

Output, in this order:
 1. one line per step, the shape of the task coordinator (agent-comms 2026-11-11 011112Z), one mark per check in a fixed
    order, then the numbers in the same order:
        win_d10  D 220.13 -> 221.13   ✓ ✓ ~ ✗ ✗ ✓   (4, 1, 2.7e-54, 2.5e-20, 1.5e-18, ok)
    checks: Newton steps, step length (lam), final residual, start residual, first move (first |dz|), series (the base's
    |z_N|, a_max and fourth ratio; the value is "ok", or the quantity that is not OK). ✓ OK, ~ WATCH, ✗ BAD. A refused
    attempt (a later attempt at the same base follows it, or no state was saved) is one line with ✗ for the Newton steps.
 2. one Delta line per saved state, only the trusted digits, cut at the error bar (the Delta of d6 minus d10 at that D, or
    the latest one): the number of digits after the point is the first whose place is at most the error bar, and the
    uncertainty is the error bar in units of the last digit.
 3. the lines the shape has no room for (horizon rung, Delta minus its degree-5 extrapolation, the bases with the smallest
    pivot, which is reported and not judged), then the table with the full numbers, then the error bar.

Bounds (coordinator, 010640Z): Newton steps OK 3 to 4, WATCH 5 to 8, BAD more; lam OK 1, WATCH 0.25 to 0.5, BAD below 0.25 or
the stall line; final max|F| OK < 1e-60, WATCH to 1e-40, BAD above or not converged; start max|F| OK < 1e-33, WATCH to 1e-25,
BAD above; first |dz| OK < 1e-29, WATCH to 1e-26, BAD above; horizon rung (last number) OK < 1e-50, WATCH to 1e-40, BAD above
or re-seed not ok; series |z_N| OK < 1e-27, WATCH to 1e-24; a_max OK > 2.5, WATCH to 2.0; fourth ratio OK > 150, else WATCH (never BAD, 013349Z);
Delta minus extrapolation OK < 1e-12, WATCH to 1e-10. The count of Newton steps is the log's "od N steps".
--selftest checks every bound at, below and above its edge, the line shape, the refused-attempt logic and the digit cut."""
import datetime as dt
import glob
import json
import math
import os
import re
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except AttributeError:
    pass
RANK = {"OK": 0, "WATCH": 1, "BAD": 2}
MARK = {"OK": "✓", "WATCH": "~", "BAD": "✗"}
NAME = {"d6": "win_d6", "d10": "win_d10"}


def worse(a, b):
    return a if RANK[a] >= RANK[b] else b


def v_newton(n):
    return "OK" if n <= 4 else ("WATCH" if n <= 8 else "BAD")


def v_lam(lams, stall):
    if stall or (lams and min(lams) < 0.25):
        return "BAD"
    return "WATCH" if lams and min(lams) < 1 else "OK"


def v_final(x):
    return "BAD" if x is None else ("OK" if x < 1e-60 else ("WATCH" if x <= 1e-40 else "BAD"))


def v_start(x):
    return "OK" if x < 1e-33 else ("WATCH" if x <= 1e-25 else "BAD")


def v_dz(x):
    return "OK" if x < 1e-29 else ("WATCH" if x <= 1e-26 else "BAD")


def v_rung(x, reseed_ok):
    if not reseed_ok:
        return "BAD"
    return "OK" if x < 1e-50 else ("WATCH" if x <= 1e-40 else "BAD")


def v_zn(x):
    return "OK" if x < 1e-27 else ("WATCH" if x <= 1e-24 else "BAD")


def v_amax(x):
    return "OK" if x > 2.5 else ("WATCH" if x >= 2.0 else "BAD")


def v_ratio(x):
    return "OK" if x > 150 else "WATCH"          # coordinator, 013349Z: describes the series, WATCH at most, never BAD


def v_dextrap(x):
    return "OK" if x < 1e-12 else ("WATCH" if x <= 1e-10 else "BAD")


def fnum(s):
    try:
        return float(s)
    except (TypeError, ValueError):
        return None


def parse(lines, chain, saved_fn=None):
    """attempts that reached an 'a ... -> D' line, each with status accepted or refused. An attempt is refused when another
    attempt at the same base follows it; accepted when the next base follows it; the last one by whether its state is saved."""
    out, base, att, cand = [], None, None, None

    def close(status):
        nonlocal cand
        if cand is not None:
            cand["status"] = status
            out.append(cand)
            cand = None
    for l in lines:
        m = re.match(r"^step (\d+): D ([0-9.]+), pivots ([0-9.e+-]+)\.\.\S+, \|z_1\| \S+, \|z_N\| (\S+), ratios 2-5 (\S+) (\S+) (\S+) (\S+), a_max ([0-9.]+), (\d+) s", l)
        if m:
            close("accepted")
            base = dict(base=m.group(2), piv=m.group(3), zN=fnum(m.group(4)), ratios=(m.group(5), m.group(6), m.group(7), m.group(8)), ratio4=fnum(m.group(8)), amax=fnum(m.group(9)), series=m.group(10))
            att = None
            continue
        if base is None:
            continue
        m = re.match(r"^    a ([0-9.]+): re-seeded \((\w+)\), ([0-9.]+) s", l)
        if m:
            close("refused")
            att = dict(a=m.group(1), rs=m.group(2), rss=m.group(3), on=[], conv=None, stall=False, rung=None)
            continue
        if att is None:
            continue
        if "horizon data refined in octo-double" in l:
            nums = re.findall(r"[0-9.]+e[+-]\d+", l)
            att["rung"] = float(nums[-1]) if nums else None
        m = re.match(r"^  on (\d+): \|F\| (\S+) -> (\S+), \|dz\| (\S+) -> (\S+), lam (\S+),", l)
        if m:
            att["on"].append(dict(F0=fnum(m.group(2)), F1=fnum(m.group(3)), dz0=fnum(m.group(4)), lam=fnum(m.group(6))))
            continue
        if "no trial step accepted" in l:
            att["stall"] = True
            m = re.match(r"^  on (\d+): \|F\| (\S+), \|dz\| (\S+):", l)
            if m and not att["on"]:
                att["on"].append(dict(F0=fnum(m.group(2)), F1=None, dz0=fnum(m.group(3)), lam=0.0))
        m = re.match(r"^  on \d+: \|F\| (\S+) converged", l)
        if m:
            att["conv"] = fnum(m.group(1))
        m = re.match(r"^    a [0-9.]+ -> D ([0-9.]+):.*od (\d+) steps.*, (\d+) s$", l)
        if m:
            cand = dict(chain=chain, D=m.group(1), n=int(m.group(2)), nt=m.group(3), **base, **{k: att[k] for k in att})
            att = None
    close("accepted" if (saved_fn is None or (cand is not None and saved_fn(chain, cand["D"]))) else "refused")
    return out


def judge_step(b, dextrap=None):
    on = b["on"]
    lams = [o["lam"] for o in on if o["lam"] is not None]
    d = {"Newton": v_newton(b["n"]) if b["status"] == "accepted" else "BAD",
         "lam": v_lam(lams, b["stall"]),
         "final": v_final(b["conv"]),
         "start": v_start(on[0]["F0"]) if on and on[0]["F0"] is not None else "BAD",
         "dz": v_dz(on[0]["dz0"]) if on and on[0]["dz0"] is not None else "BAD"}
    extra = []
    if b["rung"] is not None or b["rs"] != "ok":
        extra.append(("horizon rung", f"{b['rung']:.1e}" if b["rung"] is not None else "n/a", v_rung(b["rung"] if b["rung"] is not None else 0.0, b["rs"] == "ok")))
    if dextrap is not None:
        extra.append(("Delta - extrapolation", f"{dextrap:.1e}", v_dextrap(dextrap)))
    return d, extra


def judge_base(b):
    rows = [("series |z_N|", f"{b['zN']:.1e}", v_zn(b["zN"])), ("a_max", f"{b['amax']:g}", v_amax(b["amax"])),
            ("fourth ratio", f"{b['ratio4']:g}", v_ratio(b["ratio4"]))]
    over = "OK"
    for _, _, v in rows:
        over = worse(over, v)
    return rows, over


def shape(b, d, bover, brows):
    on = b["on"]
    lams = [o["lam"] for o in on if o["lam"] is not None]
    lam_txt = "1" if not lams or min(lams) == 1 else f"{min(lams):g}"
    ser = "ok" if bover == "OK" else ", ".join(f"{q} {val}" for q, val, v in brows if v != "OK")
    vals = [str(b["n"]) if b["status"] == "accepted" else f"{b['n']}, refused",
            lam_txt,
            f"{b['conv']:.1e}" if b["conv"] is not None else "not converged",
            f"{on[0]['F0']:.1e}" if on and on[0]["F0"] is not None else "?",
            f"{on[0]['dz0']:.1e}" if on and on[0]["dz0"] is not None else "?",
            ser]
    marks = [MARK[d["Newton"]], MARK[d["lam"]], MARK[d["final"]], MARK[d["start"]], MARK[d["dz"]], MARK[bover]]
    ds = f"{float(b['base']):.2f} -> {float(b['D']):.2f}"
    return f"  {NAME[b['chain']]:<8} D {ds}   {' '.join(marks)}   ({', '.join(vals)})"


def delta_line(D, delta, err):
    """Delta(D ...) with the digits whose place is at most the error bar, the uncertainty in units of the last digit"""
    k = max(1, math.ceil(-math.log10(err)))
    u = max(1, round(err / 10.0 ** -k))
    ds = f"{D:.5f}".rstrip("0").rstrip(".")
    return f"  Delta(D {ds}) = {format(float(delta), f'.{k}f')} (±{u} in the last digit)"


def load_deltas(chain):
    import mpmath as mp
    import numpy as np
    mp.mp.dps = 60
    out = {}
    for sub in ("I215-win", "I276-win", "I462-win"):
        for p in glob.glob(os.path.join("..", sub, f"chain_{chain}", "anm_pin3_D*.npz")):
            dd = np.load(p, allow_pickle=True)
            parts = [k for k in ("zh", "zl", "z2", "z3", "z4", "z5", "z6", "z7") if k in dd]
            out[round(float(mp.mpf(json.loads(str(dd["meta"]))["D_str"])), 5)] = mp.fsum(mp.mpf(float(dd[k][-1])) for k in parts)
    return out


def extrap_diff(deltas, D):
    import mpmath as mp
    prev = sorted(d for d in deltas if d < D - 1e-9)[-6:]
    if D not in deltas or len(prev) < 6:
        return None
    s = mp.mpf(0)
    for i, xi in enumerate(prev):
        t = deltas[xi]
        for j, xj in enumerate(prev):
            if j != i:
                t *= (mp.mpf(D) - mp.mpf(xj)) / (mp.mpf(xi) - mp.mpf(xj))
        s += t
    return float(abs(deltas[D] - s))


def saved(chain, D):
    for dd in (float(D), float(D) + 1e-9):
        f = glob.glob(f"chain_{chain}/anm_pin3_D{dd:.4f}.npz")
        if f:
            return dt.datetime.fromtimestamp(os.path.getmtime(f[0]), dt.timezone.utc).strftime("%H:%M:%S")
    return "?"


def report(since):
    import mpmath as mp
    steps, deltas = [], {}
    for c in ("d10", "d6"):
        deltas[c] = load_deltas(c)
        for b in parse(open(f"chain_{c}.log", encoding="utf-8", errors="replace").read().splitlines(), c, lambda ch, D: saved(ch, D) != "?"):
            if float(b["D"]) > since[c]:
                steps.append(b)
    steps.sort(key=lambda b: (float(b["D"]), b["chain"]))
    common = sorted(set(deltas["d6"]) & set(deltas["d10"]))
    bars = {D: abs(deltas["d6"][D] - deltas["d10"][D]) for D in common}
    last_bar = float(bars[max(bars)]) if bars else 2e-11
    shapes, dlines, also, table = [], [], [], []
    for b in steps:
        Dn = round(float(b["D"]), 5)
        de = extrap_diff(deltas[b["chain"]], Dn) if b["status"] == "accepted" else None
        d, extra = judge_step(b, de)
        brows, bover = judge_base(b)
        shapes.append(shape(b, d, bover, brows))
        if b["status"] == "accepted" and Dn in deltas[b["chain"]]:
            err = float(bars[Dn]) if Dn in bars else 2e-11      # the measured Delta d6 minus d10 at that D, else 2e-11 (coordinator)
            dlines.append((b["chain"], delta_line(Dn, deltas[b["chain"]][Dn], err)))
        if extra:
            also.append(f"  {NAME[b['chain']]} D {b['D']}: " + ", ".join(f"{q} {val} ({MARK[v]})" for q, val, v in extra))
        also.append(f"  {NAME[b['chain']]} base D {b['base']}: " + ", ".join(f"{q} {val} ({MARK[v]})" for q, val, v in brows) + f"; smallest pivot {b['piv']} (reported)")
        f1 = f"{b['on'][0]['F1']:.2e}" if b["on"] and b["on"][0]["F1"] is not None else "?"
        f2 = f"{b['on'][1]['F1']:.2e}" if len(b["on"]) > 1 and b["on"][1]["F1"] is not None else "?"
        worst = "BAD" if "BAD" in d.values() or bover == "BAD" else ("WATCH" if "WATCH" in d.values() or bover == "WATCH" else "OK")
        table.append(f"| {MARK[worst]} | {b['chain']} | {b['base']} to {b['D']} | {b['status']} | {b['series']} s | {' '.join(b['ratios'])} | {b['piv']} | {b['rs']}, {float(b['rss']):.0f} s | {b['n']} | {f1} | {f2} | "
                     f"{b['conv'] if b['conv'] is not None else '?'} | {b['nt']} s | {saved(b['chain'], b['D'])} |")
    print("checks:  Newton steps · step length · final residual · start residual · first move · series")
    for s in shapes:
        print(s)
    for c, dl in dlines:
        print(f"  {NAME[c]:<8} {dl.strip()}")      # two chains on one machine: the name tells the Delta lines of one D apart
    print("also:")
    for a in also:
        print(a)
    print("\n| worst | chain | D | status | series | ratios 2-5 of the series | smallest pivot at the base | re-seed | Newton | max\\|F\\| after solve 1 | after solve 2 | final max\\|F\\| | Newton time | saved (UTC) |")
    print("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    for t in table:
        print(t)
    print("\nerror bar (Delta d6 minus d10, same D): " + "; ".join(f"D {D:g}: {mp.nstr(deltas['d6'][D] - deltas['d10'][D], 6)}" for D in common if D >= 216))


def selftest():
    ok = True

    def chk(name, got, want):
        nonlocal ok
        if got != want:
            ok = False
            print(f"  FAIL {name}: got {got!r}, want {want!r}")
    for n, w in ((3, "OK"), (4, "OK"), (5, "WATCH"), (8, "WATCH"), (9, "BAD")):
        chk(f"newton {n}", v_newton(n), w)
    chk("lam 1", v_lam([1, 1], False), "OK"); chk("lam .5", v_lam([1, 0.5], False), "WATCH"); chk("lam .25", v_lam([0.25], False), "WATCH")
    chk("lam .125", v_lam([0.125], False), "BAD"); chk("lam stall", v_lam([1], True), "BAD")
    for x, w in ((1e-61, "OK"), (1e-60, "WATCH"), (1e-40, "WATCH"), (1e-39, "BAD"), (None, "BAD")):
        chk(f"final {x}", v_final(x), w)
    for x, w in ((1e-34, "OK"), (1e-33, "WATCH"), (1e-25, "WATCH"), (1e-24, "BAD")):
        chk(f"start {x}", v_start(x), w)
    for x, w in ((1e-30, "OK"), (1e-29, "WATCH"), (1e-26, "WATCH"), (1e-25, "BAD")):
        chk(f"dz {x}", v_dz(x), w)
    for x, w in ((1e-51, "OK"), (1e-50, "WATCH"), (1e-40, "WATCH"), (1e-39, "BAD")):
        chk(f"rung {x}", v_rung(x, True), w)
    chk("rung reseed bad", v_rung(1e-60, False), "BAD")
    for x, w in ((1e-28, "OK"), (1e-27, "WATCH"), (1e-24, "WATCH"), (1e-23, "BAD")):
        chk(f"zN {x}", v_zn(x), w)
    for x, w in ((2.6, "OK"), (2.5, "WATCH"), (2.0, "WATCH"), (1.9, "BAD")):
        chk(f"amax {x}", v_amax(x), w)
    for x, w in ((151, "OK"), (150, "WATCH"), (100, "WATCH"), (85, "WATCH"), (1, "WATCH")):
        chk(f"ratio {x}", v_ratio(x), w)
    for x, w in ((1e-13, "OK"), (1e-12, "WATCH"), (1e-10, "WATCH"), (1e-9, "BAD")):
        chk(f"dextrap {x}", v_dextrap(x), w)
    head = "step 5: D 220.13125, pivots 3.4e-17..1.4e+31, |z_1| 4.21e-04, |z_N| 3.40e-29, ratios 2-5 281.5 253.7 242.2 217.9, a_max 3.036, 3701 s"
    block = [head, "    a 1.0000: re-seeded (ok), 278.96 s",
             "  on 0: |F| 2.48e-20 -> 1.08e-30, |dz| 1.5e-18 -> 6.4e-31, lam 1, dDelta +1.45e-19, piv 1.5e-17..2.0e+31, 552.97 s",
             "  on 1: |F| 1.08e-30 -> 1.27e-29, |dz| 6.4e-31 -> 3.0e-43, lam 1, dDelta -1.73e-31, piv 1.5e-17..2.0e+31, 190.56 s",
             "  on 2: |F| 1.27e-29 -> 2.66e-54, |dz| 3.0e-43 -> 1.3e-44, lam 1, dDelta +6.98e-44, piv 1.5e-17..2.0e+31, 235.62 s",
             "  on 3: |F| 2.66e-54 converged, Delta 1.69025329286197801 -5.7938e-17",
             "    a 1.000 -> D 221.13125: predicted |F| 4.46e+02, od 4 steps -> 4.15e+02 (tol 9.3e-20), Delta 1.690253292862 (x), moved 1.5e-18, 1185 s"]
    b = parse(block, "d10", lambda c, D: True)[0]
    d, _ = judge_step(b)
    brows, bover = judge_base(b)
    line = shape(b, d, bover, brows)
    want = "  win_d10  D 220.13 -> 221.13   ✓ ✓ ~ ✗ ✗ ✓   (4, 1, 2.7e-54, 2.5e-20, 1.5e-18, ok)"
    chk("the coordinator's example line", line, want)
    good = [l.replace("2.48e-20 -> 1.08e-30", "2.48e-35 -> 1.08e-36").replace("|dz| 1.5e-18", "|dz| 1.5e-31").replace("2.66e-54", "2.66e-70") for l in block]
    gb = parse(good, "d10", lambda c, D: True)[0]
    gd, _ = judge_step(gb)
    chk("a clean step is all OK", [gd[k] for k in ("Newton", "lam", "final", "start", "dz")], ["OK"] * 5)
    two = block + ["    a 0.5000: re-seeded (ok), 200.00 s"] + block[2:5] + ["  on 3: |F| 1e-70 converged, Delta 1.7 +1e-17",
          "    a 0.500 -> D 220.63125: predicted |F| 1.0e+02, od 4 steps -> 1.0e+02 (tol 9.3e-20), Delta 1.69 (x), moved 1e-18, 100 s"]
    tb = parse(two, "d10", lambda c, D: True)
    chk("a refused attempt followed by an accepted one", [(x["D"], x["status"]) for x in tb], [("221.13125", "refused"), ("220.63125", "accepted")])
    chk("the last attempt without a saved state is refused", parse(block, "d10", lambda c, D: False)[0]["status"], "refused")
    rb = dict(b, status="refused", n=12)
    rl = shape(rb, judge_step(rb)[0], bover, brows)
    chk("a refused attempt has ✗ first", rl.split("   ")[1].split()[0], "✗")
    for err, k, u in ((2.1e-11, 11, 2), (2e-10, 10, 2), (4.6e-11, 11, 5)):
        dl = delta_line(219.13125, 1.690671452030270085, err)
        chk(f"delta digits for {err}", (len(dl.split("= ")[1].split(" ")[0].split(".")[1]), dl.rstrip(")").split("±")[1].split()[0]), (k, str(u)))
    print("selftest:", "all bounds, the example line, the refused logic and the digit cut behave" if ok else "FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    since = {"d10": 0.0, "d6": 0.0}
    for i, a in enumerate(sys.argv):
        if a == "--since-d10":
            since["d10"] = float(sys.argv[i + 1])
        if a == "--since-d6":
            since["d6"] = float(sys.argv[i + 1])
    report(since)
