# I1088-dh370-mixed2: Newton on form S at D 300 with the Jacobian in f64, double-double, quad-double or octo-double

Machine dh370 (Fedora 45, i7-8700), 4 threads at nice 10 beside other jobs. Issue:
https://github.com/nmoinvaz/choptuik-large-d/issues/1088

`mixed2.py` (the coordinator's; run by `run.sh`, then `run3.sh`) starts from the jump's rescaled guess at D 300 (the same
50 states, degree 3, held harmonics 5-13 at the guess's values, as `I1088-dh370/j300_held`), and iterates
z -= J^-1 F, with F the octo-double residual of the held system and J the form-S Jacobian (`jacobian_s`) in the named
precision, solved in double-double (`multidouble.dd_solve`) or f64 (scipy). It compares the end state with the
octo-double jump's stored solution `j300_held/jump_s_D300.0000.npz`. Code: the jump subagent's build on dh370 of
wip/large-d-form-s (python path in /home/nathan/Source/choptuik-large-d-1088a/python_path).

| log | Jacobian | refreshed | end max\|F\| | Δ − stored |
|---|---|---|---|---|
| dd.log | double-double | every step | 1.8e-12 (stalls) | −2.7e-6 |
| dd_scale101.log | double-double × 1.01 | every step | 3.7e-12 | −4.9e-6 |
| f64_fresh.log | f64 | every step | 6.9e-13 (stalls) | −9.0e-7 |
| qd_fresh.log | quad-double | every step | 3.1e-44 in 3 steps, 243 s | 3.7e-43 |
| qd_scale101.log | quad-double × 1.01 (control) | every step | 3.0e-21 after 6 steps | −6.9e-23 |
| od_chord.log | octo-double, once | no (chord) | 7.4e-43 in 9 steps, 574 s | −2.4e-38 |
