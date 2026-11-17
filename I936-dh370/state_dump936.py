"""#936: #934's state_dump.py, unchanged beside this file, with its STATES replaced by one state of #841's chain.

    python state_dump936.py HP_DIR STATES_ROOT PREFIX [--control]
    python state_dump936.py --compare OLD NEW CTL

Same arguments and the same dump and compare as state_dump.py (read its docstring); only the state differs."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import state_dump

state_dump.STATES = {"i841_D254": "I841-dh370/chain/anm_pin3_D254.9015.npz"}

if __name__ == "__main__":
    a = sys.argv[1:]
    sys.exit(state_dump.compare(*a[1:4]) if a[0] == "--compare" else state_dump.dump(a[0], a[1], a[2], "--control" in a))
