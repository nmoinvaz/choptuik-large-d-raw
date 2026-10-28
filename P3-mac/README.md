# P3-mac: the M = 5 point run (C^1 along the centre trajectory) for proof/P3_scope.md section 4

Machine: mac (Apple M5), python-flint 0.9.0 (main .venv), one process at nice 10.
Task: T90, comms entry "cloud to mac" of 2026-10-28 10:34 UTC. Source: `solver/proof` of the main checkout at d16a241 (4eab93c or later).

Command (from `solver/proof`, OUT = this folder):

    python3 certify_M.py point 5 --p=$(jq -r '.p_out | join(",")' data/A_M_refine_M5_d.json) --out=OUT/A_M_point_M5.json --log=OUT/A_M_point_M5.log
