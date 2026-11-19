import io
p = "README.md"
t = open(p, encoding="utf-8", newline="").read()
a = "the max relative radii of `route3_bound_check` (4.0e-118 to 6.1e-32), the 5 violations of the plant control at j = 10 and the first-violation columns of the psi control."
b = "the max relative radii of `route3_bound_check` (2.3e-121 to 6.1e-32), the 5 violations in every row of the plant control and the violation counts and first-violation columns of the psi control."
assert t.count(a) == 1
t = t.replace(a, b)
open(p, "w", encoding="utf-8", newline="").write(t)
print("ok")
