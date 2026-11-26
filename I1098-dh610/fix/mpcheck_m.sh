#!/bin/bash
# #1098: taylor_mp_check.py at D 1000 on M 48 and M 64 states (fastmul5, site_x), the step from x_l inward by the state's
# own last step
{
W=/home/nathan/Source/choptuik-large-d-1088a
O=$W/out/mpcheck
cd $W/hp || exit 1
PY=$(cat $W/python_path)
export HP_HORIZON_RELAXED=1 OPENBLAS_NUM_THREADS=1 PYTHONPATH=$W/site_x
for st in D1000_M48_h23 D1000_M64_step; do
  H=$($PY -c "import sys; sys.path.insert(0, '.'); from octo_corrector import load_o; z, m = load_o('$O/states/$st.npz'); g = m['segs'][-1]; print(g[-2] - g[-1], m['M'], m['nodes'][-1])")
  set -- $H
  echo "$st: M $2, x_l $3, h $1" >> $O/taylor_m.log
  $PY -u taylor_mp_check.py $O/states/$st.npz --h $1 >> $O/taylor_m.log 2>&1
  echo "rc $?" >> $O/taylor_m.log
done
exit
}
