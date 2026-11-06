# od-corrector-mac: the octo-double corrector's checks and the quad-double floor study (notes/OCTO_DOUBLE.md 5-6)

Machine: the Mac (Apple M5, NEON), 2026-11-06 13:30-18:30 UTC, a subagent of the coordinator session in its own
worktree (branch wip/octo-corrector, merged into main), kernel from the octo-double build (Rust identical to main's),
3 threads, nice 10. qd_floor.py and qd_floor.log are the coordinator's first floor measurement (plain newton_qd from
stored chain states, plan at 1e-32); step0*.log extend it to plans at 1e-40 and 1e-48 and to one octo-double Newton
step at D 188.02. check_a* to check_f.log are the checks (a)-(f) of notes/OCTO_DOUBLE.md 5.4: planted at 180.52, the
wall at 194.27, the control --mutate_offset qd, the chain step from 193.77 and its restart, the quad-double path
unchanged, check_numbers. The run_*.sh scripts hold the commands as run; the subagent's patched copy of the code
before the merge is not kept.
