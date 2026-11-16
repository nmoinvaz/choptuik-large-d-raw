#!/usr/bin/env python3
"""#882: each of the Pi's outputs against the stored file of the same content in solver/proof/.

    python3 cmp882.py RAW_FOLDER WORKTREE

Logs: my <name>.log files (one command's stdout and stderr) against the stored log, with timings removed, line by line.
A line whose text apart from its numbers differs is structural; a number that differs in its printed digits is listed
with its relative difference. A stored log that holds several commands' output is compared with the matching <name>.log
files concatenated in the script's order. JSON files (the changed/ copies, and the appended JSON-line logs) are compared
leaf by leaf against `git show HEAD:` of the worktree, the appended logs against the records they had before.
"""
import json, os, re, subprocess, sys

RAW, WT = sys.argv[1], sys.argv[2]
P = "solver/proof/"
TIME = re.compile(r"\s*[\[(]\s*\d+(\.\d+)?\s*s\s*[\])]|\b\d+(\.\d+)? s\b|\bin \d+(\.\d+)? s\b|\"time\": [0-9.]+|\"sec\": [0-9.]+")
NUM = re.compile(r"[-+]?\d+\.?\d*(?:[eE][-+]?\d+)?")
TIMEKEYS = {"sec", "time", "secs", "wall"}

# my log name(s) in script order -> the stored file
LOGS = [
    (["b8m_atoms"], "b8m_atoms_K4.log"),
    (["b8m_identities"], "b8m_identities.log"),
    (["b8m_identities_rho2old", "b8m_identities_q"], "b8m_identities_mut.log"),
    (["b8m_scan_box"], "b8m_scan_K4_box.out"),
    (["b8m_h8"], "b8m_h8_K4_L73.89.log"),
    (["b8m_numcheck"], "b8m_numcheck_n1e3.log"),
    (["b8m_numcheck_weight", "b8m_numcheck_kernel"], "b8m_numcheck_mut.log"),
    (["b8m_numcheck_tau"], "b8m_numcheck_mut_tau.log"),
    (["b5_system"], "b5_system.log"),
    (["b5_formulas"], "b5_formulas.log"),
    (["b5_numeric_residual"], "b5_numeric_residual.log"),
    (["b5_numeric_lip"], "b5_numeric_lip.log"),
    (["b5_bounds"], "b5_bounds_k0.3_Z0.0085.log"),
    (["b5_bounds_scan"], "b5_bounds_scan.log"),
    (["b5_bounds_rp"], "b5_bounds_rp.log"),
    (["b5_bounds_check"], "b5_bounds_check.log"),
    (["b5_system_epsCB", "b5_system_theta", "b5_system_t5", "b5_formulas_res", "b5_numeric_offsol", "b5_bounds_check_res",
      "b5_bounds_check_jacP", "b5_bounds_jac", "b5_bounds_series", "b5_data_gauge", "b5_threshold_sum", "b5_path_stokes"],
     "b5_mutations.log"),
    (["b5_data"], "b5_data.log"),
    (["b5_threshold"], "b5_threshold.log"),
    (["b5_path"], "b5_path_n1e8.log"),
    (["b5_label"], "b5_label.log"),
    (["b5_label_check"], "b5_label_check.log"),
    (["b5_label_Ct2", "b5_label_scale", "b5_jump_sum"], "b5_label_mutations.log"),
    (["b5_jump"], "b5_jump.log"),
    (["b8m_scan_d0"], "b8m_scan_K4_d0_1e7.log"),
    (["b8m_h8_d0"], "b8m_h8_K4_L73.89_d0_1e7.log"),
    (["b5_jump_d0"], "b5_jump_d0_1e7.log"),
    (["b8m_scan_k085"], "b8m_scan_K4_k0.85.log"),
    (["b7_box"], "b7_box.log"),
    (["b7_adjoint"], "b7_adjoint.log"),
    (["b7_point"], "b7_point.log"),
    (["b7_check"], "b7_checks.log"),
    (["b7_adjoint_mutT"], "b7_adjoint_mutT.log"),
    (["b7_ift"], "b7_ift.log"),
    (["b7_ift_JD"], "b7_ift_mutJD.log"),
    (["b8m_lc"], "b8m_lc_K4.out"),
    (["b8m_lc_lipcheck"], "b8m_lc_lipcheck.log"),
    (["b8m_lc_mut_rho2L"], "b8m_lc_K4_mut_rho2L.out"),
    (["b8m_lc_numcheck_d0", "b8m_lc_numcheck_weight", "b8m_lc_numcheck_mut"], "b8m_lc_numcheck_mut.log"),
    (["b8m_lc_numcheck"], "b8m_lc_numcheck_n1e3.log"),
    (["b8m_lcj"], "b8m_lcj.log"),
    (["b8m_lcj_kernel", "b8m_lcj_Om"], "b8m_lcj_mutations.log"),
]
JSONS = ["b5_bounds_k0.3_Z0.0085.json", "b5_label.json", "b5_jump.json", "b5_jump_d0_1e7.json", "b7_box.json", "b7_adjoint.json",
         "b7_box_point.json", "b7_adjoint_point.json", "b7_adjoint_point_mutT.json", "b7_ift.json", "b8m_lc_lip.json", "b8m_lcj.json"]
