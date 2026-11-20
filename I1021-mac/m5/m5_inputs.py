"""#1021: the inputs of an M = 7 solve from one converged fixed-(A, w) M = 5 hier.py log: its (A, w/w_inf) as passed,
xi1, and x = (B3, C3, B5, C5) from the last 'level 3 it' line (the converged state, 9 digits as printed), with the
FIXED-A block's F_3/F_1, F_5/F_1 and residuals; refuses a log whose |r_3| or |r_5| is not under 1e-6.
    python m5_inputs.py LOG NAME [COUNT.json] > OUT.json   (COUNT: the relocation's count file, for the M = 3 location)"""
import json, re, sys
log, name = sys.argv[1], sys.argv[2]
t = open(log).read()
cmd = t.splitlines()[0][2:]
a = re.search(r"hier\.py 5 ([0-9.]+) ([0-9.]+) --x=([0-9.,+-]+)", cmd)
xi = float(re.search(r"--xi1=([0-9.]+)", cmd).group(1))
its = re.findall(r"level 3 it \d+: \|r_3\| ([0-9.e+-]+) .*?x \[([^\]]+)\]", t)
f3 = re.findall(r"F_3/F_1 = ([+-][0-9.]+)([+-][0-9.]+)i.*?r_3 ([0-9.]+e[+-]\d+)", t)[-1]
f5 = re.findall(r"F_5/F_1 = ([+-][0-9.]+)([+-][0-9.]+)i.*?r_5 ([0-9.]+e[+-]\d+)", t)[-1]
r3, r5 = float(f3[2]), float(f5[2])
if not (r3 < 1e-6 and r5 < 1e-6):
    raise SystemExit(f"{log}: |r_3| {r3:g}, |r_5| {r5:g}, not converged")
x = [float(v) for v in its[-1][1].split(",")]
F3, F5 = complex(float(f3[0]), float(f3[1])), complex(float(f5[0]), float(f5[1]))
out = dict(name=name, issue=1021, A=float(a.group(1)), wf=float(a.group(2)), xi1=xi, x_B3_C3_B5_C5=x[2:6],
           F3_over_F1=[F3.real, F3.imag], F5_over_F1=[F5.real, F5.imag], abs_F5_over_F3=round(abs(F5) / abs(F3), 4),
           r3=r3, r5=r5, last_level3_r3=float(its[-1][0]), start_x_of_this_solve=[float(v) for v in a.group(3).split(",")],
           log=log.split("/")[-1], command=cmd)
if len(sys.argv) > 3:
    z = [z for z in json.load(open(sys.argv[3]))["zeros"] if z.get("located_r1b") or z.get("located")]
    out["m3_zero"] = dict(W=z[0]["W"], cell=z[0]["cell"], located=z[0].get("located"), located_r1b=z[0].get("located_r1b"))
print(json.dumps(out, indent=1))
