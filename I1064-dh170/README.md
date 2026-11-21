# I1064-dh170: #1064's order raise at D 262.0099: the start residual along the weak direction (ks 315), the amplification test

Machine dh170 (Fedora 45, i7-7700, 8 logical CPUs, 31 GiB RAM). Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1064 (the coordinator's hc, 21 Nov ~12:05 UTC and addendum; beside #1025's D 17.75 part 2, both at nice 10).

## The hypothesis (the coordinator's) and what is computed
dh610's pilot (#1064 comment 7062186280) showed that `--reseed_base 1` leaves the raise's start residual unchanged (1.1e-8 at ks 315, 2.3e-9 at ks 294), so it is not in the horizon data. Hypothesis: the start residual has a component along the weak direction (sigma_Delta 6.4e-21 at D 262.0099), so Newton's first step there is of order 1e12, far outside any basin.
At D 262.0099 (`I966-dh370/ks_chain3b/leg14_D261.1415_ks293/anm_pin3_D262.0099.npz`, raw blob eb34f3c8, checked against dh610's blob id):
1. the start residual of the stored state on the ks 315 system: anm_run's base residual at `--ks 315` before any polish (the pinned octo-double system, the plan made again at the state as anm_run does for a changed `--ks`);
2. near_null's six lowest right singular vectors v_k and sigma_k of the ks 315 Jacobian at that state, u_k = J v_k / sigma_k;
3. per k: u_k.F, the step component (u_k.F)/sigma_k, and the Delta share of v_k.
Script `raise_test1064.py` (near_null.py's setup, octo-double LU, subspace iteration and exact-Jacobian check, imported from the worktree `~/Source/choptuik-large-d-1058b/hp` at main 8179068d and its venv; `--ks` and the plan chosen as anm_run does; dot products at 140 digits). F is reported twice: the pinned system's residual R = F(z) - c (c the held offset of the state's own p1 coefficients: near_null's pinned step, the base polish's) as the headline, and the unpinned F.

## Reading (fixed before the run)
Headline quantity: **(u_1.R)/sigma_1** at ks 315, the first Newton step's component along the weakest right singular vector. **Far above 1 supports the hypothesis (I take at least 1e3); below 1e-3 rejects it; between the two is inconclusive and reported with the value.** The coordinator's expectation, about 1e12, is a prediction, not the criterion. Also reported: the other k's components, the step's Delta component, and the same at ks 293 with the stored plan (the control).

## What the earlier issues say (read first, quoted)
Both are open and were never run: #729 and #730 wait on #696, whose re-polish at a changed ks had not converged. They carry the model (notes/FACTORED_HORIZON.md sections 4.1 to 4.5) and its acceptance criteria; neither has measured results and neither has a script. What I reuse: `hp/near_null.py` (#488's sigma tool, named in both) and anm_run's base residual path (`--ks`, #696's commit 614211ab).
- **#729** ("The weak sigma against the horizon order ks at D 237.13 and 242.36, with a D 60 control", R1): "It decides between the truncation and G. The model predicts that ln sigma_3 rises by -ln f: 41.05 at D 237.13 and about 47 at D 242.36, from ks 130 to 250." Acceptance (note 4.5): "It supports the truncation if ln sigma_3 rises by the model's -ln f within 30% at ks 160 and 200 and changes by less than 1 from 250 to 300." The note (4.2): "At ks = 250 the model keeps f = 1 to 0.005 at every state." What applies: ks 293 and ks 315 both lie past the shadow, so the model predicts the weak sigma does not change between them: I report ln(sigma_1(315)/sigma_1(293)) against that "less than 1" at D 262.0099.
- **#730** ("#696's states: near_null at ks 130 and 300, and Delta(300) - Delta(130) against the amplification estimate", R2): "The model predicts that the weak sigma rise by about e^50 (D 245.14) and e^63 (D 253.80). It also gives the amplification reading's |Delta shift|: about 3e-12 and 1e-7." The note (4.3): "raising ks moves Delta by about T_omit/sigma_inf: T_omit is the omitted transient and sigma_inf = sigma_3/f the grip without truncation. M5 gives 2.7e-12 at D 245.14 and 1.4e-7 at D 253.80, good to perhaps a factor 100 (conjecture; #696 measures it, and a change below 1e-14 at D 253.80 refutes it)." What applies: the hypothesis under test is that amplification reading at ks 293 -> 315 and D 262.0099: omitted transient (the start residual) divided by the weak sigma. The model's amplification gave a Delta shift of 1e-7 at D 253.80 for the raise from ks 130 (where f was far below 1); at ks 293 -> 315 the series' omitted terms are tiny against that, yet the measured start residual is 1.1e-8 (not small), which is why the amplification by 1/sigma_1 (6.4e-21) is the quantity to look at. The test measures the step component directly instead of a converged re-polish's Delta shift (which has not been obtained).

## Controls (fixed before the run; each can fail; the script exits 1 on failure)
1. near_null's own check: sigma_1 converged to 1e-3, ||J v_1|| / sigma_1 within 1e-2 of 1 (the exact Jacobian at 140 digits).
2. Route B for k = 1: u_1 from the exact Jacobian at 140 digits (J v_1 / sigma_1, v_1 refined in octo-double) against u_1 from the transpose solve (sigma_1 J^-T v_1): u_1.R agrees in magnitude to 1e-6.
3. The planted check: R_pl = J (eps v_1) (eight parts, J's columns by od_axpy, as near_null's `--planted`) put through the same analysis must return (u_1.R_pl)/sigma_1 = |w| and u_i.R_pl = 0 (i > 1) to 1e-6, and the Newton step -J^-1 R_pl must have the v_1 component -|w| to 1e-6. `--mutate=sigma1` (sigma_1 1.05 times too large in the analysis) must make it fail.
4. The state's own order (ks 293, the stored plan, `--keep_plan 1`): the state converged there (dh370's accepted max|F| 1.5e-41), so (u_1.R)/sigma_1 must be below 1e-3 and sigma_k, the Delta shares must equal near_null's #1057 record of this state (`I1057-dh170/c3b_ks293_D262.0099.json`: sigma_1 6.379796e-21, share 0.9205) to 1e-6 relative.
5. Information: max|R| at ks 315 against dh610's start |F| at the same ks (1.15e-8 at D 261.6229); ln(sigma_1(315)/sigma_1(293)) against #729's "less than 1".
Runs, in order: the ks 293 control (4 threads, nice 10), then ks 315 (the plan made again).

## Resources
`/usr/bin/time -v` of each run (user, system, CPU %, maximum RSS) in its log; memory sampled by `memlog_*.log` (alert-only).

## Log
- 2026-11-21 12:1x UTC: folder, script and reading written before any run.
