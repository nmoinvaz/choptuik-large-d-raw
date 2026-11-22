#!/bin/bash
# quick reruns of pass 2, then the pass-1 rows that were rescored, adapted or timed out under load
cd ~/Source/choptuik-large-d/_i349/clone
python reproduce_readme.py --tree ../run --out ../out/pass2 --python ~/Source/choptuik-large-d-1058b/.venv/bin/python --pass2 ../out/pass1/results.jsonl --redo pip_install,test_bindings,plot_wave_family > ../out/pass2b.log 2>&1
python reproduce_readme.py --tree ../run --out ../out/pass1 --python ../venv/bin/python --redo cmp_ecker,planted_dinf,largeD_linear_poisson,struct_eqs > ../out/redo2.log 2>&1
