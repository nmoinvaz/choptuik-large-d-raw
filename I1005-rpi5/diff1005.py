"""#1005: |sigma_n(truncated) - sigma_n(full)| from the two JSONs.  python3 diff1005.py TRUNC.json [n]   (venv python for mpmath, run from solver/proof; n default 4)
sigma_n is entry n of sigma_str (entry 0 is sigma_0 = 1, which the logs' 'sigma_4 =' lines agree with). The full series is scan45J1500's (K 45, J 1500, 1280 bits)."""
import json, sys
import mpmath as mp
mp.mp.dps = 40
FULL = "../inner_amp/scan45J1500/sigF_w1.0000_K45_J1500_p1280.json"
t = json.load(open(sys.argv[1])); n = int(sys.argv[2]) if len(sys.argv) > 2 else 4
f = json.load(open(FULL))
z = lambda p: mp.mpc(mp.mpf(p[0]), mp.mpf(p[1]))
a, b = z(t["sigma_str"][n]), z(f["sigma_str"][n])
if "--mutate" in sys.argv:
    b = z(f["sigma_str"][n - 1])      # the wrong order: must change the answer
print(f"{sys.argv[1]}: M {t['M']} K {t['K']} J {t['J']} dps {t['dps']}  sigma_{n}(trunc) = {mp.nstr(a, 16)}  sigma_{n}(full) = {mp.nstr(b, 16)}  |diff| = {mp.nstr(abs(a - b), 6)} ")
