# #942 arm (d): rung_info.py with mp.mp.dps set before anything parses D_str (t5's test of the parse-precision trap)
import runpy, sys
import mpmath as mp
mp.mp.dps = int(sys.argv.pop(1))
print("dps before the script:", mp.mp.dps, flush=True)
sys.argv = [sys.argv[1]] + sys.argv[2:]
runpy.run_path(sys.argv[0], run_name="__main__")
