# #942 arm (d): which hpkernel rung_info.py loads, then the script itself
import runpy, sys
import hpkernel, hpkernel._hpkernel as K
print("hpkernel", hpkernel.__file__, "| so", K.__file__, flush=True)
sys.argv = sys.argv[1:]
runpy.run_path(sys.argv[0], run_name="__main__")
