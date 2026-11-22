# I1072-dh370: gamma on the tau-mapped grid, checked against the uniform grid at D 3.15, then the first gamma below D 3.15 (D 3.0444)

Written before the runs (step 0 started 2026-11-22 21:03 UTC by the clock). Machine `dh370-fedora` (Fedora, i7-8700, 6 cores / 12 threads, 31 GB). Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1072 (the record; its body is the order). Coordinator t5.

## Order (issue #1072, option A of 2026-11-22)

gamma stops at D 3.15 (#1070: gamma(128) = 0.2273872422, M error gamma(128) - gamma(96) = 1.05e-6) because `mode_det` runs only on the dense path, M <= 128. The arctan tau map (#1033, notes/LOW_D_SPEEDUP.md step 5) reaches the uniform M 384 grid's Delta to 1e-12 with M' 160 to 192 at D 3.04 to 3.05. So gamma to about 1e-8 near D 3.04 may fit in M' <= 128. One job at a time, 6 threads, nice 10, each run a systemd user unit (outside the terminal).

0. Environment and checks (this commit's `run0.sh`, unit `i1072a`): `tau_map_gain.py selftest` exit 0 and `--mutate gp` exit 1; `lowD_gamma.py --selftest data/lowD_states/highm15_D3.7000_M96.npz --threads=6` exit 0 and with `--break` exit 1; `tau_map.make_solver_mapped` constructs a solver on this hp build. If it does not, stop and report.
1. Mapped states at D 3.15: `tau_map_gain.py solve <raw>/I927-mac/inputs/lowDhm_x0.000625-0.9_D3.1500_M128.npz --pairs 0.5:96,0.5:128,0.4:96,0.4:128 --states <raw>/I1072-dh370/states --out <raw>/I1072-dh370/solve_D3.15.jsonl --threads 6`; then `lowD_gamma.py --selftest <that uniform state> <one mapped M' 128 state> --threads=6` (exit 0: the gp control moves).
2. gamma on the converged mapped states: `lowD_gamma.py -u <raw>/I1072-dh370/gamma_D3.15.jsonl <mapped states> --threads=6 --lam0=4.397784106690153 --xtol=1e-11`.
3. Only if step 2 passes: the same at D 3.0444 from the uniform M 384 state that #1033's dh610 run used (its README names it), `--pairs 0.4:96,0.4:128,0.3:128`, then gamma with `--lam0` from `lam_guess(3.0444)`.

## Acceptance (the issue's, fixed before the runs)

- Step 0: the four exits as stated (0, 1, 0, 1), and `make_solver_mapped` constructs a solver.
- Step 2, the check: for each L, gamma at M' 128 lies within 1.05e-6 (the uniform M error at D 3.15) of the uniform gamma(128) = 0.2273872422; every run ends with exactly one sign change in its bracket and |F| below 1e-27. If not, report and stop: step 3 does not run.
- Step 2, the gain (reported, not a pass rule): |gamma(M' 128) - gamma(M' 96)| per L, against the uniform 1.05e-6.
- Step 3: gamma(3.0444) at M' 96 and 128 per L, and their difference named as a resolution change, not a bound.

## Code, build and pins

- Worktree `~/Source/choptuik-large-d-1072`, detached at origin/feat/lowd-gamma-taumap 46a8dac5 (`lowD_gamma: gamma on the tau-mapped grid, with an identity selftest and controls`). Blobs: `hp/tau_map.py` 99520aad, `hp/tau_map_gain.py` bb9e313c, `hp/lowD_gamma.py` a848b9eb, `hp/raw_out.py` bc47fe90.
- hp build: `~/Source/choptuik-large-d-1058b/.venv` (Python 3.14, multidouble 5.1.0, `hpkernel` `.so` of 2026-11-20 13:43 local), built at main 8179068d (#1058). `git diff 8179068d 46a8dac5 -- hp/src hp/Cargo.toml hp/Cargo.lock hp/pyproject.toml hp/build.sh` is empty, so the kernel's sources are the branch's; no rebuild (a release build is 1.4 h and 24 GB here). Whether `make_solver_mapped` runs on it is step 0's check.
- Input of step 1 (raw clone at 254ae431 on this machine): `I927-mac/inputs/lowDhm_x0.000625-0.9_D3.1500_M128.npz`, blob df2ab378. `data/lowD_states/highm15_D3.7000_M96.npz` (blob 3eeee450) is in the repository.

## Step 1 amended (t5, #1072 comment, after the failure; written before these runs, 2026-11-22 21:20 UTC by the clock)

Hypothesis, not yet shown: #1033 mapped a well-resolved uniform state (M 384) down to M' 160 to 192, while here the source was the uniform M 128 state, barely resolved at D 3.15, and the map concentrates points where M 128 resolves least. No code change; the same acceptance for step 2. All of it runs from the worktree `~/Source/choptuik-large-d-1072b` at ae96bcc6 (t5's `sys.exit(main())` fix; `tau_map.py`, `tau_map_gain.py`, `raw_out.py` and the kernel sources unchanged; `lowD_gamma.py` blob 2e55d695). `run_new.sh` (unit `i1072c`, 6 threads, nice 10), each stage stopping at the first failure (`STOP_*.txt`) and reporting:

0. The two step-0 selftest calls on ae96bcc6: `lowD_gamma.py --selftest data/lowD_states/highm15_D3.7000_M96.npz --threads=6` exit 0 and with `--break` exit 1 (the old runs on 46a8dac5 gave 0 and 0).
1a. The identity control: `tau_map_gain.py solve I927-mac/inputs/lowDhm_x0.000625-0.9_D3.1500_M128.npz --pairs 1:128 ...` must converge, and `tau_map_gain.py report --ref` (the tool's own check) must show its Delta within 1e-20 of the state's stored Delta and its plan within 10% of the stored one.
1b. The better source, the uniform M 160 state `I927-mac/inputs/lowDhm_x0.000625-0.9_D3.1500_M160.npz`: first print `pick_s0` for L 0.5 on it (`resolve_s0(path, 0.5, None)`) and pass it as `--s0` to every solve of 1b and 1c; then `solve ... --pairs 0.9:128` and `--pairs 0.7:128` (two invocations in place of one `--pairs 0.9:128,0.7:128`, so that a failure at L 0.9 stops before L 0.7). If L 0.9 does not converge: report and stop (the map, not the source, is the problem at D 3.15).
1c. Continuation in L at M' 128, each solve from the previous converged mapped state as its source: 0.7 to 0.5 to 0.4; then M' 96 at L 0.5 and at L 0.4, each from the M' 128 state of its L.

Step 2 then runs on the converged L 0.5 and 0.4 states at M' 96 and 128, as written, with step 1's selftest (the gp control on a mapped state) on ae96bcc6 (exit 0).

## Cost (the issue's estimate)

Solves: minutes to an hour each at M' <= 128. gamma: about 170 s per determinant at M 128 (#1070's D 3.15), 7 to 11 determinants per state. Steps 0 to 2 about 3 to 5 h; step 3 a similar time.

## Status

- Step 0 (21:03 to 21:08 UTC, unit i1072a, `step0.txt`): `tau_map_gain.py selftest` exit 0 and `--mutate gp` exit 1 as required; `lowD_gamma.py --selftest` exit 0, identity bit for bit (ln|det| 1033.5811009326815 both); `--selftest --break` prints FAIL (the control fires: L 0.99 gives sign -1, ln|det| 1045.2428843957728) **but exits 0, not 1**: `main()`'s return value is dropped by `if __name__ == "__main__": main()` in the branch's `lowD_gamma.py` (a discrepancy with the issue's "exit 1", reported to t5, code not edited; fix `sys.exit(main())`). My `make_solver_mapped` construction in `run0.sh` used M 24, which the kernel does not allow; re-run with M 96 it constructs a Solver in 0.6 s, and the passing selftest built the mapped solver the same way: it runs on this hp build.
- Step 1 (21:09:46 to 21:18:40 UTC, unit i1072b, `step1.txt`, `solve_D3.15.log`, `solve_D3.15.jsonl`; worktree 46a8dac5): **0 of 4 configurations converged; no mapped state was saved, so step 2 and its selftest have no input.** Wall 534 s, exit 1.

| L | M' | start |F| (own plan) | plan steps (split) | result | wall |
|---|---|---|---|---|---|
| 0.5 | 96 | 1.76 | 634 (2) | pass 1: no |F| below tol1 in it1 = 4 calls: |F| 1.76, 1.75, 1.72, 1.71, 1.62 (|dz| 24, 9.3, 12, 45) | 94 s |
| 0.5 | 128 | 3.49e+29 | 826 (2) | pass 1: line search at call 0 (the dd4 Jacobian retry fails too) | 163 s |
| 0.4 | 96 | 6.56e+21 | 732 (2) | pass 1: line search at call 0 (dd4 retry fails) | 71 s |
| 0.4 | 128 | 9.98e+51 | 960 (4) | pass 1: line search at call 0 (dd4 retry fails) | 194 s |

  The interpolated start of the best case is still O(1) away (|F| 1.76); the other three evaluate to 1e21 to 1e52 on the source's own plan (a RuntimeWarning for overflow in the residual norm). The code is the same that passes `tau_map_gain.py selftest` (interpolation and mapped inputs against closed forms). Not tried (needs t5's word): the identity control `--pairs 1:128` (L 1 at the state's own M), a continuation in L from a converged mapped state (the tool takes a mapped state as the source: `tau_map_gain.py` line 522 reads its `map`), a larger `--it1` for L 0.5 at M' 96.
- Information from t5 (#1073, rpi5, raw d481a3a3): Ecker et al.'s gamma at D 3.15 interpolates to 0.22739 with about 1e-5 of spread (an interpolation spread, not a bound); our uniform 0.2273872422 lies inside it. They have no gamma below D 3.1, so step 3 at D 3.0444 has no outside target. The acceptance stays against our uniform gamma(128) and its 1.05e-6.
- Step 0 rerun on ae96bcc6 (2026-11-22 21:26 UTC, `selftest_lowD_gamma_ae96bcc6.txt`, `selftest_lowD_gamma_break_ae96bcc6.txt`, `steps_new.txt`): `lowD_gamma.py --selftest data/lowD_states/highm15_D3.7000_M96.npz --threads=6` **exit 0** and with `--break` **exit 1**, as the issue wants (beside the old runs on 46a8dac5: 0 and 0).
- The second worktree `~/Source/choptuik-large-d-1072b` is at ae96bcc6 (t5's fix: `sys.exit(main())`, the one-line diff to 46a8dac5; `lowD_gamma.py` blob 2e55d695, the other three scripts unchanged). Its step 0 and step 1 selftest calls run before step 2.
