{
cd ~/Source/choptuik-1101w/solver/matter || exit 1
for J in cs fast; do
  echo "start $J $(date -u '+%H:%M:%S')"
  OPENBLAS_NUM_THREADS=2 VECLIB_MAXIMUM_THREADS=2 nice -n 10 ~/venv-1025dd/bin/python3 -W ignore ell_refine.py fjsrc31 31 fje2e39$J 39 1 10.5 2.87 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma --jac $J
  echo "end $J rc $? $(date -u '+%H:%M:%S')"
done
exit
}
