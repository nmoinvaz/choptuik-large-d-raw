"""#1012 closing table: every M = 9 level-5 run of #999, #1007, #1011 and #1012 in one table, parsed from the logs (raw repo folders next to this one).

    python table1012.py [--mutate=xi|predict|count] [--allow-missing] [--md OUT.md]       (stdlib only; exit 1 when a check fails)

Columns: the configuration (polish radius XI and approach radius AP of level 5, level-5 step --h5, nested steps --h7/--h9, rtol, --predict, --floor_max, code), level 5's solve ends in order,
level 5's stop reasons, level 3's iterations and stop, the end r_3, r_5, r_7, r_9 (the accepted state's, from the FIXED-A report), the run's wall time and how it ended.
The configuration is written in MANIFEST below (the logs do not carry the command); three facts are CHECKED against each log: the `level radii` line's r_5 approach and polish radii equal AP and XI;
the `Jacobian K computed (N residuals)` line says 10 with --predict and 8 without (when K is reached); the number of finished level-5 solves counted from `level 5 solved` lines equals the number of
`level 5 (top): stop at` lines (new format) or of `level 5 (top)` stop lines (old format: only noise-floor stops are printed, so that check is skipped for those logs).
--mutate=xi changes one manifest XI, --mutate=predict flips one predict flag, --mutate=count drops a solved line from one log's text: each must make a check fail."""
import os, re, sys

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = {"999": "I999-win2/logs", "1007": "I1007-win2/logs", "1011": "I1011-win2/logs", "1012": "I1012-win2/logs"}
# (label, folder key, log name, XI, AP, h5, h7/h9, rtol, predict, floor_max, code, old-format log)
MANIFEST = [
    ("#999", "999", "hier_nb_M9_polish5_0.13_win2.log", "0.13", "0.1188", "1e-6", "1e-6", "1e-13", True, "-", "efad7afd", True),
    ("#999", "999", "hier_nb_M9_polish5_0.12_win2.log", "0.12", "0.1188", "1e-6", "1e-6", "1e-13", True, "-", "efad7afd", True),
    ("#999", "999", "hier_nb_M9_polish5_0.11_approach5_0.105_win2.log", "0.11", "0.105", "1e-6", "1e-6", "1e-13", True, "-", "efad7afd", True),
    ("#999", "999", "hier_nb_M9_polish5_0.10_approach5_0.095_win2.log", "0.10", "0.095", "1e-6", "1e-6", "1e-13", True, "-", "efad7afd", True),
    ("#1007", "1007", "hier_nb_M9_polish5_0.105_approach5_0.105_v3_win2.log", "0.105", "0.105", "1e-6", "1e-6", "1e-13", True, "-", "ec7cfea7", False),
    ("#1007", "1007", "hier_nb_M9_polish5_0.115_approach5_0.105_v3_win2.log", "0.115", "0.105", "1e-6", "1e-6", "1e-13", True, "-", "ec7cfea7", False),
    ("#1007", "1007", "hier_nb_M9_polish5_0.12_approach5_0.105_v3_win2.log", "0.12", "0.105", "1e-6", "1e-6", "1e-13", True, "-", "ec7cfea7", False),
    ("#1011", "1011", "hier_nb_M9_polish5_0.11_approach5_0.105_fm1e-4_win2.log", "0.11", "0.105", "1e-6", "1e-6", "1e-13", True, "1e-4", "656396fd", False),
    ("#1011", "1011", "hier_nb_M9_polish5_0.105_approach5_0.105_fm1e-4_win2.log", "0.105", "0.105", "1e-6", "1e-6", "1e-13", True, "1e-4", "656396fd", False),
    ("#1012 st1", "1012", "hier_nb_M9_polish5_0.11_approach5_0.105_fm1e-4_h51e-4_win2.log", "0.11", "0.105", "1e-4", "1e-6", "1e-13", True, "1e-4", "23844822", False),
    ("#1012 st1", "1012", "hier_nb_M9_polish5_0.105_approach5_0.105_fm1e-4_h51e-4_win2.log", "0.105", "0.105", "1e-4", "1e-6", "1e-13", True, "1e-4", "23844822", False),
    ("#1012 st2", "1012", "hier_nb_M9_polish5_0.11_approach5_0.105_fm1e-4_h51e-3_win2.log", "0.11", "0.105", "1e-3", "1e-6", "1e-13", True, "1e-4", "23844822", False),
    ("#1012 st3", "1012", "hier_nb_M9_polish5_0.11_approach5_0.105_fm1e-4_h51e-4_rtol1e-14_win2.log", "0.11", "0.105", "1e-4", "1e-6", "1e-14", True, "1e-4", "23844822", False),
    ("#1012 st4", "1012", "hier_nb_M9_polish5_0.11_approach5_0.105_fm1e-4_h5h7h91e-4_win2.log", "0.11", "0.105", "1e-4", "1e-4", "1e-13", True, "1e-4", "299c4eb9", False),
    ("#1012 st5a", "1012", "hier_nb_M9_polish5_0.11_approach5_0.105_fm1e-4_h53e-4_win2.log", "0.11", "0.105", "3e-4", "1e-6", "1e-13", True, "1e-4", "299c4eb9", False),
    ("#1012 st5b", "1012", "hier_nb_M9_polish5_0.11_approach5_0.105_fm1e-4_h51e-4_nopredict_win2.log", "0.11", "0.105", "1e-4", "1e-6", "1e-13", False, "1e-4", "299c4eb9", False),
    ("#1012 st6c", "1012", "hier_nb_M9_polish5_0.11_approach5_0.105_fm1e-4_h53e-5_win2.log", "0.11", "0.105", "3e-5", "1e-6", "1e-13", True, "1e-4", "299c4eb9", False),
    ("#1012 st6d", "1012", "hier_nb_M9_polish5_0.11_approach5_0.105_fm1e-4_h51e-5_win2.log", "0.11", "0.105", "1e-5", "1e-6", "1e-13", True, "1e-4", "299c4eb9", False),
]


