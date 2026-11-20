"""#1021: run a script under faulthandler, every Python thread's stack dumped to stderr each PERIOD seconds, to find
where a solve that prints nothing spends its time.
    python trace_run.py PERIOD SCRIPT ARGS...        (from the script's directory)"""
import faulthandler, os, runpy, sys

period = float(sys.argv[1])
sys.argv = sys.argv[2:]
sys.path.insert(0, os.path.dirname(os.path.abspath(sys.argv[0])))
faulthandler.dump_traceback_later(period, repeat=True)
runpy.run_path(sys.argv[0], run_name="__main__")
