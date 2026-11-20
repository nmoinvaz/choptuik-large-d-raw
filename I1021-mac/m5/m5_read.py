"""#1021: |F5/F3| from one hier.py M = 5 fixed-(A, w) log (its last FIXED-A block), against #1027's rule (0.3 or
more drops the zero); exit 1 when the log has no converged block (|r_3|, |r_5| below 1e-6).
    python m5_read.py LOG"""
import re, sys
t = open(sys.argv[1]).read()
f3 = re.findall(r"F_3/F_1 = ([+-][0-9.]+)([+-][0-9.]+)i.*?r_3 ([0-9.]+e[+-]\d+)", t)
f5 = re.findall(r"F_5/F_1 = ([+-][0-9.]+)([+-][0-9.]+)i.*?r_5 ([0-9.]+e[+-]\d+)", t)
r1 = re.findall(r"FIXED-A M 5: .*?r_1 ([+-][0-9.]+e[+-]\d+)([+-][0-9.]+e[+-]\d+)i", t)
if not (f3 and f5 and r1):
    print(f"{sys.argv[1]}: no FIXED-A block"); sys.exit(1)
F3, F5 = complex(float(f3[-1][0]), float(f3[-1][1])), complex(float(f5[-1][0]), float(f5[-1][1]))
r3, r5 = float(f3[-1][2]), float(f5[-1][2])
q = abs(F5) / abs(F3)
ok = r3 < 1e-6 and r5 < 1e-6
print(f"{sys.argv[1].split('/')[-1]}: F3/F1 {F3:.6f}, F5/F1 {F5:.6f}, |F5/F3| {q:.4f}, |r_3| {r3:.1e}, |r_5| {r5:.1e}, "
      f"r_1 {complex(float(r1[-1][0]), float(r1[-1][1])):.4e}: "
      + ("not converged" if not ok else ("dropped by #1027's rule (|F5/F3| >= 0.3)" if q >= 0.3 else "kept (|F5/F3| < 0.3)")))
sys.exit(0 if ok else 1)
