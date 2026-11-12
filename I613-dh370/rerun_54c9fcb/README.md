# rerun_54c9fcb: #613's 0.80 bracket on main 54c9fcb (the shrink-only refit and --cr_sets)

Code: choptuik-large-d main at 54c9fcb9a8fcc4ac26eaf01e8dd7c6255ea6c796, worktree `choptuik-large-d-604`, the kernel of
I604-dh370/ (hp/src and the Cargo and pyproject files are unchanged since e835d94). `cr_floor_check.log`: exit 0.

| file | what |
|---|---|
| eq_080_F5e-13, eq_080_F1e-12, eq_080_F2e-12 (.json, .log) | `near_null_eq.py ... I543-win2/renode_last080_D242.3642.npz --plant=7 --cr_sets=1 --cr_floor=F --threads=4`, the three at once |
| rerun.sh | the driver of those |
| bare_flag_ignored/ | the first start, with `--cr_sets` as the docstring writes it: the option parser keeps only `--name=value`, so the bare flag was ignored and no set comparison was printed (`cr_sets` is null in the json). Its planted values equal the runs above. |
