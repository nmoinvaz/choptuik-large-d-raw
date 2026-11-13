# I614-dh370: the x86 half of #614, hp on multishoot 1.2.2 and multidouble 4.2.1, built and checked on dh370 (Fedora Linux 45, AVX2)

Machine: dh370, Fedora Linux 45 Workstation, Intel Core i7-8700 (6 cores, 12 threads, AVX2 and FMA), 31 GB.
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/614
Code: choptuik-large-d main at 3c35f0cd0d7e8636eed426060f7f5e2a7824dad7, worktree `choptuik-large-d-614` with its own venv (no multidouble
installed before the build). The comparison build is I604-dh370/'s (main e835d94, worktree `choptuik-large-d-604`, the same kernel as
I523-mac/c3), left untouched. Toolchain: clang 23.1.5 as `cc`, `c++` and the cargo linker, rustc 1.99.1, maturin 1.16.0, Python 3.14.10.
No memory guard.
