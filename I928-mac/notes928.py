# #928: the table of matter/SIGMA_DSS.md section 11 for the chain past D 11, from the repository's csvs
# (chain_table.py's delta_D_eta*.csv and mode_table.py's lam_D.csv): every 0.25 in D from 11 to 13, with the first
# difference of lambda over the grid step of 0.0625 that ends at D, and the second difference of the two steps before
import csv, sys
d = sys.argv[1]
def sup(x): return x.replace("-", "−").translate(str.maketrans("0123456789−", "⁰¹²³⁴⁵⁶⁷⁸⁹⁻"))
print("| η | D | Δ | arithmetic | λ | γ = 1/λ | first difference of λ | second difference |")
print("|---|---|---|---|---|---|---|---|")
lam = {}
for r in csv.DictReader(open(d + "/lam_D.csv")):
    if r["M"] == "32" and r["nodes"] == "21" and r["lam"]:
        lam[(r["eta"], float(r["D"]))] = float(r["lam"])
for eta in ("0.3", "1"):
    de = {float(r["D"]): r for r in csv.DictReader(open(d + f"/delta_D_eta{eta}.csv"))}
    for i in range(9):
        D = 11 + 0.25 * i
        h = 0.0625
        l0 = lam[(eta, D)]
        d1 = (l0 - lam[(eta, D - h)]) / h if (eta, D - h) in lam else None
        d2 = ((l0 - lam[(eta, D - h)]) - (lam[(eta, D - h)] - lam[(eta, D - 2 * h)])) / h ** 2 if (eta, D - 2 * h) in lam else None
        m = "quad-double" if de[D]["method"] == "qd" else "double-double"
        print(f"| {eta} | {D:g} | {float(de[D]['Delta']):.12f} | {m} | {l0:.9f} | {1 / l0:.6f} | "
              f"{'' if d1 is None else ('−' if d1 < 0 else '+') + '%.5f' % abs(d1)} | {'' if d2 is None else ('−' if d2 < 0 else '+') + '%.4f' % abs(d2)} |")
