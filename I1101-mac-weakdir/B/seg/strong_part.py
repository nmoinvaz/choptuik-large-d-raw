import sys
sys.path.insert(0, "/Users/nathan/Source/choptuik-1101w/solver/matter")
import numpy as np
from i1101_weakdir import describe_right, unknown_labels, bands_of
from ell_fastm import load_system
d = np.load("/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/0726f216-9eae-4698-9a94-e79a55d0f725/scratchpad/w1101/jac/svd_src.npz"); s = d["s"]; Vt = d["Vt"]
S, za, rec, same, msg = load_system("/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/0726f216-9eae-4698-9a94-e79a55d0f725/scratchpad/w1101/B/in/l1kc55k035m.jsonl", "/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/0726f216-9eae-4698-9a94-e79a55d0f725/scratchpad/w1101/B/in/sol_l1kc55k035m_D16.0000.npy", 16.0)
zb = np.load("/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/0726f216-9eae-4698-9a94-e79a55d0f725/scratchpad/w1101/B/seg/sol_all_D16.0000.npy")
dz = zb - za
nul, weak, strong = bands_of(s)
c = Vt @ dz
cs = np.zeros_like(c); cs[strong] = c[strong]
part = Vt.T @ cs
lab = unknown_labels(S)
dr = describe_right(part ** 2, lab)
print("strong part |P dz|", np.linalg.norm(part))
print(" fields", dr["fields"]); print(" nodes", dr["nodes"]); print(" harmonic bands [0],[1-3],[4-7],[8-15],[16-31],[32-]", dr["hbands"]); print(" top k", dr["top_k"])
n = len(s); order = np.argsort(-np.abs(cs))[:8]
print(" largest strong coordinates (index from the smallest, s/smax, coord):", " ".join(f"[{n-1-i} {s[i]/s[0]:.2e} {c[i]:+.2e}]" for i in order))
# same for K35 - U40 and K50 - U40
for nm, f in (("K35-U40", "/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/0726f216-9eae-4698-9a94-e79a55d0f725/scratchpad/w1101/in/sol_l1kc55u040_D16.0000.npy"),):
    u = np.load(f); dd = za - u; cc = Vt @ dd; cc[nul] = 0; cc[weak] = 0; pp = Vt.T @ cc
    r = describe_right(pp ** 2, lab)
    print(nm, "strong |P dz|", np.linalg.norm(pp), "fields", r["fields"], "hbands", r["hbands"], "top k", r["top_k"][:4])
    print("   nodes", r["nodes"])
