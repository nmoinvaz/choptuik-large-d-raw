"""#1078: highm_diag.py radius with the state's own solver (the tau-map applied), beside the as-given run.

    cd hp && python3 radius_mapped.py STATE.npz M          highm_diag.radius with solver() replaced by lowD_gamma.build_solver (mapped when meta['map'] is set)
    cd hp && python3 radius_mapped.py STATE.npz M --as_given   the same call with highm_diag's own solver() (an unmapped one): a control, which must print what highm_diag.py radius prints

highm_diag.solver(m, M) is make_solver(D, M, nodes, kt, kc, ks, threads=2): the uniform-grid d/dtheta, whatever meta['map'] says; for a state without a map the two agree bit for bit."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.getcwd())
import highm_diag as H  # noqa: E402

if "--as_given" not in sys.argv:
    import lowD_gamma as LG
    H.solver = lambda m, M, nodes=None: LG.build_solver(m["D"], M, m, 2)[0]
args = [a for a in sys.argv[1:] if not a.startswith("--")]
H.radius(args[0], int(args[1]))
