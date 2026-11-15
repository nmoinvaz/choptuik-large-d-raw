# I867-mac: the reviewer's reruns and checks of fixed_point_M_b.py, the second start-value implementation

Machine: mac (Apple M5 Mac), `.venv` of the main checkout (Python 3.13.15, python-flint 0.9.0 with FLINT 3.6.0,
mpmath for the reviewer's quadratures), one process at nice 10. Issue:
https://github.com/nmoinvaz/choptuik-large-d/issues/867. The files under review are
`solver/proof/fixed_point_M_b.py` and `solver/proof/fixed_point_M_b_check.py` at main ecfc1b92 (last changed by
6b92ee40). The reviewer's scripts are in `solver/proof/review_867/`, branch `wip/sa-867`, and the review note is
`proof/A_M_b_review.md`.

## The authors' runs, rerun

`review_867/rerun_runs.sh <python> <raw clone> <output>` reran, from `solver/proof/`, the 32 runs of
`I427-mac/run_i427.sh` and the 6 of `I866-mac/run_i866.sh`. `exits.txt` has each run's exit status and the status it
must have. All 38 are as required, and equal to the authors'. `exits_at_51dceb1f.txt` is the same for the 32 runs on
the files before #866. Each run's log is `<name>.log`, and the three `start_*.json` are the start sets it wrote.

## The reviewer's checks

| log | check | verdict |
|---|---|---|
| `rv_system.log`, `rv_system_M3.log` | K1: the module's residual numerators against inner_np.py's equations and rhs, and its series | PASS. With `--mutate=scale` and `--mutate=sign`: FAIL, as required |
| `rv_kernel.log` | K2: `fast_norm` against quadrature in the 1417 cases the module asks for | PASS, largest true value 0.999815 of the bound |
| `rv_kernel_mut_offbyone.log` | K2 with the reviewer's mutation, one integration by parts too many | FAIL, as required: 2834 of 11336 values above the bound, by up to 0.68%. The authors' five checks behind it all pass |
| `rv_lipschitz.log`, `rv_lipschitz_M3.log` | K3: every entry of the Lipschitz matrix and of the forcing against the true linearization | PASS, 0 of 283 entries above the bound at M = 5 |
| `rv_lipschitz_mut_nolabel.log` | K3 without the label term of the majorant | FAIL, as required: 4 entries above the bound |
| `rv_lipschitz_mut_gpdrop.log` | K3 without [G P] in the majorant, and the authors' Lipschitz comparison with the same | both FAIL: both notice |
| `rv_cli_precision.log` | K4: the precision at which the command line reads `--x`, and the guard on the weight exponent | N = 78 at 53 bits against 105 at 512 bits. The guard fires |

Commands, from `solver/proof/review_867/`:

```
python3 rv_system.py [--M=3] [--mutate=scale|sign]
python3 rv_kernel.py [--mutate=offbyone --ray=<raw clone>/I38-macm3/lemma6b1_runs_M5_cert/ray.json]     # 4 min each
python3 rv_lipschitz.py [--M=3] [--mutate=nolabel|gpdrop]                                                # 2 min each
python3 rv_cli_precision.py --ray=<raw clone>/I38-macm3/lemma6b1_runs_M5_cert/ray.json
```
