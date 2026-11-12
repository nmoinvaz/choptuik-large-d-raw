#!/usr/bin/env bash
# #600: release build of hp (hpkernel on multishoot 1.2.1, the exact projector) and multidouble's Python package into a separate venv, venv-i600 (Python 3.14.10), not venv-t126 which the running jobs use.
# Code: worktree D:/choptuik-i600 detached at main fc697f3a. venv-i600 holds requirements.txt's pins (numpy 2.5.4, scipy 1.18.1, mpmath 1.3.0, sympy 1.14.0, python-flint 0.9.0, maturin 1.16.0); multidouble is not installed in it before the build.
export VIRTUAL_ENV=C:/Users/nathan/Source/venv-i600
export PATH="/c/Users/nathan/Source/venv-i600/Scripts:$PATH"
cd /d/choptuik-i600 || exit 9
date -u '+build start %Y-%m-%d %H:%M:%S UTC'
bash hp/build.sh
echo "build exit $? $(date -u '+%Y-%m-%d %H:%M:%S UTC')"
