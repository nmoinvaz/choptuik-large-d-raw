# I679-dh610: chain_dM's planted checks at the kfreeze-13 plants dd40 and dd58, and the --mutate=D control

Machine: dh610 (the former win3), Fedora Linux 45 Workstation (kernel 7.3.3), Intel Core i7-12700 (12 cores, 20
threads), 62 GB. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/679 (recommended by #636, assigned by the
coordinator's message of 2026-11-13 18:56 UTC).

Code: choptuik-large-d main at cbb124b5 in a detached worktree (`choptuik-i679`), on the hpkernel build that runs #608
(main a879ccc3's Rust: multishoot 1.2.1, multidouble 4.1.0, avx2; main's Python is newer). Python 3.14.10.
`--threads=2`, `OPENBLAS_NUM_THREADS=1`, nice 10, one systemd user unit (`i679-planted`) under `systemd-inhibit`,
beside #608's two chains. The two runs go one after the other (`run_679.sh`):

    cd hp && python3 chain_dM.py planted <raw clone> <raw clone>/I679-dh610/planted --threads=2 --only=dd40,dd58
    cd hp && python3 chain_dM.py planted <raw clone> <raw clone>/I679-dh610/planted_mutD --threads=2 --only=dd40,dd58 --mutate=D

Acceptance: the first ends `planted: PASS` with each plant within its bound (exit 0), the second, the control, ends
`planted: FAIL` (exit 1).

| file | what |
|---|---|
| run_679.sh | the two commands, in order, with their exits |
| planted.log, planted_mutD.log | their output |
| planted/, planted_mutD/ | each run's `chain_dM.jsonl` and M 48 solutions |
| run_679c.sh | the coordinator's rerun of the control at dd58 alone (sha1 a2eb11b6), below |
| planted_mutD_dd58.log, planted_mutD_dd58/ | its output, `chain_dM.jsonl` |
| exits_679.txt | start and exit of each run |

## The control's rerun at dd58

The reboot of 2026-11-13 22:52 UTC killed `planted_mutD` after its dd40 stage had failed as it must (record written 22:40
UTC) and while dd58 was at M 48, so that run has no exit status and no dd58 record. `run_679c.sh` reran the control at dd58
alone (`--only=dd58 --mutate=D`, 2 threads, nice 10, the same worktree and build) as the user unit `i679c`, from 2026-11-14
06:58:00 UTC to 09:42:09 UTC (wall 9849 s). Its exit was 1, as it must be.

| run | plant | verdict | numbers |
|---|---|---|---|
| planted | dd40 | pass | Delta(M 48) minus the record +2.016e-22, tolerance 1.1e-21 |
| planted | dd58 | pass | +1.875e-18, tolerance 6.1e-18 |
| planted_mutD | dd40 | FAIL, as it must | -2.323e-15 against 1.1e-21 (M 48 converged, 1.7e-58) |
| planted_mutD_dd58 | dd58 | FAIL, exit 1, as it must | M 48 refused: no trial step accepted at the first Newton step, max\|F\| 1.44e-15 above the refusal 1e-20, so no difference is reported |
