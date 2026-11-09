#!/usr/bin/env python3
"""I236-win2: amp_flint_par.py with the products of an order summed in a fixed order, whatever --procs is (mechanism test of #236).

    python -u amp_flint_par_fixsum.py wf K J [prec] [--procs N] [...]   the arguments and output of amp_flint_par.py

The module of solver/inner_amp (main of D:\choptuik-large-d, unchanged) is imported and AmpPar._products replaced. In the
original each worker sums its chunk of tasks (tasks[i::nw]) per group and the main adds the workers' partial sums, so the order
of the additions follows the worker count. Here every task is a chunk of its own (dealt to the workers as before, tasks[i::nw]),
the main receives the single products and adds them per group in task order, the same association as the serial path
(((P1 + P2) + P3) + ...). With no workers the same per-task sum is formed in process, so every --procs uses this one summation."""
import os, pickle, sys

sys.path.insert(0, os.path.join(os.environ.get("INNER_AMP", r"D:\choptuik-large-d\solver\inner_amp")))
import amp_flint_par as M


def _products_fixed(self, k, tasks):
    J = self.J
    res = {}

    def add(part):
        for g, T in part.items():
            res[g] = T if g not in res else M._add_rows(res[g], T)

    if not self.workers:
        for t in tasks:
            add(M._products(self.ctab, k, J, [t]))
    else:
        nw = len(self.workers)
        mine = [list(range(i, len(tasks), nw)) for i in range(nw)]
        for (p, conn), idxs in zip(self.workers, mine):
            for idx in idxs:
                conn.send_bytes(pickle.dumps(("prod", k, J, [tasks[idx]]), protocol=pickle.HIGHEST_PROTOCOL))
        got = {}
        for (p, conn), idxs in zip(self.workers, mine):
            for idx in idxs:
                got[idx] = {g: M._de_rows(blob) for g, blob in pickle.loads(conn.recv_bytes()).items()}
        for idx in range(len(tasks)):
            add(got[idx])
    zero = [[M.ZERO] * (k + 1) for _ in range(J + 1)]
    return {g: self.expand(res.get(g, zero), k) for g in set(t[0] for t in tasks) | set(res)}


M.AmpPar._products = _products_fixed

if __name__ == "__main__":
    M.main(sys.argv)
