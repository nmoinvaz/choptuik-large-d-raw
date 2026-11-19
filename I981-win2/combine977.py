"""#977: m7_outer.py --local over centre solves from several runs.

    python combine977.py TAG --cen LOG [LOG ...] --off LOG_dA LOG_dw

Runs m7_outer.py --local (solver/inner_stokes of the code worktree, RUN_SRC) with every --cen log as a centre solve (m7_outer keeps
those with |r_3| < 1e-6 and averages their r_1) and the two --off logs as the offsets, and writes logs/m7_outer_win2_<TAG>.txt in
run_job976's format (header `# xi1`, the command, the output, the exit), so zero_digits977.py reads it.
"""
import os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
PY = os.environ.get("RUN_PY", "C:/Users/nathan/Source/venv-i962/Scripts/python.exe")
SRC = os.environ.get("RUN_SRC", "D:/choptuik-i962/solver/inner_stokes")
a = sys.argv[1:]
tag, i, j = a[0], a.index("--cen"), a.index("--off")
cen, off = a[i + 1:j], a[j + 1:]
assert len(off) == 2 and cen, "need centre logs and two offset logs"
cmd = [PY, "m7_outer.py", "--local"] + cen + ["--"] + off
out = subprocess.run(cmd, cwd=SRC, env=dict(os.environ, PYTHONIOENCODING="utf-8"), capture_output=True, text=True, encoding="utf-8",
                     errors="replace", creationflags=0x00004000)
txt = out.stdout + out.stderr + f"(exit {out.returncode})\n"
os.makedirs(os.path.join(HERE, "logs"), exist_ok=True)
with open(os.path.join(HERE, "logs", f"m7_outer_win2_{tag}.txt"), "w", encoding="utf-8", newline="\n") as f:
    f.write(f"# xi1 0.15\n$ {' '.join(cmd)}\n" + txt)
print(txt)
sys.exit(out.returncode)
