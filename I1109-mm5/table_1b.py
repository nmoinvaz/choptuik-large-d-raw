"""#1109 stage 1 and 1b: the tables per k_c family from each state's logs (report_*.log, valley_*.log, run_*.log). usage: table_1b.py DIR"""
import re, sys
d = sys.argv[1]
fam = {31: [("ctl7.0", 7.0), ("k31_D8.0", 8.0), ("k31_D9.0", 9.0), ("ctl10.5", 10.5), ("k31_D11.0", 11.0), ("k31_D11.5", 11.5),
            ("k31_D12.0", 12.0), ("k31_D12.5", 12.5), ("k31_D13.0", 13.0), ("k31_D13.5", 13.5), ("k31_D14.0", 14.0)],
       47: [("k47_D10.5", 10.5), ("k47_D11.0", 11.0), ("k47_D11.5", 11.5), ("k47_D12.0", 12.0), ("k47_D13.5", 13.5),
            ("k47_D14.0", 14.0), ("k47_D14.5", 14.5), ("k47_D15.0", 15.0), ("k47_D16.0", 16.0)],
       55: [("D14.5", 14.5), ("D15.0", 15.0), ("D15.5", 15.5), ("D16.0", 16.0), ("D16.5", 16.5)]}
for kc, states in fam.items():
    print(f"\n**k_c {kc}**\n")
    print("| D | s/s_max, two weakest non-null | U_w^T F (two) | \\|F\\| | Gauss-Newton dDelta (full step) | seconds | report exit |")
    print("|---|---|---|---|---|---|---|")
    first = None
    for tag, D in states:
        try:
            run = open(f"{d}/run_{tag}.log").read()
        except FileNotFoundError:
            print(f"| {D} | not run | | | | | |"); continue
        if "SKIPPED" in run:
            print(f"| {D} | SKIPPED: {re.search(r'SKIPPED [^:]*: (.*)', run)[1][:80]} | | | | | |"); continue
        rep = open(f"{d}/report_{tag}.log").read().splitlines()
        val = open(f"{d}/valley_{tag}.log").read()
        wb = re.search(r"weak band .*?: \[(\d+) (\S+) (\S+)\] \[(\d+) (\S+) (\S+)\]", "\n".join(rep))
        base = [l for l in rep if l.startswith("base (")][0]
        F = float(re.search(r"\|F\| (\S+) =", base)[1])
        utf = [float(x) for x in rep[rep.index(base) + 1].split()[2:4]]
        gn = re.search(r"Gauss-Newton step \|dz\| (\S+), dDelta (\S+);", val)
        tot = int(re.search(r"total (\d+) s", run)[1])
        rrc = re.search(r"report rc (\d)", run)[1]
        dd = float(gn[2])
        if first is None and abs(dd) > 1e-6:
            first = D
        print(f"| {D} | {float(wb[3]):.3e}, {float(wb[6]):.3e} (idx {wb[1]}, {wb[4]}) | {utf[0]:+.4e}, {utf[1]:+.4e} | {F:.4e} | **{dd:+.4e}** | {tot} | {rrc} |")
    print(f"\nfirst D with |dDelta| > 1e-6 in the k_c {kc} family: {first if first is not None else 'none'}")
