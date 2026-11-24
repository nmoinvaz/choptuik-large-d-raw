# #1081 dh610 common settings (sourced by job.sh and lane_1081.sh)
RAW=/home/nathan/Source/choptuik-large-d-raw; F=$RAW/I1081-dh610
W=/home/nathan/Source/choptuik-large-d-1081; BR=9676d7c11fa61af808031839b106a4d50fa69547
PY=/home/nathan/Source/venv-i1058/bin/python; H=$F/steps.txt
export CERTIFY_M_NTAY=28 CERTIFY_M_NJAC=16 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1
unset CERTIFY_M_XI1 CERTIFY_M_PREC REVIEW_PERTURB REVIEW_SEED REVIEW_ULPS REVIEW_TIES REVIEW_STABLE
stamp() { date -u '+%F %T'; }
cfg() { case $1 in a) HH=1e-12; WW=1e-12; PREC=256;; b) HH=1e-12; WW=1e-12; PREC=384;; c) HH=1e-13; WW=1e-13; PREC=256;; *) echo "unknown config $1" >&2; return 1;; esac; }
