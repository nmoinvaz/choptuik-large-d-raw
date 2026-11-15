# I843-rpi5: Theorem A(M = 1)'s certificate reproduced on aarch64 Linux (Raspberry Pi 5)

Machine rpi5 (Raspberry Pi 5 Model B, 4 cores, 8 GB, Ubuntu), issue
https://github.com/nmoinvaz/choptuik-large-d/issues/843. Script (the coordinator's): `run843.sh`, the commands of
proof/A_certify.md sections 8 and 9 from `solver/proof/`, each with its log, exit code and wall time in
`exits_843.txt`; `env.txt` records the commit, python-flint, FLINT, numpy, mpmath, scipy and the platform. Venv
`~/Source/venv-choptuik` (Python 3.13.7, the pinned packages of requirements.txt).

The certificate's own test runs twice: from this machine's point and box runs (`vi_point.json`, `vi_box.json`), and
from the stored x86 runs next to the script (the cross-load). The coordinator checks this machine's runs on the Mac.
