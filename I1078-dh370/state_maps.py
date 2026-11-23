"""#1078 check 1 (t5's comment of 20:45 UTC): the tau-map (s0, L) of the D 3.15 states used in #1072's step 2 and in this session's controls, and of the D 3.044375 states, from meta['map'].

    python3 state_maps.py RAWPUSH     (hpkernel importable; read-only)    |    python3 state_maps.py selftest

A state without meta['map'] is on the uniform grid (printed 'unmapped (uniform)'); one with map [s0, L] is mapped (L 1, s0 0 is the identity map). selftest: planted meta dicts through the same
reader, and a planted mutation (the map read from the wrong key) which must read as unmapped and exit 1."""
import os
import sys

FILES = [  # (label, path under RAWPUSH, git blob prefix)
    ("D 3.15  step 2: L0.7 M' 128 (gamma_L07_M128.log; selftest_gp_L07_M128)", "I1072-dh370/states2/tmap_lowDhm_x0.000625-0.9_D3.1500_M160_L0.7_M128_s1.8326.npz", None),
    ("D 3.15  step 2: L0.9 M' 128 (gamma_L09_M128.log)", "I1072-dh370/states2/tmap_lowDhm_x0.000625-0.9_D3.1500_M160_L0.9_M128_s1.8326.npz", None),
    ("D 3.15  step 2: L0.7 M' 96 (gamma_L07_M96.log; this session's probes A, B, C)", "I1072-dh370/states2/tmap_tmap_lowDhm_x0.000625-0.9_D3.1500_M160_L0.7_M128_s1.8326_L0.7_M96_s1.8326.npz", "9e683a14"),
    ("D 3.15  step 2 start: L 1 (identity) M' 128", "I1072-dh370/states2/tmap_lowDhm_x0.000625-0.9_D3.1500_M128_L1_M128_s0.0000.npz", None),
    ("D 3.15  uniform M 128 (the selftest's UNIFORM state)", "I927-mac/inputs/lowDhm_x0.000625-0.9_D3.1500_M128.npz", "df2ab378"),
    ("D 3.0444 M' 96 (the state of the pair test)", "I1072-dh370/states3/tmap_tmap_tmap_lowDhm_x0.000157-0.975_D3.0444_M384_L0.4_M160_s1.9635_L0.4_M128_s1.9635_L0.4_M96_s1.9635.npz", "6a0f83d2"),
    ("D 3.0444 M' 128", "I1072-dh370/states3/tmap_tmap_lowDhm_x0.000157-0.975_D3.0444_M384_L0.4_M160_s1.9635_L0.4_M128_s1.9635.npz", "218460d9"),
    ("D 3.0444 M' 160", "I1072-dh370/in3/tmap_lowDhm_x0.000157-0.975_D3.0444_M384_L0.4_M160_s1.9635.npz", "9ccd7a9e"),
]


def read_map(meta, key="map"):
    m = meta.get(key)
    return None if m is None else (float(m[0]), float(m[1]))


def selftest():
    ok1 = read_map({"map": [1.8326, 0.7]}) == (1.8326, 0.7) and read_map({}) is None
    ok2 = read_map({"map": [1.8326, 0.7]}, key="mapp") is None          # the mutation: the wrong key reads as unmapped
    print(f"selftest: mapped and unmapped metas read as written: {'PASS' if ok1 else 'FAIL'}; the wrong-key mutation reads as unmapped (must differ from the mapped read): {'PASS' if ok2 else 'FAIL'}")
    return 0 if ok1 and ok2 else 1


if __name__ == "__main__":
    if sys.argv[1:2] == ["selftest"]:
        sys.exit(selftest())
    import subprocess
    from hpkernel.driver import load
    root = sys.argv[1]
    for label, rel, blob in FILES:
        p = os.path.join(root, rel)
        if blob:
            b = subprocess.run(["git", "hash-object", "--no-filters", p], capture_output=True, text=True).stdout.strip()[:8]
            assert b == blob, f"{rel}: blob {b} is not {blob}"
        zh, zl, meta = load(p)
        m = read_map(meta)
        print(f"{label}\n    D {meta['D']}, M {meta['M']}, nodes {len(meta['nodes'])} (x {meta['nodes'][0]} .. {meta['nodes'][-1]}), map " +
              ("unmapped (uniform)" if m is None else f"s0 {m[0]!r}, L {m[1]!r}" + ("  (identity)" if m == (0.0, 1.0) else "")) +
              f"; kt {meta.get('kt')}, kc {meta.get('kc')}, ks {meta.get('ks')}; blob {blob or '-'}")