APPENDED = ["b8m_scan_K4_box.log", "b8m_scan_K4_d0_1e7.log", "b8m_scan_K4_k0.85.log", "b8m_lc_K4.log", "b8m_lc_K4_mut_rho2L.log"]
# the stored file is a filtered or re-ordered subset of the new text: each stored line is matched to the closest new line
SUBSET = {"b5_mutations.log", "b5_label_mutations.log", "b8m_lc_numcheck_mut.log", "b8m_lc_numcheck_n1e3.log",
          "b8m_lcj_mutations.log"}
# the stored records predate the "d0": "0" key, so the new text is compared with that key removed (a format difference)
D0KEY = {"b8m_scan_K4_box.out", "b8m_scan_K4_k0.85.log", "b8m_scan_K4_d0_1e7.log"}
bad = []


def strip(s):
    return re.sub(r"arg x = +[-0-9.]+", "arg x = ?", TIME.sub("", s)).rstrip()   # the worst angle of a ray is a label


def stored(path):
    r = subprocess.run(["git", "-C", WT, "show", f"HEAD:{P}{path}"], capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else None


def read(path):
    return open(path, errors="replace").read() if os.path.exists(path) else None


def skel(l):
    return NUM.sub("#", l)


def subsetcmp(label, new, old, stored_name):
    la = [strip(x) for x in new.splitlines() if x.strip() and not re.fullmatch(r"exit \d+", x.strip())]
    lb = [strip(x) for x in old.splitlines() if x.strip() and not re.fullmatch(r"exit \d+", x.strip()) and not x.startswith("== ") and x.strip() not in ("BATCH DONE", "rho2L-done")]
    unmatched, ndiff, nnum, worst, used = [], 0, 0, (0.0, ""), set()
    for j, y in enumerate(lb):
        cand = [i for i, x in enumerate(la) if skel(x) == skel(y) and len(NUM.findall(x)) == len(NUM.findall(y))]
        if not cand:
            unmatched.append(j + 1)
            continue
        def d(i):
            t = 0.0
            for u, v in zip(NUM.findall(la[i]), NUM.findall(y)):
                try:
                    t += abs(float(u) - float(v)) / max(abs(float(u)), abs(float(v)), 1e-300)
                except ValueError:
                    t += 1.0
            return t
        i = min(cand, key=d)
        used.add(i)
        x = la[i]
        if x == y:
            continue
        ndiff += 1
        for u, v in zip(NUM.findall(x), NUM.findall(y)):
            if u != v:
                nnum += 1
                try:
                    r = abs(float(u) - float(v)) / max(abs(float(u)), abs(float(v)), 1e-300)
                except ValueError:
                    r = float("inf")
                if r > worst[0]:
                    worst = (r, f"stored line {j + 1}: {u} against {v}")
    if unmatched:
        bad.append(f"{label}: stored lines with no counterpart {unmatched[:6]}")
    print(f"| {label} | {stored_name} | subset: {len(lb)} stored lines, {len(la) - len(used)} new lines not in stored | {len(unmatched)} | {ndiff} ({nnum}) | {worst[0]:.1e} | {worst[1]} |")
    for j in unmatched[:3]:
        print(f"    stored line {j} unmatched: {lb[j - 1][:170]}")


def textcmp(label, new, old, stored_name):
    if stored_name in D0KEY:
        k = new.count('"d0": "0", ')
        new = new.replace('"d0": "0", ', "")
        print(f"|   ({label}: {k} records carry a \"d0\": \"0\" key the stored ones lack, removed for the comparison) |")
    if stored_name in SUBSET:
        return subsetcmp(label, new, old, stored_name)
    la = [strip(x) for x in new.splitlines()]
    lb_all = [strip(x) for x in old.splitlines() if not re.fullmatch(r"exit \d+", x.strip())]
    n = len(la)
    # the stored file may hold several commands' output: find the window that matches the skeletons best
    def dist(x, y):
        d = 0.0
        for u, v in zip(NUM.findall(x), NUM.findall(y)):
            try:
                d += abs(float(u) - float(v)) / max(abs(float(u)), abs(float(v)), 1e-300)
            except ValueError:
                d += 1.0
        return d

    best, boff = (-1, 0.0), 0
    for off in range(0, max(1, len(lb_all) - n + 1)):
        w = lb_all[off:off + n]
        m = sum(1 for i in range(len(w)) if skel(la[i]) == skel(w[i]) and len(NUM.findall(la[i])) == len(NUM.findall(w[i])))
        sc = (m, -sum(dist(la[i], w[i]) for i in range(len(w)) if skel(la[i]) == skel(w[i])))
        if sc > best:
            best, boff = sc, off
    lb = lb_all[boff:boff + n]
    struct, ndiff, nnum, worst = [], 0, 0, (0.0, "")
    for i in range(min(len(la), len(lb))):
        x, y = la[i], lb[i]
        if x == y:
            continue
        nx, ny = NUM.findall(x), NUM.findall(y)
        if skel(x) != skel(y) or len(nx) != len(ny):
            struct.append(i + 1)
            continue
        ndiff += 1
        for u, v in zip(nx, ny):
            if u != v:
                nnum += 1
                try:
                    r = abs(float(u) - float(v)) / max(abs(float(u)), abs(float(v)), 1e-300)
                except ValueError:
                    r = float("inf")
                if r > worst[0]:
                    worst = (r, f"line {i + 1}: {u} against {v}")
    cnt = f"{n}" if boff == 0 and len(lb_all) == n else f"{n} (stored lines {boff + 1}-{boff + n} of {len(lb_all)})"
    if len(lb) < n:
        bad.append(f"{label}: {n} lines against {len(lb)}")
    if struct:
        bad.append(f"{label}: text differs at lines {struct[:5]}")
    print(f"| {label} | {stored_name} | {cnt} | {len(struct)} | {ndiff} ({nnum}) | {worst[0]:.1e} | {worst[1]} |")
    for i in struct[:2]:
        print(f"    line {i}: new    {la[i - 1][:170]}\n    {' ' * len(str(i))}      stored {lb[i - 1][:170] if i - 1 < len(lb) else ''}")


def leaves(x, p=""):
    if isinstance(x, dict):
        for k, v in x.items():
            yield from leaves(v, p + "/" + k)
    elif isinstance(x, list):
        for i, v in enumerate(x):
            yield from leaves(v, p + f"[{i}]")
    else:
        yield p, x


def key(p):
    return re.sub(r"\[\d+\]", "", p).rsplit("/", 1)[-1]


BALL = re.compile(r"^\[\s*([-+0-9.eE]*)\s*\+/-\s*([-+0-9.eE]+)\s*\]$")
BALLS = []   # (label, path, digits agreeing, |dmid|/(r1+r2), radius ratio) over every ball leaf pair


def jsoncmp(label, new, old):
    import mpmath
    mpmath.mp.dps = 120
    try:
        A, B = dict(leaves(json.loads(new))), dict(leaves(json.loads(old)))
    except ValueError as e:
        bad.append(f"{label}: unreadable ({e})"); print(f"| {label} | unreadable |"); return
    if A.keys() != B.keys():
        bad.append(f"{label}: structure differs"); print(f"| {label} | structure differs ({len(A)} against {len(B)} leaves) |"); return
    nd, worst, other, nball, nover, mind, maxr, rr = 0, (0.0, ""), [], 0, 0, 1e9, 0.0, []
    for p in A:
        x, y = A[p], B[p]
        if x == y or key(p) in TIMEKEYS:
            continue
        nd += 1
        mx, my = (BALL.match(x) if isinstance(x, str) else None), (BALL.match(y) if isinstance(y, str) else None)
        if mx and my:
            a, b = (mpmath.mpf(mx[1]) if mx[1] else mpmath.mpf(0)), (mpmath.mpf(my[1]) if my[1] else mpmath.mpf(0))
            r1, r2 = mpmath.mpf(mx[2]), mpmath.mpf(my[2])
            dm = abs(a - b)
            nball += 1
            ov = dm <= r1 + r2
            nover += ov
            if not ov:
                bad.append(f"{label}: balls {p} are disjoint")
            maxr = max(maxr, float(dm / (r1 + r2)))
            if dm > 0 and max(abs(a), abs(b)) > 0:
                mind = min(mind, float(-mpmath.log10(dm / max(abs(a), abs(b)))))
            rr.append(float(r1 / r2))
        elif isinstance(x, (int, float)) and isinstance(y, (int, float)) and not isinstance(x, bool) and not isinstance(y, bool):
            r = abs(x - y) / max(abs(x), abs(y), 1e-300)
            if r > worst[0]:
                worst = (r, f"{p}: {x} against {y}")
        else:
            other.append(p)
            bad.append(f"{label}: {p} {str(x)[:40]} against {str(y)[:40]}")
    ball = (f"{nball} balls, {nover} overlap, midpoints agree to >= {mind:.1f} digits, |dmid|/(r1+r2) <= {maxr:.1e}, radius ratio {min(rr):.3f} to {max(rr):.3f}"
            if nball else "no balls")
    print(f"| {label} | {len(A)} leaves | {nd} differ apart from timings | {len(other)} other non-numeric | {worst[0]:.1e} | {worst[1][:80]} | {ball} |")


print("| my log(s) | stored file | lines | structural | lines with a differing number (numbers) | worst relative | where |")
print("|---|---|---|---|---|---|---|")
for names, sname in LOGS:
    parts = [read(os.path.join(RAW, n + ".log")) for n in names]
    old = stored(sname)
    if any(p is None for p in parts):
        print(f"| {'+'.join(names)} | {sname} | not run yet | | | | |"); continue
    if old is None:
        print(f"| {'+'.join(names)} | {sname} | no stored file | | | | |"); continue
    textcmp("+".join(names), "".join(parts), old, sname)
print()
print("| JSON | leaves | differ | non-numeric | worst relative (floats) | where | balls |")
print("|---|---|---|---|---|---|---|")
for j in JSONS:
    new, old = read(os.path.join(RAW, "changed", j)), stored(j)
    if new is None:
        print(f"| {j} | unchanged or not run (no changed/ copy) | | | | |"); continue
    jsoncmp(j, new, old) if old else print(f"| {j} | new file | | | | |")
print()
print("| appended log | records before | records appended | closes (stored / Pi) | worst relative of hyp, ratio, diag | status |")
print("|---|---|---|---|---|---|")
for a in APPENDED:
    new, old = read(os.path.join(RAW, "changed", a)), stored(a)
    if new is None or old is None:
        print(f"| {a} | not in changed/ or no stored file | | | | |"); continue
    ol, nl = [l for l in old.splitlines() if l.strip()], [l for l in new.splitlines() if l.strip()]
    if nl[:len(ol)] != ol:
        bad.append(f"{a}: the stored lines are not a prefix"); print(f"| {a} | NOT A PREFIX | | | | |"); continue
    added = nl[len(ol):]
    ws, closes = (0.0, ""), []
    for line in added:
        r = json.loads(line)
        match = [json.loads(o) for o in ol if json.loads(o).get("K") == r.get("K") and abs(json.loads(o).get("L0", 0) - r.get("L0", 0)) < 1e-9
                 and bool(json.loads(o).get("mutate")) == bool(r.get("mutate"))]
        if not match:
            continue
        o = match[-1]
        closes.append((o.get("closes"), r.get("closes")))
        if o.get("closes") != r.get("closes"):
            bad.append(f"{a}: closes {o.get('closes')} against {r.get('closes')} at L0 {r.get('L0')}")
        for k in ("hyp", "ratio", "diag"):
            for s in (r.get(k) or {}):
                if s in (o.get(k) or {}):
                    x, y = r[k][s], o[k][s]
                    d = abs(x - y) / max(abs(x), abs(y), 1e-300)
                    if d > ws[0]:
                        ws = (d, f"L0 {r.get('L0')} {k}.{s}")
    print(f"| {a} | {len(ol)} | {len(added)} | {sum(1 for c in closes if c[0] == c[1])} of {len(closes)} equal | {ws[0]:.1e} ({ws[1]}) | prefix intact |")
print()
print("structural, count or flag differences:", "; ".join(bad) if bad else "none")
sys.exit(1 if bad else 0)
