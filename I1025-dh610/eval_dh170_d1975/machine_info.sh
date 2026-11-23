#!/bin/bash
# #1025 eval_dh170_d1975 (dh610) machine_info.sh: this machine's CPU model and the BLAS that numpy and scipy load (the coordinator's request). threadpoolctl is not installed in the venv, so numpy.show_config() and OPENBLAS_VERBOSE=2 give the core type.
PY=/home/nathan/Source/venv-i1058/bin/python
echo "date: $(date -u '+%F %T') UTC; host: $(hostname); kernel: $(uname -r)"
lscpu | grep -E "Model name|Architecture|^CPU\(s\)|Thread|Core\(s\)|L2 cache|L3 cache"
echo "SIMD flags: $(lscpu | grep -o -E '\bavx512[a-z_0-9]*|\bavx2\b|\bfma\b|\bavx_vnni\b' | sort -u | tr '\n' ' ')"
echo "python: $($PY -VV 2>&1 | head -1)"
$PY -m pip list 2>/dev/null | grep -i -E "^(numpy|scipy|multidouble|python-flint|mpmath|threadpoolctl) "
echo "--- OPENBLAS_VERBOSE=2: import numpy, import scipy.linalg"
OPENBLAS_VERBOSE=2 $PY -c "import numpy" 2>&1 | head -2
OPENBLAS_VERBOSE=2 $PY -c "import scipy.linalg" 2>&1 | head -2
echo "--- numpy.show_config(), the BLAS/LAPACK part"
$PY -c "import numpy; numpy.show_config()" 2>&1 | grep -E -A8 '"blas"|"lapack"|SIMD|baseline|found' | grep -E "name|version|openblas configuration|found|baseline|found|not found|SIMD" | head -16
echo "--- scipy.__config__"
$PY -c "import scipy; scipy.show_config()" 2>&1 | grep -E "name|version|openblas configuration|found" | head -10
echo "--- multidouble isa"
$PY -c "import multidouble as md; print('multidouble', getattr(md,'__version__','?'), 'isa', md.isa() if hasattr(md,'isa') else '?')" 2>&1 | tail -1
