"""#903 grip: kern_run.py SITE SCRIPT ARGS... runs hp's SCRIPT in this process after logging the hpkernel it loads.

From 07:02 to about 14:40 UTC on 2026-11-17 site2 lacked hpkernel/__init__.py, and runs silently loaded venv-314's Nov 8
kernel (multidouble 4.0.0). So this imports hpkernel first, in the process that then runs SCRIPT (whose own import reuses
it), and prints its __init__.py, its extension module and the crate versions the module embeds (the cargo source paths
in its panic strings: multidouble-X.Y.Z, multishoot-X.Y.Z).

Check (can fail): the package lies under SITE and the module embeds exactly one multidouble version, 4.2.1 (main
3c35f0c's build), else exit 7 before SCRIPT runs. Control: SITE given as a path without the package, which resolves to
venv-314's kernel (multidouble 4.0.0) and must exit 7.

Run from hp/: PYTHONPATH=SITE python3 kern_run.py SITE near_null.py ARGS...
"""
import glob
import os
import re
import runpy
import sys

WANT = "4.2.1"
site, script = os.path.realpath(sys.argv[1]), sys.argv[2]
sys.path.insert(0, os.getcwd())                 # hp/, as when SCRIPT runs directly
import hpkernel  # noqa: E402

pkg = os.path.dirname(os.path.realpath(hpkernel.__file__))
so = sorted(glob.glob(os.path.join(pkg, "_hpkernel*.so")) + glob.glob(os.path.join(pkg, "_hpkernel*.pyd")))
crates = {}
if so:
    blob = open(so[0], "rb").read()
    for name in (b"multidouble", b"multishoot", b"multisolver"):
        crates[name.decode()] = sorted({m.decode() for m in re.findall(name + rb"-(\d+\.\d+\.\d+)", blob)})
print(f"hpkernel {hpkernel.__file__}; module {so[0] if so else 'none'}; crates "
      + ", ".join(f"{k} {'/'.join(v) or '-'}" for k, v in crates.items()), flush=True)
if not pkg.startswith(site + os.sep) or crates.get("multidouble") != [WANT]:
    print(f"hpkernel is not site2's (multidouble {WANT}): stop", flush=True)
    sys.exit(7)
sys.argv = [script] + sys.argv[3:]
runpy.run_path(script, run_name="__main__")
