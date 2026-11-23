# I1079-macm3: Theorem A(M = 3)'s certificate tried at the two excited M = 3 zeros (#1079)

Machine: macm3 (Apple M3, 8 CPUs, 24 GB, macOS 26.3.1, arm64; runner macm3b). Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1079
(from #1076 https://github.com/nmoinvaz/choptuik-large-d/issues/1076 and #1021). Task from the coordinator (hc of 2026-11-23, after the zero0_cert acceptance).
Written 2026-11-23 13:36 UTC, before any step ran. The steps, stops and acceptance are the issue's; the choices below are mine and are named.

## The question

Do the two excited zeros of the M = 3 multiplier, located in extended precision in #1076 (`zero_mp.py`, orientation +1 each), have a Krawczyk certificate of the kind of
Theorem A(M = 3) (`proof/A_M.md` section 6.2: K(X) in int X on a box h = 1e-10, w = 4e-16 around the zero)?

| zero | A | w/w_inf | source |
|---|---|---|---|
| x1 | 3.446218246366727 | 0.347606965217407 | #1076 zero1 run (raw c31b5d24), last row; `zero_mp.py` at 2dada6c4 |
| x2 | 3.526473056695715 | 0.211497981391215 | #1076 zero2 run (comment 7099358732), the point after the unapplied step |

## Code and versions

- Certificate code: a clean detached worktree of main, `~/Source/choptuik-large-d-1079`, at **a4cd5eaa7b297ffc6f171551fa15ba054e970e21** (`solver/proof`: `certify_M.py` blob 330d3a22,
  `certify_M_sys.py` 62ad5c15, `certify_M_lohner.py` 100c2cb9, `certify_M_recheck.py` 8ac746c6, `fixed_point_M.py` 71cee337 with sha256 prefix 589e5a810bc50289, the lemma's file as `proof/A_M.md` section 6.2 names it,
  `validated_int.py` 39794d0c). Python 3.14.3 (`~/Source/venv-macm3-1058b`), **python-flint 0.9.0, FLINT 3.6.0**, numpy 2.5.4, mpmath 1.3.0. Nothing in the worktree's tracked files is changed; the runs add new files named with the tags x1 and x2.
- Step 1 (F_3): `~/Source/choptuik-inner-mp` at **79d4af3b47ea39310ab5263f63ff3b8f1609f6eb** (feat/inner-mp; against 90d914e9 only `zero_mp.py` changed, 1 line; `value_mp.py` is the one of pass 3 and the zero runs).

## Plan (the issue's work list; `proof/A_M.md` section 8 commands, with the excited zeros as centres)

All certify commands from `solver/proof`, `OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1`, `nice -n 10`, own session under caffeinate, one process each.

1. **F_3 at each zero**: `value_mp.py point A WF F3RE F3IM` with the F_3 of the nearest valued cache record (the cache of #1076 after pass 3, `I1021-macm3/fu022mp/m3/points_M3_r0.17.jsonl`, 3605 lines, sha256 8d7cb732...;
   "valued" as `zero_mp.py` reads it: `info` below 1e-8 and a finite F_3; the records are named in the results), 2 processes. Then p = (A, w/w_inf, B3 = -2 Im F3, C3 = 2 Re F3).
2. **Checks and centre** (`solver/proof`): `certify_M.py startcheck 3` (contains) and `--mutate` (must fail); `crosscheck 3` (agree) and `--mutate` (must DISAGREE);
   `refine 3 --p=<p> --iters=3 --tag=x1` and `--tag=x2`. **Stop if refine moves A or w/w_inf by more than 1e-8 from the zero_mp values above** (the models would differ). Extra, seconds each and named in `proof/A_M.md` section 8 as the first checks:
   `certify_M_sys.py selftest` (PASS) and `--mutate=coupling` (must FAIL).
3. **Certificate** for each zero: `certify_M.py plan --centre=data/A_M_refine_M3_x1.json`; `box 3 --centre=data/A_M_refine_M3_x1.json --use_out --h=1e-10 --w=4e-16 --out=data/A_M_box_M3x1_1e-10.json --log=logs/A_M_box_M3x1_1e-10.log`;
   `krawczyk --box=data/A_M_box_M3x1_1e-10.json --hier`; `controls --box=...` (C0 to C8, exit 0 iff all as expected); `krawczyk ... --hier --mutate=hier`; `certify_M_recheck.py data/A_M_box_M3x1_1e-10.json` and its `--mutate` (must fail).
   Same for x2 (files `..._M3x2_...`).

## Stops and acceptance (the issue's)

Stops: any failing check; refine not converging; the box run failing (path, start data or a singularity); refine moving A or w/w_inf by more than 1e-8 from the zero_mp values. On any of these: report the cause and change nothing.
A Krawczyk test that fails at h = 1e-10 is reported with its margins; a smaller box needs the coordinator's word.
Acceptance: for each zero, the Krawczyk test passes with every control as documented and the recheck agreeing, or the obstacle is named precisely (which step, which quantity) with the logs. The result is a Krawczyk enclosure
(rigorous given the start-value lemma `fixed_point_M.start_data_M` and Braaksma's theorem, with the trusted code named in `proof/A_M.md`), or it is numerical evidence with the obstacle named.

## Known before the run (read from `certify_M.py`, not a result)

- `krawczyk --hier` compares the box with `HIER[3]`, the stored double-precision solves of the **fundamental** zero (A 2.7265, w/w_inf 1.0156). If the Krawczyk test passes, the exit code is that of `hier_check`
  (`certify_M.py` lines 875-877), so at an excited zero `--hier` can only fail (its containment (a) is false by 0.7 in A), and `--hier --mutate=hier` fails trivially. I run the test **without `--hier`** as well, so that the
  Krawczyk verdict is read on its own, and report the `--hier` runs as run, with this reason; I do not edit the script.
- `start_data_M` raises unless the fixed point holds on the set and on its Cauchy box; at these parameters (far from the fundamental zero) the start data may not exist: that would be the obstacle named (box step).
- `startcheck 3` and `crosscheck 3` check the system, start data and path at fixed points near the fundamental zero (`XCHECK[3]` p = (2.7, 1.0, 0.14, 0.01)), not at the excited zeros.

## Output

Live files are written by the scripts into `~/Source/choptuik-large-d-1079/solver/proof/{data,logs}` (new names only) and copied here at each milestone (not the `.ckpt` files): `data/`, `logs/`, `runner/` (my wrappers, launcher outputs,
session checks), `steps.txt`. Memory and disk: alerts only to the coordinator (available memory under 2 GiB, free memory under 8%, disk under 3 GiB); nothing is stopped for memory.
