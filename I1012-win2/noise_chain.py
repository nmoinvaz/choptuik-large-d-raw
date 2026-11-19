"""#1012: the noise measurements of noise_r5.py in sequence (BelowNormal): nested 1e-12 x16, nested 1e-10 x16, control B (x5 1e-12) x6. Exits to logs/noise_exits.txt."""
import os, subprocess, sys, time
HERE = os.path.dirname(os.path.abspath(__file__))
env = dict(os.environ, INNER_NB_RTOL="1e-13", PYTHONDONTWRITEBYTECODE="1", PYTHONIOENCODING="utf-8")
for mode, rel, n, tag in (("nested", "1e-12", "16", "nested_1e-12"), ("nested", "1e-10", "16", "nested_1e-10"), ("x5", "1e-12", "6", "x5_1e-12")):
    t0 = time.time()
    with open(os.path.join(HERE, "logs", f"noise_r5_{tag}.log"), "w", encoding="utf-8", newline="\n") as f:
        rc = subprocess.run([sys.executable, "-u", os.path.join(HERE, "noise_r5.py"), "D:/choptuik-h9b/solver/inner_stokes", mode, rel, n,
                             os.path.join(HERE, "logs", f"noise_r5_{tag}.json")], cwd=HERE, env=env, stdout=f, stderr=subprocess.STDOUT, creationflags=0x4000).returncode
    with open(os.path.join(HERE, "logs", "noise_exits.txt"), "a") as g:
        g.write(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())} UTC {tag} exit {rc} after {time.time() - t0:.0f} s\n")
