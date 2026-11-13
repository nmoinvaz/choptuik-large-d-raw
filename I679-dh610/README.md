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
| exits_679.txt | start and exit of each run |
