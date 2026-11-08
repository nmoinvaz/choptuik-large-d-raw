"""I190-macm3: how the converged D 45 M 48 state moves with the cut: max |z(kf) - z(kf')| over the unknowns (hi + lo), from the saved states of
I178-macm3 (kf 13 to 21) and this folder (kf 21 to 27).    python3 state_vs_kf.py"""
import numpy as np
P = {13: "../I178-macm3/data_kf13", 15: "../I178-macm3/data_kf15", 17: "../I178-macm3/data_kf17", 19: "../I178-macm3/data_kf19", 21: "data_kf21",
     23: "data_kf23", 25: "data_kf25", 27: "data_kf27"}
Z = {}
for K, d in P.items():
    s = np.load(f"{d}/modecount_state_D45.0507_M48_kf{K}.npz", allow_pickle=True)
    Z[K] = s["zh"] + s["zl"]
Ks = sorted(Z)
print("| kf | kf next | max abs difference of the states | Delta(kf) - Delta(27) |\n|---|---|---|---|")
for a, b in zip(Ks[:-1], Ks[1:]):
    print(f"| {a} | {b} | {np.abs(Z[b] - Z[a]).max():.2e} | {Z[a][-1] - Z[27][-1]:+.2e} |")
print(f"| 27 | - | - | {Z[27][-1] - Z[27][-1]:+.2e} |")