def two(x):
    x = float(x)
    if 1e-2 <= x < 1e3:
        return f"{x:.3g}"
    return f"{x:.1e}".replace("e-0", "e-").replace("e+0", "e+").replace(".0e", "e")


def parse(text, old):
    t = text.replace("\r", "").splitlines()
    d = {"lines": t}
    m = re.search(r"level radii \(approach -> polish\):.*? r_5 ([0-9.]+) -> ([0-9.]+)", text)
    d["ap"], d["xi"] = (float(m.group(1)), float(m.group(2))) if m else (None, None)
    d["solves"] = [(float(a), int(b), int(c), int(e)) for a, b, c, e in re.findall(r"level 5 solved: \|r_5\| (\S+)\s+\((\d+) residuals, (\d+) s\)\s+\[(\d+) s total\]", text)]
    d["n_solved_lines"] = len(re.findall(r"level 5 solved", text))
    if old:
        d["stops5"] = {"noise-floor stop lines only (old format)": len(re.findall(r"level 5 \((?:low|top)\): stop at \|g\|", text))}
        d["n_top_stops"] = None
    else:
        tally = {}
        for r in re.findall(r"level 5 \((?:low|top)\): stop at \|r_5\| \S+: (.*)", text):
            r = re.sub(r"every trial rejected.*", "every trial rejected", r)
            r = re.sub(r"a fresh Jacobian no longer halves.*", "no longer halves", r)
            tally[r] = tally.get(r, 0) + 1
        d["stops5"] = tally
        d["n_top_stops"] = len(re.findall(r"level 5 \(top\): stop at", text))
    k = re.search(r"Jacobian K computed \((\d+) residuals\)", text)
    d["k"] = int(k.group(1)) if k else None
    d["l3its"] = re.findall(r"^level 3 it \d+: \|r_3\| (\S+)", text, re.M)
    s3 = re.search(r"level 3 \(top\): stop at \|r_3\| (\S+): (.*)", text)
    d["l3stop"] = (s3.group(1), re.sub(r"every trial rejected.*", "every trial rejected", re.sub(r"a fresh Jacobian no longer halves.*", "no longer halves", s3.group(2)))) if s3 else None
    s3b = re.search(r"level 3 solved: \|r_3\| (\S+)\s+\((\d+) residuals, (\d+) s\)", text)
    d["l3solved"] = (s3b.group(1), int(s3b.group(2)), int(s3b.group(3))) if s3b else None
    fx = re.search(r"FIXED-A M 9:.*?r_1 (\S+)\s+\[(\d+) s, (\d+) residuals\]", text)
    d["fixed"] = fx is not None
    d["wall"] = int(fx.group(2)) if fx else None
    d["end"] = {int(a): b for a, b in re.findall(r"F_(\d+)/F_1 = .*? r_\d+ (\S+)$", text, re.M)}
    tt = re.findall(r"\[(\d+) s total\]", text)
    d["last_t"] = int(tt[-1]) if tt else None
    return d


