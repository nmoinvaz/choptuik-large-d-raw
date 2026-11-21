# Diagnostic only (unsound): w1 <= w on F instead of w/theta_F, to size that factor's share of the offset-case gap.
import sys
sys.path.insert(0, "/Users/nathan/Source/choptuik-large-d-1061/solver/proof/review_p2c")
import p2c_b8_alg as ALG, p2c_b8_boot as B, p2c_b8_series as SER
orig = ALG.CellArith.rem
def rem(self, name, h_index, w1=False):
    if self.cl.mode == "F" and w1:
        return [ALG.const(self.cl, 1, 0, 0, h_index)]
    return orig(self, name, h_index, w1)
ALG.CellArith.rem = rem
at = SER.atoms(SER.params())
r = B.run_L0("73.89", "1e7", "D", at)
print(B.fmt(r))
print("hstar", r.get("hstar"))
