# I1080-dh370: the control of the extended-precision M = 5 walk (zero_mp.py from the fundamental's M = 3 zero)

Machine `dh370-fedora` (Fedora, i7-8700, 6 cores / 12 threads, 31 GB). Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1080 (macm3's #1080; the rule is the coordinator's comment 7111416293, 2026-11-23 19:30 UTC by its heading). Coordinator t5's order by hc, received about 19:15 UTC by the clock; this README written 2026-11-23 19:20 UTC, before the run. The run starts after #1078's diagnostic (a) ends (same machine, one job at a time; t5: #1078 stays first if (a) needs a follow-up).

## Order

The control of the extended-precision M = 5 walk: Newton in (A, omega/omega_inf) on R_1 by central differences (5 values per iteration), from the fundamental's M = 3 zero, with the M = 5 harmonics solved by `value_mp.value_v` at 34 and 42 digits (step halving for M > 3).

- Code: branch `feat/inner-mp` at a0441d8b (`value_mp: step halving in the M > 3 solve (#1080)`), a new worktree `~/Source/choptuik-large-d-1080` (detached), pure Python on mpmath, run with main's venv `~/Source/choptuik-large-d/.venv` (Python 3.14.10, mpmath 1.3.0, no gmpy). Pins checked by `run_control.sh` before the run: `zero_mp.py` 0d94efcd, `value_mp.py` fbb1b1fa, `inner_mp.py` 563bc062 (git blob ids, `--no-filters`).
- Command, from `solver/inner_stokes`, 5 processes at nice 10:

      nice -n 10 python3 -u zero_mp.py 2.726475885672135 1.0156030949093042 - <raw>/I1080-dh370/control_walk.jsonl --M=5 --v0=0.1444194785,0.0110874259,0,0 --procs=5 --iters=8

  (`run_control.sh`, systemd unit `i1080a` under `systemd-inhibit`; one thread per process; log `control_walk.log`, rows `control_walk.jsonl`, steps `steps_control.txt`.) `zero_mp.py selftest` and its `--mutate=sign` control run first and must exit 0 and 1.

## Pass rule, written before the run (t5's)

**It passes** when the walk ends **"located"** (zero_mp's own rule: |R| below 10^3 sigma_mp, or the next step below 1e-13 with |R| what that step removes, within 10x) **within 10^-10 of Theorem A(5)'s box centre (2.71857918921174, 0.999228403206568)**. I read "within 10^-10" as the last row's (A, omega/omega_inf), the point the 'located' line prints, differing from the centre by at most 10^-10 in each coordinate; the step it did not apply is printed beside it. `control_check.py` reads the log and the rows and exits 0 on that rule; its selftest (a pass and three planted failures: NOT located, A off by 2e-10, no verdict line) exits 0 only if each reads as written (`control_check.py selftest`, exit 0 now). A walk that ends NOT located after the 8 iterations, or located elsewhere, is a failure of the control: I stop and report it with its rows, and start nothing else. t5's reading: a reading of the excited zeros counts only if the control passes.

## Cost, written before the run

t5: each iteration takes about 30 to 60 min (macm3 measured about 80 s for one M = 5 residual at 34 digits, 3657 s for x1fm's whole solve), 8 iterations at most: 4 to 8 h. Memory is small (macm3: 24.5 MB a process). 5 processes on 6 physical cores; the #1025 lesson is that more than 4 single-thread processes beside anything else slows all of them, so nothing else runs beside it.

## Status

Written as the run goes.
