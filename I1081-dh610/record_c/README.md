# I1081-dh610/record_c: configuration c (h = w = 1e-13, PREC 256) as the second excited zero's certificate of record: controls, recheck, H3 (lemma 6a) and the inclusion

Machine dh610 (Fedora 45, i7-12700, Linux). Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1081, item 1 (follow-up of #1079). Parent folder `../README.md` (the three configurations). Written 2026-11-24 01:40 UTC, before any run of this folder. Status words: numerical evidence; nothing here asserts Theorem A(3).

## Order (coordinator t5, hc after the #1081 read, and the #1081 comment headed "2026-11-24 01:45 UTC")
"(c) robust, (b) identical to (a): the frames, not PREC. Next, making (c) the second zero's certificate of record, from your I1081 worktree (main 9676d7c1, NTAY 28 NJAC 16, PREC 256): (1) certify_M.py controls --point=<c point> --box=<c box U> and certify_M_recheck.py <c box> plus its --mutate; (2) export6a on c's box, then lemma6_jump_M.py --M=3 --x=<p^> --box=<that export> (as your #1079 H3 chain) with --mutate=partial and swap; (3) theorem_A_sets_M.py --M=3 --cert=<c box U> --ray=<your #1079 exc2 covering's ray.json> and the same with --selftest. Push the c box and point files with sha256 in the README. Report each." The comment adds: H1 and H2 hold unchanged (X_c in p^ +- 1e-12 in X_b); the coordinator cross-loads c's files on the Mac; then proof/A_lemmas_M.md 7.1 cites c's files, by sha256.

## Checkout, environment, inputs
- Worktree `~/Source/choptuik-large-d-1081` at main 9676d7c11fa61af808031839b106a4d50fa69547 (clean; the steps write only into this folder, by explicit paths); `solver/proof`; `~/Source/venv-i1058/bin/python` (3.14.10, python-flint 0.9.0, FLINT 3.6.0); `CERTIFY_M_NTAY=28 CERTIFY_M_NJAC=16 CERTIFY_M_PREC=256`, one BLAS/OMP thread, nice 10, at most 2 processes (the steps are short); threads beside the leg lane's 8 and the recount's 2 stay below 20.
- The files of record, copies of `../cfg_c/box_U.json` and `../cfg_c/point.json` (config c, the unperturbed box and its point run; sha256 in `in/sha256_start.txt`, equal to the cfg_c files):
  - 7cd7c809a5442aec24a9a1f712edb550f1a5e9384943397f31d468193d5e549e  A_M_box_M3x2E2_h1e-13_w1e-13.json
  - f060ecffc4f7c88db6c32849daf64572c876acc06e9fef0f47fc131d0593bfb4  A_M_point_M3x2E2.json
- The covering's ray: `in/ray_exc2_linux.json`, a copy of `../../I1079-dh610/out/lemma6b1_runs_M3_exc2_linux/ray.json` (my #1079 H2 run for the second zero, `lemma6b1_cover_M.py ray --M=3 --x=<p^> --h=1e-11 --tag=_exc2_linux --c1`, p^ +- 1e-11, 63 steps), sha256 81355ccd7dd1cfe1b21610c5fbac36eb9da834a869754d2e53dc8f6760aea273.

## Steps (`run_record_c.sh`, from `solver/proof`; every command and its seconds in `steps.txt`, logs in `logs/`)
1. `certify_M.py krawczyk --point=A_M_point_M3x2E2.json --box=A_M_box_M3x2E2_h1e-13_w1e-13.json` (the record's own margins), `certify_M.py controls --point=... --box=...` (exit 0, CONTROLS ALL AS EXPECTED), `certify_M_recheck.py <box>` (exit 0) and `certify_M_recheck.py <box> --mutate` (exit 1).
2. H3: `certify_M.py export6a --box=<box> --out=A_M_6a_M3x2E2_h1e-13_w1e-13.json`; the same file with `x` = `p` as `..._in.json`; `lemma6_jump_M.py --M=3 --box=<in> --x=<p^> --json=lemma6a_....json --save-B=lemma6a_..._B.json` (exit 0, "lemma 6a" holds, rho_6a < 1); `--mutate=partial --load-B=...` and `--mutate=swap` (the script returns 0 for a caught mutation, so the caught line is counted: "NOT established" with "G_slow is ... not square" for partial, "backward integration failed" for swap).
3. The inclusion: `theorem_A_sets_M.py --M=3 --cert=<box> --ray=in/ray_exc2_linux.json` (exit 0, "HOLD") and the same with `--selftest` (exit 0, "SELFTEST (M = 3): PASS").
The wrapper's decisions (exit codes and caught lines against the wanted values) are one function, `judge`, with a selftest (`bash run_record_c.sh selftest` exit 0) and its mutation (`selftest --mutate`, exit 1: the judge accepts every value, so the planted wrong exit codes pass).

## Acceptance (fixed before the run)
- Every wanted exit and caught line as listed; any other result stops the chain and is reported, with the step's log. A control that fires or a mutation that is not caught is not loosened.
- The record's margins (step 1) equal `../cfg_c/krawczyk_U.log`'s to the printed digits (same files, same code).

## Predictions, registered before the run (mine, information)
- controls exit 0 with CONTROLS ALL AS EXPECTED (95%); recheck exit 0 (92%) and `--mutate` exit 1 (95%); the margins equal the cfg_c ones (99%).
- export6a exit 0 (97%); lemma 6a exit 0 with rho_6a < 1 (90%); rho_6a within 20% of the #1079 box's 1.259e-02 (55%); partial caught (97%); swap caught (95%).
- The inclusion exit 0 with HOLD (90%); its selftest exit 0 with PASS (95%).
- All of it as wanted (78%); the chain ends within 20 min of its start (70%; the #1079 H3 chain took about 7 min at the h = 1e-12 box, the swap run 247 s).

## Status
- 2026-11-24 01:40 UTC: folder and README written, files of record copied (sha256 above); the script and its selftest next, nothing run.
- 2026-11-24 01:41 UTC: `run_record_c.sh` written; its judge selftest passes (exit 0) and `selftest --mutate` exits 1. The unit `i1081rc` starts after this README is pushed.


## Result (`steps.txt` has every command, its seconds and each judge line; all steps as wanted, `record_c done: all steps as wanted`)
Lane 01:41:28 to 01:46:59 UTC (5.5 min). The worktree stayed clean (no WARNING line); the five input files still match `in/sha256_start.txt`.

| step | command (from `solver/proof` of the worktree at 9676d7c1) | result |
|---|---|---|
| 1 | `certify_M.py krawczyk --point=A_M_point_M3x2E2.json --box=A_M_box_M3x2E2_h1e-13_w1e-13.json` | exit 0; K(X) in int X: True; relative margins +0.971, +0.953, +0.998, +0.999 (the first line equals `../cfg_c/krawczyk_U.log`'s) |
| 1 | `certify_M.py controls --point=... --box=...` | exit 0, CONTROLS ALL AS EXPECTED |
| 1 | `certify_M_recheck.py <box>` | exit 0 |
| 1 | `certify_M_recheck.py <box> --mutate` | exit 1, control FIRED (C3 enclosure moved to [-1.9390548205994221, -1.9390548205994217]) |
| 2 | `certify_M.py export6a --box=<box> --out=A_M_6a_M3x2E2_h1e-13_w1e-13.json` | exit 0, state box at xi1 = 0.3, max radius 1.21e-13 (the h = 1e-12 box's export: 1.21e-12) |
| 2 | `lemma6_jump_M.py --M=3 --box=<export with x = p> --x=<p^> --json=... --save-B=...` | exit 0, 139 s: contraction 0.6782, Lambda = 0.2368, rho_6a = 1.259e-02 < 1: True, all J_D,mu(0.3) = 0 implies psi = 0 (whole jump): True |
| 2 | the same with `--mutate=partial --load-B=...` | exit 0 (the script returns 0 for a caught mutation); caught: "G_slow is 9 x 11: not square ... lemma 6a NOT established" |
| 2 | the same with `--mutate=swap` | exit 0, 189 s; caught: "backward integration failed (step size underflow at t = 0.04316854849457741): lemma 6a NOT established" |
| 3 | `theorem_A_sets_M.py --M=3 --cert=<box> --ray=in/ray_exc2_linux.json` | exit 0, THEOREM A SETS (M = 3, mutation None): HOLD; X_c (h = w = 1e-13, hull half-widths A 1.00e-13, w/w_inf 1.00e-13, B3 1.72e-13, C3 1.37e-13) inside X_b (radius 1e-11 + 1.425e-20), slack +9.828e-12 at B3 |
| 3 | the same with `--selftest` | exit 0, SELFTEST (M = 3): PASS |

- **Lemma 6a does not change with the box:** Lambda, rho_6a (1.259e-02) and the swap mutation's failure point (t = 0.04316854849457741) are the same to the printed digits as in the h = 1e-12 box's run (`../../I1079-dh610/steps.txt`, h3 exc2), although the exported state box is ten times smaller. I report the equality; the code path that makes it so I have not read.
- **Files of record** (sha256 at the end of the run, `sha256_end.txt`; the first two are config c's box U and point run of `../cfg_c/`, byte-identical copies; their git blobs are e0357b2a for the box and e915d083 for the point):
```
7cd7c809a5442aec24a9a1f712edb550f1a5e9384943397f31d468193d5e549e  A_M_box_M3x2E2_h1e-13_w1e-13.json
f060ecffc4f7c88db6c32849daf64572c876acc06e9fef0f47fc131d0593bfb4  A_M_point_M3x2E2.json
27b129842549ae61aa9f8d472114763b57f786924457457928cf5fbdd6c17171  A_M_6a_M3x2E2_h1e-13_w1e-13.json
12c13fe70875adea0d29db77aa1b62650af6c7155a8ac2fcd7f72b92fee91bb1  A_M_6a_M3x2E2_h1e-13_w1e-13_in.json
c11db3de5b714a3370fec22430829613cffc08f704875c6e15f60fa21f3ad28e  lemma6a_M3x2E2_h1e-13_w1e-13.json
227964ab3fef759f3d12650e26147d666db7999fa27e7b6cb4c60f0ab2fa17cf  lemma6a_M3x2E2_h1e-13_w1e-13_B.json
81355ccd7dd1cfe1b21610c5fbac36eb9da834a869754d2e53dc8f6760aea273  in/ray_exc2_linux.json
```
- Seconds in the 1079 chain for the same steps at the h = 1e-12 box: lemma 6a about 3 min, swap 247 s; here 139 s and 189 s.

### Predictions scorecard (written before the run; "right" = the stated event happened)
| prediction | result |
|---|---|
| controls exit 0 with CONTROLS ALL AS EXPECTED (95%); recheck exit 0 (92%); `--mutate` exit 1 (95%); margins equal the cfg_c ones (99%) | right, right, right, right |
| export6a exit 0 (97%); lemma 6a exit 0 with rho_6a < 1 (90%); rho_6a within 20% of 1.259e-02 (55%); partial caught (97%); swap caught (95%) | right, right, right (equal to the printed digits), right, right |
| the inclusion exit 0 with HOLD (90%); its selftest exit 0 with PASS (95%) | right, right |
| all of it as wanted (78%) | right |
| the chain ends within 20 min of its start (70%) | right (5.5 min) |

## Status after the run
- 2026-11-24 01:47 UTC: record_c done, all steps as wanted; result, hashes and scorecard above. The coordinator cross-loads c's files on the Mac.
