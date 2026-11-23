#!/usr/bin/env python3
"""#1079 dh610 compare_macm3.py [--mutate] | selftest [--mutate]: this machine's results of the excited-zero certificates beside macm3's (in/macm3_ref/ and in/macm3/, pinned by blob), per zero N = 1, 2, from the files;
no number is typed by hand. Per metric: this machine's value, macm3's, the relative difference; the four relative margins of the Krawczyk test are the order's check (a difference above 1% is REPORTED); the others
(point run g_rad and Dg_rad, rho_6a, the 6a flat estimate, lemma S and old-sector contractions, the inclusion's slack, the C1 set radii, the covering's tiles, pieces and links) are information with the same 1% mark.
The slack and the radii are bounds assembled from upper bounds and move with every radius (AGENTS.md, #111): they pass on their own and are not an enclosure of one number.
usage (from this folder): python3 -I compare_macm3.py > compare_macm3.txt     ; exit 0 after printing when no margin is REPORTED, 1 otherwise.
selftest: the comparison of macm3's own files with themselves flags nothing; with one margin changed by 2% it flags exactly that margin; --mutate widens the 1% bar to 50%, which the 2% case must then fail to flag (exit 1)."""
import json, re, sys, os, copy

F = os.path.dirname(os.path.abspath(__file__))
W = "/home/nathan/Source/choptuik-large-d-1079a/solver/proof"
BAR = 0.01
BOX = {1: ("x1E2", "M3x1E2_h1e-12_w1e-13"), 2: ("x2E2", "M3x2E2_h1e-12_w1e-12")}
FL = r"([+-]?\d+\.?\d*(?:e[+-]?\d+)?)"


def first(s):
    return float(re.search(r"[+-]?\d+\.?\d*(?:[eE][+-]?\d+)?", str(s)).group(0))


def rd(p):
    return open(p).read() if os.path.exists(p) else None


def extract(N, mine):
    T, B = BOX[N]
    if mine:
        logs, data, lem, ray, chk, pt, ptj = f"{W}/logs", f"{W}/data", f"{W}/lemmas_M_runs", f"{W}/lemma6b1_runs_M3_exc{N}_linux/ray.json", f"{W}/lemmas_M_runs/lemma6b1_check_M3_exc{N}_linux.json", None, f"{W}/data/A_M_point_M3{T}.json"
        kl, l6l, sl, inl, c1l, chl = (f"{logs}/A_M_krawczyk_pt_{B}.log", f"{logs}/I1079_lemma6a_{B}.log", f"{logs}/I1079_sector_{B}.log", f"{logs}/I1079_incl_exc{N}.log", f"{logs}/I1079_h2_c1check_exc{N}.log", f"{logs}/I1079_h2_check_exc{N}.log")
        l6j, sj = f"{lem}/lemma6a_{B}.json", f"{lem}/lemma6_sector_M3_{B}.json"
    else:
        R = f"{F}/in/macm3_ref"
        kl, l6l, sl, inl, c1l, chl = (f"{R}/A_M_krawczyk_pt_{B}.log", f"{R}/I1079_lemma6a_{B}.log", f"{R}/I1079_sector_{B}.log", f"{R}/I1079_incl_exc{N}.log", f"{R}/I1079_h2_c1check_exc{N}.log", f"{R}/I1079_h2_check_exc{N}.log")
        l6j, sj, ptj = f"{R}/lemma6a_{B}.json", f"{R}/lemma6_sector_M3_{B}.json", f"{F}/in/macm3/A_M_point_M3{T}.json"
    out = {}
    t = rd(kl)
    if t:
        m = re.search(r"relative margins " + FL + ", " + FL + ", " + FL + ", " + FL, t)
        if m:
            for i in range(4):
                out[f"margin {i + 1}"] = float(m.group(i + 1))
    if rd(ptj):
        r = json.load(open(ptj))
        out["point g_rad"], out["point Dg_rad"] = float(r["g_rad"]), float(r["Dg_rad"])
    if rd(l6j):
        r = json.load(open(l6j))
        out["rho_6a"], out["6a flat Lambda"] = first(r["rho6a"]), first(r["Lambda"])
    if rd(sj):
        r = json.load(open(sj))
        for k in ("rho_S", "lip_S", "lip_old", "Lambda_plain", "Lambda_diag"):
            if k in r and r[k] is not None:
                try:
                    out[f"sector {k}"] = first(r[k])
                except Exception:
                    pass
    t = rd(l6l)
    if t:
        m = re.search(r"lemma S \(M = 3.*?contraction " + FL, t)
        if m:
            out["lemma S contraction"] = float(m.group(1))
        m = re.search(r"old sector lemma.*?contraction " + FL, rd(sl) or "")
        if m:
            out["old sector contraction"] = float(m.group(1))
    t = rd(inl)
    if t:
        m = re.search(r"slack " + FL, t)
        if m:
            out["inclusion slack"] = float(m.group(1))
    t = rd(c1l)
    if t:
        for row, rad in re.findall(r"row (\d+) \(\|u\| = [0-9.]+\): set radius " + FL, t):
            out[f"c1 set radius row {row}"] = float(rad)
    t = rd(chl)
    if t:
        m = re.search(r"tiles glued: (\d+) \(meeting sets: (\d+) polar rectangles, (\d+) links\)", t)
        if m:
            out["covering tiles"], out["covering pieces"], out["covering links"] = (float(x) for x in m.groups())
    return out


def compare(a, b, bar=BAR):
    rows = []
    for k in b:
        if k in a:
            d = (a[k] - b[k]) / abs(b[k]) if b[k] else float("nan")
            rows.append((k, a[k], b[k], d, abs(d) > bar))
        else:
            rows.append((k, None, b[k], None, True))
    return rows


def selftest(mutate):
    bar = 0.5 if mutate else BAR
    ref = extract(1, False)
    same = compare(ref, ref, bar)
    ok1 = not any(r[4] for r in same) and len(same) > 8
    m = copy.deepcopy(ref)
    m["margin 2"] *= 1.02
    flagged = [r[0] for r in compare(m, ref, bar) if r[4]]
    ok2 = flagged == ["margin 2"]
    print(f"  macm3's files against themselves: {len(same)} metrics, none flagged: {'ok' if ok1 else 'WRONG'}")
    print(f"  one margin changed by 2%: flagged {flagged}: {'ok' if ok2 else 'WRONG'}")
    print("selftest" + (" --mutate" if mutate else ""), "PASS" if ok1 and ok2 else "FAIL")
    return 0 if ok1 and ok2 else 1


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "selftest":
        sys.exit(selftest("--mutate" in sys.argv))
    bar = 0.5 if "--mutate" in sys.argv else BAR
    rep = 0
    for N in (1, 2):
        a, b = extract(N, True), extract(N, False)
        print(f"zero {N} ({BOX[N][1]}): this machine against macm3 (relative difference; REPORT above {bar:g})")
        print("| metric | this machine | macm3 | relative difference | |")
        print("|---|---|---|---|---|")
        for k, x, y, d, f in compare(a, b, bar):
            if k.startswith("margin") and f:
                rep += 1
            print(f"| {k} | {x if x is None else format(x, '.10g')} | {format(y, '.10g')} | {'n/a' if d is None else format(d, '+.2e')} | {'REPORT' if f else ''} |")
        print()
    print(f"margins REPORTED: {rep}")
    sys.exit(0 if rep == 0 else 1)
