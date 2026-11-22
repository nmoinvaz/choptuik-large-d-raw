#!/bin/bash
# the adapted reruns of pass 1, then pass 2 with an existing build; one command at a time
cd ~/Source/choptuik-large-d/_i349/clone
python reproduce_readme.py --tree ../run --out ../out/pass1 --python ../venv/bin/python --redo formula_refit,formula_all,rational_fit,plot_extrapolation,data_all,plot_solver_limits,plot_echo,plot_dropoffs,track_c,track_c_fold,arg_crossing,cmp_ecker,lowD_formula,export_delta_all_verify > ../out/redo.log 2>&1
python reproduce_readme.py --tree ../run --out ../out/pass2 --python ~/Source/choptuik-large-d-1058b/.venv/bin/python --pass2 ../out/pass1/results.jsonl > ../out/pass2.log 2>&1
