#!/usr/bin/env python3
"""mp_args.py NAME: print A, WF and the --v value (B3,C3,B5,C5) of one extended-precision point, one per line (#1080, exploratory).
x1, x2   the box centres of ../inputs/ (A, w/w_inf, B3, C3 as the full decimal strings of the file), --v=B3,C3,0,0
x1fm     x1's A and w/w_inf, --v = the last level-3 iterate (B3, C3, B5, C5) of ../explore/logs/start_x1_xi0.2_fm.log (the floor_max start at xi1 0.2),
         to the 9 decimals hier prints at --verbose=2"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
M5 = os.path.dirname(HERE)
BOXES = dict(x1="A_M_box_M3x1E2_h1e-12_w1e-13.json", x2="A_M_box_M3x2E2_h1e-12_w1e-12.json")


def main(name):
    box = BOXES["x1" if name == "x1fm" else name]
    p = json.load(open(os.path.join(M5, "inputs", box)))["p"]
    if name == "x1fm":
        t = open(os.path.join(M5, "explore", "logs", "start_x1_xi0.2_fm.log")).read()
        x = re.findall(r"^level 3 it \d+: .* x \[([^\]]*)\]", t, re.M)[-1].split(",")
        v = ",".join(s.strip() for s in x[2:6])
    else:
        v = f"{p[2]},{p[3]},0,0"
    print(p[0])
    print(p[1])
    print(v)


if __name__ == "__main__":
    main(sys.argv[1])
