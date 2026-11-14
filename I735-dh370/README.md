# I735-dh370: #603's D 252.2497 state on the layouts with last node 0.80 and 0.92, polished, with its series' singularity

Machine dh370 (Fedora 45, i7-8700, 12 threads, 31 GB), issue https://github.com/nmoinvaz/choptuik-large-d/issues/735.

`run_735.sh 080 092` (written by the coordinator), worktree choptuik-large-d-685 at main f40deb4a, venv of
choptuik-large-d-614 (the 3c35f0c build), 12 threads, nice 10:
- `jet_singularity.py locate` on #685's series at the 0.70 layout from the same state (`I685-dh370/repro/jet_pin3_D252.2497.npz`), the reference;
- per layout L: `renode_o.py` to the nodes 0.3,0.4,0.5,0.6,L (exit 0) and its `--mutate sign` control (exit 1);
- the base polish, #603's corrector flags with `--steps 0 --save_base 1 --tol 1e-30 --qd_it 12 --elim_switch 0`;
- where the polish converges below 1e-60: the 24-order series with #712's flags (`--steps 1 --qd_it 20 --save_jet 2`), and `locate` on its jet.

Pass criteria, written before the run (#735): for each layout, the polish converges below 1e-60 or its step history is
reported; for a converged one, the distance between its nearest Padé pole's D* and the 0.70 layout's (252.31 + 5.81i
from #686) is compared with the poles' spread. The renode controls must fail. `exits_735.txt` has one line per step.