def main():
    mut = next((a.split("=")[1] for a in sys.argv if a.startswith("--mutate=")), "")
    out = next((sys.argv[sys.argv.index("--md") + 1] for a in sys.argv if a == "--md"), None)
    man = list(MANIFEST)
    if mut == "xi":
        man[2] = man[2][:3] + ("0.12",) + man[2][4:]
    if mut == "predict":
        man[9] = man[9][:8] + (False,) + man[9][9:]
    bad, rows, notes = 0, [], []
    for i, (lab, key, name, xi, ap, h5, h7, rtol, predict, fm, code, old) in enumerate(man):
        path = os.path.join(R, D[key], name)
        if not os.path.exists(path):
            notes.append(f"{lab} {name}: log not found" + (" (allowed)" if "--allow-missing" in sys.argv else ""))
            bad = bad or ("--allow-missing" not in sys.argv)
            continue
        text = open(path, encoding="utf-8", errors="replace").read()
        if mut == "count" and i == 9:
            text = text.replace("level 5 solved", "level 5 SOLVED", 1)
        d = parse(text, old)
        chk = []
        if d["xi"] is not None and (abs(d["xi"] - float(xi)) > 5.1e-5 or abs(d["ap"] - float(ap)) > 5.1e-5):
            chk.append(f"radii line says AP {d['ap']} XI {d['xi']}, manifest AP {ap} XI {xi}")
        if d["k"] is not None and d["k"] != (10 if predict else 8):
            chk.append(f"K line says {d['k']} residuals, manifest predict={predict}")
        if len(d["solves"]) != d["n_solved_lines"]:
            chk.append(f"{len(d['solves'])} parsed level-5 solves against {d['n_solved_lines']} 'level 5 solved' lines")
        if d["n_top_stops"] is not None and d["n_top_stops"] != d["n_solved_lines"]:
            chk.append(f"{d['n_top_stops']} level 5 (top) stop lines against {d['n_solved_lines']} solved lines")
        if chk:
            bad = 1
            notes.append(f"CHECK FAILED {lab} {name}: " + "; ".join(chk))
        ends = ", ".join(two(s[0]) for s in d["solves"]) or "none finished"
        stops = "not printed (old format)" if old else ("; ".join(f"{n} {r}" for r, n in sorted(d["stops5"].items(), key=lambda kv: -kv[1])) or "-")
        if d["l3solved"] and d["fixed"]:
            l3 = (f"{len(d['l3its'])} accepted it, " if d["l3its"] else "") + (f"stop {d['l3stop'][1]} at {two(d['l3stop'][0])}" if d["l3stop"] else f"solved {two(d['l3solved'][0])} (no stop line printed)")
        elif d["l3its"]:
            l3 = f"{len(d['l3its'])} accepted it: {', '.join(two(x) for x in d['l3its'])} (unfinished)"
        else:
            l3 = "not reached"
        e = d["end"]
        endv = ", ".join(f"{two(e[k])}" for k in (3, 5, 7, 9) if k in e) if d["fixed"] and e else "-"
        exf = path[:-4] + ".exit"
        extext = open(exf, encoding="utf-8", errors="replace").read().strip() if os.path.exists(exf) else ""
        secs = re.search(r"after (\d+) s", extext)
        secs = secs.group(1) if secs else str(d["last_t"])
        if d["fixed"]:
            how = f"own end, {d['wall']} s"
        elif "capped" in extext:
            how = f"capped at {secs} s"
        elif extext.startswith("exit 1"):
            how = f"stopped by me after {secs} s"
        else:
            how = f"unfinished (no exit file), about {d['last_t']} s"
        rows.append(f"| {lab} | {xi} / {ap} | {h5} | {h7} | {rtol} | {'yes' if predict else 'no'} | {fm} | {code} | {ends} | {stops} | {l3} | {endv} | {how} |")
    head = ("| run | XI / AP | level-5 step | levels 7, 9 step | rtol | --predict | --floor_max | code | level-5 solve ends | level-5 stops | level 3 | end r_3, r_5, r_7, r_9 | how it ended |\n"
            "|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    txt = head + "\n" + "\n".join(rows) + ("\n\n" + "\n".join(notes) if notes else "")
    print(txt)
    if out:
        open(out, "w", encoding="utf-8", newline="\n").write(txt + "\n")
    sys.exit(bad)


if __name__ == "__main__":
    main()
