"""#1002: per-solve table of the 40 solves (stdlib).  python3 summarize1002.py LOGDIR > solves_table.md   (run from solver/inner_stokes; LOGDIR = logs)"""
import glob, re, sys
d = sys.argv[1]
groups = [("0.145 centre (#1000)", "xi0145_s98?"), ("0.145 dA", "xi0145_dA_s100?"), ("0.145 dw", "xi0145_dw_s101?"),
          ("0.15 centre", "xi0150_zero_s102?"), ("0.15 dA", "xi0150_dA_s103?"), ("0.15 dw", "xi0150_dw_s104?")]
print("| group | seed | r_1 | \\|r_3\\| | under 1e-6 | residuals | seconds |\n|---|---|---|---|---|---|---|")
for name, pat in groups:
    for f in sorted(glob.glob(f"{d}/hier_nb_M7_rpi5_rtol14_{pat}*.log")):
        t = open(f).read(); seed = re.search(r"_s(\d+)(_r3high)?\.log", f).group(1)
        m = re.findall(r"FIXED-A M 7:.*?r_1 ([+-][0-9.]+e[+-]\d+)([+-][0-9.]+e[+-]\d+)i\s+\[(\d+) s, (\d+) residuals\]", t)[-1]
        r3 = re.findall(r"F_3/F_1 = .*? r_3 ([0-9.]+e[+-]\d+)", t)[-1]
        print(f"| {name} | {seed} | {float(m[0]):+.4f} {float(m[1]):+.4f}i | {r3.replace('e-0', 'e-')} | {'yes' if float(r3) < 1e-6 else 'no'} | {m[3]} | {m[2]} |")
