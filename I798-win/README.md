# I798-win: where between D 3.0434 and 3.043 the low-D planner's freeze begins, by order

Machine win (surface-laptop-4, 8 threads; 6 used), issue https://github.com/nmoinvaz/choptuik-large-d/issues/798.

Scripts (written by the coordinator): `run798.sh` (`hp/lowD_plan_probe.py` from T135's M 384 base at D 3.04375 with
T135's stored series, in T135's build and checkout, venv-t125 and choptuik-t125) and `check798.py` (the planted case and
the table; its selftest must pass).

Criteria, fixed before the run (#798): (1) planted truth: (3.0425, order 3) capped with its last trace at x within 1e-9
of T135's 0.013725225625; (2) the table of the targets 3.0433, 3.0432, 3.0431 and 3.04305 by order, each planned with its
time or capped with its frozen x; (3) the control `--cap 0.001` at 3.0433 reports every case capped and exits 1.
