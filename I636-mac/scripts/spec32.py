import sys
sys.path.insert(0, "/Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-a85c4feb2fd2f0829/hp")
import chain_dM as c

R = "/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/11bcbd25-9376-453b-88d5-a7c6ad0172dd/scratchpad/raw-i636/"
for st in sys.argv[1:]:
    parts, meta = c.load_parts(R + st)
    M, K = int(meta["M"]), len(meta["nodes"])
    sp = c.spectrum(c.mp_sum(parts), M, K)
    print(st, "D", meta["D"])
    for kind in ("p1", "c0", "p", "m", "a", "c", "m_h", "a_h"):
        m = sp[kind]
        odd = kind in ("p1", "p", "m", "m_h")
        print(f"  {kind:4s} " + " ".join(f"{k}:{m[k]:.0e}" for k in range(M + 1) if (k % 2 == 1) == odd and k >= 9))
