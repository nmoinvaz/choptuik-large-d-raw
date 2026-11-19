"""#1012: control B' of noise_r5.py after control B (x5 at rel 1e-12) fired: x5 perturbed at rel 1e-9 and 1e-8 (8 samples each), to measure the slope of the corrected r5 in x5 above the noise. BelowNormal."""
import os, subprocess, sys, time
HERE = os.path.dirname(os.path.abspath(__file__))
env = dict(os.environ, INNER_NB_RTOL="1e-13", PYTHONDONTWRITEBYTECODE="1", PYTHONIOENCODING="utf-8")
for rel, n in (("1e-9", "8"), ("1e-8", "8")):
    t0 = time.time()
    with open(os.path.join(HERE, "logs", f"noise_r5_x5_{rel}.log"), "w", encoding="utf-8", newline="\n") as f:
        rc = subprocess.run([sys.executable, "-u", os.path.join(HERE, "noise_r5.py"), "D:/choptuik-h9b/solver/inner_stokes", "x5", rel, n,
                             os.path.join(HERE, "logs", f"noise_r5_x5_{rel}.json")], cwd=HERE, env=env, stdout=f, stderr=subprocess.STDOUT, creationflags=0x4000).returncode
    with open(os.path.join(HERE, "logs", "noise_exits.txt"), "a") as g:
        g.write(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())} UTC x5_{rel} exit {rc} after {time.time() - t0:.0f} s\n")
