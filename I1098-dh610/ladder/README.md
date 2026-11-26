# I1098-dh610/ladder: ladder points run on dh610 (#1098)

Machine: dh610 (Fedora 45, i7-12700). Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1098

- `D360/`: the pilot point, on fastmul6 (site_y: d368a0c0 kernel, Python 478e9d86). The steps:
  - The jump (`jump/`): Moebius a 8, ks 557, kc 146, from fastmul6's D 300 and D 1000 states. It converged in 5
    double-double steps in 84 s, after the floor rule's small-step condition (478e9d86) was added.
  - h5..h13 (`rls/`) by ladder_point.sh, all to tol 1e-48. Delta 1.672499793793157139862134965199708001492.
  - The Moebius tail (`tail_mob/`) by ladder_tail.sh mob: M 32, ks 957, kmax 23, 4 threads, 43 min. h23 was released
    with a pending dDelta of -3.6e-27. Delta 1.672499793793157083326890316334382065517.
  - Its ladder record is I1098-mac-a/ladder_records/D360.
