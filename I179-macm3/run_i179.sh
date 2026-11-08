#!/bin/bash
# I179-macm3 phase 2: the hp build into venv-macm3-314, then the checks. Plain steps, each exit in exits.txt.
cd ~/Source/choptuik-large-d
R=$(cd ../choptuik-large-d-raw/I179-macm3 && pwd)
source ~/Source/venv-macm3-314/bin/activate
export CARGO_PROFILE_RELEASE_LTO=false
export CARGO_PROFILE_RELEASE_CODEGEN_UNITS=16
echo "python $(command -v python3) $(python3 --version)" >> $R/driver.txt

pip uninstall -y multidouble > $R/uninstall_multidouble.log 2>&1
echo "pip uninstall multidouble exit $?" >> $R/exits.txt

T0=$(date +%s)
date -u '+== %Y-%m-%d %H:%M:%S UTC bash hp/build.sh (venv-macm3-314, LTO off, 16 codegen units)' > $R/build.log
/usr/bin/time -l -o $R/build_time.txt nice -n 10 bash hp/build.sh >> $R/build.log 2>&1
echo "hp/build.sh exit $? wall $(( $(date +%s) - T0 )) s" >> $R/exits.txt
pip freeze > $R/freeze_venv-macm3-314_after_build.txt

T0=$(date +%s)
date -u '+== %Y-%m-%d %H:%M:%S UTC python3 check_numbers.py --selftest' > $R/check_numbers_selftest.log
nice -n 10 python3 check_numbers.py --selftest >> $R/check_numbers_selftest.log 2>&1
echo "check_numbers --selftest exit $? wall $(( $(date +%s) - T0 )) s" >> $R/exits.txt

cd solver/inner_amp
T0=$(date +%s)
date -u '+== %Y-%m-%d %H:%M:%S UTC python3 -u amp_flint_par.py 1.10 15 750 640 --procs 1 --fit phys --mf 6:12' > $R/amp_314.log
nice -n 10 python3 -u amp_flint_par.py 1.10 15 750 640 --procs 1 --fit phys --mf 6:12 --out $R/amp_314_macm3.json >> $R/amp_314.log 2>&1
echo "amp_flint_par exit $? wall $(( $(date +%s) - T0 )) s" >> $R/exits.txt
cd ../../hp

T0=$(date +%s)
date -u '+== %Y-%m-%d %H:%M:%S UTC python highm_check.py ref --compare=../../choptuik-large-d-raw/T81/ref_main.json --Ms=48,64,80 --threads=4' > $R/check_ref.log
nice -n 10 python3 highm_check.py ref --compare=../../choptuik-large-d-raw/T81/ref_main.json --Ms=48,64,80 --threads=4 >> $R/check_ref.log 2>&1
echo "check_ref exit $? wall $(( $(date +%s) - T0 )) s" >> $R/exits.txt

T0=$(date +%s)
date -u '+== %Y-%m-%d %H:%M:%S UTC python highm_check.py scaled --compare=../../choptuik-large-d-raw/T81/scaled_main.json --threads=4' > $R/check_scaled.log
nice -n 10 python3 highm_check.py scaled --compare=../../choptuik-large-d-raw/T81/scaled_main.json --threads=4 >> $R/check_scaled.log 2>&1
echo "check_scaled exit $? wall $(( $(date +%s) - T0 )) s" >> $R/exits.txt

T0=$(date +%s)
date -u '+== %Y-%m-%d %H:%M:%S UTC python highm_check.py jets --compare=../../choptuik-large-d-raw/anm-mac/jets_inputs/jets_inputs.json --threads=4' > $R/check_jets.log
nice -n 10 python3 highm_check.py jets --compare=../../choptuik-large-d-raw/anm-mac/jets_inputs/jets_inputs.json --threads=4 >> $R/check_jets.log 2>&1
echo "check_jets exit $? wall $(( $(date +%s) - T0 )) s" >> $R/exits.txt

T0=$(date +%s)
date -u '+== %Y-%m-%d %H:%M:%S UTC python highm_check.py jets --compare=../../choptuik-large-d-raw/anm-mac/jets_inputs/jets_inputs.json --threads=4 --mutate=kappa' > $R/check_jets_mutate_kappa.log
nice -n 10 python3 highm_check.py jets --compare=../../choptuik-large-d-raw/anm-mac/jets_inputs/jets_inputs.json --threads=4 --mutate=kappa >> $R/check_jets_mutate_kappa.log 2>&1
echo "check_jets --mutate=kappa exit $? wall $(( $(date +%s) - T0 )) s" >> $R/exits.txt

date -u '+end %Y-%m-%d %H:%M:%S UTC' >> $R/driver.txt
